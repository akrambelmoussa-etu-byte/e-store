-- ============================================================
-- Script SQL E-Store — Creation manuelle des tables
-- Base de donnees : estore
-- Executer dans MySQL Workbench si le backend ne demarre pas
-- ============================================================

CREATE DATABASE IF NOT EXISTS estore
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE estore;

-- ------------------------------------------------------------
-- 1. USERS (domaine customer)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('ROLE_USER','ROLE_ADMIN') NOT NULL DEFAULT 'ROLE_USER',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 2. CATEGORIES (domaine catalog)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 3. PRODUCTS (domaine catalog)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    description  TEXT,
    price        DECIMAL(10,2) NOT NULL,
    image_url    VARCHAR(500),
    category_id  BIGINT NOT NULL,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id)
        REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 4. INVENTORY (domaine inventory)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS inventory (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id  BIGINT NOT NULL UNIQUE,
    quantity    INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_inventory_product FOREIGN KEY (product_id)
        REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 5. CARTS (domaine shopping)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS carts (
    id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    CONSTRAINT fk_cart_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 6. CART_ITEMS (domaine shopping)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cart_items (
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    cart_id    BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity   INT NOT NULL DEFAULT 1,
    CONSTRAINT fk_cartitem_cart    FOREIGN KEY (cart_id)   REFERENCES carts(id)    ON DELETE CASCADE,
    CONSTRAINT fk_cartitem_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 7. ORDERS (domaine billing)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id     BIGINT NOT NULL,
    status      ENUM('PENDING','CONFIRMED','SHIPPED','DELIVERED','CANCELLED')
                    NOT NULL DEFAULT 'PENDING',
    total       DECIMAL(10,2) NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- 8. ORDER_ITEMS (domaine billing)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id    BIGINT NOT NULL,
    product_id  BIGINT NOT NULL,
    quantity    INT NOT NULL,
    unit_price  DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_orderitem_order   FOREIGN KEY (order_id)   REFERENCES orders(id)   ON DELETE CASCADE,
    CONSTRAINT fk_orderitem_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Donnees de test (optionnel)
-- ============================================================

INSERT IGNORE INTO categories (name, description) VALUES
    ('Electronique',   'Smartphones, laptops, accessoires high-tech'),
    ('Vetements',      'Mode homme et femme'),
    ('Livres',         'Romans, manuels techniques, BD'),
    ('Sport',          'Equipements et vetements sportifs'),
    ('Maison',         'Decoration et mobilier');

INSERT IGNORE INTO users (first_name, last_name, email, password, role) VALUES
    ('Admin',   'E-Store',  'admin@estore.ma',
     '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'ROLE_ADMIN'),
    ('Akram',   'Belmoussa','akram@estore.ma',
     '$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'ROLE_USER');
-- Mot de passe : password (BCrypt)

-- ============================================================
-- Verification rapide
-- ============================================================
SHOW TABLES;

SELECT
    TABLE_NAME        AS 'Table',
    TABLE_ROWS        AS 'Lignes (approx)',
    ENGINE            AS 'Moteur',
    TABLE_COMMENT     AS 'Commentaire'
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'estore'
ORDER BY TABLE_NAME;
