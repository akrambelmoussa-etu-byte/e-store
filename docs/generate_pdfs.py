# -*- coding: utf-8 -*-
"""
Génère un ensemble de PDF explicatifs du projet E-Store.
Usage : python generate_pdfs.py
Sortie : docs/*.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Styles ─────────────────────────────────────────────────────────
PRIMARY = HexColor("#0d6efd")
DARK = HexColor("#212529")
LIGHT_BG = HexColor("#f5f7fa")
CODE_BG = HexColor("#1e1e1e")
CODE_FG = HexColor("#dcdcdc")

styles = getSampleStyleSheet()

H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=22, textColor=PRIMARY, spaceAfter=14, leading=26)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=15, textColor=DARK, spaceBefore=18, spaceAfter=8, leading=18)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=12, textColor=PRIMARY, spaceBefore=10, spaceAfter=4, leading=14)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica",
                      fontSize=10.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
LIST_ITEM = ParagraphStyle("ListItem", parent=BODY, leftIndent=18, bulletIndent=6, spaceAfter=2)
COVER_TITLE = ParagraphStyle("CoverTitle", parent=H1, fontSize=32, textColor=PRIMARY,
                             alignment=TA_CENTER, leading=36, spaceAfter=20)
COVER_SUB = ParagraphStyle("CoverSub", parent=BODY, fontSize=14, alignment=TA_CENTER,
                           textColor=DARK, leading=20, spaceAfter=10)
CODE = ParagraphStyle("Code", parent=styles["Code"], fontName="Courier",
                      fontSize=8.5, leading=11, textColor=black,
                      backColor=HexColor("#f4f4f4"),
                      borderPadding=6, leftIndent=4, rightIndent=4)


def header_footer(canvas, doc):
    """En-tête et pied de page sur chaque page (sauf couverture)."""
    canvas.saveState()
    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(grey)
    canvas.drawString(2 * cm, 1.2 * cm, "E-Store — Mini-projet Full-Stack — A. Belmoussa & N. Ben Soumane")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    # Header line
    canvas.setStrokeColor(PRIMARY)
    canvas.setLineWidth(0.6)
    canvas.line(2 * cm, A4[1] - 1.6 * cm, A4[0] - 2 * cm, A4[1] - 1.6 * cm)
    canvas.setFillColor(PRIMARY)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(2 * cm, A4[1] - 1.4 * cm, "E-STORE")
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.4 * cm, doc.title.upper())
    canvas.restoreState()


def code_block(text):
    """Bloc de code Java/TypeScript, bien rendu avec fond gris."""
    # Échapper les chevrons HTML
    safe = (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))
    return Preformatted(safe, CODE)


def bullet(text):
    return Paragraph(f"• {text}", LIST_ITEM)


def make_doc(filename, title):
    path = os.path.join(OUT_DIR, filename)
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2.2 * cm, bottomMargin=1.8 * cm,
        title=title, author="A. Belmoussa & N. Ben Soumane"
    )
    return doc, path


def cover_page(title, subtitle, num):
    """Page de couverture standard."""
    flow = []
    flow.append(Spacer(1, 4 * cm))
    flow.append(Paragraph(f"E-STORE", COVER_SUB))
    flow.append(Spacer(1, 0.6 * cm))
    flow.append(Paragraph(title, COVER_TITLE))
    flow.append(Spacer(1, 0.4 * cm))
    flow.append(Paragraph(subtitle, COVER_SUB))
    flow.append(Spacer(1, 4 * cm))

    info = Table([
        ["Module", "Full-Stack"],
        ["Encadrant", "Pr. Omar Zahour"],
        ["Établissement", "FSBM — Université Hassan II"],
        ["Année", "2025-2026"],
        ["Auteurs", "Akram Belmoussa & Nouhaila Ben Soumane"],
        ["Document", f"{num} d'une série explicative"],
    ], colWidths=[5 * cm, 9 * cm])
    info.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    flow.append(info)
    flow.append(PageBreak())
    return flow


# ─────────────────────────────────────────────────────────────────────
# PDF 01 — Présentation et architecture
# ─────────────────────────────────────────────────────────────────────
def build_pdf_01():
    doc, path = make_doc("01-presentation-architecture.pdf",
                         "Présentation & Architecture")
    s = []
    s += cover_page("Présentation & Architecture", "Vue d'ensemble du projet E-Store", "1/7")

    s.append(Paragraph("1. Présentation du projet", H1))
    s.append(Paragraph(
        "E-Store est une application e-commerce complète développée dans le cadre du module "
        "<b>Full-Stack</b> sous la direction du <b>Pr. Omar Zahour</b> (Faculté des Sciences "
        "Ben M'Sick — Université Hassan II de Casablanca). Le projet permet à un utilisateur "
        "de s'inscrire, parcourir un catalogue, ajouter des produits à un panier, valider une "
        "commande, consulter son historique et déposer des avis.", BODY))

    s.append(Paragraph("Objectifs pédagogiques", H2))
    for b in [
        "Maîtriser une architecture full-stack moderne (Spring Boot + Angular).",
        "Implémenter une persistance hybride : relationnelle (MySQL/H2 via JPA) + documentaire (MongoDB).",
        "Mettre en place une sécurité robuste basée sur JWT et Spring Security 6.",
        "Appliquer les bonnes pratiques : DTOs, gestion globale des exceptions, transactions, tests unitaires.",
        "Réaliser une interface utilisateur réactive avec Angular 17 (composants standalone, signals).",
    ]:
        s.append(bullet(b))

    s.append(Paragraph("2. Stack technique", H1))
    tech = Table([
        ["Couche", "Technologies"],
        ["Présentation", "Angular 17+ standalone, Bootstrap 5, RxJS, TypeScript 5"],
        ["Logique métier", "Spring Boot 3.3, Spring Security 6, JWT (jjwt 0.12)"],
        ["Accès aux données", "Spring Data JPA + Hibernate, Spring Data MongoDB"],
        ["Bases de données", "MySQL 8 (prod) / H2 in-memory (dev) + MongoDB 7"],
        ["Build & outils", "Maven 3.9, npm, Angular CLI, JUnit 5 + Mockito"],
        ["Conteneurisation", "Docker Compose (MySQL + MongoDB + interfaces admin)"],
    ], colWidths=[4 * cm, 12 * cm])
    tech.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
        ("BACKGROUND", (0, 1), (-1, -1), white),
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_BG),
        ("BACKGROUND", (0, 4), (-1, 4), LIGHT_BG),
        ("BACKGROUND", (0, 6), (-1, 6), LIGHT_BG),
    ]))
    s.append(tech)

    s.append(Paragraph("3. Architecture en 3 couches", H1))
    s.append(Paragraph(
        "L'application suit le modèle classique en couches techniques, garantissant une "
        "séparation claire des responsabilités et facilitant la maintenance.", BODY))
    layers = Table([
        ["Couche", "Responsabilité", "Implémentation"],
        ["Présentation",
         "Affichage, interactions utilisateur, validation côté client",
         "Composants Angular, services HTTP, formulaires réactifs"],
        ["Logique métier",
         "Règles métier, orchestration, sécurité",
         "Controllers REST, Services Spring, DTOs"],
        ["Accès aux données",
         "Persistance, requêtes",
         "Repositories Spring Data (JPA + MongoDB)"],
    ], colWidths=[3.5 * cm, 6 * cm, 6.5 * cm])
    layers.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(layers)

    s.append(Paragraph("4. Architecture en 5 domaines fonctionnels", H1))
    s.append(Paragraph(
        "Chaque domaine est un sous-package autonome avec ses propres entités, "
        "DTOs, repositories, services et controllers — facilitant le DDD (Domain-Driven Design).", BODY))
    domains = Table([
        ["Domaine", "Rôle métier"],
        ["customer",  "Inscription, connexion, profil utilisateur, JWT"],
        ["catalog",   "Catégories et produits, recherche, pagination"],
        ["inventory", "Gestion du stock par produit (vérification, décrémentation)"],
        ["shopping",  "Panier (Cart, CartItem) et opérations associées"],
        ["billing",   "Validation transactionnelle des commandes (Order, OrderItem)"],
        ["review",    "Avis produits stockés dans MongoDB (séparé du SGBDR)"],
    ], colWidths=[3.5 * cm, 12.5 * cm])
    domains.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_BG),
        ("BACKGROUND", (0, 4), (-1, 4), LIGHT_BG),
        ("BACKGROUND", (0, 6), (-1, 6), LIGHT_BG),
    ]))
    s.append(domains)

    s.append(PageBreak())
    s.append(Paragraph("5. Diagramme conceptuel (texte)", H1))
    schema = """
