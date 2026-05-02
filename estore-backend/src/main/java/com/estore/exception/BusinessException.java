package com.estore.exception;

/**
 * Erreur métier (ex : stock insuffisant, panier vide, email déjà pris) → HTTP 409.
 */
public class BusinessException extends RuntimeException {
    public BusinessException(String message) {
        super(message);
    }
}
