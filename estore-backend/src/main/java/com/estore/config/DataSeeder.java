package com.estore.config;

import com.estore.catalog.entity.Category;
import com.estore.catalog.entity.Product;
import com.estore.catalog.repository.CategoryRepository;
import com.estore.catalog.repository.ProductRepository;
import com.estore.customer.entity.Profile;
import com.estore.customer.entity.Role;
import com.estore.customer.entity.User;
import com.estore.customer.repository.UserRepository;
import com.estore.inventory.entity.Inventory;
import com.estore.review.document.Review;
import com.estore.review.repository.ReviewRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Initialise la base avec des données de démonstration si elle est vide.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class DataSeeder implements CommandLineRunner {

    private final UserRepository userRepository;
    private final CategoryRepository categoryRepository;
    private final ProductRepository productRepository;
    private final ReviewRepository reviewRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    @Transactional
    public void run(String... args) {
        seedRelational();
        seedMongo();
    }

    private void seedRelational() {
        if (userRepository.count() > 0) {
            log.info("Base relationnelle déjà peuplée — seed ignoré.");
            return;
        }
        log.info("Seed des données relationnelles…");

        // ─── Utilisateurs ─────────────────────────────────────────────
        User admin = User.builder()
                .firstName("Akram")
                .lastName("Admin")
                .email("admin@estore.ma")
                .password(passwordEncoder.encode("Admin@123"))
                .role(Role.ADMIN)
                .build();
        admin.setProfile(Profile.builder()
                .user(admin)
                .phone("+212 600 000 001")
                .address("Faculté des Sciences Ben M'Sick")
                .city("Casablanca")
                .country("Maroc")
                .build());

        User user = User.builder()
                .firstName("Nouhaila")
                .lastName("Test")
                .email("user@estore.ma")
                .password(passwordEncoder.encode("User@123"))
                .role(Role.USER)
                .build();
        user.setProfile(Profile.builder()
                .user(user)
                .phone("+212 600 000 002")
                .address("Université Hassan II")
                .city("Casablanca")
                .country("Maroc")
                .build());

        userRepository.save(admin);
        userRepository.save(user);
        log.info("→ 2 utilisateurs créés (admin@estore.ma / user@estore.ma)");

        // ─── Catégories ───────────────────────────────────────────────
        Category informatique = categoryRepository.save(Category.builder()
                .name("Informatique")
                .description("Ordinateurs, accessoires et périphériques")
                .build());
        Category livres = categoryRepository.save(Category.builder()
                .name("Livres")
                .description("Romans, BD, ouvrages techniques")
                .build());
        Category sport = categoryRepository.save(Category.builder()
                .name("Sport")
                .description("Équipement et vêtements de sport")
                .build());

        // ─── Produits (images Unsplash CDN) ───────────────────────────
        List<Product> products = List.of(
                buildProduct("Ordinateur portable Dell XPS 13", "Intel i7, 16 Go RAM, SSD 512 Go",
                        new BigDecimal("12500.00"),
                        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop",
                        informatique),
                buildProduct("Clavier mécanique Logitech G Pro", "Switches GX Blue, rétroéclairage RGB",
                        new BigDecimal("1450.00"),
                        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop",
                        informatique),
                buildProduct("Souris Logitech MX Master 3", "Sans fil, ergonomique, autonomie 70 jours",
                        new BigDecimal("950.00"),
                        "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop",
                        informatique),
                buildProduct("Écran Dell 27\" 4K UltraSharp", "U2723QE — IPS Black, USB-C 90W",
                        new BigDecimal("4800.00"),
                        "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=400&h=300&fit=crop",
                        informatique),

                buildProduct("Clean Code", "Robert C. Martin — guide d'écriture de code propre",
                        new BigDecimal("320.00"),
                        "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=300&fit=crop",
                        livres),
                buildProduct("Le Petit Prince", "Antoine de Saint-Exupéry, édition illustrée",
                        new BigDecimal("85.00"),
                        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=300&fit=crop",
                        livres),
                buildProduct("Sapiens", "Yuval Noah Harari — Une brève histoire de l'humanité",
                        new BigDecimal("180.00"),
                        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&h=300&fit=crop",
                        livres),
                buildProduct("Spring Boot in Action", "Craig Walls — manuel de référence Spring Boot",
                        new BigDecimal("420.00"),
                        "https://images.unsplash.com/photo-1517842645767-c639042777db?w=400&h=300&fit=crop",
                        livres),

                buildProduct("Ballon de football Adidas", "Taille 5, officiel FIFA Quality",
                        new BigDecimal("250.00"),
                        "https://images.unsplash.com/photo-1614632537190-23e4b39afebd?w=400&h=300&fit=crop",
                        sport),
                buildProduct("Raquette de tennis Wilson Pro", "Pour joueurs intermédiaires, 300g",
                        new BigDecimal("780.00"),
                        "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=400&h=300&fit=crop",
                        sport),
                buildProduct("Tapis de yoga premium", "6mm d'épaisseur, antidérapant",
                        new BigDecimal("220.00"),
                        "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=400&h=300&fit=crop",
                        sport),
                buildProduct("Haltères 10 kg (paire)", "Caoutchouc hexagonal, prise antidérapante",
                        new BigDecimal("450.00"),
                        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop",
                        sport)
        );
        productRepository.saveAll(products);
        log.info("→ 3 catégories + {} produits créés", products.size());
    }

    private Product buildProduct(String name, String desc, BigDecimal price, String img, Category cat) {
        Product p = Product.builder()
                .name(name)
                .description(desc)
                .price(price)
                .imageUrl(img)
                .category(cat)
                .build();
        Inventory inv = Inventory.builder()
                .product(p)
                .quantity(ThreadLocalRandom.current().nextInt(20, 101))
                .build();
        p.setInventory(inv);
        return p;
    }

    private void seedMongo() {
        try {
            if (reviewRepository.count() > 0) {
                log.info("Collection reviews déjà peuplée — seed Mongo ignoré.");
                return;
            }
            List<Product> products = productRepository.findAll();
            if (products.isEmpty()) return;

            List<Review> seeds = List.of(
                    Review.builder().productId(products.get(0).getId()).userId(2L)
                            .authorName("Nouhaila Test").rating(5)
                            .comment("Excellent ordinateur, performances au top !")
                            .createdAt(Instant.now().minusSeconds(3600 * 24 * 5)).build(),
                    Review.builder().productId(products.get(0).getId()).userId(1L)
                            .authorName("Akram Belmoussa").rating(4)
                            .comment("Très bon rapport qualité-prix.")
                            .createdAt(Instant.now().minusSeconds(3600 * 24 * 3)).build(),
                    Review.builder().productId(products.get(1).getId()).userId(2L)
                            .authorName("Nouhaila Test").rating(5)
                            .comment("Clavier réactif et silencieux, parfait pour le gaming.")
                            .createdAt(Instant.now().minusSeconds(3600 * 24 * 2)).build(),
                    Review.builder().productId(products.get(4).getId()).userId(2L)
                            .authorName("Nouhaila Test").rating(5)
                            .comment("Un grand classique, à lire absolument !")
                            .createdAt(Instant.now().minusSeconds(3600 * 24)).build(),
                    Review.builder().productId(products.get(8).getId()).userId(1L)
                            .authorName("Akram Belmoussa").rating(4)
                            .comment("Bon ballon, bon rebond, livraison rapide.")
                            .createdAt(Instant.now().minusSeconds(3600 * 12)).build()
            );
            reviewRepository.saveAll(seeds);
            log.info("→ {} avis créés dans MongoDB", seeds.size());
        } catch (Exception e) {
            log.warn("MongoDB indisponible — seed des avis ignoré ({}). " +
                    "Démarrez Mongo pour activer la fonctionnalité avis.", e.getMessage());
        }
    }
}
