package com.estore.shopping.dto;

import com.estore.shopping.entity.Cart;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CartDto {

    private Long id;
    private List<CartItemDto> items;
    private BigDecimal total;
    private Integer itemCount;
    private Instant updatedAt;

    public static CartDto from(Cart c) {
        List<CartItemDto> items = c.getItems().stream().map(CartItemDto::from).toList();
        BigDecimal total = items.stream()
                .map(CartItemDto::getSubtotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        int count = items.stream().mapToInt(CartItemDto::getQuantity).sum();
        return CartDto.builder()
                .id(c.getId())
                .items(items)
                .total(total)
                .itemCount(count)
                .updatedAt(c.getUpdatedAt())
                .build();
    }
}
