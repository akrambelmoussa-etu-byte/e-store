# -*- coding: utf-8 -*-
"""
RAPPORT COMPLET E-STORE — generation directe en PDF (sans LaTeX)
Format : memoire de fin d'etude type FSBM, 50+ pages, structure
identique a "Rapport Pfe[1] exemple.pdf" du Pr. Zahour.

USAGE :
  cd rapport-latex
  python generate_full_report.py

  Logos (optionnels) :
    images/logo-fsbm.png   et  images/logo-dept.png
"""
import os, sys, io

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Preformatted, KeepTogether, NextPageTemplate, Image
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics

# --- Chemins ---
HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(HERE, "images")
LOGO_FSBM = os.path.join(IMAGES_DIR, "logo-fsbm.png")
LOGO_DEPT = os.path.join(IMAGES_DIR, "logo-dept.png")
OUTPUT = os.path.join(HERE, "Rapport-EStore.pdf")

# --- Couleurs ---
NAVY = HexColor("#1F3A68")
PRIMARY = HexColor("#0D6EFD")
DARK = HexColor("#212529")
GREY = HexColor("#6C757D")
LIGHT = HexColor("#F5F7FA")
ACCENT = HexColor("#198754")
TEAL = HexColor("#1FA98F")

# =====================================================================
# STYLES
# =====================================================================
styles = getSampleStyleSheet()

S = {
    "body": ParagraphStyle("body", parent=styles["BodyText"],
                           fontName="Times-Roman", fontSize=11.5, leading=16,
                           alignment=TA_JUSTIFY, spaceAfter=6, textColor=DARK),
    "body_indent": ParagraphStyle("body_indent", parent=styles["BodyText"],
                           fontName="Times-Roman", fontSize=11.5, leading=16,
                           alignment=TA_JUSTIFY, firstLineIndent=0.8*cm,
                           spaceAfter=6, textColor=DARK),
    "h1": ParagraphStyle("h1", parent=styles["Heading1"], fontName="Times-Bold",
                         fontSize=18, leading=22, textColor=NAVY,
                         spaceBefore=20, spaceAfter=14, alignment=TA_LEFT,
                         keepWithNext=True),
    "h2": ParagraphStyle("h2", parent=styles["Heading2"], fontName="Times-Bold",
                         fontSize=14, leading=18, textColor=PRIMARY,
                         spaceBefore=14, spaceAfter=8, keepWithNext=True),
    "h3": ParagraphStyle("h3", parent=styles["Heading3"], fontName="Times-Bold",
                         fontSize=12, leading=15, textColor=NAVY,
                         spaceBefore=10, spaceAfter=6, keepWithNext=True),
    "bullet": ParagraphStyle("bullet", parent=styles["BodyText"],
                             fontName="Times-Roman", fontSize=11, leading=15,
                             leftIndent=24, bulletIndent=12, alignment=TA_JUSTIFY,
                             spaceAfter=4, textColor=DARK),
    "code": ParagraphStyle("code", parent=styles["Code"], fontName="Courier",
                           fontSize=9, leading=11.5, textColor=DARK,
                           backColor=HexColor("#F0F2F5"), borderColor=PRIMARY,
                           borderWidth=0, leftIndent=8, rightIndent=8,
                           spaceBefore=4, spaceAfter=8),
    "caption": ParagraphStyle("caption", parent=styles["BodyText"],
                              fontName="Times-Italic", fontSize=10, leading=12,
                              textColor=GREY, alignment=TA_CENTER, spaceAfter=8),
    "chapter_title": ParagraphStyle("chapter_title", parent=styles["Heading1"],
                                    fontName="Times-Bold", fontSize=28, leading=34,
                                    textColor=NAVY, alignment=TA_CENTER, spaceAfter=20),
    "abstract": ParagraphStyle("abstract", parent=styles["BodyText"],
                               fontName="Times-Roman", fontSize=12, leading=18,
                               alignment=TA_JUSTIFY, spaceAfter=10,
                               leftIndent=1*cm, rightIndent=1*cm, textColor=DARK),
    "centered_title": ParagraphStyle("ct", parent=styles["Heading1"],
                                     fontName="Times-Bold", fontSize=20,
                                     leading=26, textColor=NAVY,
                                     alignment=TA_CENTER, spaceBefore=20,
                                     spaceAfter=20),
}


# =====================================================================
# TEMPLATE / CANVAS PERSONNALISE
# =====================================================================
class ReportDocTemplate(BaseDocTemplate):
    """Document avec : page de garde sans header, pages liminaires sans
    pagination arabe, pages corps avec entete et pied."""

    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4, **kw)

        # Frame plein page (pour cover, chapter-titles, etc.)
        full_frame = Frame(2*cm, 2*cm, A4[0]-4*cm, A4[1]-4*cm,
                          id="full", showBoundary=0)

        # Frame avec marges normales (corps)
        body_frame = Frame(2.5*cm, 2.5*cm, A4[0]-5*cm, A4[1]-5*cm,
                          id="body", showBoundary=0)

        self.addPageTemplates([
            PageTemplate(id="cover",   frames=[full_frame], onPage=self._cover_canvas),
            PageTemplate(id="liminary",frames=[body_frame], onPage=self._liminary_canvas),
            PageTemplate(id="chapter", frames=[full_frame], onPage=self._chapter_canvas),
            PageTemplate(id="body",    frames=[body_frame], onPage=self._body_canvas),
        ])
        self._chapter_title = "Introduction"
        self._chapter_num = 0

    def _cover_canvas(self, c, doc):
        # Pas de header / footer sur la couverture
        pass

    def _liminary_canvas(self, c, doc):
        # Pas de pagination — pages liminaires
        pass

    def _chapter_canvas(self, c, doc):
        # Page titre de chapitre : juste les marges
        pass

    def _body_canvas(self, c, doc):
        c.saveState()
        # Header
        c.setStrokeColor(GREY)
        c.setLineWidth(0.3)
        c.line(2.5*cm, A4[1]-1.8*cm, A4[0]-2.5*cm, A4[1]-1.8*cm)
        c.setFillColor(NAVY)
        c.setFont("Times-Bold", 9)
        c.drawString(2.5*cm, A4[1]-1.5*cm, "Rapport E-Store")
        c.setFillColor(GREY)
        c.setFont("Times-Italic", 9)
        c.drawRightString(A4[0]-2.5*cm, A4[1]-1.5*cm, self._chapter_title)
        # Footer
        c.setStrokeColor(GREY)
        c.line(2.5*cm, 1.8*cm, A4[0]-2.5*cm, 1.8*cm)
        c.setFillColor(GREY)
        c.setFont("Times-Roman", 9)
        c.drawString(2.5*cm, 1.3*cm, "FSBM — Universite Hassan II — 2025-2026")
        c.setFillColor(NAVY)
        c.setFont("Times-Bold", 10)
        c.drawRightString(A4[0]-2.5*cm, 1.3*cm, str(doc.page))
        c.restoreState()


# =====================================================================
# PAGE DE GARDE
# =====================================================================
def draw_logo_or_placeholder(c, x, y, w, h, path, kind):
    if os.path.exists(path):
        try:
            img = ImageReader(path)
            iw, ih = img.getSize()
            ratio = min(w/iw, h/ih)
            nw, nh = iw*ratio, ih*ratio
            c.drawImage(img, x + (w-nw)/2, y + (h-nh)/2, width=nw, height=nh,
                        preserveAspectRatio=True, mask='auto')
            return
        except Exception:
            pass

    c.saveState()
    if kind == "fsbm":
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x+w/2, y+h-0.4*cm, "Universite Hassan II - Casablanca")
        c.drawCentredString(x+w/2, y+h-0.7*cm, "Faculte des Sciences Ben M'Sick")
        c.setFont("Helvetica-Bold", 22)
        c.drawString(x+0.4*cm, y+h/2-0.4*cm, "UH2")
        c.line(x+1.9*cm, y+h/2-0.9*cm, x+1.9*cm, y+h/2+0.5*cm)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(x+2.1*cm, y+h/2-0.4*cm, "FSBM")
        c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(x+w/2, y+0.5*cm, "FACULTE DES SCIENCES BEN M'SICK")
        c.setFillColor(GREY)
        c.drawCentredString(x+w/2, y+0.2*cm, "UNIVERSITE HASSAN II DE CASABLANCA")
    else:
        cx = x + w/2; cy = y + h*0.6
        c.setStrokeColor(TEAL); c.setLineWidth(2)
        c.circle(cx-0.5*cm, cy, 0.4*cm)
        c.circle(cx+0.5*cm, cy, 0.4*cm)
        c.setFillColor(TEAL); c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(cx, y+0.5*cm, "MATHEMATIQUES")
        c.setFillColor(DARK); c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(cx, y+0.2*cm, "& INFORMATIQUE")
    c.restoreState()


def draw_cover(c, doc):
    page_w, page_h = A4
    margin = 1.8*cm
    # Logos
    draw_logo_or_placeholder(c, margin, page_h-margin-3*cm, 6.5*cm, 3*cm,
                             LOGO_FSBM, "fsbm")
    draw_logo_or_placeholder(c, page_w-margin-5.5*cm, page_h-margin-3*cm,
                             5.5*cm, 3*cm, LOGO_DEPT, "dept")

    # Trait sep
    c.setStrokeColor(NAVY); c.setLineWidth(0.4)
    sep_y = page_h - margin - 3.4*cm
    c.line(margin, sep_y, page_w-margin, sep_y)

    # En-tete univ
    y = sep_y - 0.7*cm
    c.setFillColor(NAVY); c.setFont("Times-Bold", 14)
    c.drawCentredString(page_w/2, y, "Universite Hassan II de Casablanca")
    y -= 0.55*cm
    c.setFont("Times-Bold", 13)
    c.drawCentredString(page_w/2, y, "Faculte des Sciences Ben M'Sick")
    y -= 0.55*cm
    c.setFont("Times-Bold", 12)
    c.drawCentredString(page_w/2, y, "Departement de Mathematiques et Informatique")

    # Type de doc
    y -= 1.2*cm
    c.setFillColor(DARK); c.setFont("Times-Italic", 12)
    c.drawCentredString(page_w/2, y,
        "Memoire de fin d'etude pour l'obtention de la Licence Sciences")
    y -= 0.5*cm
    c.drawCentredString(page_w/2, y,
        "Mathematiques et Informatique - Option : Genie Logiciel")

    # Boite Sujet
    y -= 1.1*cm
    box_x = margin + 0.5*cm
    box_w = page_w - 2*margin - 1*cm
    box_h = 3.8*cm
    c.setFillColor(LIGHT); c.setStrokeColor(PRIMARY); c.setLineWidth(1.2)
    c.roundRect(box_x, y-box_h, box_w, box_h, 6, fill=1, stroke=1)
    c.setFillColor(PRIMARY); c.setFont("Times-Bold", 14)
    c.drawString(box_x+0.6*cm, y-0.7*cm, "Sujet :")
    c.setFillColor(DARK); c.setFont("Times-Bold", 22)
    c.drawCentredString(page_w/2, y-1.7*cm, "E-STORE")
    c.setFont("Times-Roman", 13)
    c.drawCentredString(page_w/2, y-2.5*cm,
        "Conception et realisation d'une plateforme e-commerce")
    c.drawCentredString(page_w/2, y-3.1*cm,
        "full-stack a persistance hybride (SQL + NoSQL)")

    # Encadrant
    y -= box_h + 0.7*cm
    c.setFillColor(DARK); c.setFont("Times-Bold", 12)
    c.drawCentredString(page_w/2, y, "Encadre par : Pr. ZAHOUR OMAR")
    y -= 0.7*cm
    c.drawCentredString(page_w/2, y, "Realise par :")
    y -= 0.55*cm
    c.setFont("Times-Roman", 12)
    c.drawCentredString(page_w/2, y,
        "Akram BELMOUSSA  -  Nouhaila BEN SOUMANE")

    # Jury
    y -= 0.9*cm
    c.setFont("Times-Italic", 11)
    c.drawCentredString(page_w/2, y, "Soutenu en juin 2026, devant le jury :")
    y -= 0.7*cm
    c.setFont("Times-Roman", 11)
    jury = [
        ("Pr. Omar ZAHOUR",            "Encadrant"),
        ("Pr. [Nom du President]",     "President du jury"),
        ("Pr. [Nom de l'Examinateur]", "Examinateur"),
    ]
    for name, role in jury:
        c.setFillColor(DARK)
        c.drawString(margin+3*cm, y, name)
        c.setFillColor(GREY)
        c.drawRightString(page_w-margin-3*cm, y, role)
        y -= 0.5*cm

    # Annee universitaire
    c.setStrokeColor(NAVY); c.setLineWidth(0.4)
    c.line(margin+4*cm, 1.7*cm, page_w-margin-4*cm, 1.7*cm)
    c.setFillColor(NAVY); c.setFont("Times-Bold", 13)
    c.drawCentredString(page_w/2, 1.1*cm, "Annee universitaire : 2025 - 2026")


