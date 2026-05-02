package com.estore.inventory.dto;

import com.estore.inventory.entity.Inventory;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InventoryDto {

    private Long productId;

    @NotNull
    @Min(0)
    private Integer quantity;

    public static InventoryDto from(Inventory inv) {
        return InventoryDto.builder()
                .productId(inv.getProduct().getId())
                .quantity(inv.getQuantity())
                .build();
    }
}
