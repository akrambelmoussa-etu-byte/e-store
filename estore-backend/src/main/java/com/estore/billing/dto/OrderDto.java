package com.estore.billing.dto;

import com.estore.billing.entity.Order;
import com.estore.billing.entity.OrderStatus;
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
public class OrderDto {

    private Long id;
    private Instant orderDate;
    private BigDecimal totalAmount;
    private OrderStatus status;
    private List<OrderItemDto> items;

    public static OrderDto from(Order o) {
        return OrderDto.builder()
                .id(o.getId())
                .orderDate(o.getOrderDate())
                .totalAmount(o.getTotalAmount())
                .status(o.getStatus())
                .items(o.getItems().stream().map(OrderItemDto::from).toList())
                .build();
    }
}
