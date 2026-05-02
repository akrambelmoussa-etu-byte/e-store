package com.estore.review.controller;

import com.estore.review.dto.CreateReviewDto;
import com.estore.review.dto.ReviewDto;
import com.estore.review.service.ReviewService;
import com.estore.shared.ApiResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reviews")
@RequiredArgsConstructor
public class ReviewController {

    private final ReviewService reviewService;

    @PostMapping
    public ResponseEntity<ApiResponse<ReviewDto>> create(@Valid @RequestBody CreateReviewDto dto) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Avis publié", reviewService.create(dto)));
    }

    @GetMapping("/product/{productId}")
    public ResponseEntity<ApiResponse<List<ReviewDto>>> byProduct(@PathVariable Long productId) {
        return ResponseEntity.ok(ApiResponse.ok(reviewService.findByProduct(productId)));
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<ApiResponse<List<ReviewDto>>> byUser(@PathVariable Long userId) {
        return ResponseEntity.ok(ApiResponse.ok(reviewService.findByUser(userId)));
    }
}
