package com.estore.catalog;

import com.estore.catalog.dto.ProductDto;
import com.estore.catalog.entity.Category;
import com.estore.catalog.entity.Product;
import com.estore.catalog.repository.CategoryRepository;
import com.estore.catalog.repository.ProductRepository;
import com.estore.catalog.service.ProductService;
import com.estore.exception.ResourceNotFoundException;
import com.estore.inventory.entity.Inventory;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ProductServiceTest {

    @Mock
    private ProductRepository productRepository;

    @Mock
    private CategoryRepository categoryRepository;

    @InjectMocks
    private ProductService productService;

    private Product product;

    @BeforeEach
    void setUp() {
        Category cat = Category.builder().id(1L).name("Informatique").build();
        product = Product.builder()
                .id(10L)
                .name("Dell XPS 13")
                .description("Ordinateur portable")
                .price(new BigDecimal("12500.00"))
                .category(cat)
                .build();
        product.setInventory(Inventory.builder().quantity(20).product(product).build());
    }

    @Test
    void findById_existant_renvoieDto() {
        when(productRepository.findById(10L)).thenReturn(Optional.of(product));

        ProductDto dto = productService.findById(10L);

        assertThat(dto.getId()).isEqualTo(10L);
        assertThat(dto.getName()).isEqualTo("Dell XPS 13");
        assertThat(dto.getStock()).isEqualTo(20);
    }

    @Test
    void findById_inexistant_lanceException() {
        when(productRepository.findById(999L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> productService.findById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("Produit introuvable");
    }

    @Test
    void search_parMotCle_filtreSurLeNom() {
        Page<Product> page = new PageImpl<>(List.of(product));
        when(productRepository.search(isNull(), eq("dell"), any(Pageable.class))).thenReturn(page);

        Page<ProductDto> result = productService.search(null, "dell", 0, 10);

        assertThat(result.getContent()).hasSize(1);
        assertThat(result.getContent().get(0).getName()).contains("Dell");
    }

    @Test
    void search_sansMotCle_renvoieTous() {
        Page<Product> page = new PageImpl<>(List.of(product));
        when(productRepository.search(isNull(), isNull(), any(Pageable.class))).thenReturn(page);

        Page<ProductDto> result = productService.search(null, null, 0, 10);

        assertThat(result.getContent()).hasSize(1);
    }
}