┌────────────────────────────────────────────────────────────────┐
│                      NAVIGATEUR (utilisateur)                   │
└────────────────────────────────────────────────────────────────┘
                              │ HTTP/JSON
                              ▼
┌────────────────────────────────────────────────────────────────┐
│   FRONTEND ANGULAR 17 (port 4200)                               │
│   - Composants standalone (login, catalog, cart, orders…)       │
│   - AuthService + AuthGuard + AuthInterceptor (JWT)             │
└────────────────────────────────────────────────────────────────┘
                              │ REST + JWT Bearer
                              ▼
┌────────────────────────────────────────────────────────────────┐
│   BACKEND SPRING BOOT 3.3 (port 8080)                           │
│   ─ Controllers REST (/api/auth, /api/products, /api/cart…)     │
│   ─ Services métier (5 domaines + review)                       │
│   ─ Spring Security + Filter JWT                                │
│   ─ Repositories (JpaRepository + MongoRepository)              │
└────────────────────────────────────────────────────────────────┘
            │                                    │
            ▼                                    ▼
   ┌──────────────────┐               ┌──────────────────┐
   │ MySQL / H2       │               │ MongoDB 7        │
   │ users, products  │               │ collection       │
   │ orders, carts…   │               │ "reviews"        │
   └──────────────────┘               └──────────────────┘
"""
    s.append(code_block(schema))

    s.append(Paragraph("6. Flux d'une commande (séquence)", H2))
    s.append(Paragraph(
        "Voici le déroulement complet d'un achat, qui mobilise tous les domaines :", BODY))
    for step in [
        "<b>1.</b> L'utilisateur consulte le catalogue (<i>catalog</i>).",
        "<b>2.</b> Il ajoute un produit au panier — vérification du stock (<i>shopping</i> + <i>inventory</i>).",
        "<b>3.</b> Il valide sa commande — appel à <code>OrderService.checkout()</code>.",
        "<b>4.</b> En transaction : création <code>Order</code>+<code>OrderItem</code>, décrément du stock, vidage du panier.",
        "<b>5.</b> La commande passe en statut <b>CONFIRMED</b>, l'utilisateur est redirigé vers /orders.",
        "<b>6.</b> Il peut ensuite déposer un avis sur le produit (<i>review</i> → MongoDB).",
    ]:
        s.append(bullet(step))

    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    return path


# ─────────────────────────────────────────────────────────────────────
# PDF 02 — Backend : 5 domaines fonctionnels
# ─────────────────────────────────────────────────────────────────────
def build_pdf_02():
    doc, path = make_doc("02-backend-domaines.pdf",
                         "Backend — 5 domaines fonctionnels")
    s = []
    s += cover_page("Backend Spring Boot",
                    "Détail des 5 domaines fonctionnels et de leur code", "2/7")

    s.append(Paragraph("Structure générale d'un domaine", H1))
    s.append(Paragraph(
        "Chaque domaine est organisé selon le même schéma, ce qui assure une cohérence "
        "forte et une lecture rapide du code.", BODY))
    s.append(code_block("""com/estore/<domaine>/
├── entity/        Classes JPA (@Entity)
├── repository/    Interfaces Spring Data (extends JpaRepository)
├── dto/           Objets de transport (sortie/entrée API)
├── service/       Logique métier (annotée @Service @Transactional)
└── controller/    Endpoints REST (@RestController)"""))

    # ─── customer ─────────────────────────────────────────────────
    s.append(Paragraph("1. Domaine customer", H1))
    s.append(Paragraph(
        "Gère les utilisateurs : inscription, connexion, profil. C'est le domaine qui "
        "héberge également la sécurité (JWT, BCrypt, filtres Spring Security).", BODY))

    s.append(Paragraph("Entité User", H3))
    s.append(code_block("""@Entity
