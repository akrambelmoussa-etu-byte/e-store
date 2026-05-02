package com.estore.exception;

/**
 * Lancée lorsqu'une opération nécessite une authentification valide.
 */
public class UnauthorizedException extends RuntimeException {
    public UnauthorizedException(String message) {
        super(message);
    }
}
