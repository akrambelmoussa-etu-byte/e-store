# -*- coding: utf-8 -*-
"""
Generateur du Glossaire Technique — Projet E-Store
Definitions simples et courtes pour chaque mot-cle technique.

Usage : python generate_glossaire.py
"""
import os
import sys
import io

# Force UTF-8 sur Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
OUT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(OUT_DIR, "Glossaire-E-Store.pdf")

PRIMARY   = HexColor("#1f4e79")
ACCENT    = HexColor("#0d6efd")
LIGHT_BG  = HexColor("#eef4fb")
DARK      = HexColor("#1a1a1a")
GREY_MID  = HexColor("#555555")
GREY_LITE = HexColor("#dddddd")
GREEN     = HexColor("#198754")
ORANGE    = HexColor("#fd7e14")
PURPLE    = HexColor("#6f42c1")
RED       = HexColor("#dc3545")

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm

# ─────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────
styles = getSampleStyleSheet()

S_TITLE = ParagraphStyle("GlossTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=26,
    textColor=white,
    alignment=TA_CENTER,
    spaceAfter=4)

S_SUBTITLE = ParagraphStyle("GlossSub",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=12,
    textColor=HexColor("#cce4ff"),
    alignment=TA_CENTER,
    spaceAfter=2)

S_SECTION = ParagraphStyle("Section",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=13,
    textColor=white,
    alignment=TA_LEFT,
    spaceAfter=0,
    spaceBefore=0)

S_TERM = ParagraphStyle("Term",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    textColor=PRIMARY,
    spaceAfter=1,
    spaceBefore=0)

S_DEF = ParagraphStyle("Def",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    textColor=DARK,
    alignment=TA_JUSTIFY,
    spaceAfter=0,
    spaceBefore=0,
    leading=14)

S_TAG = ParagraphStyle("Tag",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=8,
    textColor=GREY_MID,
    spaceAfter=2)

S_FOOTER = ParagraphStyle("Footer",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    textColor=GREY_MID,
    alignment=TA_CENTER)

S_INTRO = ParagraphStyle("Intro",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10,
    textColor=DARK,
    alignment=TA_JUSTIFY,
    leading=15,
    spaceAfter=6)