@Table(name = "users", uniqueConstraints = @UniqueConstraint(columnNames = "email"))
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String firstName, lastName;
    @Column(unique = true) private String email;
    @JsonIgnore private String password;     // BCrypt
    @Enumerated(EnumType.STRING) private Role role;  // USER | ADMIN
    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL) private Profile profile;
}"""))
    s.append(Paragraph(
        "<b>Points clés :</b> @JsonIgnore protège le mot de passe dans toutes les sérialisations, "
        "@Enumerated(STRING) stocke le rôle en clair (lisible dans la BD), la relation @OneToOne "
        "vers Profile utilise mappedBy = \"user\" pour éviter les colonnes redondantes.", BODY))

    s.append(Paragraph("AuthService — inscription", H3))
    s.append(code_block("""@Transactional
public AuthResponseDto register(RegisterDto dto) {
    if (userRepository.existsByEmail(dto.getEmail())) {
        throw new BusinessException("Cet email est déjà utilisé");  // → 409
    }
    User user = User.builder()
        .firstName(dto.getFirstName()).lastName(dto.getLastName())
        .email(dto.getEmail())
        .password(passwordEncoder.encode(dto.getPassword()))  // BCrypt
        .role(Role.USER).build();
    Profile profile = Profile.builder().user(user).build();
    user.setProfile(profile);
    User saved = userRepository.save(user);
    return AuthResponseDto.builder()
        .token(jwtService.generateToken(saved))
        .user(UserDto.from(saved)).build();
}"""))

    s.append(PageBreak())

    # ─── catalog ─────────────────────────────────────────────────
    s.append(Paragraph("2. Domaine catalog", H1))
    s.append(Paragraph(
        "Catégories et produits. Le ProductRepository expose une recherche paginée combinée "
        "(filtre catégorie + mot-clé) via une requête JPQL personnalisée.", BODY))
    s.append(code_block("""public interface ProductRepository extends JpaRepository<Product, Long> {

    @Query(\"\"\"
        SELECT p FROM Product p
        WHERE (:categoryId IS NULL OR p.category.id = :categoryId)
          AND (:q IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%', :q, '%'))
                          OR LOWER(p.description) LIKE LOWER(CONCAT('%', :q, '%')))
        \"\"\")
    Page<Product> search(@Param("categoryId") Long categoryId,
                         @Param("q") String q,
                         Pageable pageable);
}"""))
    s.append(Paragraph(
        "<b>Avantages :</b> requête unique, paramètres optionnels gérés via "
        "<code>IS NULL OR …</code>, pagination native via Pageable, recherche insensible "
        "à la casse.", BODY))

    # ─── inventory ───────────────────────────────────────────────
    s.append(Paragraph("3. Domaine inventory", H1))
    s.append(Paragraph(
        "Le stock est modélisé par une entité distincte avec relation @OneToOne vers Product. "
        "Cela permet de gérer le stock indépendamment du produit (audit, historique, etc.).", BODY))
    s.append(code_block("""@Transactional
public void decrement(Long productId, int quantity) {
    Inventory inv = inventoryRepository.findByProductId(productId)
            .orElseThrow(() -> new ResourceNotFoundException("Stock introuvable"));
    if (inv.getQuantity() < quantity) {
        throw new BusinessException("Stock insuffisant pour le produit " + productId);
    }
    inv.setQuantity(inv.getQuantity() - quantity);
    inventoryRepository.save(inv);
}"""))

    # ─── shopping ────────────────────────────────────────────────
    s.append(Paragraph("4. Domaine shopping (panier)", H1))
    s.append(Paragraph(
        "Cart possède un @OneToMany vers CartItem avec orphanRemoval=true : la suppression "
        "d'un item du panier le supprime aussi en BDD. Le prix unitaire est figé à l'ajout "
        "pour garantir la stabilité du panier malgré d'éventuelles évolutions tarifaires.", BODY))
    s.append(code_block("""@Transactional
public CartDto addItem(AddToCartDto dto) {
    User user = securityUtils.currentUser();
    Cart cart = getOrCreateCart(user);
    Product product = productService.get(dto.getProductId());

    Optional<CartItem> existing = cart.getItems().stream()
        .filter(ci -> ci.getProduct().getId().equals(product.getId()))
        .findFirst();

    int newQty = existing.map(CartItem::getQuantity).orElse(0) + dto.getQuantity();
    inventoryService.checkAvailability(product.getId(), newQty);  // 409 si insuffisant

    if (existing.isPresent()) existing.get().setQuantity(newQty);
    else cart.getItems().add(CartItem.builder()
            .cart(cart).product(product)
            .quantity(dto.getQuantity()).unitPrice(product.getPrice()).build());
    cart.touch();
    return CartDto.from(cartRepository.save(cart));
}"""))

    s.append(PageBreak())

    # ─── billing ────────────────────────────────────────────────
    s.append(Paragraph("5. Domaine billing (commande)", H1))
    s.append(Paragraph(
        "Le checkout est l'opération métier la plus critique : elle est transactionnelle "
        "(<code>@Transactional</code>) — si l'une des étapes échoue, tout est rollbacké.", BODY))
    s.append(code_block("""@Transactional
public OrderDto checkout() {
    User user = securityUtils.currentUser();
    Cart cart = cartService.getOrCreateCart(user);

    if (cart.getItems().isEmpty())
        throw new BusinessException("Votre panier est vide");

    // 1) Vérifier le stock pour TOUS les items AVANT toute modification
    for (CartItem ci : cart.getItems())
        inventoryService.checkAvailability(ci.getProduct().getId(), ci.getQuantity());

    // 2) Créer la commande
    Order order = Order.builder().user(user).status(OrderStatus.PENDING).build();
    BigDecimal total = BigDecimal.ZERO;
    for (CartItem ci : cart.getItems()) {
        order.getItems().add(OrderItem.builder()
            .order(order).product(ci.getProduct())
            .quantity(ci.getQuantity()).unitPrice(ci.getUnitPrice()).build());
        total = total.add(ci.getUnitPrice().multiply(BigDecimal.valueOf(ci.getQuantity())));
        // 3) Décrémenter le stock
        inventoryService.decrement(ci.getProduct().getId(), ci.getQuantity());
    }
    order.setTotalAmount(total);
    order.setStatus(OrderStatus.CONFIRMED);
    Order saved = orderRepository.save(order);

    // 4) Vider le panier
    cartService.clearCart(cart);
    return OrderDto.from(saved);
}"""))
    s.append(Paragraph(
        "<b>Garanties :</b> si le stock est insuffisant en cours de route, ou si la BDD échoue, "
        "<b>aucun</b> Order n'est créé, <b>aucun</b> stock n'est décrémenté, le panier reste intact. "
        "C'est l'atomicité ACID en action.", BODY))

    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    return path


# ─────────────────────────────────────────────────────────────────────
# PDF 03 — Sécurité, JWT et MongoDB
# ─────────────────────────────────────────────────────────────────────
def build_pdf_03():
    doc, path = make_doc("03-securite-mongodb.pdf",
                         "Sécurité JWT & MongoDB")
    s = []
    s += cover_page("Sécurité JWT & MongoDB",
                    "Authentification, autorisation et persistance documentaire", "3/7")

    s.append(Paragraph("1. Vue d'ensemble de la sécurité", H1))
    s.append(Paragraph(
        "L'application utilise <b>Spring Security 6</b> en mode <b>stateless</b> (pas de session), "
        "avec authentification par <b>JWT</b> (JSON Web Token) signés en HS256. "
        "Les mots de passe sont hashés avec <b>BCrypt</b>.", BODY))

    s.append(Paragraph("Endpoints publics vs protégés", H2))
    rules = Table([
        ["Endpoint", "Accès", "Détail"],
        ["POST /api/auth/register",  "Public",         "Inscription"],
        ["POST /api/auth/login",     "Public",         "Renvoie le JWT"],
        ["GET  /api/products/**",    "Public",         "Catalogue lisible sans auth"],
        ["GET  /api/categories/**",  "Public",         "Idem"],
        ["GET  /api/reviews/**",     "Public",         "Avis consultables sans auth"],
        ["POST /api/products",       "ADMIN",          "@PreAuthorize(\"hasRole('ADMIN')\")"],
        ["GET  /api/cart",           "Authentifié",    "Panier de l'utilisateur courant"],
        ["POST /api/orders",         "Authentifié",    "Validation de la commande"],
    ], colWidths=[5.5 * cm, 3 * cm, 7.5 * cm])
    rules.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 1), (0, -1), "Courier"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(rules)

    s.append(Paragraph("2. JwtService — génération du token", H1))
    s.append(code_block("""public String generateToken(User user) {
    Map<String, Object> claims = new HashMap<>();
    claims.put("uid", user.getId());
    claims.put("role", user.getRole().name());
    claims.put("name", user.getFirstName() + " " + user.getLastName());

    Date now = new Date();
    Date exp = new Date(now.getTime() + expirationMs);  // 24h

    return Jwts.builder()
        .claims(claims).subject(user.getEmail())
        .issuedAt(now).expiration(exp)
        .signWith(key).compact();   // signature HMAC-SHA256
}"""))
    s.append(Paragraph(
        "Le token contient l'email (subject), l'id utilisateur, son rôle et son nom complet. "
        "Il est signé avec une clé secrète (configurée dans <code>application.properties</code>) "
        "et expire au bout de <b>24 heures</b>.", BODY))

    s.append(Paragraph("3. JwtAuthenticationFilter — filtre Spring", H2))
    s.append(code_block("""@Override
protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                FilterChain chain) {
    String header = req.getHeader("Authorization");
    if (header == null || !header.startsWith("Bearer ")) {
        chain.doFilter(req, res); return;
    }
    String token = header.substring(7);
    String email = jwtService.extractEmail(token);
    if (email != null && SecurityContextHolder.getContext().getAuthentication() == null) {
        UserDetails user = userDetailsService.loadUserByUsername(email);
        if (jwtService.isTokenValid(token, email)) {
            UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
    }
    chain.doFilter(req, res);
}"""))

    s.append(PageBreak())

    s.append(Paragraph("4. Côté frontend — AuthInterceptor", H1))
    s.append(Paragraph(
        "Toutes les requêtes HTTP passent par l'intercepteur, qui ajoute automatiquement "
        "le token au header Authorization. Aucun composant n'a à le gérer manuellement.", BODY))
    s.append(code_block("""export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.token;
  if (!token) return next(req);
  return next(req.clone({ setHeaders: { Authorization: `Bearer ${token}` } }));
};"""))

    s.append(Paragraph("5. AuthGuard — protection des routes", H2))
    s.append(code_block("""export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (auth.isAuthenticated) return true;
  router.navigate(['/login']);
  return false;
};"""))
    s.append(Paragraph(
        "Appliqué aux routes <b>/cart</b>, <b>/orders</b> et <b>/profile</b> dans "
        "<code>app.routes.ts</code> via <code>canActivate: [authGuard]</code>.", BODY))

    s.append(Paragraph("6. MongoDB — domaine review", H1))
    s.append(Paragraph(
        "Les avis utilisateurs sont stockés dans <b>MongoDB</b> plutôt qu'en SQL pour "
        "illustrer la coexistence de deux paradigmes de persistance. "
        "Cela répond à un cas d'usage typique : données semi-structurées, volumineuses, "
        "lues fréquemment mais peu contraintes relationnellement.", BODY))

    s.append(Paragraph("Document Mongo", H3))
    s.append(code_block("""@Document(collection = "reviews")