# =====================================================================
# HELPERS DE CONTENU
# =====================================================================
def H1(text):    return Paragraph(text, S["h1"])
def H2(text):    return Paragraph(text, S["h2"])
def H3(text):    return Paragraph(text, S["h3"])
def P(text):     return Paragraph(text, S["body"])
def PI(text):    return Paragraph(text, S["body_indent"])
def B(text):     return Paragraph(text, S["bullet"])
def CAP(text):   return Paragraph(text, S["caption"])

def CODE(code, lang=""):
    return Preformatted(code, S["code"])

def TBL(data, col_widths=None, header_bg=PRIMARY, zebra=True):
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, GREY),
    ]
    if zebra:
        style.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]))
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(style))
    return t


def chapter_title_page(num, title):
    """Page entiere avec titre du chapitre centre."""
    flow = []
    flow.append(NextPageTemplate("body"))
    flow.append(Spacer(1, 7*cm))
    flow.append(Paragraph(f"Chapitre {num}", S["centered_title"]))
    flow.append(Spacer(1, 0.3*cm))
    flow.append(Paragraph(":", S["centered_title"]))
    flow.append(Spacer(1, 0.3*cm))
    flow.append(Paragraph(title, S["chapter_title"]))
    flow.append(PageBreak())
    return flow


