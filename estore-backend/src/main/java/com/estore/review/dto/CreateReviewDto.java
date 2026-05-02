package com.estore.review.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class CreateReviewDto {

    @NotNull
    private Long productId;

    @Min(1)
    @Max(5)
    private int rating;

    @NotBlank
    @Size(max = 1000)
    private String comment;
}
