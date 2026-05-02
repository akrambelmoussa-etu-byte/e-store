package com.estore.review.dto;

import com.estore.review.document.Review;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReviewDto {

    private String id;
    private Long productId;
    private Long userId;
    private String authorName;
    private int rating;
    private String comment;
    private Instant createdAt;

    public static ReviewDto from(Review r) {
        return ReviewDto.builder()
                .id(r.getId())
                .productId(r.getProductId())
                .userId(r.getUserId())
                .authorName(r.getAuthorName())
                .rating(r.getRating())
                .comment(r.getComment())
                .createdAt(r.getCreatedAt())
                .build();
    }
}
