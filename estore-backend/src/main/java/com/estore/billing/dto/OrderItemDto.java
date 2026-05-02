package com.estore.billing.dto;

import com.estore.billing.entity.OrderItem;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderItemDto {

    private Long id;
    private Long productId;
    private String productName;
    private Integer quantity;
    private BigDecimal unitPrice;
    private BigDecimal subtotal;

    public static OrderItemDto from(OrderItem oi) {
        BigDecimal subtotal = oi.getUnitPrice().multiply(BigDecimal.valueOf(oi.getQuantity()));
        return OrderItemDto.builder()
                .id(oi.getId())
                .productId(oi.getProduct().getId())
                .productName(oi.getProduct().getName())
                .quantity(oi.getQuantity())
                .unitPrice(oi.getUnitPrice())
                .subtotal(subtotal)
                .build();
    }
}
