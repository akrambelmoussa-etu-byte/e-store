package com.estore.billing.service;

import com.estore.billing.dto.OrderDto;
import com.estore.billing.entity.Order;
import com.estore.billing.entity.OrderItem;
import com.estore.billing.entity.OrderStatus;
import com.estore.billing.repository.OrderRepository;
import com.estore.customer.entity.User;
import com.estore.customer.security.SecurityUtils;
import com.estore.exception.BusinessException;
import com.estore.exception.ResourceNotFoundException;
import com.estore.inventory.service.InventoryService;
import com.estore.shopping.entity.Cart;
import com.estore.shopping.entity.CartItem;
import com.estore.shopping.service.CartService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final CartService cartService;
    private final InventoryService inventoryService;
    private final SecurityUtils securityUtils;

    /**
     * Valide le panier de l'utilisateur courant : crée la commande, décrémente le stock,
     * vide le panier. Tout en transactionnel — rollback si une étape échoue.
     */
    @Transactional
    public OrderDto checkout() {
        User user = securityUtils.currentUser();
        Cart cart = cartService.getOrCreateCart(user);

        if (cart.getItems().isEmpty()) {
            throw new BusinessException("Votre panier est vide");
        }

        // Vérifier le stock pour tous les items AVANT de commencer
        for (CartItem ci : cart.getItems()) {
            inventoryService.checkAvailability(ci.getProduct().getId(), ci.getQuantity());
        }

        // Créer la commande PENDING
        Order order = Order.builder()
                .user(user)
                .status(OrderStatus.PENDING)
                .totalAmount(BigDecimal.ZERO)
                .items(new ArrayList<>())
                .build();

        BigDecimal total = BigDecimal.ZERO;
        for (CartItem ci : cart.getItems()) {
            OrderItem oi = OrderItem.builder()
                    .order(order)
                    .product(ci.getProduct())
                    .quantity(ci.getQuantity())
                    .unitPrice(ci.getUnitPrice())
                    .build();
            order.getItems().add(oi);
            total = total.add(ci.getUnitPrice().multiply(BigDecimal.valueOf(ci.getQuantity())));

            // Décrémenter le stock
            inventoryService.decrement(ci.getProduct().getId(), ci.getQuantity());
        }

        order.setTotalAmount(total);
        order.setStatus(OrderStatus.CONFIRMED);
        Order saved = orderRepository.save(order);

        // Vider le panier
        cartService.clearCart(cart);

        log.info("Commande #{} confirmée pour {} (total : {})", saved.getId(), user.getEmail(), total);
        return OrderDto.from(saved);
    }

    @Transactional(readOnly = true)
    public List<OrderDto> myOrders() {
        User user = securityUtils.currentUser();
        return orderRepository.findByUserIdOrderByOrderDateDesc(user.getId())
                .stream().map(OrderDto::from).toList();
    }

    @Transactional(readOnly = true)
    public OrderDto findById(Long id) {
        User user = securityUtils.currentUser();
        Order o = orderRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Commande introuvable : " + id));
        if (!o.getUser().getId().equals(user.getId())
                && !user.getRole().name().equals("ADMIN")) {
            throw new BusinessException("Cette commande ne vous appartient pas");
        }
        return OrderDto.from(o);
    }
}