public class Review {
    @Id private String id;
    @Indexed private Long productId;
    @Indexed private Long userId;
    private String authorName;
    private int rating;       // 1 à 5
    private String comment;
    private Instant createdAt;
}"""))

    s.append(Paragraph("Repository réactif Mongo", H3))
    s.append(code_block("""public interface ReviewRepository extends MongoRepository<Review, String> {
    List<Review> findByProductIdOrderByCreatedAtDesc(Long productId);
    List<Review> findByUserIdOrderByCreatedAtDesc(Long userId);
}"""))
    s.append(Paragraph(
        "Spring Data MongoDB génère automatiquement la requête à partir du nom de la "
        "méthode — aucune SQL ni JPQL à écrire.", BODY))

    s.append(Paragraph("Exemple de document JSON stocké", H3))
    s.append(code_block("""{
  "_id": ObjectId("671f3a2..."),
  "productId": 1,
  "userId": 2,
  "authorName": "Nouhaila Test",
  "rating": 5,
  "comment": "Excellent ordinateur, performances au top !",
  "createdAt": ISODate("2026-04-28T14:32:11.123Z")
}"""))

    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    return path


# ─────────────────────────────────────────────────────────────────────
# PDF 04 — Frontend Angular
# ─────────────────────────────────────────────────────────────────────
def build_pdf_04():
    doc, path = make_doc("04-frontend-angular.pdf", "Frontend Angular 17")
    s = []
    s += cover_page("Frontend Angular 17",
                    "Composants standalone, services réactifs, interceptors", "4/7")

    s.append(Paragraph("1. Choix techniques Angular 17", H1))
    for b in [
        "<b>Standalone components</b> — pas de NgModule, déclarations dans la classe.",
        "<b>Lazy loading</b> par route — chaque feature est chargée à la demande (bundles plus petits).",
        "<b>Signals</b> pour l'état réactif (panier, toasts) — alternative moderne à RxJS pour l'UI.",
        "<b>HttpInterceptor fonctionnel</b> (Angular 15+) — code plus concis qu'une classe.",
        "<b>Reactive Forms</b> avec validation déclarative.",
        "<b>Bootstrap 5</b> pour le style — pas de dépendance JS, juste le CSS.",
    ]:
        s.append(bullet(b))

    s.append(Paragraph("2. Structure du dossier src/app", H1))
    s.append(code_block("""src/app/
