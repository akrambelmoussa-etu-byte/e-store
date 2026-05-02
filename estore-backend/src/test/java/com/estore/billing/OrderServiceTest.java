package com.estore.billing;

import com.estore.billing.dto.OrderDto;
import com.estore.billing.entity.Order;
import com.estore.billing.entity.OrderStatus;
import com.estore.billing.repository.OrderRepository;
import com.estore.billing.service.OrderService;
import com.estore.catalog.entity.Category;
import com.estore.catalog.entity.Product;
import com.estore.customer.entity.Role;
import com.estore.customer.entity.User;
import com.estore.customer.security.SecurityUtils;
import com.estore.exception.BusinessException;
import com.estore.inventory.service.InventoryService;
import com.estore.shopping.entity.Cart;
import com.estore.shopping.entity.CartItem;
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
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class OrderServiceTest {

    @Mock private OrderRepository orderRepository;
    @Mock private CartService cartService;
    @Mock private InventoryService inventoryService;
    @Mock private SecurityUtils securityUtils;

    @InjectMocks private OrderService orderService;

    private User user;
    private Cart cart;
    private Product product;

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
        cart = Cart.builder().id(100L).user(user).items(new ArrayList<>()).build();

        when(securityUtils.currentUser()).thenReturn(user);
        when(cartService.getOrCreateCart(user)).thenReturn(cart);
    }

    @Test
    void checkout_panierVide_lanceException() {
        assertThatThrownBy(() -> orderService.checkout())
                .isInstanceOf(BusinessException.class)
                .hasMessageContaining("vide");
    }

    @Test
    void checkout_panierValide_creeCommandeEtViderPanier() {
        CartItem item = CartItem.builder()
                .id(1L)
                .product(product)
                .quantity(2)
                .unitPrice(product.getPrice())
                .cart(cart)
                .build();
        cart.getItems().add(item);

        when(orderRepository.save(any(Order.class))).thenAnswer(inv -> {
            Order o = inv.getArgument(0);
            o.setId(500L);
            return o;
        });

        OrderDto dto = orderService.checkout();

        assertThat(dto.getId()).isEqualTo(500L);
        assertThat(dto.getStatus()).isEqualTo(OrderStatus.CONFIRMED);
        assertThat(dto.getTotalAmount()).isEqualByComparingTo(new BigDecimal("25000.00"));
        assertThat(dto.getItems()).hasSize(1);

        // Vérifie le décrément de stock + vidage panier
        verify(inventoryService).decrement(10L, 2);
        verify(cartService).clearCart(cart);
    }

    @Test
    void myOrders_renvoieListeTrieeParDate() {
        Order order = Order.builder()
                .id(1L)
                .user(user)
                .status(OrderStatus.CONFIRMED)
                .totalAmount(BigDecimal.TEN)
                .items(new ArrayList<>())
                .build();
        when(orderRepository.findByUserIdOrderByOrderDateDesc(1L)).thenReturn(List.of(order));

        List<OrderDto> orders = orderService.myOrders();

        assertThat(orders).hasSize(1);
        assertThat(orders.get(0).getId()).isEqualTo(1L);
    }
}
