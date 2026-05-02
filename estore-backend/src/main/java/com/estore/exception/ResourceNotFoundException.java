package com.estore.exception;

/**
 * Lancée lorsqu'une ressource n'est pas trouvée (404).
 */
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