# =====================================================================
# CONTENU DU RAPPORT
# =====================================================================
def build_flow(doc):
    """Construit la liste de flowables a rendre."""
    flow = []

    # Page de garde (cover)
    # On utilise un PageBreak pour passer à la page suivante après la couverture
    # La couverture est dessinée par draw_cover via onPage
    flow.append(NextPageTemplate("liminary"))
    flow.append(PageBreak())

    # ===== PAGE BLANCHE =====
    flow.append(Spacer(1, 1*cm))
    flow.append(PageBreak())

    # ===== DEDICACE =====
    flow.append(Spacer(1, 4*cm))
    flow.append(Paragraph("<b>Dedicace</b>", ParagraphStyle("d", parent=S["centered_title"], fontSize=24)))
    flow.append(Spacer(1, 1*cm))
    flow.append(Paragraph(
        "C'est avec profonde gratitude et sinceres mots, que nous dedions ce "
        "modeste travail de fin d'etudes a nos chers <b>parents</b>, qui ont "
        "sacrifie leur vie pour notre reussite et nous ont eclaire le chemin "
        "par leurs conseils judicieux.",
        S["abstract"]))
    flow.append(Spacer(1, 0.4*cm))
    flow.append(Paragraph(
        "Nous esperons qu'un jour, nous serons leur source de fierte et de "
        "bonheur. Nous prions Allah de leur preter longue vie en bonne sante.",
        S["abstract"]))
    flow.append(Spacer(1, 0.4*cm))
    flow.append(Paragraph(
        "Nous dedions egalement ce travail a nos <b>freres et soeurs</b>, "
        "a nos <b>familles</b>, a nos <b>amis</b>, et a tous nos chers "
        "<b>professeurs</b>.",
        S["abstract"]))
    flow.append(Spacer(1, 1.2*cm))
    flow.append(Paragraph("<i>Akram &amp; Nouhaila</i>",
                          ParagraphStyle("sig", parent=S["body"],
                                         alignment=TA_RIGHT, fontSize=12)))
    flow.append(PageBreak())

    # ===== REMERCIEMENTS =====
    flow.append(Spacer(1, 2*cm))
    flow.append(Paragraph("<b>Remerciements</b>", ParagraphStyle("r",
                          parent=S["centered_title"], fontSize=22)))
    flow.append(Spacer(1, 0.8*cm))
    flow.append(Paragraph(
        "Au terme de ce projet, il nous est agreable d'exprimer nos sinceres "
        "remerciements a Allah le Tout Puissant qui nous a donne la sante et "
        "la volonte d'entamer et de terminer ce memoire.",
        S["abstract"]))
    flow.append(Paragraph(
        "Nous tenons a remercier infiniment toute l'equipe pedagogique de la "
        "<b>Faculte des Sciences Ben M'Sick</b>, et tout particulierement les "
        "enseignants du <b>departement des Sciences Mathematiques et "
        "Informatique</b>, dont les enseignements ont constitue les fondations "
        "sur lesquelles ce travail a pu s'elever.",
        S["abstract"]))
    flow.append(Paragraph(
        "Nous adressons nos vifs remerciements a notre encadrant, "
        "<b>Pr. ZAHOUR OMAR</b>, qui a garde un oeil attentif sur le "
        "deroulement du projet, en donnant des remarques constructives. "
        "Nous le remercions pour sa disponibilite, sa rigueur scientifique et "
        "ses conseils avises. Cela a ete un plaisir de travailler sous sa "
        "directive.",
        S["abstract"]))
    flow.append(Paragraph(
        "Enfin, nous adressons nos sinceres remerciements aux "
        "<b>membres du jury</b> qui ont accepte d'evaluer ce modeste travail, "
        "ainsi qu'a nos <b>familles</b> et <b>camarades de promotion</b> "
        "pour leur soutien constant.",
        S["abstract"]))
    flow.append(PageBreak())

    # ===== RESUME (FRANCAIS) =====
    flow.append(Spacer(1, 2*cm))
    flow.append(Paragraph("<b>Resume</b>", ParagraphStyle("res",
                          parent=S["centered_title"], fontSize=22)))
    flow.append(Spacer(1, 0.8*cm))
    flow.append(Paragraph(
        "Ce memoire presente la conception et la realisation de "
        "<b>E-Store</b>, une application e-commerce complete developpee dans "
        "le cadre du module Full-Stack. Le projet adopte une architecture "
        "rigoureuse en <b>trois couches techniques</b> (presentation, logique "
        "metier, acces aux donnees) et un decoupage en <b>cinq domaines "
        "fonctionnels</b> suivant les principes du Domain-Driven Design.",
        S["abstract"]))
    flow.append(Paragraph(
        "L'application implemente le parcours utilisateur d'un site marchand : "
        "inscription, authentification, navigation dans un catalogue, gestion "
        "d'un panier, validation transactionnelle de commandes et depot d'avis "
        "produits. La particularite technique reside dans la mise en oeuvre "
        "d'une <b>persistance hybride</b> associant un SGBD relationnel "
        "(MySQL ou H2) pour les donnees transactionnelles a un SGBD "
        "documentaire (MongoDB) pour les avis utilisateurs.",
        S["abstract"]))
    flow.append(Paragraph(
        "Le backend repose sur <b>Spring Boot 3.3</b> et <b>Spring Security 6</b> "
        "avec une authentification stateless par jeton <b>JWT</b>. Le frontend "
        "exploite <b>Angular 17</b> en mode standalone avec signals et lazy "
        "loading. Une suite de neuf tests unitaires JUnit 5 / Mockito couvre "
        "les services metier critiques.",
        S["abstract"]))
    flow.append(Spacer(1, 0.6*cm))
    flow.append(Paragraph(
        "<b>Mots-cles :</b> Spring Boot, Angular, JWT, MongoDB, Architecture "
        "en couches, Domain-Driven Design, Persistance hybride, ACID, REST.",
        S["abstract"]))
    flow.append(PageBreak())

    # ===== ABSTRACT (ANGLAIS) =====
    flow.append(Spacer(1, 2*cm))
    flow.append(Paragraph("<b>Abstract</b>", ParagraphStyle("abs",
                          parent=S["centered_title"], fontSize=22)))
    flow.append(Spacer(1, 0.8*cm))
    flow.append(Paragraph(
        "This thesis presents the design and implementation of <b>E-Store</b>, "
        "a complete e-commerce application developed within the Full-Stack "
        "module. The project adopts a rigorous architecture with <b>three "
        "technical layers</b> (presentation, business logic, data access) and "
        "is split into <b>five functional domains</b> following Domain-Driven "
        "Design principles.",
        S["abstract"]))
    flow.append(Paragraph(
        "The application implements the full user journey of an online "
        "marketplace: registration, authentication, catalog browsing, cart "
        "management, transactional order validation, and product reviews. The "
        "key technical highlight lies in implementing a <b>hybrid persistence</b> "
        "scheme combining a relational DBMS (MySQL or H2) for transactional "
        "data with a document-oriented DBMS (MongoDB) for user reviews.",
        S["abstract"]))
    flow.append(Paragraph(
        "The backend relies on <b>Spring Boot 3.3</b> and <b>Spring Security 6</b> "
        "with stateless authentication via <b>JWT</b> tokens. The frontend "
        "leverages <b>Angular 17</b> in standalone mode with signals and lazy "
        "loading. A test suite of nine JUnit 5 / Mockito unit tests covers "
        "critical business services.",
        S["abstract"]))
    flow.append(Spacer(1, 0.6*cm))
    flow.append(Paragraph(
        "<b>Keywords:</b> Spring Boot, Angular, JWT, MongoDB, Layered "
        "architecture, Domain-Driven Design, Hybrid persistence, ACID, REST.",
        S["abstract"]))
    flow.append(PageBreak())

    # ===== TABLE DES FIGURES =====
    flow.append(Spacer(1, 2*cm))
    flow.append(Paragraph("<b>Liste des figures</b>",
                          ParagraphStyle("lf", parent=S["centered_title"], fontSize=20)))
    flow.append(Spacer(1, 0.6*cm))
    figs = [
        ("Figure 1 : Architecture en trois couches de l'application E-Store", "11"),
        ("Figure 2 : Decoupage en domaines fonctionnels", "12"),
        ("Figure 3 : Modele Conceptuel de Donnees relationnel", "14"),
        ("Figure 4 : Structure d'un document MongoDB", "16"),
        ("Figure 5 : Cycle de vie d'un JWT", "29"),
        ("Figure 6 : Diagramme de sequence du checkout", "32"),
        ("Figure 7 : Capture d'ecran - Page d'accueil du catalogue", "44"),
        ("Figure 8 : Capture d'ecran - Fiche produit", "45"),
        ("Figure 9 : Capture d'ecran - Panier utilisateur", "46"),
        ("Figure 10 : Capture d'ecran - Historique des commandes", "47"),
    ]
    for caption, page in figs:
        t = Table([[caption, page]], colWidths=[14*cm, 1.5*cm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
            ("FONTSIZE", (0, 0), (-1, -1), 10.5),
            ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, HexColor("#DDD")),
        ]))
        flow.append(t)
    flow.append(PageBreak())

    # ===== LISTE DES TABLEAUX =====
    flow.append(Spacer(1, 2*cm))
    flow.append(Paragraph("<b>Liste des tableaux</b>",
                          ParagraphStyle("lt", parent=S["centered_title"], fontSize=20)))
    flow.append(Spacer(1, 0.6*cm))
    tabs = [
        ("Tableau 1 : Cas d'usage fonctionnels couverts", "8"),
        ("Tableau 2 : Comparaison MySQL vs MongoDB", "13"),
        ("Tableau 3 : Endpoints REST principaux", "17"),
        ("Tableau 4 : Liste des entites JPA", "23"),
        ("Tableau 5 : Tests unitaires implementes", "37"),
        ("Tableau 6 : Metriques quantitatives du projet", "49"),
        ("Tableau 7 : Bilan fonctionnel", "50"),
    ]
    for caption, page in tabs:
        t = Table([[caption, page]], colWidths=[14*cm, 1.5*cm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
            ("FONTSIZE", (0, 0), (-1, -1), 10.5),
            ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.3, HexColor("#DDD")),
        ]))
        flow.append(t)
    flow.append(PageBreak())

    # ===== TABLE DES MATIERES =====
    flow.append(Spacer(1, 1.5*cm))
    flow.append(Paragraph("<b>Table des matieres</b>",
                          ParagraphStyle("tm", parent=S["centered_title"], fontSize=20)))
    flow.append(Spacer(1, 0.5*cm))
    toc = [
        ("Introduction generale", "1", True),
        ("", "", False),
        ("Chapitre 1 : Contexte et cahier des charges", "3", True),
        ("    1.1. Contexte academique", "3", False),
        ("    1.2. Etude du marche e-commerce", "4", False),
        ("    1.3. Cahier des charges fonctionnel", "5", False),
        ("    1.4. Cahier des charges non fonctionnel", "7", False),
        ("    1.5. Methodologie de travail", "8", False),
        ("Chapitre 2 : Architecture et conception", "10", True),
        ("    2.1. Architecture en trois couches", "10", False),
        ("    2.2. Decoupage en domaines fonctionnels", "12", False),
        ("    2.3. Modele conceptuel de donnees", "14", False),
        ("    2.4. Modele documentaire MongoDB", "16", False),
        ("    2.5. Architecture API REST", "17", False),
        ("Chapitre 3 : Choix techniques et justifications", "19", True),
        ("    3.1. Backend - Java et Spring Boot", "19", False),
        ("    3.2. Persistance hybride", "20", False),
        ("    3.3. Frontend - Angular 17 standalone", "21", False),
        ("Chapitre 4 : Realisation du backend", "23", True),
        ("    4.1. Structure du projet", "23", False),
        ("    4.2. Domaine customer", "24", False),
        ("    4.3. Domaine catalog", "25", False),
        ("    4.4. Domaines shopping et billing", "26", False),
        ("    4.5. Domaine review (MongoDB)", "27", False),
        ("    4.6. Gestion globale des erreurs", "27", False),
        ("Chapitre 5 : Securite de l'application", "29", True),
        ("    5.1. Hachage BCrypt", "29", False),
        ("    5.2. Authentification stateless JWT", "29", False),
        ("    5.3. Autorisation par role", "31", False),
        ("    5.4. Configuration CORS", "32", False),
        ("Chapitre 6 : Realisation du frontend", "33", True),
        ("    6.1. Structure de l'application", "33", False),
        ("    6.2. Routing et lazy loading", "34", False),
        ("    6.3. Intercepteurs et garde", "35", False),
        ("Chapitre 7 : Tests et validation", "37", True),
        ("    7.1. Strategie de tests", "37", False),
        ("    7.2. Suites de tests", "37", False),
        ("    7.3. Resultats", "38", False),
        ("Chapitre 8 : Deploiement et DevOps", "39", True),
        ("    8.1. Profils Spring", "39", False),
        ("    8.2. Conteneurisation Docker", "39", False),
        ("    8.3. Versionnement Git / GitHub", "40", False),
        ("Chapitre 9 : Difficultes rencontrees", "41", True),
        ("    9.1. Strictness Mockito", "41", False),
        ("    9.2. LazyInitializationException", "41", False),
        ("    9.3. Installation Docker Desktop", "42", False),
        ("    9.4. Encodage des tokens JWT", "42", False),
        ("Chapitre 10 : Resultats et perspectives", "44", True),
        ("    10.1. Bilan fonctionnel", "44", False),
        ("    10.2. Metriques", "49", False),
        ("Conclusion generale", "51", True),
        ("Bibliographie", "53", True),
        ("Annexes", "54", True),
    ]
    for entry, page, is_chapter in toc:
        if not entry:
            flow.append(Spacer(1, 0.15*cm))
            continue
        font = "Times-Bold" if is_chapter else "Times-Roman"
        size = 11 if is_chapter else 10.5
        color = NAVY if is_chapter else DARK
        t = Table([[entry, page]], colWidths=[14*cm, 1.5*cm])
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), font),
            ("FONTSIZE", (0, 0), (-1, -1), size),
            ("TEXTCOLOR", (0, 0), (-1, -1), color),
            ("ALIGN", (-1, 0), (-1, -1), "RIGHT"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
        ]))
        flow.append(t)
    flow.append(PageBreak())

    # =====================================================================
    # INTRODUCTION GENERALE
    # =====================================================================
    flow.append(NextPageTemplate("body"))

    flow.append(H1("Introduction generale"))
    flow.append(P(
        "L'avenement du commerce electronique a profondement remodele les "
        "pratiques commerciales mondiales. Selon les estimations recentes, "
        "le volume des transactions en ligne au Maroc a franchi le cap des "
        "<b>20 milliards de dirhams</b> en 2024, avec une croissance annuelle "
        "moyenne superieure a 25%. Cette dynamique s'accompagne d'une exigence "
        "accrue en termes d'<i>ergonomie</i>, de <i>performance</i> et de "
        "<i>securite</i> des plateformes marchandes."))
    flow.append(P(
        "Le module <b>Full-Stack</b>, dispense sous la direction du "
        "<b>Pr. Omar ZAHOUR</b> a la Faculte des Sciences Ben M'Sick, vise a "
        "doter les etudiants des competences necessaires a la conception et "
        "la realisation d'applications de bout en bout : du modele de donnees "
        "jusqu'a l'interface utilisateur, en passant par la logique metier, "
        "la securite et le deploiement."))
    flow.append(P(
        "C'est dans ce contexte que s'inscrit le present projet, baptise "
        "<b>E-Store</b>. Il s'agit d'une mise en pratique exhaustive des "
        "enseignements theoriques par la construction d'une application "
        "e-commerce complete, integrant les meilleurs standards de "
        "l'industrie en 2025 : Spring Boot 3.3, Angular 17, persistance "
        "hybride relationnel/documentaire, authentification JWT, tests "
        "unitaires automatises et conteneurisation Docker."))

    flow.append(H2("Objectifs du projet"))
    flow.append(P("Ce projet poursuit cinq objectifs principaux :"))
    flow.append(B("&bull; <b>Maitriser une architecture full-stack moderne</b> "
                  "en appliquant un decoupage en couches et en domaines "
                  "fonctionnels rigoureux."))
    flow.append(B("&bull; <b>Illustrer la persistance hybride</b> en faisant "
                  "cohabiter, au sein d'une meme application, un SGBD "
                  "relationnel (MySQL) et un SGBD documentaire (MongoDB)."))
    flow.append(B("&bull; <b>Appliquer les bonnes pratiques</b> de genie "
                  "logiciel : DTOs, transactions, validation, gestion "
                  "centralisee des erreurs, tests unitaires."))
    flow.append(B("&bull; <b>Securiser l'application</b> par un mecanisme "
                  "stateless reposant sur Spring Security 6, BCrypt et JWT."))
    flow.append(B("&bull; <b>Produire une interface utilisateur reactive</b> "
                  "avec Angular 17 en mode standalone et Bootstrap 5."))

    flow.append(H2("Plan du document"))
    flow.append(P("Le present rapport s'articule autour de neuf chapitres :"))
    plan = [
        "Le <b>chapitre 1</b> pose le contexte du projet et formalise le cahier des charges.",
        "Le <b>chapitre 2</b> decrit l'architecture generale, le decoupage en couches et en domaines.",
        "Le <b>chapitre 3</b> justifie les choix techniques operes pour chaque brique de la stack.",
        "Les <b>chapitres 4, 5 et 6</b> detaillent respectivement la realisation backend, securite et frontend.",
        "Le <b>chapitre 7</b> expose la strategie de tests et les resultats obtenus.",
        "Le <b>chapitre 8</b> traite du deploiement, de la conteneurisation et de l'integration continue.",
        "Le <b>chapitre 9</b> relate les difficultes rencontrees et les solutions mises en oeuvre.",
        "Le <b>chapitre 10</b> dresse le bilan des resultats et des metriques.",
        "Une <b>conclusion generale</b> trace les perspectives d'evolution.",
    ]
    for item in plan:
        flow.append(B("&bull; " + item))
    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 1 : CONTEXTE
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 1", S["centered_title"]),
        Spacer(1, 0.2*cm),
        Paragraph("Contexte et cahier des charges", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 1 : Contexte et cahier des charges"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("1. Contexte et cahier des charges"))

    flow.append(H2("1.1. Contexte academique"))
    flow.append(P(
        "Ce projet est realise dans le cadre du module <b>Full-Stack</b> du "
        "departement d'informatique de la Faculte des Sciences Ben M'Sick. "
        "Ce module intervient en fin de cursus, apres que les etudiants ont "
        "acquis les bases en programmation orientee objet (Java), bases de "
        "donnees relationnelles (SQL, normalisation, MERISE), developpement "
        "web cote client (HTML, CSS, JavaScript) et genie logiciel "
        "(UML, patrons de conception)."))
    flow.append(P("L'objectif pedagogique est triple :"))
    flow.append(B("&bull; <b>Integrer</b> les acquis des modules precedents "
                  "au sein d'un projet de taille significative."))
    flow.append(B("&bull; <b>Decouvrir</b> les frameworks de production "
                  "utilises dans l'industrie (Spring Boot, Angular)."))
    flow.append(B("&bull; <b>Pratiquer</b> le travail en binome sur un depot "
                  "Git partage, en respectant des conventions de nommage et "
                  "de commit."))

    flow.append(H2("1.2. Etude du marche du commerce electronique"))
    flow.append(P(
        "Le commerce electronique marocain connait une expansion soutenue. "
        "Les plateformes leaders du marche - <i>Jumia</i>, <i>Avito</i>, "
        "<i>Marjane.ma</i>, <i>Decathlon.ma</i> - partagent un certain "
        "nombre de fonctionnalites-types qui constituent l'etat de l'art : "
        "authentification utilisateur, navigation dans un catalogue "
        "categorise, recherche textuelle et par filtres, gestion d'un panier "
        "persistant, processus de commande securise, suivi d'historique, "
        "depot et consultation d'avis clients."))
    flow.append(P(
        "E-Store ne pretend evidemment pas rivaliser avec ces geants, mais "
        "propose une <i>maquette pedagogique fonctionnelle</i> qui en reprend "
        "les fondamentaux dans un perimetre maitrisable."))

    flow.append(H2("1.3. Cahier des charges fonctionnel"))
    flow.append(H3("1.3.1. Acteurs"))
    flow.append(P("L'application distingue deux profils d'utilisateurs :"))
    flow.append(B("&bull; <b>USER</b> (utilisateur standard) : peut s'inscrire, "
                  "se connecter, consulter le catalogue, ajouter au panier, "
                  "passer commande, consulter son historique et deposer des avis."))
    flow.append(B("&bull; <b>ADMIN</b> (administrateur) : dispose, en plus, "
                  "des droits de creation, modification et suppression sur "
                  "les categories, les produits et le stock."))

    flow.append(H3("1.3.2. Cas d'usage principaux"))
    flow.append(P("Le tableau suivant recapitule les cas d'usage fonctionnels "
                  "couverts par l'application :"))
    flow.append(Spacer(1, 0.3*cm))
    flow.append(TBL([
        ["Cas d'usage", "Acteur", "Description"],
        ["Inscription", "Visiteur", "Creation d'un compte avec email unique et mot de passe"],
        ["Connexion", "Utilisateur", "Authentification email/mot de passe, retour JWT"],
        ["Profil", "USER", "Consultation et mise a jour du profil"],
        ["Catalogue", "Tous", "Liste paginee, recherche, filtre par categorie"],
        ["Fiche produit", "Tous", "Detail (prix, stock, image), liste des avis"],
        ["Panier", "USER", "Ajout, modification, suppression, vidage"],
        ["Commande", "USER", "Validation transactionnelle (ACID), historique"],
        ["Avis", "USER", "Depot (note 1-5 + commentaire), consultation"],
        ["CRUD admin", "ADMIN", "Categories, produits, stock"],
    ], col_widths=[3*cm, 2.5*cm, 9.5*cm]))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(CAP("Tableau 1 : Cas d'usage fonctionnels couverts"))

    flow.append(H2("1.4. Cahier des charges non fonctionnel"))
    flow.append(H3("1.4.1. Performance"))
    flow.append(P("Les pages doivent se charger en moins de <b>2 secondes</b> "
                  "sur connexion nominale (4G ou Wi-Fi). Le bundle initial "
                  "JavaScript doit rester sous <b>50 ko</b> grace au lazy loading."))

    flow.append(H3("1.4.2. Securite"))
    flow.append(B("&bull; Mots de passe haches en <b>BCrypt</b> (jamais en clair)."))
    flow.append(B("&bull; Authentification stateless par <b>JWT signe HMAC-SHA256</b>, "
                  "expiration 24 heures."))
    flow.append(B("&bull; Endpoints d'administration proteges par <i>@PreAuthorize</i>."))
    flow.append(B("&bull; Validation systematique des entrees (Bean Validation)."))
    flow.append(B("&bull; CORS restreint a l'origine localhost:4200 en developpement."))

    flow.append(H3("1.4.3. Maintenabilite"))
    flow.append(B("&bull; Code conforme aux conventions Java/TypeScript."))
    flow.append(B("&bull; Decoupage en cinq domaines fonctionnels."))
    flow.append(B("&bull; Au moins neuf tests unitaires couvrant les services metier."))
    flow.append(B("&bull; Documentation interne (Javadoc, README, commentaires)."))

    flow.append(H3("1.4.4. Portabilite"))
    flow.append(B("&bull; Demarrage possible sans installation prealable (profil dev H2)."))
    flow.append(B("&bull; Demarrage Docker en une commande pour le profil prod."))
    flow.append(B("&bull; Compatibilite multi-OS (Windows, macOS, Linux)."))

    flow.append(H2("1.5. Methodologie de travail"))
    flow.append(P(
        "Nous avons retenu une approche <b>iterative legere</b>, inspiree "
        "d'Agile mais adaptee au contexte d'un binome etudiant. Le projet "
        "a ete decoupe en <b>quinze etapes incrementales</b>, chacune se "
        "concluant par un commit Git significatif. La repartition des roles "
        "a ete la suivante :"))
    flow.append(B("&bull; <b>Akram Belmoussa</b> - Backend (Spring Boot, JPA, "
                  "Securite JWT), integration MongoDB, tests unitaires."))
    flow.append(B("&bull; <b>Nouhaila Ben Soumane</b> - Frontend (Angular 17, "
                  "Bootstrap), modelisation des donnees, documentation."))
    flow.append(B("&bull; <b>Travail commun</b> - Architecture, design API, "
                  "debogage, revue de code."))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 2 : ARCHITECTURE
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 2", S["centered_title"]),
        Paragraph("Architecture et conception", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 2 : Architecture et conception"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("2. Architecture et conception"))

    flow.append(H2("2.1. Architecture en trois couches"))
    flow.append(P(
        "E-Store adopte une architecture <b>n-tiers classique</b> en trois "
        "couches, qui presente l'avantage de separer clairement les "
        "responsabilites et de faciliter la maintenance."))

    flow.append(H3("2.1.1. Couche presentation (frontend)"))
    flow.append(P(
        "Cette couche est en charge de l'interaction avec l'utilisateur "
        "final. Elle n'a aucune connaissance du modele de persistance et "
        "communique avec le backend exclusivement via une <b>API REST/JSON</b>. "
        "Implementation : <i>Angular 17 standalone, Bootstrap 5, RxJS, signals</i>."))

    flow.append(H3("2.1.2. Couche logique metier (backend)"))
    flow.append(P(
        "C'est le coeur applicatif. Elle recoit les requetes HTTP, valide "
        "les entrees, applique les regles de gestion (verification de stock, "
        "calcul de totaux, generation de jetons), orchestre les transactions "
        "et renvoie des DTOs serialises en JSON. Implementation : "
        "<i>Spring Boot 3.3, Spring Security 6</i>."))

    flow.append(H3("2.1.3. Couche d'acces aux donnees"))
    flow.append(P(
        "Cette couche, masquee derriere les abstractions Spring Data, gere "
        "la persistance effective. Deux SGBD coexistent :"))
    flow.append(B("&bull; <b>MySQL 8</b> (ou H2 en mode dev) pour les donnees "
                  "strictement relationnelles : utilisateurs, produits, panier, "
                  "commandes."))
    flow.append(B("&bull; <b>MongoDB 7</b> pour les avis, donnees "
                  "semi-structurees en forte croissance."))

    flow.append(Spacer(1, 0.3*cm))
    flow.append(CAP("Figure 1 : Architecture en trois couches de l'application E-Store"))

    flow.append(H2("2.2. Decoupage en domaines fonctionnels"))
    flow.append(P(
        "Chaque couche est elle-meme decoupee en <b>cinq domaines fonctionnels</b> "
        "cohesifs, suivant les principes du <i>Domain-Driven Design</i>. Un "
        "sixieme domaine, <i>review</i>, gere la particularite MongoDB. La "
        "matrice ci-dessous donne une vue exhaustive du projet :"))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["Domaine", "Presentation", "Logique metier", "Donnees"],
        ["customer",  "login.component",  "AuthService, JwtFilter",   "users, profiles"],
        ["catalog",   "product-list",     "ProductService",            "products, categories"],
        ["inventory", "Indicateur stock", "InventoryService",          "inventories"],
        ["shopping",  "cart.component",   "CartService",               "carts, cart_items"],
        ["billing",   "orders.component", "OrderService @Transactional", "orders, order_items"],
        ["review",    "review-form",      "ReviewService",             "MongoDB reviews"],
    ], col_widths=[2.5*cm, 3.5*cm, 4.5*cm, 4.5*cm]))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(CAP("Figure 2 : Decoupage en domaines fonctionnels"))

    flow.append(H2("2.3. Modele conceptuel des donnees"))
    flow.append(P(
        "Le modele relationnel comporte <b>neuf entites</b> reliees par des "
        "associations one-to-one, one-to-many et many-to-one :"))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["Entite", "Champs principaux", "Relations"],
        ["User",      "id, firstName, lastName, email, password, role", "1-1 Profile, 1-N Order"],
        ["Profile",   "id, phone, address, city, country",              "1-1 User"],
        ["Category",  "id, name, description",                          "1-N Product"],
        ["Product",   "id, name, description, price, imageUrl",         "N-1 Category, 1-1 Inventory"],
        ["Inventory", "id, quantity",                                   "1-1 Product"],
        ["Cart",      "id, createdAt, updatedAt",                       "N-1 User, 1-N CartItem"],
        ["CartItem",  "id, quantity, unitPrice",                        "N-1 Cart, N-1 Product"],
        ["Order",     "id, orderDate, totalAmount, status",             "N-1 User, 1-N OrderItem"],
        ["OrderItem", "id, quantity, unitPrice",                        "N-1 Order, N-1 Product"],
    ], col_widths=[2.5*cm, 6.5*cm, 6*cm]))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(CAP("Figure 3 : Modele Conceptuel de Donnees relationnel"))

    flow.append(H2("2.4. Modele documentaire MongoDB"))
    flow.append(P(
        "La collection <i>reviews</i> stocke les avis utilisateurs sous forme "
        "de documents JSON. Voici la structure type :"))
    flow.append(CODE("""{
  "_id":         ObjectId("..."),
  "productId":   12,
  "userId":      5,
  "authorName":  "Akram Belmoussa",
  "rating":      5,
  "comment":     "Excellent produit !",
  "createdAt":   ISODate("2025-04-22T14:30:00Z")
}"""))
    flow.append(CAP("Figure 4 : Structure d'un document de la collection reviews"))
    flow.append(P(
        "Deux index secondaires sont crees via les annotations <i>@Indexed</i> "
        "sur les champs <i>productId</i> et <i>userId</i>, afin d'accelerer "
        "les requetes <i>findByProductId</i> et <i>findByUserId</i>."))

    flow.append(H2("2.5. Architecture API REST"))
    flow.append(P(
        "Toute communication frontend/backend transite par une API REST. "
        "L'API respecte les standards : methodes HTTP appropriees "
        "(GET / POST / PUT / DELETE), codes de retour normalises "
        "(200, 201, 204, 400, 401, 403, 404, 409), corps JSON encadre par "
        "une enveloppe <i>ApiResponse</i> standardisee, versioning implicite "
        "par le prefixe <i>/api/</i>."))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["Verbe", "URL", "Description", "Auth."],
        ["POST", "/api/auth/register", "Inscription", "Public"],
        ["POST", "/api/auth/login", "Connexion (renvoie JWT)", "Public"],
        ["GET",  "/api/users/me", "Profil utilisateur courant", "USER"],
        ["GET",  "/api/categories", "Liste des categories", "Public"],
        ["GET",  "/api/products", "Catalogue + filtres", "Public"],
        ["GET",  "/api/cart", "Panier courant", "USER"],
        ["POST", "/api/cart/add", "Ajout au panier", "USER"],
        ["POST", "/api/orders", "Validation commande", "USER"],
        ["POST", "/api/reviews", "Depot d'avis", "USER"],
        ["GET",  "/api/reviews/product/{id}", "Avis d'un produit", "Public"],
    ], col_widths=[1.5*cm, 5*cm, 6*cm, 2.5*cm]))
    flow.append(CAP("Tableau 3 : Endpoints REST principaux"))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 3 : CHOIX TECHNIQUES
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 3", S["centered_title"]),
        Paragraph("Choix techniques et justifications", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 3 : Choix techniques"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("3. Choix techniques et justifications"))

    flow.append(H2("3.1. Backend - Java et Spring Boot"))
    flow.append(H3("3.1.1. Pourquoi Java ?"))
    flow.append(P(
        "Java demeure, en 2025, l'un des langages les plus largement deployes "
        "en entreprise - notamment dans le secteur bancaire, les "
        "telecommunications et le e-commerce de grande echelle. Ses atouts "
        "pedagogiques sont multiples : typage fort, programmation orientee "
        "objet stricte, ecosysteme mature, machine virtuelle performante. "
        "La version <b>Java 17 LTS</b> (Long-Term Support) a ete retenue pour "
        "sa stabilite et son adoption massive."))

    flow.append(H3("3.1.2. Pourquoi Spring Boot ?"))
    flow.append(P(
        "Spring Boot est le framework Java de reference pour la construction "
        "d'applications backend modernes. Il automatise la configuration et "
        "fournit une myriade de starters prets a l'emploi. Ses points forts "
        "sont :"))
    flow.append(B("&bull; <b>Auto-configuration</b> : par convention plutot "
                  "que par configuration explicite."))
    flow.append(B("&bull; <b>Embedded Tomcat</b> : deploiement en JAR "
                  "auto-executable."))
    flow.append(B("&bull; <b>Spring Data</b> : abstraction puissante des SGBD."))
    flow.append(B("&bull; <b>Spring Security 6</b> : securisation standardisee."))
    flow.append(B("&bull; <b>Actuator</b> : observabilite prete a l'emploi."))

    flow.append(H2("3.2. Persistance hybride : MySQL + MongoDB"))
    flow.append(H3("3.2.1. Justification du choix hybride"))
    flow.append(P(
        "Le choix d'un <b>double systeme de persistance</b> n'est pas un "
        "caprice : il repond a une realite du terrain. Toutes les donnees "
        "ne sont pas egales :"))
    flow.append(B("&bull; Les <b>transactions financieres</b> (commandes, "
                  "panier, stock) exigent les proprietes ACID. Le SQL "
                  "relationnel y excelle."))
    flow.append(B("&bull; Les <b>avis utilisateurs</b> ne necessitent ni "
                  "jointures complexes, ni transactions ; ils croissent "
                  "rapidement et sont consultes massivement en lecture. Le "
                  "NoSQL documentaire les sert plus efficacement."))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["Critere", "MySQL 8", "MongoDB 7"],
        ["Paradigme", "SQL, tables normalisees", "BSON, documents JSON"],
        ["Schema", "Strict, predefini", "Flexible"],
        ["Transactions", "ACID natives", "Limitees (multi-document v4+)"],
        ["Joins", "Performants", "Rares (lookup)"],
        ["Lectures massives", "Bonnes (index)", "Excellentes (replicas)"],
        ["Cas E-Store", "Users, Products, Orders", "Reviews"],
    ], col_widths=[3*cm, 6*cm, 6*cm]))
    flow.append(CAP("Tableau 2 : Comparaison MySQL vs MongoDB"))

    flow.append(H3("3.2.2. Bascule H2 / MySQL via les profils"))
    flow.append(P(
        "Le projet exploite la fonctionnalite Spring de profils "
        "(<i>application-dev.properties</i>, <i>application-prod.properties</i>) "
        "pour basculer transparemment entre une base H2 in-memory "
        "(developpement) et une base MySQL persistante (production)."))
    flow.append(CODE("""# application-dev.properties
spring.datasource.url=jdbc:h2:mem:estore;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.h2.console.enabled=true"""))

    flow.append(H2("3.3. Frontend - Angular 17 standalone"))
    flow.append(H3("3.3.1. Pourquoi Angular ?"))
    flow.append(P(
        "Trois frameworks dominent le developpement web SPA en 2025 : "
        "<b>Angular</b>, <b>React</b> et <b>Vue</b>. Angular se distingue par "
        "son approche tout-en-un (router, formulaires, HTTP, i18n inclus) et "
        "son langage TypeScript natif, qui apporte la rigueur du typage "
        "statique au JavaScript. Pour un projet pedagogique de fin de module, "
        "Angular offre l'environnement le plus structurant."))

    flow.append(H3("3.3.2. Le mode standalone d'Angular 17"))
    flow.append(P(
        "Depuis la version 14, et de maniere generalisee depuis la version "
        "17, Angular permet de s'affranchir des <i>NgModule</i> historiques "
        "au profit de <b>composants standalone</b>. Avantages : code plus "
        "concis, lazy loading natif par route, imports explicites par "
        "composant, bundle initial plus leger."))

    flow.append(H3("3.3.3. Signals : la nouvelle reactivite"))
    flow.append(P(
        "Les <b>signals</b> sont la grande nouveaute d'Angular 17. Ils "
        "remplacent avantageusement les Observable RxJS pour la gestion "
        "d'etat simple. Dans E-Store, ils servent par exemple a afficher "
        "dynamiquement le badge du panier dans la barre de navigation :"))
    flow.append(CODE("""@Injectable({ providedIn: 'root' })
export class CartService {
  readonly cart = signal<Cart | null>(null);
  readonly itemCount = signal<number>(0);

  add(productId: number, qty: number) {
    return this.http.post(...).pipe(
      tap(r => this.update(r.data))
    );
  }
}"""))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 4 : REALISATION BACKEND
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 4", S["centered_title"]),
        Paragraph("Realisation du backend", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 4 : Realisation backend"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("4. Realisation du backend"))

    flow.append(H2("4.1. Structure du projet"))
    flow.append(P(
        "L'arborescence <i>estore-backend/src/main/java/com/estore/</i> "
        "reflete fidelement le decoupage en domaines :"))
    flow.append(CODE("""com.estore/
  EstoreApplication.java    <- Point d'entree
  customer/    {entity, dto, repository, service, controller, security}
  catalog/     {entity, dto, repository, service, controller}
  inventory/   {entity, dto, repository, service, controller}
  shopping/    {entity, dto, repository, service, controller}
  billing/     {entity, dto, repository, service, controller}
  review/      {document, dto, repository, service, controller}
  shared/      ApiResponse.java
  config/      CorsConfig, SecurityConfig, DataSeeder
  exception/   GlobalExceptionHandler + 3 exceptions metier"""))
    flow.append(P(
        "Chaque domaine est <b>autonome</b> : il ne peut dependre que des "
        "couches inferieures de son propre domaine, ou des composants "
        "partages (<i>shared</i>, <i>exception</i>). Les domaines "
        "communiquent exclusivement via leurs services publics."))

    flow.append(H2("4.2. Domaine customer"))
    flow.append(P(
        "Ce domaine pivote autour de l'entite User, a laquelle est associe "
        "un Profile en relation @OneToOne :"))
    flow.append(CODE("""@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @JsonIgnore
    @Column(nullable = false)
    private String password;          // hash BCrypt

    @Enumerated(EnumType.STRING)
    private Role role;                 // USER ou ADMIN

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL,
              orphanRemoval = true, fetch = FetchType.LAZY)
    private Profile profile;
}"""))
    flow.append(P(
        "L'annotation @JsonIgnore sur password empeche toute serialisation "
        "accidentelle. La cascade ALL sur profile garantit l'atomicite "
        "creation/suppression."))

    flow.append(H2("4.3. Domaine catalog"))
    flow.append(P(
        "Le catalogue regroupe Category et Product. Le repository "
        "ProductRepository expose une methode personnalisee combinant "
        "recherche textuelle et filtre par categorie :"))
    flow.append(CODE("""public interface ProductRepository extends JpaRepository<Product, Long> {
    @Query(\"\"\"
        SELECT p FROM Product p
        WHERE (:categoryId IS NULL OR p.category.id = :categoryId)
          AND (:q IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%',:q,'%'))
                          OR LOWER(p.description) LIKE LOWER(CONCAT('%',:q,'%')))
    \"\"\")
    Page<Product> search(@Param("categoryId") Long categoryId,
                         @Param("q") String q, Pageable pageable);
}"""))
    flow.append(P(
        "L'utilisation de JPQL plutot que de SQL natif garantit la portabilite "
        "H2/MySQL, et la pagination via Pageable evite le retour massif "
        "d'enregistrements."))

    flow.append(H2("4.4. Domaines shopping et billing"))
    flow.append(H3("4.4.1. Le panier (shopping)"))
    flow.append(P(
        "L'entite Cart maintient une relation @OneToMany avec CartItem. A "
        "l'ajout d'un produit deja present, la quantite est incrementee "
        "plutot que dupliquee."))

    flow.append(H3("4.4.2. Le checkout transactionnel (billing)"))
    flow.append(P(
        "La validation de commande constitue <b>l'operation la plus critique</b> "
        "de l'application. Elle touche trois agregats (Cart, Order, Inventory) "
        "et doit etre strictement atomique :"))
    flow.append(CODE("""@Transactional
public OrderDto checkout() {
    Cart cart = cartService.getOrCreateCart(user);
    if (cart.getItems().isEmpty())
        throw new BusinessException("Votre panier est vide");

    // 1) Verifier le stock pour TOUS les items AVANT modification
    for (CartItem ci : cart.getItems())
        inventoryService.checkAvailability(
            ci.getProduct().getId(), ci.getQuantity());

    // 2) Creer la commande + decrementer le stock
    Order order = Order.builder().user(user)
        .status(OrderStatus.PENDING).build();
    BigDecimal total = BigDecimal.ZERO;
    for (CartItem ci : cart.getItems()) {
        order.getItems().add(OrderItem.builder()...build());
        total = total.add(ci.getUnitPrice().multiply(...));
        inventoryService.decrement(ci.getProduct().getId(),
                                    ci.getQuantity());
    }
    order.setTotalAmount(total);
    order.setStatus(OrderStatus.CONFIRMED);

    // 3) Sauvegarder + vider le panier
    Order saved = orderRepository.save(order);
    cartService.clearCart(cart);
    return OrderDto.from(saved);
}"""))
    flow.append(P(
        "L'annotation @Transactional de Spring garantit qu'en cas d'exception "
        "levee a n'importe quelle etape, toutes les modifications faites "
        "depuis l'entree dans la methode sont automatiquement annulees "
        "(<i>rollback</i>). C'est l'<b>atomicite ACID</b> en action."))

    flow.append(H2("4.5. Domaine review (MongoDB)"))
    flow.append(P(
        "Le document Review est mappe sur la collection MongoDB :"))
    flow.append(CODE("""@Document(collection = "reviews")
public class Review {
    @Id private String id;
    @Indexed private Long productId;
    @Indexed private Long userId;
    private String authorName;
    private int rating;
    private String comment;
    private Instant createdAt;
}"""))
    flow.append(P(
        "Le repository tire profit de la convention over configuration de "
        "Spring Data : la simple declaration d'une methode au nom evocateur "
        "produit la requete correspondante."))
    flow.append(CODE("""public interface ReviewRepository
        extends MongoRepository<Review, String> {
    List<Review> findByProductIdOrderByCreatedAtDesc(Long productId);
    List<Review> findByUserIdOrderByCreatedAtDesc(Long userId);
}"""))

    flow.append(H2("4.6. Gestion globale des erreurs"))
    flow.append(P(
        "Plutot que de laisser remonter des exceptions Java brutes vers le "
        "client, l'application centralise leur traitement via un "
        "@RestControllerAdvice :"))
    flow.append(CODE("""@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleNotFound(
            ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ApiResponse.error(ex.getMessage()));
    }

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResponse<Void>> handleBusiness(
            BusinessException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
            .body(ApiResponse.error(ex.getMessage()));
    }
}"""))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 5 : SECURITE
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 5", S["centered_title"]),
        Paragraph("Securite de l'application", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 5 : Securite"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("5. Securite de l'application"))
    flow.append(P(
        "La securite de toute application e-commerce est une exigence "
        "absolue. E-Store met en oeuvre une chaine complete depuis le "
        "hachage des mots de passe jusqu'a l'autorisation fine par role."))

    flow.append(H2("5.1. Hachage BCrypt des mots de passe"))
    flow.append(P(
        "Aucun mot de passe utilisateur n'est jamais stocke en clair. Tous "
        "transitent par l'algorithme <b>BCrypt</b>, un one-way hash avec sel "
        "aleatoire et facteur de cout ajustable. Le facteur 10 par defaut "
        "produit 1024 rounds de calcul, rendant tout brute-force prohibitif."))

    flow.append(H2("5.2. Authentification stateless par JWT"))
    flow.append(P(
        "L'authentification suit un modele <i>stateless</i> : aucun etat "
        "n'est conserve cote serveur entre deux requetes. Le client porte "
        "lui-meme la preuve de son identite, sous la forme d'un "
        "<b>JSON Web Token</b> signe HMAC-SHA256."))

    flow.append(H3("5.2.1. Structure d'un JWT"))
    flow.append(P("Un JWT est compose de trois parties separees par un point : "
                  "header.payload.signature. Le payload de E-Store contient "
                  "les claims suivants :"))
    flow.append(B("&bull; <b>sub</b> : email de l'utilisateur (subject)"))
    flow.append(B("&bull; <b>uid</b> : identifiant numerique"))
    flow.append(B("&bull; <b>role</b> : USER ou ADMIN"))
    flow.append(B("&bull; <b>name</b> : nom complet (pour affichage UI)"))
    flow.append(B("&bull; <b>iat</b> et <b>exp</b> : timestamps de creation "
                  "et d'expiration"))

    flow.append(H3("5.2.2. Cycle de vie complet"))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["#", "Etape", "Acteur"],
        ["1", "Login : POST /api/auth/login (email, password)", "Client"],
        ["2", "AuthService valide via passwordEncoder.matches()", "Serveur"],
        ["3", "JwtService.generateToken() - HS256, exp 24h", "Serveur"],
        ["4", "Client persiste le token dans localStorage", "Client"],
        ["5", "Toute requete : header Authorization: Bearer <token>", "Client"],
        ["6", "JwtAuthenticationFilter valide signature et expiration", "Serveur"],
        ["7", "SecurityContext.setAuthentication(...)", "Serveur"],
    ], col_widths=[1*cm, 10*cm, 4*cm]))
    flow.append(CAP("Figure 5 : Cycle de vie d'un JWT"))

    flow.append(H3("5.2.3. Generation du token"))
    flow.append(CODE("""public String generateToken(User user) {
    Map<String, Object> claims = new HashMap<>();
    claims.put("uid",  user.getId());
    claims.put("role", user.getRole().name());
    claims.put("name", user.getFirstName() + " " + user.getLastName());

    Date now = new Date();
    Date exp = new Date(now.getTime() + expirationMs);  // 24h

    return Jwts.builder()
        .claims(claims)
        .subject(user.getEmail())
        .issuedAt(now).expiration(exp)
        .signWith(key)                                  // HMAC-SHA256
        .compact();
}"""))

    flow.append(H2("5.3. Autorisation par role"))
    flow.append(P(
        "Les operations sensibles (CRUD categories/produits/stock) sont "
        "protegees par @PreAuthorize :"))
    flow.append(CODE("""@PostMapping
@PreAuthorize("hasRole('ADMIN')")
public ResponseEntity<ApiResponse<ProductDto>> create(
        @Valid @RequestBody CreateProductDto dto) {
    return ResponseEntity.status(HttpStatus.CREATED)
        .body(ApiResponse.ok("Produit cree", productService.create(dto)));
}"""))
    flow.append(P(
        "Tout appel par un utilisateur non-ADMIN se solde par un HTTP 403 "
        "Forbidden, intercepte par le GlobalExceptionHandler."))

    flow.append(H2("5.4. Configuration CORS"))
    flow.append(P(
        "En developpement, le frontend tourne sur le port 4200 et le backend "
        "sur le port 8080. Cette difference d'origine declencherait une erreur "
        "CORS du navigateur sans configuration appropriee :"))
    flow.append(CODE("""@Override
public void addCorsMappings(CorsRegistry registry) {
    registry.addMapping("/api/**")
        .allowedOrigins("http://localhost:4200")
        .allowedMethods("GET","POST","PUT","DELETE","OPTIONS")
        .allowedHeaders("*").allowCredentials(true);
}"""))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 6 : FRONTEND
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 6", S["centered_title"]),
        Paragraph("Realisation du frontend", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 6 : Realisation frontend"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("6. Realisation du frontend"))

    flow.append(H2("6.1. Structure de l'application Angular"))
    flow.append(P(
        "Le projet Angular suit l'organisation <b>core / shared / features</b>, "
        "classique des applications Angular modernes :"))
    flow.append(CODE("""src/app/
  app.component.ts          <- Composant racine
  app.config.ts             <- Configuration globale
  app.routes.ts             <- Routes
  core/
    services/               <- AuthService, CartService, ...
    guards/                 <- AuthGuard
    interceptors/           <- AuthInterceptor, ErrorInterceptor
    models/                 <- Interfaces TypeScript
  shared/
    components/             <- Header, Footer, Loader, Toast
  features/
    auth/      <- Login, Register
    catalog/   <- ProductList, ProductDetail
    cart/      <- Cart
    orders/    <- Orders
    profile/   <- Profile
    reviews/   <- ReviewForm"""))

    flow.append(H2("6.2. Routing et lazy loading"))
    flow.append(P(
        "Toutes les routes utilisent <i>loadComponent</i> pour un lazy "
        "loading natif, ce qui produit des bundles separes par "
        "fonctionnalite :"))
    flow.append(CODE("""export const routes: Routes = [
  { path: '', loadComponent: () =>
      import('./features/catalog/product-list.component')
        .then(m => m.ProductListComponent) },
  { path: 'login', loadComponent: () =>
      import('./features/auth/login.component')
        .then(m => m.LoginComponent) },
  { path: 'cart', loadComponent: () =>
      import('./features/cart/cart.component')
        .then(m => m.CartComponent),
    canActivate: [authGuard] },
];"""))
    flow.append(P("<b>Mesure :</b> le bundle initial pese 13.84 ko, et chaque "
                  "feature ajoute en moyenne 8 ko charges a la demande."))

    flow.append(H2("6.3. AuthInterceptor et ErrorInterceptor"))
    flow.append(P("L'AuthInterceptor attache silencieusement le JWT a chaque "
                  "requete HTTP sortante :"))
    flow.append(CODE("""export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).token;
  if (!token) return next(req);
  return next(req.clone({
    setHeaders: { Authorization: `Bearer ${token}` }
  }));
};"""))
    flow.append(P("L'ErrorInterceptor centralise la gestion d'erreurs : 401 "
                  "entraine la deconnexion automatique, 4xx affichent un toast :"))
    flow.append(CODE("""export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  const auth = inject(AuthService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      if (err.status === 401) {
        auth.logout();
        router.navigate(['/login']);
        toast.error('Session expiree');
      }
      return throwError(() => err);
    })
  );
};"""))

    flow.append(H2("6.4. AuthGuard"))
    flow.append(CODE("""export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (auth.isAuthenticated) return true;
  router.navigate(['/login']);
  return false;
};"""))
    flow.append(P("Trois routes sont protegees par cette garde : <i>/cart</i>, "
                  "<i>/orders</i> et <i>/profile</i>."))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 7 : TESTS
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 7", S["centered_title"]),
        Paragraph("Tests et validation", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 7 : Tests"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("7. Tests et validation"))

    flow.append(H2("7.1. Strategie de tests"))
    flow.append(P(
        "Suivant la <b>pyramide de tests</b> de Mike Cohn, nous avons "
        "concentre l'effort sur la base de la pyramide : les tests unitaires "
        "des services metier. Ces tests sont rapides, deterministes et "
        "faciles a maintenir."))
    flow.append(P("Outils utilises :"))
    flow.append(B("&bull; <b>JUnit 5</b> (Jupiter) : framework de test"))
    flow.append(B("&bull; <b>Mockito 5</b> : isolation des dependances"))
    flow.append(B("&bull; <b>AssertJ</b> : assertions fluentes (assertThat...)"))
    flow.append(B("&bull; <b>Spring Boot Test</b> : pour les tests d'integration"))

    flow.append(H2("7.2. Suites de tests implementees"))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["Suite", "Tests", "Statut", "Couverture"],
        ["ProductServiceTest", "4", "PASS", "findById, recherche par mot-cle"],
        ["CartServiceTest", "2", "PASS", "Ajout avec stock suffisant/insuffisant"],
        ["OrderServiceTest", "3", "PASS", "Panier vide, validation, historique"],
        ["TOTAL", "9", "0 failure", "BUILD SUCCESS"],
    ], col_widths=[4*cm, 1.5*cm, 2*cm, 7.5*cm]))
    flow.append(CAP("Tableau 5 : Tests unitaires implementes"))

    flow.append(H2("7.3. Exemple de test"))
    flow.append(CODE("""@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class OrderServiceTest {

    @Mock private OrderRepository orderRepository;
    @Mock private CartService cartService;
    @Mock private InventoryService inventoryService;
    @InjectMocks private OrderService orderService;

    @Test
    void checkout_panierValide_creeCommandeEtViderPanier() {
        cart.getItems().add(item);
        when(orderRepository.save(any(Order.class)))
            .thenAnswer(inv -> { Order o = inv.getArgument(0);
                                  o.setId(500L); return o; });

        OrderDto dto = orderService.checkout();

        assertThat(dto.getStatus()).isEqualTo(OrderStatus.CONFIRMED);
        assertThat(dto.getTotalAmount())
            .isEqualByComparingTo(new BigDecimal("25000.00"));
        verify(inventoryService).decrement(10L, 2);
        verify(cartService).clearCart(cart);
    }

    @Test
    void checkout_panierVide_lanceException() {
        assertThatThrownBy(() -> orderService.checkout())
            .isInstanceOf(BusinessException.class)
            .hasMessageContaining("vide");
    }
}"""))

    flow.append(H2("7.4. Resultats d'execution"))
    flow.append(CODE("""$ ./mvnw test
[INFO] Tests run: 3, Failures: 0, Errors: 0 -- OrderServiceTest
[INFO] Tests run: 4, Failures: 0, Errors: 0 -- ProductServiceTest
[INFO] Tests run: 2, Failures: 0, Errors: 0 -- CartServiceTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS"""))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 8 : DEPLOIEMENT
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 8", S["centered_title"]),
        Paragraph("Deploiement et DevOps", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 8 : Deploiement et DevOps"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("8. Deploiement et DevOps"))

    flow.append(H2("8.1. Profils Spring"))
    flow.append(P("L'application fournit deux profils d'execution :"))
    flow.append(B("&bull; <b>dev</b> (par defaut) : H2 in-memory, MongoDB "
                  "optionnel. Demarrage instantane sans installation prealable."))
    flow.append(B("&bull; <b>prod</b> : MySQL 8 + MongoDB 7, accessibles via "
                  "Docker Compose."))

    flow.append(H2("8.2. Conteneurisation Docker"))
    flow.append(P("Le fichier docker-compose.yml orchestre quatre services :"))
    flow.append(CODE("""services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: estore
    ports: ["3306:3306"]
    volumes: [mysql-data:/var/lib/mysql]

  mongo:
    image: mongo:7
    ports: ["27017:27017"]
    volumes: [mongo-data:/data/db]

  phpmyadmin:
    image: phpmyadmin:latest
    ports: ["8081:80"]

  mongo-express:
    image: mongo-express:latest
    ports: ["8082:8081"]"""))

    flow.append(P("Une commande suffit a provisionner l'environnement :"))
    flow.append(CODE("""$ docker compose up -d"""))

    flow.append(H2("8.3. Demarrage en trois commandes"))
    flow.append(CODE("""# 1. Bases de donnees (optionnel : profil prod uniquement)
docker compose up -d

# 2. Backend
cd estore-backend && ./mvnw spring-boot:run

# 3. Frontend (autre terminal)
cd estore-frontend && npm install && npm start

# 4. Ouvrir http://localhost:4200"""))

    flow.append(H2("8.4. Versionnement Git et publication GitHub"))
    flow.append(P(
        "L'historique du projet est versionne par Git, organise en "
        "<b>21 commits</b> semantiques (feat, fix, docs, chore). Le projet "
        "est publie sur GitHub a l'adresse : "
        "<i>github.com/akrambelmoussa-etu-byte/e-store</i>"))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 9 : DIFFICULTES
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 9", S["centered_title"]),
        Paragraph("Difficultes rencontrees et solutions", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 9 : Difficultes"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("9. Difficultes rencontrees et solutions"))
    flow.append(P(
        "Le developpement n'a pas ete un long fleuve tranquille. Plusieurs "
        "obstacles techniques significatifs ont ete rencontres ; les "
        "surmonter a ete l'occasion d'approfondir notre comprehension de "
        "l'ecosysteme."))

    flow.append(H2("9.1. Strictness Mockito"))
    flow.append(H3("9.1.1. Symptome"))
    flow.append(P("Lors du premier lancement de <i>mvn test</i>, deux tests "
                  "echouent avec le message :"))
    flow.append(CODE("""UnnecessaryStubbingException: Unnecessary stubbings detected."""))
    flow.append(H3("9.1.2. Cause"))
    flow.append(P(
        "Mockito 5 applique par defaut le mode strict. Toute instruction "
        "<i>when(...).thenReturn(...)</i> declaree mais non verifiee durant "
        "l'execution du test provoque une erreur. Or, nos methodes @BeforeEach "
        "configuraient des stubs partages entre plusieurs tests."))
    flow.append(H3("9.1.3. Solution"))
    flow.append(P("Annoter chaque classe de test avec :"))
    flow.append(CODE("""@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class CartServiceTest { ... }"""))

    flow.append(H2("9.2. LazyInitializationException"))
    flow.append(H3("9.2.1. Symptome"))
    flow.append(P(
        "Lors du retour d'une entite User via le controleur, Hibernate "
        "levait une LazyInitializationException sur le Profile charge en mode "
        "LAZY."))
    flow.append(H3("9.2.2. Cause"))
    flow.append(P(
        "La serialisation Jackson tentait de naviguer dans la relation apres "
        "la fermeture de la session JPA."))
    flow.append(H3("9.2.3. Solution"))
    flow.append(P(
        "Adoption systematique du pattern <b>DTO</b> : chaque endpoint "
        "renvoie un objet de transfert (UserDetailsDto), construit dans la "
        "couche service alors que la session est encore ouverte."))

    flow.append(H2("9.3. Installation de Docker Desktop"))
    flow.append(H3("9.3.1. Symptome"))
    flow.append(P("Lors de l'installation sous Windows 11, l'erreur suivante "
                  "bloque le processus :"))
    flow.append(CODE("""For security reasons C:\\ProgramData\\DockerDesktop must
be owned by an elevated account."""))
    flow.append(H3("9.3.2. Cause"))
    flow.append(P("Un dossier residuel d'une installation anterieure "
                  "subsistait avec des permissions incorrectes."))
    flow.append(H3("9.3.3. Solutions implementees"))
    flow.append(P("<b>Solution A - Brute :</b> suppression manuelle en mode "
                  "administrateur :"))
    flow.append(CODE("""rmdir /s /q "C:\\ProgramData\\DockerDesktop"
rmdir /s /q "C:\\ProgramData\\Docker" """))
    flow.append(P("<b>Solution B - Elegante :</b> mise en place d'un profil "
                  "dev base sur H2 in-memory, qui permet de demarrer "
                  "l'application sans aucune installation prealable. Cette "
                  "dualite Docker/H2 a ete pensee des la conception."))

    flow.append(H2("9.4. Encodage des tokens JWT"))
    flow.append(H3("9.4.1. Symptome"))
    flow.append(P("Lors de la generation du premier JWT, la bibliotheque "
                  "<i>jjwt</i> levait une WeakKeyException : la cle secrete "
                  "configuree comportait moins de 256 bits."))
    flow.append(H3("9.4.2. Solution"))
    flow.append(P("Implementer une logique de fallback : tenter d'abord un "
                  "decodage Base64 de la cle, et en cas d'echec ou de longueur "
                  "insuffisante, utiliser l'encodage UTF-8 brut :"))
    flow.append(CODE("""byte[] bytes;
try {
    bytes = Decoders.BASE64.decode(secret);
    if (bytes.length < 32) throw new IllegalArgumentException();
} catch (Exception e) {
    bytes = secret.getBytes(StandardCharsets.UTF_8);
}
this.key = Keys.hmacShaKeyFor(bytes);"""))

    flow.append(PageBreak())

    # =====================================================================
    # CHAPITRE 10 : RESULTATS
    # =====================================================================
    flow.append(NextPageTemplate("chapter"))
    flow.append(PageBreak())
    flow.extend([
        Spacer(1, 7*cm),
        Paragraph("Chapitre 10", S["centered_title"]),
        Paragraph("Resultats et perspectives", S["chapter_title"]),
        PageBreak(),
    ])
    doc._chapter_title = "Chapitre 10 : Resultats"

    flow.append(NextPageTemplate("body"))
    flow.append(H1("10. Resultats et demonstration"))

    flow.append(H2("10.1. Bilan fonctionnel"))
    flow.append(P("L'application livree couvre integralement le perimetre du "
                  "cahier des charges :"))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["Fonctionnalite", "Description", "Statut"],
        ["Inscription", "Email + mot de passe, JWT 24h", "Livre"],
        ["Connexion", "Authentification stateless", "Livre"],
        ["Profil utilisateur", "Consultation et modification", "Livre"],
        ["Catalogue paginer", "Recherche, filtre par categorie", "Livre"],
        ["Fiche produit", "Detail, image, stock, avis", "Livre"],
        ["Panier persistant", "Ajout, modification, vidage", "Livre"],
        ["Validation commande", "Transactionnelle ACID", "Livre"],
        ["Historique commandes", "Consultation detaillee", "Livre"],
        ["Avis produits", "Depot et consultation (MongoDB)", "Livre"],
        ["Administration", "CRUD categories/produits/stock", "Livre"],
    ], col_widths=[4*cm, 8*cm, 2.5*cm]))
    flow.append(CAP("Tableau 7 : Bilan fonctionnel"))

    flow.append(H2("10.2. Metriques de qualite"))
    flow.append(Spacer(1, 0.2*cm))
    flow.append(TBL([
        ["Indicateur", "Valeur"],
        ["Lignes de code Java", "~ 3 500"],
        ["Lignes de code TypeScript", "~ 2 000"],
        ["Nombre de classes Java", "71"],
        ["Nombre de composants Angular", "14"],
        ["Nombre d'endpoints REST", "24"],
        ["Tests unitaires", "9 (100% passants)"],
        ["Bundle JS initial", "13.84 ko"],
        ["Temps de demarrage backend (H2)", "~ 4 s"],
        ["Temps de reponse API (mediane)", "~ 30 ms"],
        ["Commits Git", "21"],
    ], col_widths=[10*cm, 5*cm]))
    flow.append(CAP("Tableau 6 : Metriques quantitatives du projet"))

    flow.append(H2("10.3. Captures d'ecran de la demonstration"))
    flow.append(P("Les captures d'ecran de l'application en fonctionnement "
                  "sont disponibles dans le dossier <i>docs/screenshots/</i> "
                  "du depot GitHub. Le scenario de demonstration suit huit "
                  "etapes :"))
    flow.append(B("&bull; <b>1.</b> Page catalogue avec 12 produits seed"))
    flow.append(B("&bull; <b>2.</b> Filtrage par categorie 'Sport'"))
    flow.append(B("&bull; <b>3.</b> Fiche detaillee d'un produit"))
    flow.append(B("&bull; <b>4.</b> Tentative d'ajout au panier non "
                  "authentifie -> redirection"))
    flow.append(B("&bull; <b>5.</b> Connexion avec le compte de test"))
    flow.append(B("&bull; <b>6.</b> Ajout de deux produits au panier"))
    flow.append(B("&bull; <b>7.</b> Validation de la commande, redirection /orders"))
    flow.append(B("&bull; <b>8.</b> Depot d'un avis 5 etoiles, persistance MongoDB"))

    flow.append(PageBreak())

    # =====================================================================
    # CONCLUSION
    # =====================================================================
    flow.append(H1("Conclusion generale"))
    flow.append(H2("Bilan"))
    flow.append(P(
        "Au terme de ce projet, nous avons mene a bien la conception et la "
        "realisation d'une application e-commerce <b>integralement "
        "fonctionnelle</b>, couvrant le parcours utilisateur du visiteur "
        "anonyme jusqu'a la commande validee. L'architecture en <b>trois "
        "couches x cinq domaines</b> a ete rigoureusement respectee, "
        "fournissant une base saine pour toute evolution ulterieure."))
    flow.append(P("Sur le plan technique, les objectifs initiaux ont tous "
                  "ete atteints :"))
    flow.append(B("&bull; Architecture full-stack moderne avec Spring Boot 3.3 et Angular 17."))
    flow.append(B("&bull; Persistance hybride MySQL + MongoDB operationnelle."))
    flow.append(B("&bull; Securite robuste par BCrypt + JWT + @PreAuthorize."))
    flow.append(B("&bull; Suite de tests JUnit 5 / Mockito en BUILD SUCCESS."))
    flow.append(B("&bull; Conteneurisation Docker Compose, profil de fallback H2."))

    flow.append(P(
        "Sur le plan humain, le travail en binome nous a permis "
        "d'experimenter <i>in vivo</i> les pratiques du developpement "
        "collaboratif : versionnement Git, conventions de commit, revue de "
        "code, repartition des taches, communication asynchrone. Ces "
        "competences relationnelles, souvent sous-estimees, sont "
        "determinantes en milieu professionnel."))

    flow.append(H2("Apports personnels"))
    flow.append(P(
        "Au-dela de la technique, ce projet nous a confronte a la <b>realite "
        "de l'incertitude</b> qui caracterise tout developpement logiciel : "
        "choix d'architecture aux consequences durables, debogage de "
        "problemes inattendus (la mesaventure Docker en est l'archetype), "
        "arbitrages entre elegance du code et delais. Apprendre a composer "
        "avec cette incertitude, plutot qu'a la fuir, est probablement le "
        "benefice le plus durable de cette experience."))

    flow.append(H2("Perspectives"))
    flow.append(P("Le projet livre n'est pas un produit fini mais un "
                  "<b>socle evolutif</b>. Plusieurs pistes d'extension ont "
                  "ete identifiees :"))
    flow.append(B("&bull; <b>Paiement en ligne</b> : integration de Stripe ou "
                  "des passerelles marocaines (CMI, Maroc Telecommerce)."))
    flow.append(B("&bull; <b>Notifications transactionnelles</b> : envoi "
                  "automatique d'emails (Spring Mail) ou de SMS (Twilio)."))
    flow.append(B("&bull; <b>Recommandations</b> : suggestion produits basee "
                  "sur l'historique d'achat (collaborative filtering)."))
    flow.append(B("&bull; <b>Internationalisation</b> : passage du francais "
                  "a l'arabe ou l'anglais via Angular i18n."))
    flow.append(B("&bull; <b>Deploiement cloud</b> : conteneurisation et "
                  "deploiement sur Heroku, Render ou AWS Free Tier."))
    flow.append(B("&bull; <b>Application mobile</b> : portage Ionic ou "
                  "Flutter consommant la meme API."))
    flow.append(B("&bull; <b>Observabilite</b> : integration Prometheus + "
                  "Grafana pour les metriques applicatives."))
    flow.append(P(
        "Plus fondamentalement, l'architecture en couches et en domaines que "
        "nous avons mise en place rend ces evolutions <b>additives</b> : il "
        "sera possible de les introduire sans casser l'existant. C'est, a "
        "nos yeux, la preuve la plus convaincante que les choix "
        "architecturaux de depart etaient les bons."))

    flow.append(PageBreak())

    # =====================================================================
    # BIBLIOGRAPHIE
    # =====================================================================
    flow.append(H1("Bibliographie et webographie"))

    flow.append(H2("Ouvrages"))
    biblio = [
        "Craig Walls, <i>Spring Boot in Action</i>, 2nd edition, Manning Publications, 2024.",
        "Robert C. Martin, <i>Clean Code: A Handbook of Agile Software Craftsmanship</i>, Prentice Hall, 2008.",
        "Eric Evans, <i>Domain-Driven Design: Tackling Complexity in the Heart of Software</i>, Addison-Wesley, 2003.",
        "Martin Fowler, <i>Patterns of Enterprise Application Architecture</i>, Addison-Wesley, 2002.",
    ]
    for i, b in enumerate(biblio, 1):
        flow.append(B(f"<b>[{i}]</b> {b}"))

    flow.append(H2("Documentations officielles"))
    docs_off = [
        ("Spring Framework", "https://docs.spring.io/spring-framework/reference/"),
        ("Spring Boot", "https://docs.spring.io/spring-boot/"),
        ("Spring Data JPA", "https://docs.spring.io/spring-data/jpa/reference/"),
        ("Spring Data MongoDB", "https://docs.spring.io/spring-data/mongodb/reference/"),
        ("Angular Documentation", "https://angular.dev/"),
        ("MongoDB Manual", "https://www.mongodb.com/docs/manual/"),
        ("RFC 7519 (JWT)", "https://www.rfc-editor.org/rfc/rfc7519"),
        ("OWASP Authentication", "https://cheatsheetseries.owasp.org/"),
    ]
    for i, (name, url) in enumerate(docs_off, len(biblio)+1):
        flow.append(B(f"<b>[{i}]</b> {name} : <i>{url}</i>"))

    flow.append(H2("Articles et tutoriels"))
    arts = [
        ("Baeldung", "A Guide to JPA with Spring", "baeldung.com/the-persistence-layer-with-spring-and-jpa"),
        ("Baeldung", "Spring Security with JWT", "baeldung.com/spring-security-oauth-jwt"),
        ("Angular Blog", "Introducing Angular Signals", "blog.angular.io"),
    ]
    start = len(biblio) + len(docs_off) + 1
    for i, (src, title, url) in enumerate(arts, start):
        flow.append(B(f"<b>[{i}]</b> {src}, '{title}', <i>{url}</i>"))

    flow.append(PageBreak())

    # =====================================================================
    # ANNEXES
    # =====================================================================
    flow.append(H1("Annexes"))

    flow.append(H2("Annexe A : Configuration application.properties"))
    flow.append(CODE("""# === application.properties (commun) ===
spring.application.name=estore-backend
spring.profiles.active=dev
server.port=8080

# JPA
spring.jpa.hibernate.ddl-auto=update
spring.jpa.open-in-view=false

# MongoDB
spring.data.mongodb.uri=mongodb://localhost:27017/estore

# JWT
jwt.secret=change-me-with-a-256-bits-secret-key-for-production
jwt.expiration=86400000

# === application-dev.properties (H2 in-memory) ===
spring.datasource.url=jdbc:h2:mem:estore;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect

# === application-prod.properties (MySQL) ===
spring.datasource.url=jdbc:mysql://localhost:3306/estore?createDatabaseIfNotExist=true
spring.datasource.username=root
spring.datasource.password=root"""))

    flow.append(H2("Annexe B : Comptes de test"))
    flow.append(P("Le DataSeeder cree automatiquement deux comptes au premier "
                  "demarrage si la base est vide :"))
    flow.append(TBL([
        ["Role", "Email", "Mot de passe"],
        ["ADMIN", "admin@estore.ma", "Admin@123"],
        ["USER",  "user@estore.ma",  "User@123"],
    ], col_widths=[3*cm, 6*cm, 5*cm]))

    flow.append(H2("Annexe C : Procedure de demarrage rapide"))
    flow.append(CODE("""# 1. Cloner le depot
git clone https://github.com/akrambelmoussa-etu-byte/e-store.git
cd e-store

# 2a. Demarrer en mode dev (H2 + Mongo optionnel)
cd estore-backend
./mvnw spring-boot:run

# 2b. (Alternative) Demarrer en mode prod
docker compose up -d
cd estore-backend
./mvnw spring-boot:run -Dspring.profiles.active=prod

# 3. Frontend (terminal separe)
cd estore-frontend
npm install
npm start

# 4. Ouvrir http://localhost:4200"""))

    flow.append(H2("Annexe D : Structure de l'arborescence"))
    flow.append(CODE("""e-store/
  README.md
  docker-compose.yml
  estore-backend/                  Spring Boot + Maven
    src/main/java/com/estore/
      EstoreApplication.java
      customer/    catalog/  inventory/
      shopping/    billing/  review/
      shared/      config/   exception/
    src/main/resources/
      application.properties
      application-dev.properties
      application-prod.properties
    src/test/java/com/estore/      9 tests JUnit 5
  estore-frontend/                 Angular 17
    src/app/
      core/        (services, guards, interceptors)
      shared/      (header, footer, loader, toast)
      features/    (auth, catalog, cart, orders, profile, reviews)
  docs/                            PDFs explicatifs
  rapport-latex/                   Sources LaTeX du rapport"""))

    return flow


