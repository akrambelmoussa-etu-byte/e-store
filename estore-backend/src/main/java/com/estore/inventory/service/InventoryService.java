package com.estore.inventory.service;

import com.estore.exception.BusinessException;
import com.estore.exception.ResourceNotFoundException;
import com.estore.inventory.dto.InventoryDto;
import com.estore.inventory.entity.Inventory;
import com.estore.inventory.repository.InventoryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class InventoryService {

    private final InventoryRepository inventoryRepository;

    @Transactional(readOnly = true)
    public InventoryDto get(Long productId) {
        Inventory inv = inventoryRepository.findByProductId(productId)
                .orElseThrow(() -> new ResourceNotFoundException("Stock introuvable pour le produit : " + productId));
        return InventoryDto.from(inv);
    }

    @Transactional
    public InventoryDto update(Long productId, InventoryDto dto) {
        Inventory inv = inventoryRepository.findByProductId(productId)
                .orElseThrow(() -> new ResourceNotFoundException("Stock introuvable pour le produit : " + productId));
        inv.setQuantity(dto.getQuantity());
        return InventoryDto.from(inventoryRepository.save(inv));
    }

    /**
     * Décrémente le stock du produit après vérification. Lance BusinessException si insuffisant.
     */
    @Transactional
    public void decrement(Long productId, int quantity) {
        Inventory inv = inventoryRepository.findByProductId(productId)
                .orElseThrow(() -> new ResourceNotFoundException("Stock introuvable pour le produit : " + productId));
        if (inv.getQuantity() < quantity) {
            throw new BusinessException("Stock insuffisant pour le produit " + productId);
        }
        inv.setQuantity(inv.getQuantity() - quantity);
        inventoryRepository.save(inv);
    }

    /**
     * Vérifie sans modifier qu'au moins `quantity` unités sont disponibles.
     */
    @Transactional(readOnly = true)
    public void checkAvailability(Long productId, int quantity) {
        Inventory inv = inventoryRepository.findByProductId(productId)
                .orElseThrow(() -> new ResourceNotFoundException("Stock introuvable pour le produit : " + productId));
        if (inv.getQuantity() < quantity) {
            throw new BusinessException("Stock insuffisant pour le produit " + productId
                    + " (disponible : " + inv.getQuantity() + ", demandé : " + quantity + ")");
        }
    }
}
