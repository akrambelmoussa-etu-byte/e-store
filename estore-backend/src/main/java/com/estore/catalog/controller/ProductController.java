package com.estore.catalog.controller;

import com.estore.catalog.dto.CreateProductDto;
import com.estore.catalog.dto.ProductDto;
import com.estore.catalog.service.GeminiImageService;
import com.estore.catalog.service.ProductService;
import com.estore.shared.ApiResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.Map;

@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;
    private final GeminiImageService geminiImageService;

    /**
     * Liste paginée du catalogue avec filtres optionnels.
     *
     * <p>{@code sort} accepte : {@code newest} (défaut), {@code oldest},
     * {@code price_asc}, {@code price_desc}, {@code name_asc}, {@code name_desc}.
     */
    @GetMapping
    public ResponseEntity<ApiResponse<Page<ProductDto>>> list(
            @RequestParam(required = false) Long categoryId,
            @RequestParam(required = false) String q,
            @RequestParam(required = false) BigDecimal minPrice,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(defaultValue = "false") boolean inStockOnly,
            @RequestParam(defaultValue = "newest") String sort,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "12") int size) {
        Page<ProductDto> result = productService.search(
                categoryId, q, minPrice, maxPrice, inStockOnly, sort, page, size);
        return ResponseEntity.ok(ApiResponse.ok(result));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<ProductDto>> get(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok(productService.findById(id)));
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<ProductDto>> create(@Valid @RequestBody CreateProductDto dto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Produit créé", productService.create(dto)));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<ProductDto>> update(@PathVariable Long id,
                                                          @Valid @RequestBody CreateProductDto dto) {
        return ResponseEntity.ok(ApiResponse.ok("Produit mis à jour", productService.update(id, dto)));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        productService.delete(id);
        return ResponseEntity.noContent().build();
    }

    /**
     * Génère une nouvelle image studio via Gemini Nano Banana et met à jour
     * l'URL d'image du produit. Réservé aux ADMIN.
     *
     * <p>Body optionnel : {@code { "prompt": "texte override" }} — sinon un
     * prompt est construit à partir du produit.
     */
    @PostMapping("/{id}/generate-image")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<ProductDto>> generateImage(
            @PathVariable Long id,
            @RequestBody(required = false) Map<String, String> body) {
        String prompt = body == null ? null : body.get("prompt");
        String url = geminiImageService.generateForProduct(id, prompt);
        ProductDto updated = productService.updateImage(id, url);
        return ResponseEntity.ok(ApiResponse.ok("Image générée par Gemini", updated));
    }
}
