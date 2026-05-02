# E-Store — Mini-projet Full-Stack

Application e-commerce pédagogique développée dans le cadre du module **Full-Stack** sous la direction du **Pr. Omar Zahour**, Faculté des Sciences Ben M'Sick — Université Hassan II de Casablanca.

> Auteurs : **Akram Belmoussa** & **Nouhaila Ben Soumane** — 2025-2026

## Stack technique

| Couche | Technologie |
| --- | --- |
| Frontend | Angular 17+ (standalone components), Bootstrap 5 |
| Backend | Spring Boot 3.3, Spring Data JPA, Spring Security, JWT |
| Base relationnelle | MySQL 8 (prod) / H2 in-memory (dev) |
| Base documentaire | MongoDB 7 |
| Build | Maven (backend), npm/Angular CLI (frontend) |

## Architecture

3 couches techniques :
1. **Presentation** — Angular (composants, routes, services HTTP)
2. **Business Logic** — Spring Boot (controllers REST, services, DTOs)
3. **Data Access** — Spring Data JPA + Spring Data MongoDB

5 domaines fonctionnels : `customer`, `catalog`, `inventory`, `shopping`, `billing` (+ `review` pour MongoDB).

## Pré-requis

- JDK 17+
- Node 20+
- Docker Desktop *(recommandé)* ou MySQL 8 + MongoDB 7 installés localement

## Démarrage rapide en 5 minutes

### 1. Lancer les bases de données (Docker)

```bash
docker compose up -d
```

Cela démarre MySQL (port 3306), MongoDB (port 27017), phpMyAdmin (port 8081) et mongo-express (port 8082).

> Pour démarrer **sans Docker**, utilisez le profil `dev` (H2 in-memory) — le backend démarre tel quel.

### 2. Backend Spring Boot

```bash
cd estore-backend
./mvnw spring-boot:run
```

Le backend écoute sur `http://localhost:8080`.

### 3. Frontend Angular

```bash
cd estore-frontend
npm install
npm start
```

Ouvrir `http://localhost:4200`.

## Comptes de test

| Email | Mot de passe | Rôle |
| --- | --- | --- |
| `admin@estore.ma` | `Admin@123` | ADMIN |
| `user@estore.ma`  | `User@123`  | USER |

## Endpoints REST principaux

| Méthode | URL | Description |
| --- | --- | --- |
| POST | `/api/auth/register` | Inscription |
| POST | `/api/auth/login` | Connexion (renvoie le JWT) |
| GET | `/api/products` | Liste des produits (filtres : `categoryId`, `q`, `page`, `size`) |
| GET | `/api/products/{id}` | Détail d'un produit |
| GET | `/api/categories` | Liste des catégories |
| GET | `/api/cart` | Panier de l'utilisateur courant |
| POST | `/api/cart/add` | Ajouter un produit au panier |
| POST | `/api/orders` | Valider la commande |
| GET | `/api/orders` | Historique des commandes |
| POST | `/api/reviews` | Déposer un avis (Mongo) |
| GET | `/api/reviews/product/{id}` | Avis d'un produit |

## Structure des dossiers

```
estore/
├── README.md
├── docker-compose.yml
├── estore-backend/      Spring Boot
│   └── src/main/java/com/estore/
│       ├── customer/    User, auth, profile
│       ├── catalog/     Catégories + produits
│       ├── inventory/   Stock
│       ├── shopping/    Panier
│       ├── billing/     Commandes
│       ├── review/      Avis (MongoDB)
│       ├── shared/      Utilitaires partagés
│       ├── config/      CORS, Security, DataSeeder
│       └── exception/   Gestion globale des erreurs
└── estore-frontend/     Angular 17
    └── src/app/
        ├── core/        Services, guards, interceptors
        ├── shared/      Composants partagés
        └── features/    Pages métier
```

## Tests

```bash
cd estore-backend
./mvnw test
```

Trois tests unitaires couvrent les services principaux : `ProductService`, `CartService`, `OrderService`.

## Sécurité

- BCrypt pour les mots de passe
- JWT signé HMAC-SHA256, expiration 24h
- Endpoints publics : `/api/auth/**`, `GET /api/products/**`, `GET /api/categories/**`, `GET /api/reviews/**`
- Endpoints `ADMIN` protégés par `@PreAuthorize("hasRole('ADMIN')")`

## Captures d'écran

*(à compléter après la démo — placeholders dans `docs/screenshots/`)*

## Architecture détaillée

Voir le rapport technique : `docs/rapport-estore.pdf` *(à générer)*.
