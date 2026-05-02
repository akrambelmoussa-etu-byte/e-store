package com.estore.inventory.controller;

import com.estore.inventory.dto.InventoryDto;
import com.estore.inventory.service.InventoryService;
import com.estore.shared.ApiResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/inventory")
@RequiredArgsConstructor
public class InventoryController {

    private final InventoryService inventoryService;

    @GetMapping("/{productId}")
    public ResponseEntity<ApiResponse<InventoryDto>> get(@PathVariable Long productId) {
        return ResponseEntity.ok(ApiResponse.ok(inventoryService.get(productId)));
    }

    @PutMapping("/{productId}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<InventoryDto>> update(@PathVariable Long productId,
                                                            @Valid @RequestBody InventoryDto dto) {
        return ResponseEntity.ok(ApiResponse.ok("Stock mis à jour", inventoryService.update(productId, dto)));
    }
}
