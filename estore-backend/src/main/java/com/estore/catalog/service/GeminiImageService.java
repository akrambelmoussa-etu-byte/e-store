package com.estore.catalog.service;

import com.estore.catalog.entity.Product;
import com.estore.exception.BusinessException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Bridges product-image generation to Google Gemini's Nano Banana image model
 * (`gemini-2.5-flash-image-preview`).
 *
 * <p>Workflow per request:
 *   <ol>
 *     <li>Resolves the target product (so we can build a context-aware prompt)</li>
 *     <li>Calls the Gemini :generateContent endpoint with a studio-photo system prompt</li>
 *     <li>Extracts the inline base64 payload from the first image part</li>
 *     <li>Saves the bytes to {@code ${gemini.images.dir}} under a UUID name</li>
 *     <li>Returns a public URL the frontend can render directly</li>
 *   </ol>
 *
 * <p>If no API key is configured this service throws a {@link BusinessException}
 * with a clear message — admins see the failure in the UI rather than a 500.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class GeminiImageService {

    private static final String IMAGE_MODEL = "gemini-2.5-flash-image-preview";
    private static final String API_BASE =
            "https://generativelanguage.googleapis.com/v1beta/models/" + IMAGE_MODEL + ":generateContent";

    @Value("${gemini.api.key:}")
    private String apiKey;

    @Value("${gemini.images.dir:./uploads/products}")
    private String imagesDir;

    @Value("${gemini.images.public-path:/uploads/products}")
    private String publicPath;

    private final ProductService productService;

    /**
     * @param productId product to refresh — used purely to seed the prompt
     * @param overridePrompt optional admin override; null/blank uses an auto prompt
     * @return public URL of the generated image, e.g. {@code /uploads/products/abc.png}
     */
    public String generateForProduct(Long productId, String overridePrompt) {
        if (apiKey == null || apiKey.isBlank()) {
            throw new BusinessException(
                    "Clé Gemini non configurée. Renseignez gemini.api.key dans application.properties.");
        }

        Product product = productService.get(productId);
        String prompt = buildPrompt(product, overridePrompt);
        log.info("Génération Gemini pour produit #{} : {}", productId, abbreviate(prompt, 80));

        Map<String, Object> requestBody = Map.of(
                "contents", List.of(Map.of(
                        "parts", List.of(Map.of("text", prompt))
                ))
        );

        try {
            ResponseEntity<Map> response = RestClient.create()
                    .post()
                    .uri(API_BASE)
                    .header("X-goog-api-key", apiKey)
                    .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                    .body(requestBody)
                    .retrieve()
                    .toEntity(Map.class);

            String base64 = extractInlineImage(response.getBody());
            if (base64 == null) {
                throw new BusinessException("Gemini n'a pas renvoyé d'image (peut-être un blocage de sécurité).");
            }

            return persistImage(base64);

        } catch (RestClientException e) {
            log.error("Erreur Gemini API : {}", e.getMessage());
            throw new BusinessException("Appel Gemini échoué : " + e.getMessage());
        } catch (IOException e) {
            log.error("Erreur d'écriture de l'image : {}", e.getMessage());
            throw new BusinessException("Impossible d'enregistrer l'image générée.");
        }
    }

    private String buildPrompt(Product p, String override) {
        if (override != null && !override.isBlank()) {
            return override;
        }
        return """
                Studio product photography of: %s.
                %s
                Category context: %s.
                Style: ultra-premium e-commerce hero shot, soft diffused studio lighting,
                seamless dark neutral background (charcoal #121414 with subtle gradient),
                centered composition, slight reflective surface, sharp focus,
                editorial magazine quality, 4K, no text, no watermark, square 1:1 frame.
                """.formatted(
                        p.getName(),
                        p.getDescription() == null ? "" : p.getDescription(),
                        p.getCategory() == null ? "produit" : p.getCategory().getName())
                .replace('\n', ' ')
                .trim();
    }

    @SuppressWarnings("unchecked")
    private String extractInlineImage(Map<String, Object> body) {
        if (body == null) return null;
        List<Map<String, Object>> candidates = (List<Map<String, Object>>) body.get("candidates");
        if (candidates == null || candidates.isEmpty()) return null;
        Map<String, Object> content = (Map<String, Object>) candidates.get(0).get("content");
        if (content == null) return null;
        List<Map<String, Object>> parts = (List<Map<String, Object>>) content.get("parts");
        if (parts == null) return null;
        for (Map<String, Object> part : parts) {
            Map<String, Object> inlineData = (Map<String, Object>) part.get("inlineData");
            if (inlineData == null) inlineData = (Map<String, Object>) part.get("inline_data");
            if (inlineData != null) {
                return (String) inlineData.get("data");
            }
        }
        return null;
    }

    private String persistImage(String base64) throws IOException {
        byte[] bytes = Base64.getDecoder().decode(base64);
        Path dir = Paths.get(imagesDir).toAbsolutePath();
        Files.createDirectories(dir);

        String filename = UUID.randomUUID() + ".png";
        Path target = dir.resolve(filename);
        Files.write(target, bytes);
        log.info("Image enregistrée : {} ({} octets)", target, bytes.length);

        // Public URL served by Spring static resource handler (configured in WebConfig)
        return publicPath + "/" + filename;
    }

    private String abbreviate(String s, int max) {
        return s.length() <= max ? s : s.substring(0, max) + "…";
    }
}