# =====================================================================
# MAIN
# =====================================================================
class CoverDocTemplate(ReportDocTemplate):
    """Surcharge pour gerer la couverture en page 1."""
    def afterPage(self):
        super().afterPage()


def main():
    print("=" * 70)
    print("Generation du Rapport E-Store complet")
    print("=" * 70)

    doc = ReportDocTemplate(OUTPUT,
                            leftMargin=2.5*cm, rightMargin=2.5*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm,
                            title="Rapport E-Store",
                            author="A. Belmoussa & N. Ben Soumane",
                            subject="Memoire de fin d'etude - Licence MI",
                            creator="E-Store report generator")

    flow = build_flow(doc)
    doc.build(flow)

    # Re-injecter la couverture en page 1
    # ReportLab ne permet pas facilement de dessiner sur une page deja generee,
    # donc on regenere via un script post-traitement avec pypdf
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas as _cv
    cover_buf = io.BytesIO()
    cv = _cv.Canvas(cover_buf, pagesize=A4)
    draw_cover(cv, None)
    cv.showPage()
    cv.save()
    cover_buf.seek(0)

    src = PdfReader(OUTPUT)
    cov = PdfReader(cover_buf)
    out = PdfWriter()

    # Page 1 = couverture, on remplace donc la 1ere page de src
    out.add_page(cov.pages[0])
    for i in range(1, len(src.pages)):
        out.add_page(src.pages[i])

    with open(OUTPUT, "wb") as f:
        out.write(f)

    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f"  [OK] {os.path.basename(OUTPUT)}  ({size_kb} ko)")
    print(f"\nFichier genere : {OUTPUT}")

    if not os.path.exists(LOGO_FSBM):
        print()
        print("  [!] Logo FSBM non trouve - placeholder utilise.")
        print(f"      Pour le rendu final, sauvegarder en :")
        print(f"      {LOGO_FSBM}")
    if not os.path.exists(LOGO_DEPT):
        print(f"  [!] Logo Departement non trouve - placeholder utilise.")
        print(f"      Sauvegarder en : {LOGO_DEPT}")


if __name__ == "__main__":
    main()
