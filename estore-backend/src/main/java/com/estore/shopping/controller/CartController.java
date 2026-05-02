package com.estore.shopping.controller;

import com.estore.shared.ApiResponse;
import com.estore.shopping.dto.AddToCartDto;
import com.estore.shopping.dto.CartDto;
import com.estore.shopping.dto.UpdateCartItemDto;
import com.estore.shopping.service.CartService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/cart")
@RequiredArgsConstructor
public class CartController {

    private final CartService cartService;

    @GetMapping
    public ResponseEntity<ApiResponse<CartDto>> get() {
        return ResponseEntity.ok(ApiResponse.ok(cartService.getMyCart()));
    }

    @PostMapping("/add")
    public ResponseEntity<ApiResponse<CartDto>> add(@Valid @RequestBody AddToCartDto dto) {
        return ResponseEntity.ok(ApiResponse.ok("Article ajouté au panier", cartService.addItem(dto)));
    }

    @PutMapping("/update")
    public ResponseEntity<ApiResponse<CartDto>> update(@Valid @RequestBody UpdateCartItemDto dto) {
        return ResponseEntity.ok(ApiResponse.ok("Quantité mise à jour", cartService.updateItem(dto)));
    }

    @DeleteMapping("/remove/{itemId}")
    public ResponseEntity<ApiResponse<CartDto>> remove(@PathVariable Long itemId) {
        return ResponseEntity.ok(ApiResponse.ok("Article retiré", cartService.removeItem(itemId)));
    }

    @DeleteMapping("/clear")
    public ResponseEntity<ApiResponse<CartDto>> clear() {
        return ResponseEntity.ok(ApiResponse.ok("Panier vidé", cartService.clear()));
    }
}
