package com.estore.billing.controller;

import com.estore.billing.dto.OrderDto;
import com.estore.billing.service.OrderService;
import com.estore.shared.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @PostMapping
    public ResponseEntity<ApiResponse<OrderDto>> checkout() {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.ok("Commande créée", orderService.checkout()));
    }

    @GetMapping
    public ResponseEntity<ApiResponse<List<OrderDto>>> list() {
        return ResponseEntity.ok(ApiResponse.ok(orderService.myOrders()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<OrderDto>> get(@PathVariable Long id) {
        return ResponseEntity.ok(ApiResponse.ok(orderService.findById(id)));
    }
}
