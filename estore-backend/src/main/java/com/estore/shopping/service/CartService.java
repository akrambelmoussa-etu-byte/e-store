package com.estore.shopping.service;

import com.estore.catalog.entity.Product;
import com.estore.catalog.service.ProductService;
import com.estore.customer.entity.User;
import com.estore.customer.security.SecurityUtils;
import com.estore.exception.BusinessException;
import com.estore.exception.ResourceNotFoundException;
import com.estore.inventory.service.InventoryService;
import com.estore.shopping.dto.AddToCartDto;
import com.estore.shopping.dto.CartDto;
import com.estore.shopping.dto.UpdateCartItemDto;
import com.estore.shopping.entity.Cart;
import com.estore.shopping.entity.CartItem;
import com.estore.shopping.repository.CartItemRepository;
import com.estore.shopping.repository.CartRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * Gère le panier de l'utilisateur courant.
 */
@Service
@RequiredArgsConstructor
public class CartService {

    private final CartRepository cartRepository;
    private final CartItemRepository cartItemRepository;
    private final ProductService productService;
    private final InventoryService inventoryService;
    private final SecurityUtils securityUtils;

    @Transactional
    public CartDto getMyCart() {
        Cart cart = getOrCreateCart(securityUtils.currentUser());
        return CartDto.from(cart);
    }

    @Transactional
    public CartDto addItem(AddToCartDto dto) {
        User user = securityUtils.currentUser();
        Cart cart = getOrCreateCart(user);
        Product product = productService.get(dto.getProductId());

        // Quantité totale après ajout (si déjà présent)
        Optional<CartItem> existing = cart.getItems().stream()
                .filter(ci -> ci.getProduct().getId().equals(product.getId()))
                .findFirst();

        int currentQty = existing.map(CartItem::getQuantity).orElse(0);
        int newQty = currentQty + dto.getQuantity();
        inventoryService.checkAvailability(product.getId(), newQty);

        if (existing.isPresent()) {
            existing.get().setQuantity(newQty);
        } else {
            CartItem item = CartItem.builder()
                    .cart(cart)
                    .product(product)
                    .quantity(dto.getQuantity())
                    .unitPrice(product.getPrice())
                    .build();
            cart.getItems().add(item);
        }
        cart.touch();
        return CartDto.from(cartRepository.save(cart));
    }

    @Transactional
    public CartDto updateItem(UpdateCartItemDto dto) {
        User user = securityUtils.currentUser();
        Cart cart = getOrCreateCart(user);

        CartItem item = cart.getItems().stream()
                .filter(ci -> ci.getId().equals(dto.getItemId()))
                .findFirst()
                .orElseThrow(() -> new ResourceNotFoundException("Article introuvable dans le panier"));

        inventoryService.checkAvailability(item.getProduct().getId(), dto.getQuantity());
        item.setQuantity(dto.getQuantity());
        cart.touch();
        return CartDto.from(cartRepository.save(cart));
    }

    @Transactional
    public CartDto removeItem(Long itemId) {
        User user = securityUtils.currentUser();
        Cart cart = getOrCreateCart(user);

        boolean removed = cart.getItems().removeIf(ci -> ci.getId().equals(itemId));
        if (!removed) {
            throw new ResourceNotFoundException("Article introuvable dans le panier");
        }
        cart.touch();
        return CartDto.from(cartRepository.save(cart));
    }

    @Transactional
    public CartDto clear() {
        User user = securityUtils.currentUser();
        Cart cart = getOrCreateCart(user);
        cart.getItems().clear();
        cart.touch();
        return CartDto.from(cartRepository.save(cart));
    }

    /** Vide le panier sans vérifier l'utilisateur courant (utilisé après commande). */
    @Transactional
    public void clearCart(Cart cart) {
        cart.getItems().clear();
        cart.touch();
        cartRepository.save(cart);
    }

    /** Récupère ou crée le panier de l'utilisateur. */
    @Transactional
    public Cart getOrCreateCart(User user) {
        return cartRepository.findByUserId(user.getId())
                .orElseGet(() -> {
                    if (cartRepository.findByUserId(user.getId()).isPresent()) {
                        return cartRepository.findByUserId(user.getId()).get();
                    }
                    Cart c = Cart.builder().user(user).build();
                    return cartRepository.save(c);
                });
    }

    @Transactional(readOnly = true)
    public Cart getMyCartEntity() {
        User user = securityUtils.currentUser();
        return cartRepository.findByUserId(user.getId())
                .orElseThrow(() -> new BusinessException("Panier vide"));
    }
}
