package com.estore.review.service;

import com.estore.catalog.service.ProductService;
import com.estore.customer.entity.User;
import com.estore.customer.security.SecurityUtils;
import com.estore.review.document.Review;
import com.estore.review.dto.CreateReviewDto;
import com.estore.review.dto.ReviewDto;
import com.estore.review.repository.ReviewRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;

/**
 * Gestion des avis (MongoDB).
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class ReviewService {

    private final ReviewRepository reviewRepository;
    private final ProductService productService;
    private final SecurityUtils securityUtils;

    public ReviewDto create(CreateReviewDto dto) {
        // Vérifier que le produit existe
        productService.get(dto.getProductId());

        User user = securityUtils.currentUser();
        Review review = Review.builder()
                .productId(dto.getProductId())
                .userId(user.getId())
                .authorName(user.getFirstName() + " " + user.getLastName())
                .rating(dto.getRating())
                .comment(dto.getComment())
                .createdAt(Instant.now())
                .build();
        Review saved = reviewRepository.save(review);
        log.info("Avis #{} créé sur produit {}", saved.getId(), dto.getProductId());
        return ReviewDto.from(saved);
    }

    public List<ReviewDto> findByProduct(Long productId) {
        return reviewRepository.findByProductIdOrderByCreatedAtDesc(productId)
                .stream().map(ReviewDto::from).toList();
    }

    public List<ReviewDto> findByUser(Long userId) {
        return reviewRepository.findByUserIdOrderByCreatedAtDesc(userId)
                .stream().map(ReviewDto::from).toList();
    }
}
