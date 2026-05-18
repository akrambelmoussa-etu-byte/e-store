package com.estore.catalog.repository;

import com.estore.catalog.entity.Product;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.math.BigDecimal;

public interface ProductRepository extends JpaRepository<Product, Long> {

    /**
     * Recherche multi-critères du catalogue.
     *
     * <p>Tous les paramètres sont optionnels — passer {@code null} (ou {@code false}
     * pour {@code inStockOnly}) revient à désactiver le filtre correspondant.
     */
    @Query("""
            SELECT p FROM Product p
            WHERE (:categoryId IS NULL OR p.category.id = :categoryId)
              AND (:q IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%', :q, '%'))
                              OR LOWER(p.description) LIKE LOWER(CONCAT('%', :q, '%')))
              AND (:minPrice IS NULL OR p.price >= :minPrice)
              AND (:maxPrice IS NULL OR p.price <= :maxPrice)
              AND (:inStockOnly = FALSE OR (p.inventory IS NOT NULL AND p.inventory.quantity > 0))
            """)
    Page<Product> search(@Param("categoryId") Long categoryId,
                         @Param("q") String q,
                         @Param("minPrice") BigDecimal minPrice,
                         @Param("maxPrice") BigDecimal maxPrice,
                         @Param("inStockOnly") boolean inStockOnly,
                         Pageable pageable);
}
