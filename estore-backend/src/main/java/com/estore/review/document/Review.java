package com.estore.review.document;

import lombok.*;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.Instant;

/**
 * Document Mongo pour les avis produits.
 */
@Document(collection = "reviews")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Review {

    @Id
    private String id;

    @Indexed
    private Long productId;

    @Indexed
    private Long userId;

    private String authorName;

    private int rating;

    private String comment;

    private Instant createdAt;
}
