package com.estore.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * <ul>
 *   <li>Autorise le frontend Angular (localhost:4200) à appeler {@code /api/**} et {@code /uploads/**}</li>
 *   <li>Expose le dossier local d'images générées par Gemini ({@code gemini.images.dir})
 *       sous l'URL {@code /uploads/products/*}, en lecture seule</li>
 * </ul>
 */
@Configuration
public class CorsConfig implements WebMvcConfigurer {

    @Value("${gemini.images.dir:./uploads/products}")
    private String imagesDir;

    @Value("${gemini.images.public-path:/uploads/products}")
    private String publicPath;

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:4200")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true)
                .maxAge(3600);

        registry.addMapping("/uploads/**")
                .allowedOrigins("http://localhost:4200")
                .allowedMethods("GET")
                .maxAge(3600);
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        Path absolute = Paths.get(imagesDir).toAbsolutePath().normalize();
        String location = absolute.toUri().toString(); // file:/C:/.../uploads/products/
        String mapping = publicPath.endsWith("/") ? publicPath + "**" : publicPath + "/**";

        registry.addResourceHandler(mapping)
                .addResourceLocations(location)
                .setCachePeriod(3600);
    }
}