# ─────────────────────────────────────────────
# DONNEES DU GLOSSAIRE
# (terme, definition, categorie/tag)
# ─────────────────────────────────────────────
CATEGORIES = [
    {
        "titre": "A — Backend & Framework Java",
        "color": PRIMARY,
        "entrees": [
            ("Spring Boot",
             "Framework Java qui permet de creer des applications web pretes a l'emploi rapidement, "
             "sans configuration complexe. Il integre un serveur Tomcat integre et gere automatiquement "
             "les dependances.",
             "Backend / Java"),

            ("Spring Security",
             "Module Spring qui securise l'application : il gere l'authentification (qui es-tu ?) "
             "et l'autorisation (qu'as-tu le droit de faire ?). Il protege chaque endpoint HTTP.",
             "Backend / Securite"),

            ("Spring Data JPA",
             "Module Spring qui simplifie l'acces a la base de donnees relationnelle. "
             "Il genere automatiquement les requetes SQL a partir d'interfaces Java (Repository).",
             "Backend / Base de donnees"),

            ("Spring Data MongoDB",
             "Module Spring qui permet d'interagir avec MongoDB (base NoSQL) de la meme maniere "
             "que Spring Data JPA, sans ecrire de requetes manuelles.",
             "Backend / NoSQL"),

            ("Maven",
             "Outil de gestion de projet Java. Il telecharg automatiquement les dependances "
             "(bibliotheques) declarees dans le fichier pom.xml et compile le code.",
             "Backend / Outils"),

            ("pom.xml",
             "Fichier de configuration Maven d'un projet Java. Il liste toutes les dependances "
             "(libraries), les plugins et les informations du projet.",
             "Backend / Outils"),

            ("Lombok",
             "Bibliotheque Java qui genere automatiquement le code repetitif : constructeurs, "
             "getters, setters, toString, equals via des annotations (@Data, @Builder...).",
             "Backend / Java"),

            ("@Transactional",
             "Annotation Java qui enveloppe une methode dans une transaction base de donnees : "
             "si une erreur survient, toutes les modifications sont annulees (rollback).",
             "Backend / Base de donnees"),

            ("GlobalExceptionHandler",
             "Classe Spring qui intercepte toutes les exceptions de l'application et renvoie "
             "des messages d'erreur JSON uniformes au client, au lieu d'une page d'erreur blanche.",
             "Backend / Architecture"),

            ("DataSeeder",
             "Composant Spring qui s'execute au demarrage de l'application pour inserer "
             "des donnees initiales (produits, categories) dans la base de donnees.",
             "Backend / Architecture"),
        ]
    },
    {
        "titre": "B — Architecture & Patterns",
        "color": GREEN,
        "entrees": [
            ("MVC (Model-View-Controller)",
             "Patron d'architecture qui separe une application en trois parties : "
             "Model (donnees), View (affichage) et Controller (logique). "
             "Facilite la maintenance et les tests.",
             "Architecture"),

            ("DTO (Data Transfer Object)",
             "Objet simple utilise pour transferer des donnees entre couches de l'application. "
             "Il evite d'exposer directement les entites de la base de donnees a l'API.",
             "Architecture / Pattern"),

            ("Repository Pattern",
             "Pattern qui isole la logique d'acces aux donnees dans une classe dedicee. "
             "Le reste de l'application n'a pas besoin de savoir si les donnees viennent "
             "d'une base SQL, NoSQL ou d'un fichier.",
             "Architecture / Pattern"),

            ("Service Layer",
             "Couche intermediaire entre le Controller et le Repository. "
             "Elle contient la logique metier (calculs, validations, regles). "
             "Chaque service gere un domaine precis (produits, commandes...).",
             "Architecture"),

            ("Controller",
             "Classe qui recoit les requetes HTTP entrantes, appelle le service adequat "
             "et retourne la reponse au client (en JSON). Dans Spring, annotee @RestController.",
             "Architecture / Backend"),

            ("Entity",
             "Classe Java qui represente une table en base de donnees relationnelle. "
             "Chaque instance de la classe correspond a une ligne dans la table. "
             "Annotee @Entity en JPA.",
             "Backend / Base de donnees"),

            ("Domain-Driven Design (DDD)",
             "Approche de conception ou le code est organise autour des domaines metier "
             "(customer, catalog, billing...) plutot que des couches techniques. "
             "Chaque domaine est autonome et coherent.",
             "Architecture"),

            ("ACID",
             "Proprietes garantissant la fiabilite des transactions base de donnees : "
             "Atomicite (tout ou rien), Coherence, Isolation (transactions independantes), "
             "Durabilite (donnees persistantes apres commit).",
             "Base de donnees"),

            ("Endpoint",
             "URL specifique d'une API qui repond a une action precise. "
             "Exemple : GET /api/products retourne la liste des produits. "
             "Chaque endpoint correspond a une methode dans un Controller.",
             "API / REST"),

            ("REST (Representational State Transfer)",
             "Style d'architecture pour les APIs web. Les ressources sont identifiees par des URLs, "
             "et les actions sont definies par les methodes HTTP (GET, POST, PUT, DELETE).",
             "API"),
        ]
    },
    {
        "titre": "C — Securite & Authentification",
        "color": RED,
        "entrees": [
            ("JWT (JSON Web Token)",
             "Token numerique signe utilise pour authentifier un utilisateur. "
             "Il contient des informations (utilisateur, roles, expiration) encodees en Base64. "
             "Le serveur le verifie sans stocker de session.",
             "Securite"),

            ("BCrypt",
             "Algorithme de hachage utilise pour stocker les mots de passe de facon securisee. "
             "Il ajoute un 'sel' aleatoire et est intentionnellement lent pour resister "
             "aux attaques par force brute.",
             "Securite"),

            ("CORS (Cross-Origin Resource Sharing)",
             "Mecanisme de securite du navigateur qui bloque les requetes HTTP vers un domaine different. "
             "Le serveur doit explicitement autoriser les origines frontends "
             "(ex: http://localhost:4200).",
             "Securite / Web"),

            ("Hachage (Hash)",
             "Transformation irreversible d'une donnee (mot de passe) en une chaine fixe. "
             "Contrairement au chiffrement, on ne peut pas retrouver l'original. "
             "On verifie en hachant l'entree et comparant au hash stocke.",
             "Securite"),

            ("@PreAuthorize",
             "Annotation Spring Security qui protege une methode : seuls les utilisateurs "
             "ayant le role adequat (ROLE_ADMIN, ROLE_USER) peuvent l'appeler. "
             "Leve une exception 403 sinon.",
             "Securite / Backend"),

            ("Filter (Filtre HTTP)",
             "Composant qui s'intercale dans la chaine de traitement des requetes HTTP "
             "avant qu'elles atteignent le Controller. Le JwtAuthenticationFilter valide "
             "le token JWT a chaque requete.",
             "Securite / Backend"),

            ("Role",
             "Permission attribuee a un utilisateur qui determine ses droits dans l'application. "
             "Dans E-Store : ROLE_USER (client) et ROLE_ADMIN (administrateur).",
             "Securite"),

            ("Stateless (sans etat)",
             "Architecture ou le serveur ne garde aucune session utilisateur en memoire. "
             "Chaque requete doit s'auto-authentifier via son token JWT. "
             "Facilite la scalabilite horizontale.",
             "Architecture / Securite"),
        ]
    },
    {
        "titre": "D — Base de Donnees",
        "color": ORANGE,
        "entrees": [
            ("JPA (Java Persistence API)",
             "Specification Java standard pour mapper des objets Java (entites) "
             "vers des tables SQL. Spring Data JPA est l'implementation la plus utilisee.",
             "Base de donnees / Java"),

            ("ORM (Object-Relational Mapping)",
             "Technique qui fait la correspondance automatique entre les objets Java "
             "et les tables SQL. Evite d'ecrire du SQL manuellement pour les operations CRUD.",
             "Base de donnees"),

            ("MySQL",
             "Systeme de gestion de base de donnees relationnelle (SQL) open-source. "
             "Stocke des donnees structurees en tables avec des relations (cles etrangeres). "
             "Utilise en production dans E-Store.",
             "Base de donnees"),

            ("H2",
             "Base de donnees relationnelle en memoire (in-memory), ecrite en Java. "
             "Utilisee en mode developpement : aucune installation requise, "
             "les donnees disparaissent a l'arret de l'application.",
             "Base de donnees / Dev"),

            ("MongoDB",
             "Base de donnees NoSQL qui stocke les donnees sous forme de documents JSON "
             "(appeles BSON). Adaptee aux donnees flexibles sans schema fixe, "
             "comme les avis clients dans E-Store.",
             "Base de donnees / NoSQL"),

            ("NoSQL",
             "Famille de bases de donnees qui ne suivent pas le modele relationnel SQL. "
             "Elles sont adaptees aux grandes quantites de donnees variables "
             "et aux structures non tabulaires.",
             "Base de donnees"),

            ("JPQL (Java Persistence Query Language)",
             "Langage de requetes similaire a SQL, mais qui opere sur les entites Java "
             "plutot que sur les tables SQL directement. Utilise avec l'annotation @Query.",
             "Base de donnees / JPA"),

            ("Migration / Seeder",
             "Script qui initialise ou met a jour la structure et les donnees d'une base. "
             "Un seeder insere des donnees de test ou initiales au demarrage de l'application.",
             "Base de donnees"),

            ("Transaction",
             "Ensemble d'operations base de donnees traitees comme une unite atomique. "
             "Si une operation echoue, toutes les precedentes sont annulees (rollback).",
             "Base de donnees"),
        ]
    },
    {
        "titre": "E — Frontend & Angular",
        "color": HexColor("#c0392b"),
        "entrees": [
            ("Angular",
             "Framework TypeScript developpe par Google pour creer des applications web "
             "SPA (Single Page Application). Il structure le code en composants, "
             "services et modules.",
             "Frontend / Framework"),

            ("TypeScript",
             "Langage de programmation base sur JavaScript qui ajoute le typage statique. "
             "Il detecte les erreurs a la compilation, avant l'execution dans le navigateur.",
             "Frontend / Langage"),

            ("Composant (Component)",
             "Unite de base d'Angular. Chaque composant gere une partie de l'interface : "
             "un bouton, un formulaire, une page entiere. Il a son propre HTML, CSS et logique.",
             "Frontend / Angular"),

            ("SPA (Single Page Application)",
             "Application web qui charge une seule page HTML et met a jour dynamiquement "
             "le contenu sans rechargement complet du navigateur. Angular est un framework SPA.",
             "Frontend"),

            ("Standalone Component",
             "Composant Angular 17 qui n'a pas besoin d'etre declare dans un NgModule. "
             "Il importe directement ses dependances, simplifiant l'architecture de l'application.",
             "Frontend / Angular 17"),

            ("Signal",
             "Nouveau mecanisme de reactivite dans Angular 17. Un signal est une valeur "
             "reactive : quand elle change, les composants qui la lisent se mettent a jour "
             "automatiquement, sans RxJS.",
             "Frontend / Angular 17"),

            ("Lazy Loading",
             "Technique qui charge le code d'une fonctionnalite seulement quand l'utilisateur "
             "navigue vers elle. Reduit le temps de chargement initial de l'application.",
             "Frontend / Performance"),

            ("Route (Routage)",
             "Mecanisme Angular qui affiche un composant different selon l'URL du navigateur. "
             "Exemple : /products affiche la liste, /cart affiche le panier.",
             "Frontend / Angular"),

            ("AuthGuard",
             "Garde Angular qui protege certaines routes. Il verifie si l'utilisateur "
             "est connecte avant d'afficher une page. Si non, il redirige vers /login.",
             "Frontend / Securite"),

            ("Interceptor",
             "Service Angular qui intercepte toutes les requetes HTTP sortantes ou "
             "les reponses entrantes. Utilise pour ajouter automatiquement le token JWT "
             "a chaque requete (authInterceptor).",
             "Frontend / Angular"),

            ("Bootstrap 5",
             "Bibliotheque CSS qui fournit des composants graphiques predefinis "
             "(boutons, cartes, grilles, formulaires). Rend l'interface responsive "
             "sur mobile et desktop.",
             "Frontend / CSS"),

            ("Responsive Design",
             "Conception d'interface qui s'adapte automatiquement a la taille de l'ecran "
             "(mobile, tablette, desktop). Utilise les grilles CSS flexibles et les media queries.",
             "Frontend / Design"),
        ]
    },
    {
        "titre": "F — Concepts Web & HTTP",
        "color": PURPLE,
        "entrees": [
            ("HTTP (HyperText Transfer Protocol)",
             "Protocole de communication entre navigateur et serveur web. "
             "Chaque echange est une requete (client -> serveur) et une reponse (serveur -> client) "
             "independantes.",
             "Web"),

            ("GET",
             "Methode HTTP pour lire des donnees. Ne modifie rien sur le serveur. "
             "Exemple : GET /api/products recupere la liste des produits.",
             "HTTP / REST"),

            ("POST",
             "Methode HTTP pour creer une nouvelle ressource. "
             "Les donnees sont envoyees dans le corps de la requete (body). "
             "Exemple : POST /api/auth/register cree un compte.",
             "HTTP / REST"),

            ("PUT",
             "Methode HTTP pour remplacer completement une ressource existante. "
             "Envoie toutes les donnees de la ressource mise a jour.",
             "HTTP / REST"),

            ("DELETE",
             "Methode HTTP pour supprimer une ressource. "
             "Exemple : DELETE /api/cart/items/5 supprime l'article 5 du panier.",
             "HTTP / REST"),

            ("JSON (JavaScript Object Notation)",
             "Format de donnees texte leger utilise pour echanger des informations "
             "entre frontend et backend. Lisible par les humains et les machines.",
             "Web / Format"),

            ("API (Application Programming Interface)",
             "Interface qui permet a deux logiciels de communiquer. "
             "Dans E-Store, le frontend Angular communique avec le backend Spring Boot "
             "via une API REST en JSON.",
             "Web / Architecture"),

            ("Status HTTP",
             "Code numerique qu'un serveur renvoie pour indiquer le resultat d'une requete. "
             "200 = succes, 201 = cree, 400 = mauvaise requete, 401 = non authentifie, "
             "403 = interdit, 404 = non trouve, 500 = erreur serveur.",
             "HTTP"),

            ("Header HTTP",
             "Metadonnee envoyee avec une requete ou reponse HTTP. "
             "Le token JWT est envoye dans le header 'Authorization: Bearer <token>'.",
             "HTTP / Securite"),

            ("Payload",
             "Donnees utiles transportees dans le corps d'une requete ou reponse HTTP. "
             "Aussi le contenu encode d'un JWT (userId, roles, expiration).",
             "HTTP / JWT"),

            ("Observable (RxJS)",
             "Flux de donnees asynchrone utilise dans Angular. "
             "Permet de reagir aux evenements (reponses HTTP, clics) de facon reactive "
             "et de les transformer avec des operateurs (map, filter, switchMap...).",
             "Frontend / RxJS"),

            ("BehaviorSubject",
             "Type special d'Observable RxJS qui memorise la derniere valeur emise "
             "et la diffuse immediatement aux nouveaux abonnes. "
             "Utilise pour partager l'etat de l'utilisateur connecte dans AuthService.",
             "Frontend / RxJS"),
        ]
    },
    {
        "titre": "G — DevOps & Outils",
        "color": HexColor("#2c3e50"),
        "entrees": [
            ("Docker",
             "Outil qui permet d'empaqueter une application et ses dependances "
             "dans un 'conteneur' portable. Le conteneur s'execute de la meme facon "
             "sur n'importe quelle machine.",
             "DevOps"),

            ("Docker Compose",
             "Outil Docker qui permet de definir et lancer plusieurs conteneurs "
             "simultanement via un fichier docker-compose.yml. "
             "Dans E-Store : MySQL, MongoDB, PHPMyAdmin, Mongo-Express.",
             "DevOps"),

            ("Conteneur",
             "Environnement isole et leger qui contient une application et tout ce dont "
             "elle a besoin pour fonctionner. Similaire a une machine virtuelle mais "
             "beaucoup plus leger.",
             "DevOps"),

            ("Git",
             "Systeme de controle de version distribue. Il enregistre l'historique de toutes "
             "les modifications du code, permet de revenir en arriere et de travailler "
             "a plusieurs en parallele.",
             "DevOps / Versioning"),

            ("GitHub",
             "Plateforme en ligne qui heberge des repositories Git. "
             "Permet la collaboration, le partage de code et l'integration continue. "
             "Le projet E-Store y est depose.",
             "DevOps / Collaboration"),

            ("Commit",
             "Instantane du code a un moment donne, enregistre dans l'historique Git. "
             "Chaque commit a un message qui decrit le changement effectue.",
             "Git"),

            ("Branch (Branche)",
             "Copie independante du code sur laquelle on peut travailler sans affecter "
             "la branche principale (main). Permet de developper des fonctionnalites en parallele.",
             "Git"),

            ("npm (Node Package Manager)",
             "Gestionnaire de paquets pour JavaScript/Node.js. "
             "Permet d'installer les dependances Angular et les outils frontend "
             "declares dans package.json.",
             "Frontend / Outils"),

            ("Profil Spring (application-dev.properties)",
             "Configuration specifique a un environnement (dev, prod). "
             "En dev : H2 en memoire. En prod : MySQL. "
             "Active via la variable spring.profiles.active.",
             "Backend / Configuration"),

            ("JUnit 5",
             "Framework de tests unitaires pour Java. Permet de verifier "
             "que chaque methode fonctionne correctement de facon isolee, "
             "sans lancer toute l'application.",
             "Tests"),

            ("Mockito",
             "Bibliotheque Java qui cree des 'faux' objets (mocks) pour les tests unitaires. "
             "Permet de tester un service sans avoir besoin d'une vraie base de donnees.",
             "Tests"),

            ("Test Unitaire",
             "Test qui verifie le bon fonctionnement d'une seule unite de code "
             "(methode ou classe) de facon isolee. "
             "Dans E-Store : 9 tests pour les services produit, panier et commande.",
             "Tests"),
        ]
    },
    {
        "titre": "H — Concepts E-Commerce",
        "color": HexColor("#7d6608"),
        "entrees": [
            ("Catalogue",
             "Ensemble des produits disponibles a la vente, organises par categories. "
             "Dans E-Store, le catalogue est gere par le domaine 'catalog' (Product, Category).",
             "E-Commerce / Domaine"),

            ("Panier (Cart)",
             "Liste temporaire des articles selectionnes par un utilisateur avant achat. "
             "Dans E-Store, le panier est gere en base de donnees et lie au compte utilisateur.",
             "E-Commerce / Domaine"),

            ("Commande (Order)",
             "Achat finalise par un client. Elle contient la liste des articles, "
             "les quantites, le total et le statut (PENDING, CONFIRMED, SHIPPED, DELIVERED).",
             "E-Commerce / Domaine"),

            ("Inventaire (Inventory)",
             "Gestion du stock disponible pour chaque produit. "
             "Lors d'une commande, le stock est decremente. "
             "Si le stock est insuffisant, la commande est refusee.",
             "E-Commerce / Domaine"),

            ("Avis (Review)",
             "Commentaire et note laisses par un client sur un produit. "
             "Dans E-Store, les avis sont stockes dans MongoDB (document flexible).",
             "E-Commerce / Domaine"),

            ("Checkout",
             "Processus de finalisation d'une commande : verification du stock, "
             "creation de la commande, decrementation de l'inventaire, "
             "vidage du panier. Execute dans une seule transaction ACID.",
             "E-Commerce / Process"),

            ("Categorie",
             "Groupe de produits ayant des caracteristiques communes. "
             "Exemple : Electronique, Vetements, Livres. "
             "Permet de filtrer et naviguer dans le catalogue.",
             "E-Commerce / Catalogue"),
        ]
    },
]