├── app.config.ts          Configuration globale (router, http, interceptors)
├── app.routes.ts          Définition des routes avec lazy-loading
├── app.component.ts       Layout racine (header + outlet + footer)
├── core/
│   ├── models/            Interfaces TypeScript (User, Product, Cart…)
│   ├── services/          Services HTTP (AuthService, CartService…)
│   ├── guards/            AuthGuard
│   └── interceptors/      AuthInterceptor + ErrorInterceptor
├── shared/
│   └── components/        HeaderComponent, FooterComponent, LoaderComponent, ToastComponent
└── features/
    ├── auth/              login.component.ts, register.component.ts
    ├── catalog/           product-list, product-detail
    ├── cart/              cart.component.ts
    ├── orders/            orders.component.ts
    ├── profile/           profile.component.ts
    └── reviews/           review-form.component.ts"""))

    s.append(Paragraph("3. AuthService — gestion de l'utilisateur courant", H1))
    s.append(code_block("""@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private currentUser$ = new BehaviorSubject<User | null>(this.loadUser());
  readonly user$ = this.currentUser$.asObservable();

  login(email: string, password: string) {
    return this.http
      .post<ApiResponse<AuthResponse>>(`${env.apiUrl}/auth/login`, { email, password })
      .pipe(tap((res) => res.data && this.persist(res.data)));
  }

  private persist(data: AuthResponse): void {
    localStorage.setItem('estore.token', data.token);
    localStorage.setItem('estore.user', JSON.stringify(data.user));
    this.currentUser$.next(data.user);
  }
}"""))
    s.append(Paragraph(
        "Le token et l'utilisateur sont stockés en <b>localStorage</b> pour survivre au "
        "rafraîchissement. Un BehaviorSubject permet aux composants de réagir aux changements.", BODY))

    s.append(PageBreak())

    s.append(Paragraph("4. CartService avec signals", H1))
    s.append(code_block("""@Injectable({ providedIn: 'root' })
export class CartService {
  private http = inject(HttpClient);
  readonly cart = signal<Cart | null>(null);
  readonly itemCount = signal<number>(0);

  add(productId: number, quantity: number) {
    return this.http
      .post<ApiResponse<Cart>>(`${env.apiUrl}/cart/add`, { productId, quantity })
      .pipe(tap((r) => this.update(r.data)));
  }

  private update(cart: Cart | undefined): void {
    if (!cart) return;
    this.cart.set(cart);
    this.itemCount.set(cart.itemCount);
  }
}"""))
    s.append(Paragraph(
        "Le badge du panier dans le header utilise directement <code>cartSvc.itemCount()</code> — "
        "Angular détecte automatiquement la dépendance et met à jour le DOM.", BODY))

    s.append(Paragraph("5. ErrorInterceptor — gestion centralisée", H1))
    s.append(code_block("""export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  const auth = inject(AuthService);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      const msg = err.error?.message || `Erreur HTTP ${err.status}`;
      if (err.status === 401) {
        auth.logout();
        toast.error('Session expirée, veuillez vous reconnecter');
      } else if (err.status !== 0) {
        toast.error(msg);
      } else {
        toast.error('Serveur injoignable');
      }
      return throwError(() => err);
    })
  );
};"""))
    s.append(Paragraph(
        "Aucun composant n'a besoin de gérer manuellement les erreurs HTTP : un toast "
        "approprié s'affiche automatiquement, et un 401 déclenche la déconnexion + "
        "redirection vers /login.", BODY))

    s.append(Paragraph("6. Routes paresseuses (lazy loading)", H1))
    s.append(code_block("""export const routes: Routes = [
  { path: '', loadComponent: () =>
      import('./features/catalog/product-list.component').then((m) => m.ProductListComponent) },
  { path: 'cart',
    loadComponent: () => import('./features/cart/cart.component').then((m) => m.CartComponent),
    canActivate: [authGuard]
  },
  { path: 'orders',
    loadComponent: () => import('./features/orders/orders.component').then((m) => m.OrdersComponent),
    canActivate: [authGuard]
  },
  // …
];"""))
    s.append(Paragraph(
        "Chaque route charge son composant à la demande — le bundle initial reste léger "
        "(13 ko de main.js + 245 ko de framework partagé), les features sont des bundles "
        "indépendants chargés au besoin.", BODY))

    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    return path


# ─────────────────────────────────────────────────────────────────────
# PDF 05 — Tests, configuration, données de seed
# ─────────────────────────────────────────────────────────────────────
def build_pdf_05():
    doc, path = make_doc("05-tests-configuration.pdf",
                         "Tests, configuration et données de seed")
    s = []
    s += cover_page("Tests & Configuration",
                    "Tests unitaires, profils Spring, données de démonstration", "5/7")

    s.append(Paragraph("1. Tests unitaires (JUnit 5 + Mockito)", H1))
    s.append(Paragraph(
        "Trois suites de tests couvrent les services métier critiques — "
        "<b>9 tests</b> au total, tous verts.", BODY))

    tests = Table([
        ["Suite", "Cas testés", "Nb"],
        ["ProductServiceTest",
         "findById existant / inexistant ; search avec et sans mot-clé", "4"],
        ["CartServiceTest",
         "add avec stock suffisant / avec stock insuffisant", "2"],
        ["OrderServiceTest",
         "checkout panier vide / panier valide ; myOrders trié", "3"],
        ["TOTAL", "", "9"],
    ], colWidths=[4.5 * cm, 9.5 * cm, 1.5 * cm])
    tests.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), LIGHT_BG),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (-1, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(tests)

    s.append(Paragraph("Exemple : OrderServiceTest.checkout valide", H3))
    s.append(code_block("""@Test
