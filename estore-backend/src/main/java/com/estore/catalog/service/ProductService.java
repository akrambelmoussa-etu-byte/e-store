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

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository productRepository;
    private final CategoryRepository categoryRepository;

    @Transactional(readOnly = true)
    public Page<ProductDto> search(Long categoryId, String q, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("id").descending());
        String query = (q != null && q.isBlank()) ? null : q;
        return productRepository.search(categoryId, query, pageable).map(ProductDto::from);
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

    /** Méthode utilitaire interne. */
    public Product get(Long id) {
        return productRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Produit introuvable : " + id));
    }
}
