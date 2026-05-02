package com.estore.shopping.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class UpdateCartItemDto {

    @NotNull
    private Long itemId;

    @NotNull
    @Min(1)
    private Integer quantity;
}