# ─────────────────────────────────────────────
# CONSTRUCTION DU PDF
# ─────────────────────────────────────────────
def page_header_footer(canvas, doc):
    """En-tete et pied de page sur chaque page."""
    canvas.saveState()
    w, h = A4

    # Bande superieure fine
    canvas.setFillColor(PRIMARY)
    canvas.rect(0, h - 18*mm, w, 18*mm, fill=1, stroke=0)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(white)
    canvas.drawString(MARGIN, h - 11*mm, "Glossaire Technique — Projet E-Store")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(w - MARGIN, h - 11*mm,
        "Akram Belmoussa & Nouhaila Ben Soumane | FSBM — DEV-INFO S6 | 2026")

    # Pied de page
    canvas.setFillColor(GREY_LITE)
    canvas.rect(0, 0, w, 10*mm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY_MID)
    canvas.drawCentredString(w / 2, 3.5*mm,
        f"Page {doc.page}  |  Module Full-Stack — Pr. Omar ZAHOUR  |  Universite Hassan II Casablanca")

    canvas.restoreState()


def make_cover(story):
    """Page de couverture du glossaire."""
    PAGE_W, PAGE_H = A4

    # Bloc de titre central (simule via Table)
    cover_data = [[
        Paragraph("GLOSSAIRE TECHNIQUE", S_TITLE),
    ]]
    tbl = Table(cover_data, colWidths=[PAGE_W - 2*MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), PRIMARY),
        ("TOPPADDING",    (0,0), (-1,-1), 20),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 16),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), [8,8,8,8]),
    ]))

    sub_data = [[
        Paragraph("Projet E-Store — Definitions simples et courtes", S_SUBTITLE),
    ]]
    tbl2 = Table(sub_data, colWidths=[PAGE_W - 2*MARGIN])
    tbl2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 16),
    ]))

    story.append(Spacer(1, 3.5*cm))
    story.append(tbl)
    story.append(Spacer(1, 2*mm))
    story.append(tbl2)
    story.append(Spacer(1, 1*cm))

    info = ParagraphStyle("CoverInfo",
        fontName="Helvetica", fontSize=10.5,
        textColor=GREY_MID, alignment=TA_CENTER, leading=18)

    story.append(Paragraph(
        "Module : Developpement Full-Stack &nbsp;|&nbsp; Encadrant : Pr. Omar ZAHOUR", info))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "Filiere : DEV-INFO S6 &nbsp;|&nbsp; Faculte des Sciences Ben M'Sick — Universite Hassan II", info))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Annee universitaire : 2025–2026", info))

    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GREY_LITE))
    story.append(Spacer(1, 8*mm))

    intro_text = (
        "Ce glossaire rassemble les definitions courtes et simples de tous les termes techniques "
        "utilises dans le projet E-Store. Il est organise par domaines thematiques pour faciliter "
        "la lecture et la revision avant la soutenance. Chaque definition est volontairement "
        "concise (2 a 3 phrases) afin de permettre une comprehension rapide du concept."
    )
    story.append(Paragraph(intro_text, S_INTRO))
    story.append(Spacer(1, 6*mm))

    # Comptage
    total = sum(len(c["entrees"]) for c in CATEGORIES)
    stats = [
        [Paragraph(f"<b>{len(CATEGORIES)}</b><br/>Categories", S_FOOTER),
         Paragraph(f"<b>{total}</b><br/>Definitions", S_FOOTER),
         Paragraph("<b>8</b><br/>Domaines", S_FOOTER),
         Paragraph("<b>2026</b><br/>Annee", S_FOOTER)],
    ]
    stats_tbl = Table(stats, colWidths=[(PAGE_W - 2*MARGIN)/4]*4)
    stats_tbl.setStyle(TableStyle([
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_BG),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LINEAFTER",  (0,0), (2,-1), 0.5, GREY_LITE),
        ("FONTNAME",   (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
    ]))
    story.append(stats_tbl)
    story.append(PageBreak())


def make_section_header(cat):
    """Bandeau de section colore."""
    data = [[Paragraph(cat["titre"], S_SECTION)]]
    tbl = Table(data, colWidths=[PAGE_W - 2*MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), cat["color"]),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return tbl


def make_entry(terme, definition, tag, cat_color, idx):
    """Carte pour une entree du glossaire."""
    bg = LIGHT_BG if idx % 2 == 0 else white

    tag_style = ParagraphStyle("TagLocal",
        parent=S_TAG, textColor=cat_color)

    term_style = ParagraphStyle("TermLocal",
        parent=S_TERM, textColor=cat_color)

    data = [[
        Paragraph(terme, term_style),
        Paragraph(definition, S_DEF),
        Paragraph(tag, tag_style),
    ]]

    col_w = PAGE_W - 2*MARGIN
    tbl = Table(data, colWidths=[4.8*cm, col_w - 4.8*cm - 2.8*cm, 2.8*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("LINEBELOW",     (0,0), (-1,-1), 0.5, GREY_LITE),
        ("LINEABOVE",     (0,0), (0,-1), 3, cat_color),
        ("ALIGN",         (2,0), (2,-1), "RIGHT"),
    ]))
    return tbl