void checkout_panierValide_creeCommandeEtViderPanier() {
    CartItem item = CartItem.builder().id(1L).product(product)
        .quantity(2).unitPrice(product.getPrice()).cart(cart).build();
    cart.getItems().add(item);

    when(orderRepository.save(any(Order.class))).thenAnswer(inv -> {
        Order o = inv.getArgument(0); o.setId(500L); return o;
    });

    OrderDto dto = orderService.checkout();

    assertThat(dto.getId()).isEqualTo(500L);
    assertThat(dto.getStatus()).isEqualTo(OrderStatus.CONFIRMED);
    assertThat(dto.getTotalAmount()).isEqualByComparingTo(new BigDecimal("25000.00"));

    verify(inventoryService).decrement(10L, 2);
    verify(cartService).clearCart(cart);
}"""))
    s.append(Paragraph(
        "Le test vérifie à la fois le résultat (<b>state-based</b>) <i>et</i> les interactions "
        "avec les dépendances mockées (<b>behavior-based</b>) — couverture complète.", BODY))

    s.append(Paragraph("Exécution", H3))
    s.append(code_block("""$ cd estore-backend
$ mvn test
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS"""))

    s.append(PageBreak())

    s.append(Paragraph("2. Configuration multi-profils", H1))
    s.append(Paragraph(
        "L'application supporte deux profils Spring sélectionnables avec "
        "<code>spring.profiles.active=dev|prod</code>.", BODY))

    profiles = Table([
        ["Profil", "Base relationnelle", "Cas d'usage"],
        ["dev",  "H2 in-memory (auto)",   "Démo rapide sans installation"],
        ["prod", "MySQL 8 (port 3306)",   "Déploiement réel ou via Docker"],
    ], colWidths=[2 * cm, 6 * cm, 7.5 * cm])
    profiles.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(profiles)

    s.append(Paragraph("application.properties (commun)", H3))
    s.append(code_block("""spring.application.name=estore-backend
spring.profiles.active=dev
server.port=8080

spring.jpa.hibernate.ddl-auto=update
spring.data.mongodb.uri=mongodb://localhost:27017/estore

jwt.secret=change-me-with-a-256-bits-secret-key-for-production…
jwt.expiration=86400000   # 24h en ms"""))

    s.append(Paragraph("application-dev.properties (H2)", H3))
    s.append(code_block("""spring.datasource.url=jdbc:h2:mem:estore;DB_CLOSE_DELAY=-1;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.h2.console.enabled=true        # /h2-console accessible"""))

    s.append(Paragraph("3. DataSeeder — jeu de données initial", H1))
    s.append(Paragraph(
        "Implémente <code>CommandLineRunner</code> et s'exécute au démarrage. Si la BDD "
        "est vide, il crée :", BODY))
    for b in [
        "<b>2 utilisateurs</b> : admin@estore.ma (ADMIN) et user@estore.ma (USER), avec profils complets.",
        "<b>3 catégories</b> : Informatique, Livres, Sport.",
        "<b>12 produits</b> répartis dans les 3 catégories, avec stock aléatoire 20-100.",
        "<b>5 avis</b> dans MongoDB sur les premiers produits.",
    ]:
        s.append(bullet(b))
    s.append(Paragraph(
        "Le seeder est <b>idempotent</b> : s'il est relancé sur une BDD non vide, il "
        "ne fait rien — donc on peut le laisser activé sans risque.", BODY))
    s.append(Paragraph(
        "Le seeder Mongo est <b>défensif</b> : si MongoDB n'est pas disponible, il loggue "
        "un warning et continue, sans bloquer le démarrage de l'application.", BODY))

    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    return path


