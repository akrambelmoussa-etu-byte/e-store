package com.estore.catalog.service;

import com.estore.catalog.dto.CreateProductDto;
import com.estore.catalog.dto.ProductDto;
import com.estore.catalog.entity.Category;
import com.estore.catalog.entity.Product;
import com.estore.catalog.repository.CategoryRepository;
import com.estore.catalog.repository.ProductRepository;
import com.estore.exception.ResourceNotFoundException;
import com.estore.inventory.entity.Inventory;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;

    @Transactional(readOnly = true)
    public Page<ProductDto> search(Long categoryId,
                                   String q,
                                   BigDecimal minPrice,
                                   BigDecimal maxPrice,
                                   boolean inStockOnly,
                                   String sort,
                                   int page,
                                   int size) {
        Pageable pageable = PageRequest.of(page, size, resolveSort(sort));
        String query = (q != null && q.isBlank()) ? null : q;
        return productRepository
                .search(categoryId, query, minPrice, maxPrice, inStockOnly, pageable)
                .map(ProductDto::from);
    }

    /** Compat overload — appelé par d'autres modules qui ne filtrent pas par prix/stock. */
    @Transactional(readOnly = true)
    public Page<ProductDto> search(Long categoryId, String q, int page, int size) {
        return search(categoryId, q, null, null, false, "newest", page, size);
    }

    @Transactional(readOnly = true)
    public ProductDto findById(Long id) {
        return ProductDto.from(get(id));
    }

    @Transactional
    public ProductDto create(CreateProductDto dto) {
        Category category = categoryRepository.findById(dto.getCategoryId())
                .orElseThrow(() -> new ResourceNotFoundException("Catégorie introuvable : " + dto.getCategoryId()));

        Product product = Product.builder()
                .name(dto.getName())
                .description(dto.getDescription())
                .price(dto.getPrice())
                .imageUrl(dto.getImageUrl())
                .category(category)
                .build();

        Inventory inventory = Inventory.builder()
                .product(product)
                .quantity(dto.getInitialStock() == null ? 0 : dto.getInitialStock())
                .build();
        product.setInventory(inventory);

        Product saved = productRepository.save(product);
        return ProductDto.from(saved);
    }

    @Transactional
    public ProductDto update(Long id, CreateProductDto dto) {
        Product p = get(id);
        if (dto.getCategoryId() != null && !dto.getCategoryId().equals(p.getCategory().getId())) {
            Category category = categoryRepository.findById(dto.getCategoryId())
                    .orElseThrow(() -> new ResourceNotFoundException("Catégorie introuvable : " + dto.getCategoryId()));
            p.setCategory(category);
        }
        p.setName(dto.getName());
        p.setDescription(dto.getDescription());
        p.setPrice(dto.getPrice());
        p.setImageUrl(dto.getImageUrl());
        return ProductDto.from(productRepository.save(p));
    }

    @Transactional
    public void delete(Long id) {
        productRepository.delete(get(id));
    }

    /** Met à jour uniquement l'URL d'image — utilisé par GeminiImageService. */
    @Transactional
    public ProductDto updateImage(Long id, String imageUrl) {
        Product p = get(id);
        p.setImageUrl(imageUrl);
        return ProductDto.from(productRepository.save(p));
    }

    /** Méthode utilitaire interne. */
    public Product get(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Produit introuvable : " + id));
    }

    /**
     * Mappe une clé textuelle ("newest", "price_asc"...) vers une {@link Sort} JPA.
     * Inconnu / null → tri par défaut (plus récent en premier).
     */
    private Sort resolveSort(String key) {
        if (key == null) return Sort.by("id").descending();
        return switch (key.toLowerCase()) {
            case "price_asc"  -> Sort.by("price").ascending();
            case "price_desc" -> Sort.by("price").descending();
            case "name_asc"   -> Sort.by("name").ascending();
            case "name_desc"  -> Sort.by("name").descending();
            case "oldest"     -> Sort.by("id").ascending();
            default           -> Sort.by("id").descending();
        };
    }
}
