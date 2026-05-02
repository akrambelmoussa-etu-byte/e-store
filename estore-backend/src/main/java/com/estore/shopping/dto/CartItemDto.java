package com.estore.shopping.dto;

import com.estore.shopping.entity.CartItem;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CartItemDto {

    private Long id;
    private Long productId;
    private String productName;
    private String imageUrl;
    private Integer quantity;
    private BigDecimal unitPrice;
    private BigDecimal subtotal;

    public static CartItemDto from(CartItem ci) {
        BigDecimal subtotal = ci.getUnitPrice().multiply(BigDecimal.valueOf(ci.getQuantity()));
        return CartItemDto.builder()
                .id(ci.getId())
                .productId(ci.getProduct().getId())
                .productName(ci.getProduct().getName())
                .imageUrl(ci.getProduct().getImageUrl())
                .quantity(ci.getQuantity())
                .unitPrice(ci.getUnitPrice())
                .subtotal(subtotal)
                .build();
    }
}