# ─────────────────────────────────────────────────────────────────────
# PDF 06 — Docker : problème rencontré et solution
# ─────────────────────────────────────────────────────────────────────
def build_pdf_06():
    doc, path = make_doc("06-docker-probleme-solution.pdf",
                         "Docker — problème rencontré & solution")
    s = []
    s += cover_page("Docker Desktop",
                    "Problème d'installation rencontré et solutions appliquées", "6/7")

    s.append(Paragraph("1. Contexte", H1))
    s.append(Paragraph(
        "Le projet E-Store fournit un fichier <code>docker-compose.yml</code> qui démarre "
        "en une seule commande l'ensemble des services nécessaires à l'environnement "
        "de production :", BODY))
    for b in [
        "<b>MySQL 8</b> sur le port 3306 (BDD relationnelle).",
        "<b>MongoDB 7</b> sur le port 27017 (BDD documentaire).",
        "<b>phpMyAdmin</b> sur le port 8081 (UI d'inspection MySQL).",
        "<b>mongo-express</b> sur le port 8082 (UI d'inspection Mongo).",
    ]:
        s.append(bullet(b))

    s.append(Paragraph("2. Problème rencontré", H1))
    s.append(Paragraph(
        "Lors de l'installation de Docker Desktop sur Windows 11, le message suivant "
        "est apparu :", BODY))
    s.append(code_block("""Docker Desktop installation failed.

For security reasons C:\\ProgramData\\DockerDesktop must be owned
by an elevated account."""))

    s.append(Paragraph("Cause", H3))
    s.append(Paragraph(
        "Docker exige que son dossier de configuration <code>C:\\ProgramData\\DockerDesktop</code> "
        "soit créé avec des permissions élevées (compte administrateur). Ce message apparaît "
        "généralement quand :", BODY))
    for b in [
        "Une installation précédente a laissé un dossier résiduel avec de mauvais propriétaires.",
        "L'installeur a été lancé en mode utilisateur normal (sans \"Exécuter en tant qu'administrateur\").",
        "Une stratégie de groupe Windows restreint l'écriture dans ProgramData.",
    ]:
        s.append(bullet(b))

    s.append(PageBreak())

    s.append(Paragraph("3. Solution appliquée — méthode 1 (manuelle)", H1))
    s.append(Paragraph(
        "Suppression manuelle des dossiers résiduels en mode administrateur, puis "
        "réinstallation de Docker Desktop.", BODY))

    s.append(Paragraph("Étape 1 — Ouvrir un terminal en admin", H3))
    s.append(Paragraph(
        "Clic droit sur le menu Démarrer → <b>Terminal Windows (administrateur)</b> "
        "ou <b>Invite de commandes (administrateur)</b>.", BODY))

    s.append(Paragraph("Étape 2 — Supprimer les dossiers résiduels", H3))
    s.append(Paragraph("En CMD :", BODY))
    s.append(code_block("""rmdir /s /q "C:\\ProgramData\\DockerDesktop"
rmdir /s /q "C:\\ProgramData\\Docker\""""))
    s.append(Paragraph("En PowerShell :", BODY))
    s.append(code_block("""Remove-Item -Path "C:\\ProgramData\\DockerDesktop" -Recurse -Force
Remove-Item -Path "C:\\ProgramData\\Docker" -Recurse -Force -ErrorAction SilentlyContinue"""))

    s.append(Paragraph("Étape 3 — Réinstaller Docker Desktop", H3))
    for b in [
        "Télécharger l'installeur sur <i>docker.com/products/docker-desktop</i>.",
        "Clic droit sur l'exécutable téléchargé → <b>Exécuter en tant qu'administrateur</b>.",
        "Suivre l'assistant (activer WSL 2 si demandé).",
        "Redémarrer le PC après installation.",
        "Lancer Docker Desktop, attendre que l'icône baleine 🐳 apparaisse en bas à droite.",
    ]:
        s.append(bullet(b))

    s.append(Paragraph("Étape 4 — Vérification", H3))
    s.append(code_block("""docker --version
# Docker version 27.x.x

docker compose version
# Docker Compose version v2.x.x"""))

    s.append(Paragraph("4. Solution appliquée — méthode 2 (alternative)", H1))
    s.append(Paragraph(
        "Compte tenu de la complexité d'installation de Docker Desktop sur certaines "
        "configurations Windows, une <b>solution alternative</b> a été retenue pour la "
        "démonstration finale : utilisation du <b>profil Spring \"dev\"</b> avec H2 in-memory.", BODY))

    s.append(Paragraph("Avantages de l'alternative H2", H3))
    for b in [
        "Aucune installation requise — H2 est embarquée dans le JAR Spring Boot.",
        "Démarrage instantané, idéal pour la démonstration en classe.",
        "Console web H2 disponible sur <code>http://localhost:8080/h2-console</code>.",
        "Le code est <b>identique</b> entre H2 et MySQL grâce à JPA — aucune adaptation à faire.",
    ]:
        s.append(bullet(b))

    s.append(Paragraph("Limitation", H3))
    s.append(Paragraph(
        "H2 in-memory perd ses données au redémarrage de l'application. Le DataSeeder "
        "recrée automatiquement les comptes de test et les produits à chaque démarrage, "
        "ce qui rend cette limitation transparente pour la démonstration.", BODY))

    s.append(PageBreak())

    s.append(Paragraph("5. Comparaison Docker vs H2 dev", H1))
    comp = Table([
        ["Critère", "Docker Compose", "H2 dev (alternative)"],
        ["Installation requise",
         "Docker Desktop + WSL2",
         "Aucune (H2 embarquée)"],
        ["Démarrage",
         "docker compose up -d (~30 s)",
         "mvn spring-boot:run (~10 s)"],
        ["Persistance",
         "Volumes Docker (survit au redémarrage)",
         "Mémoire (perdue au redémarrage)"],
        ["MySQL",
         "Port 3306, accessible via Workbench",
         "H2, console sur /h2-console"],
        ["MongoDB",
         "Port 27017",
         "Indisponible (avis désactivés)"],
        ["UIs admin",
         "phpMyAdmin (8081), mongo-express (8082)",
         "Console H2 native"],
        ["Adapté à",
         "Développement collaboratif, prod-like",
         "Démo rapide, soutenance"],
    ], colWidths=[3.5 * cm, 6 * cm, 6 * cm])
    comp.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(comp)

    s.append(Paragraph("6. Leçon retenue", H1))
    s.append(Paragraph(
        "Dans un projet pédagogique comme dans la vie professionnelle, il est essentiel "
        "de prévoir des <b>chemins alternatifs</b> en cas de blocage technique. "
        "L'architecture du projet a été conçue dès le départ pour supporter deux modes "
        "(Docker production-like + H2 développement) — ce qui a permis de poursuivre "
        "la démonstration sans interruption malgré l'incident Docker.", BODY))

    s.append(Paragraph(
        "Cette dualité est une <b>bonne pratique</b> classique : utiliser une base "
        "embarquée pour les tests et le développement local, et une base réelle (Dockerisée "
        "ou installée) pour la pré-production et la production.", BODY))

    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    return path