def build_pdf():
    story = []

    doc = SimpleDocTemplate(
        OUT_FILE,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=2.2*cm,
        bottomMargin=1.5*cm,
        title="Glossaire Technique E-Store",
        author="Akram Belmoussa & Nouhaila Ben Soumane",
        subject="Definitions techniques du projet E-Store",
        creator="ReportLab",
    )

    make_cover(story)

    for cat in CATEGORIES:
        # En-tete de section
        story.append(Spacer(1, 6*mm))
        story.append(make_section_header(cat))
        story.append(Spacer(1, 3*mm))

        for i, (terme, definition, tag) in enumerate(cat["entrees"]):
            card = make_entry(terme, definition, tag, cat["color"], i)
            story.append(KeepTogether(card))

        story.append(Spacer(1, 8*mm))

    # Page finale
    story.append(PageBreak())
    end_style = ParagraphStyle("End",
        fontName="Helvetica-Bold", fontSize=14,
        textColor=PRIMARY, alignment=TA_CENTER,
        spaceBefore=100, spaceAfter=8)
    story.append(Paragraph("Fin du Glossaire", end_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=PRIMARY))
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph(
        "Projet E-Store — Module Full-Stack — FSBM, Universite Hassan II de Casablanca",
        ParagraphStyle("EndSub", fontName="Helvetica", fontSize=10,
                       textColor=GREY_MID, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Akram Belmoussa &amp; Nouhaila Ben Soumane — Encadrant : Pr. Omar ZAHOUR — 2025/2026",
        ParagraphStyle("EndSub2", fontName="Helvetica", fontSize=9,
                       textColor=GREY_MID, alignment=TA_CENTER, spaceBefore=4)))

    doc.build(story, onFirstPage=page_header_footer, onLaterPages=page_header_footer)
    print(f"[OK] Glossaire genere : {OUT_FILE}")


if __name__ == "__main__":
    build_pdf()
