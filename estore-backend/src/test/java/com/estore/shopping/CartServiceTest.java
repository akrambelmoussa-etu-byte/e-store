package com.estore.shopping;

import com.estore.catalog.entity.Category;
import com.estore.catalog.entity.Product;
import com.estore.catalog.service.ProductService;
import com.estore.customer.entity.Role;
import com.estore.customer.entity.User;
import com.estore.customer.security.SecurityUtils;
import com.estore.exception.BusinessException;
import com.estore.inventory.entity.Inventory;
import com.estore.inventory.service.InventoryService;
import com.estore.shopping.dto.AddToCartDto;
import com.estore.shopping.dto.CartDto;
import com.estore.shopping.entity.Cart;
import com.estore.shopping.repository.CartItemRepository;
import com.estore.shopping.repository.CartRepository;
import com.estore.shopping.service.CartService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class CartServiceTest {

    @Mock private CartRepository cartRepository;
    @Mock private CartItemRepository cartItemRepository;
    @Mock private ProductService productService;
    @Mock private InventoryService inventoryService;
    @Mock private SecurityUtils securityUtils;

    @InjectMocks private CartService cartService;

    private User user;
    private Product product;
    private Cart cart;

    @BeforeEach
    void setUp() {
        user = User.builder().id(1L).email("user@test.ma").role(Role.USER).build();
        Category cat = Category.builder().id(1L).name("Informatique").build();
        product = Product.builder()
                .id(10L)
                .name("Dell XPS 13")
                .price(new BigDecimal("12500.00"))
                .category(cat)
                .build();
        product.setInventory(Inventory.builder().quantity(20).product(product).build());
        cart = Cart.builder().id(100L).user(user).items(new ArrayList<>()).build();

        when(securityUtils.currentUser()).thenReturn(user);
        when(cartRepository.findByUserId(1L)).thenReturn(Optional.of(cart));
        when(cartRepository.save(any(Cart.class))).thenAnswer(inv -> inv.getArgument(0));
    }

    @Test
    void addItem_avecStockSuffisant_ajouteAuPanier() {
        when(productService.get(10L)).thenReturn(product);
        AddToCartDto dto = new AddToCartDto();
        dto.setProductId(10L);
        dto.setQuantity(2);

        CartDto result = cartService.addItem(dto);

        assertThat(result.getItems()).hasSize(1);
        assertThat(result.getItems().get(0).getQuantity()).isEqualTo(2);
        assertThat(result.getTotal()).isEqualByComparingTo(new BigDecimal("25000.00"));
        verify(inventoryService).checkAvailability(10L, 2);
    }

    @Test
    void addItem_avecStockInsuffisant_lanceException() {
        when(productService.get(10L)).thenReturn(product);
        doThrow(new BusinessException("Stock insuffisant"))
                .when(inventoryService).checkAvailability(10L, 999);
        AddToCartDto dto = new AddToCartDto();
        dto.setProductId(10L);
        dto.setQuantity(999);

        assertThatThrownBy(() -> cartService.addItem(dto))
                .isInstanceOf(BusinessException.class)
                .hasMessageContaining("Stock insuffisant");
    }
}