# ─────────────────────────────────────────────────────────────────────
# PDF 07 — Guide de démarrage et soutenance
# ─────────────────────────────────────────────────────────────────────
def build_pdf_07():
    doc, path = make_doc("07-guide-demarrage-soutenance.pdf",
                         "Guide de démarrage et soutenance")
    s = []
    s += cover_page("Guide de démarrage & Soutenance",
                    "Comment lancer le projet et présenter la démo", "7/7")

    s.append(Paragraph("1. Pré-requis", H1))
    pre = Table([
        ["Logiciel", "Version", "Vérification"],
        ["JDK",      "17 ou +", "java -version"],
        ["Maven",    "3.9 ou +", "mvn -version"],
        ["Node.js",  "20 ou +", "node --version"],
        ["npm",      "10 ou +", "npm --version"],
    ], colWidths=[3 * cm, 3 * cm, 6 * cm])
    pre.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (-1, 1), (-1, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(pre)

    s.append(Paragraph("2. Démarrage en 3 étapes", H1))

    s.append(Paragraph("Étape 1 — (Optionnel) Lancer les BDD via Docker", H3))
    s.append(code_block("""cd C:\\Users\\belmo\\studies\\Full-stack\\E-stor
docker compose up -d"""))
    s.append(Paragraph(
        "Si Docker n'est pas installé, <b>passer cette étape</b> — l'application démarrera "
        "avec H2 in-memory (profil dev par défaut).", BODY))

    s.append(Paragraph("Étape 2 — Lancer le backend Spring Boot", H3))
    s.append(code_block("""cd estore-backend
mvn spring-boot:run

# Sortie attendue :
# Tomcat started on port 8080
# DataSeeder : 2 utilisateurs créés
# DataSeeder : 3 catégories + 12 produits créés
# Started EstoreApplication in 6.5 seconds"""))

    s.append(Paragraph("Étape 3 — Lancer le frontend Angular", H3))
    s.append(code_block("""cd estore-frontend
npm install     # première fois seulement
npm start

# Ouvre automatiquement http://localhost:4200"""))

    s.append(PageBreak())

    s.append(Paragraph("3. Comptes de test", H1))
    accounts = Table([
        ["Email", "Mot de passe", "Rôle", "Permissions"],
        ["admin@estore.ma", "Admin@123", "ADMIN", "Catalogue, panier, commandes, CRUD produits/catégories"],
        ["user@estore.ma",  "User@123",  "USER",  "Catalogue, panier, commandes, avis"],
    ], colWidths=[4 * cm, 2.5 * cm, 1.5 * cm, 6 * cm])
    accounts.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (1, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(accounts)

    s.append(Paragraph("4. Scénario de démonstration recommandé", H1))
    s.append(Paragraph(
        "Voici un parcours en 8 étapes qui couvre toutes les fonctionnalités du projet — "
        "durée totale ~5 minutes.", BODY))
    scenario = [
        ("1", "Ouvrir http://localhost:4200 — montrer le catalogue avec 12 produits, la pagination, le filtre par catégorie."),
        ("2", "Cliquer sur un produit → fiche détaillée avec image, prix, stock, et liste des avis."),
        ("3", "Tenter d'ajouter au panier sans être connecté → message \"Veuillez vous connecter\" + redirection /login."),
        ("4", "Se connecter avec user@estore.ma / User@123 → header met à jour le nom et le badge panier."),
        ("5", "Ajouter 2 produits différents au panier → badge passe à 2, toast vert de confirmation."),
        ("6", "Aller dans /cart → modifier les quantités, voir le total recalculé."),
        ("7", "Cliquer \"Valider la commande\" → redirection /orders, voir la commande #1 confirmée."),
        ("8", "Retourner sur un produit, déposer un avis 5 étoiles → l'avis apparaît immédiatement dans la liste."),
    ]
    for n, step in scenario:
        s.append(Paragraph(f"<b>{n}.</b> {step}", BODY))

    s.append(Paragraph("5. Points forts à mettre en avant", H1))
    points = [
        ("Architecture", "3 couches × 5 domaines, structure cohérente et scalable."),
        ("Sécurité", "JWT + BCrypt + Spring Security 6, @PreAuthorize sur les endpoints ADMIN."),
        ("Persistance hybride", "JPA pour la cohérence transactionnelle, MongoDB pour les avis volumineux."),
        ("Robustesse", "Tout le checkout est transactionnel (@Transactional) — atomicité garantie."),
        ("Tests", "9 tests unitaires JUnit 5 + Mockito, BUILD SUCCESS."),
        ("DevOps", "Profils dev/prod, Docker Compose multi-services, fallback H2 sans installation."),
        ("UI/UX", "Angular 17 standalone + signals, Bootstrap 5, toasts, lazy loading, responsive."),
        ("Documentation", "README complet + 7 PDF explicatifs (ce document)."),
    ]
    for title, txt in points:
        s.append(Paragraph(f"<b>{title}.</b> {txt}", BODY))

    s.append(PageBreak())

    s.append(Paragraph("6. Questions courantes du jury et réponses", H1))

    qa = [
        ("Pourquoi avoir choisi MongoDB pour les avis et pas SQL ?",
         "Les avis sont des données semi-structurées, peu contraintes relationnellement, "
         "lues très fréquemment et écrites en flux tendu. MongoDB offre de meilleures "
         "performances en lecture/écriture pour ce type de données et permet d'illustrer "
         "la coexistence de deux paradigmes de persistance dans une même application."),

        ("Comment garantissez-vous la cohérence du panier en cas de stock insuffisant ?",
         "L'opération checkout est annotée @Transactional. Toutes les vérifications de "
         "stock sont effectuées AVANT toute modification. Si une vérification échoue, "
         "une BusinessException est levée → le rollback automatique annule toutes les "
         "opérations déjà effectuées dans la transaction."),

        ("Pourquoi H2 en plus de MySQL ?",
         "H2 est utilisée pour le profil dev — démarrage instantané sans installation, "
         "idéale pour les démos et le développement local. MySQL est utilisée pour la "
         "production. Le code est strictement identique grâce à JPA."),

        ("Comment le JWT est-il sécurisé ?",
         "Signé en HMAC-SHA256 avec une clé secrète configurée hors du code "
         "(application.properties). Expiration 24h. Vérifié à chaque requête par "
         "JwtAuthenticationFilter avant exécution du controller."),

        ("Pourquoi Angular standalone et pas un NgModule classique ?",
         "C'est le standard depuis Angular 17. Plus concis, plus performant (lazy loading "
         "natif), pas de boilerplate. Les composants déclarent leurs dépendances directement."),
    ]
    for q, a in qa:
        s.append(Paragraph(f"<b>Q : {q}</b>", H3))
        s.append(Paragraph(a, BODY))

    s.append(Paragraph("7. Liens utiles pendant la démo", H1))
    links = Table([
        ["Adresse", "Contenu"],
        ["http://localhost:4200",            "Frontend Angular"],
        ["http://localhost:8080/api/products", "API REST (lecture publique)"],
        ["http://localhost:8080/h2-console", "Console H2 (profil dev)"],
        ["http://localhost:8081",            "phpMyAdmin (si Docker)"],
        ["http://localhost:8082",            "mongo-express (si Docker)"],
    ], colWidths=[7 * cm, 7 * cm])
    links.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.4, grey),
    ]))
    s.append(links)

    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    return path


# ─────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, io
    # Force UTF-8 sur la console Windows pour eviter UnicodeEncodeError
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 60)
    print("Generation des PDF explicatifs E-Store")
    print("=" * 60)
    builders = [
        ("Presentation & Architecture", build_pdf_01),
        ("Backend - 5 domaines", build_pdf_02),
        ("Securite JWT & MongoDB", build_pdf_03),
        ("Frontend Angular", build_pdf_04),
        ("Tests & Configuration", build_pdf_05),
        ("Docker - probleme & solution", build_pdf_06),
        ("Guide demarrage & soutenance", build_pdf_07),
    ]
    for name, fn in builders:
        path = fn()
        size_kb = os.path.getsize(path) // 1024
        print(f"  [OK] {os.path.basename(path):50s} ({size_kb} ko)")
    print("=" * 60)
    print(f"7 PDF generes dans : {OUT_DIR}")
