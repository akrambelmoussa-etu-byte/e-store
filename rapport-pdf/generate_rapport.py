# -*- coding: utf-8 -*-
"""
Generateur du rapport de projet E-Store au format PDF.
Style : memoire de fin d'etude FSBM (Universite Hassan II Casablanca).

Usage : python generate_rapport.py
"""
import os
import sys
import io

# Force UTF-8 sur la console Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted,
    Image, NextPageTemplate, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.flowables import HRFlowable

# =====================================================================
# CONFIGURATION
# =====================================================================
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(OUT_DIR, "assets")
LOGO_DEPT = os.path.join(ASSETS, "dept_logo.png")
LOGO_FSBM = os.path.join(ASSETS, "fsbm_logo.png")

# Couleurs (style universitaire sobre)
PRIMARY = HexColor("#1f4e79")   # bleu academique
DARK = HexColor("#1a1a1a")
GREY_MID = HexColor("#595959")
GREY_LIGHT = HexColor("#bfbfbf")
BG_LIGHT = HexColor("#f2f2f2")
ACCENT_GREEN = HexColor("#2e7d32")

# =====================================================================
# STYLES
# =====================================================================
def build_styles():
    base = getSampleStyleSheet()
    st = {}

    st["TitleCover"] = ParagraphStyle("TitleCover", parent=base["Title"],
        fontName="Times-Bold", fontSize=18, textColor=DARK, leading=22,
        alignment=TA_CENTER, spaceAfter=8)

    st["TitleCoverBig"] = ParagraphStyle("TitleCoverBig", parent=base["Title"],
        fontName="Times-Bold", fontSize=22, textColor=PRIMARY, leading=28,
        alignment=TA_CENTER, spaceAfter=12)

    st["SubTitleCover"] = ParagraphStyle("SubTitleCover", parent=base["Normal"],
        fontName="Times-Italic", fontSize=14, textColor=DARK, leading=18,
        alignment=TA_CENTER, spaceAfter=6)

    st["HeaderCover"] = ParagraphStyle("HeaderCover", parent=base["Normal"],
        fontName="Times-Roman", fontSize=12, textColor=DARK, leading=16,
        alignment=TA_CENTER, spaceAfter=4)

    st["BoldCenter"] = ParagraphStyle("BoldCenter", parent=base["Normal"],
        fontName="Times-Bold", fontSize=11, textColor=DARK, leading=15,
        alignment=TA_CENTER, spaceAfter=4)

    # Sections
    st["H1"] = ParagraphStyle("H1", parent=base["Heading1"],
        fontName="Helvetica-Bold", fontSize=18, textColor=PRIMARY,
        leading=24, spaceBefore=24, spaceAfter=18, alignment=TA_LEFT)

    st["H2"] = ParagraphStyle("H2", parent=base["Heading2"],
        fontName="Helvetica-Bold", fontSize=14, textColor=PRIMARY,
        leading=20, spaceBefore=16, spaceAfter=8, alignment=TA_LEFT)

    st["H3"] = ParagraphStyle("H3", parent=base["Heading3"],
        fontName="Helvetica-Bold", fontSize=12, textColor=DARK,
        leading=16, spaceBefore=10, spaceAfter=6, alignment=TA_LEFT)

    st["H4"] = ParagraphStyle("H4", parent=base["Heading4"],
        fontName="Helvetica-BoldOblique", fontSize=11, textColor=GREY_MID,
        leading=14, spaceBefore=8, spaceAfter=4, alignment=TA_LEFT)

    # Corps
    st["Body"] = ParagraphStyle("Body", parent=base["BodyText"],
        fontName="Times-Roman", fontSize=11.5, textColor=DARK,
        leading=16, alignment=TA_JUSTIFY, spaceAfter=6,
        firstLineIndent=12)

    st["BodyNoIndent"] = ParagraphStyle("BodyNI", parent=st["Body"],
        firstLineIndent=0)

    st["Bullet"] = ParagraphStyle("Bullet", parent=st["BodyNoIndent"],
        leftIndent=24, bulletIndent=12, spaceAfter=3, leading=15)

    st["Caption"] = ParagraphStyle("Caption", parent=base["BodyText"],
        fontName="Times-Italic", fontSize=10, textColor=GREY_MID,
        leading=12, alignment=TA_CENTER, spaceBefore=2, spaceAfter=10)

    st["Code"] = ParagraphStyle("Code", parent=base["Code"],
        fontName="Courier", fontSize=8.5, textColor=DARK,
        backColor=BG_LIGHT, borderPadding=6, leading=11,
        leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=8)

    st["Quote"] = ParagraphStyle("Quote", parent=st["BodyNoIndent"],
        fontName="Times-Italic", leftIndent=24, rightIndent=24,
        textColor=GREY_MID, spaceAfter=10)

    # Arabe (résumé)
    st["Arabic"] = ParagraphStyle("Arabic", parent=base["BodyText"],
        fontName="Times-Roman", fontSize=12, textColor=DARK,
        leading=20, alignment=TA_RIGHT, spaceAfter=6)

    # Liminaires (dédicace, remerciement)
    st["LiminaireTitle"] = ParagraphStyle("LimT", parent=base["Title"],
        fontName="Times-Bold", fontSize=20, textColor=PRIMARY,
        leading=26, alignment=TA_CENTER, spaceAfter=24)

    st["LiminaireBody"] = ParagraphStyle("LimB", parent=st["BodyNoIndent"],
        fontName="Times-Italic", fontSize=12.5, leading=20,
        alignment=TA_JUSTIFY)

    st["LiminaireBodyCenter"] = ParagraphStyle("LimBC", parent=st["LiminaireBody"],
        alignment=TA_CENTER)

    # ChapHeader
    st["ChapNumber"] = ParagraphStyle("ChapNum", parent=base["Normal"],
        fontName="Helvetica", fontSize=12, textColor=GREY_MID,
        leading=14, alignment=TA_LEFT, spaceAfter=4)
    st["ChapTitle"] = ParagraphStyle("ChapT", parent=base["Title"],
        fontName="Helvetica-Bold", fontSize=26, textColor=PRIMARY,
        leading=32, alignment=TA_LEFT, spaceAfter=20)

    return st

ST = None  # initialise dans main


# =====================================================================
# HEADER / FOOTER
# =====================================================================
class PageState:
    """Etat partage entre les pages pour piloter header/footer."""
    chapter_title = ""
    page_number = 0
    show_header_footer = True
    show_page_number = True
    pre_intro = False  # avant l'introduction, numerotation romaine

STATE = PageState()

def to_roman(n):
    """Conversion en chiffres romains pour la pagination liminaire."""
    vals = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),
            (50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    s = ''
    for v, sym in vals:
        while n >= v:
            s += sym
            n -= v
    return s

def header_footer(canvas, doc):
    """Trace le header et footer sur chaque page (sauf cover)."""
    canvas.saveState()
    # En-tete
    if STATE.show_header_footer:
        canvas.setStrokeColor(GREY_LIGHT)
        canvas.setLineWidth(0.5)
        canvas.line(2 * cm, A4[1] - 1.6 * cm, A4[0] - 2 * cm, A4[1] - 1.6 * cm)

        canvas.setFillColor(GREY_MID)
        canvas.setFont("Helvetica", 9)
        canvas.drawString(2 * cm, A4[1] - 1.3 * cm, "E-Store - Memoire de fin de module")
        canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.3 * cm, STATE.chapter_title)

        # Pied
        canvas.line(2 * cm, 1.8 * cm, A4[0] - 2 * cm, 1.8 * cm)
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(GREY_MID)
        canvas.drawString(2 * cm, 1.3 * cm, "Belmoussa & Ben Soumane")
        canvas.drawCentredString(A4[0] / 2, 1.3 * cm, "FSBM - DEV-INFO S6")
        if STATE.show_page_number:
            if STATE.pre_intro:
                page_txt = to_roman(doc.page).lower()
            else:
                page_txt = str(STATE.page_number)
            canvas.drawRightString(A4[0] - 2 * cm, 1.3 * cm, page_txt)
    canvas.restoreState()


def no_decoration(canvas, doc):
    """Aucune decoration (page de garde)."""
    pass


# =====================================================================
# UTILITAIRES DE MISE EN PAGE
# =====================================================================
def chap_header(num, title):
    """Bloc d'en-tete d'un chapitre."""
    elems = []
    STATE.chapter_title = f"Chapitre {num}"
    elems.append(Paragraph(f"CHAPITRE {num}", ST["ChapNumber"]))
    elems.append(HRFlowable(width="100%", thickness=2, color=PRIMARY,
                            spaceBefore=2, spaceAfter=4))
    elems.append(Paragraph(title, ST["ChapTitle"]))
    elems.append(Spacer(1, 0.4 * cm))
    return elems


def section(num, title):
    return Paragraph(f"<b>{num}.</b> {title}", ST["H2"])

def subsection(num, title):
    return Paragraph(f"<b>{num}.</b> {title}", ST["H3"])

def p(text):
    return Paragraph(text, ST["Body"])

def pl(text):
    """Paragraph sans indent."""
    return Paragraph(text, ST["BodyNoIndent"])

def bullet(text):
    return Paragraph(f"<bullet>&bull;</bullet> {text}", ST["Bullet"])

def code(text):
    return Preformatted(text, ST["Code"])

def caption(text, num):
    return Paragraph(f"<i>Figure {num} : {text}</i>", ST["Caption"])

def tcaption(text, num):
    return Paragraph(f"<i>Tableau {num} : {text}</i>", ST["Caption"])


# =====================================================================
# PAGE DE GARDE
# =====================================================================
def cover_page(story):
    """Page 1 - couverture."""
    # En-tete bilingue (FR au-dessus, AR a droite)
    # On utilise un tableau a 3 colonnes : Logo FSBM | Texte central | Logo Dept
    fsbm = Image(LOGO_FSBM, width=3 * cm, height=2.2 * cm, hAlign="LEFT")
    dept = Image(LOGO_DEPT, width=3 * cm, height=2.2 * cm, hAlign="RIGHT")

    center_text = [
        Paragraph("<b>Universite Hassan II de Casablanca</b>", ST["HeaderCover"]),
        Paragraph("<b>Faculte des Sciences Ben M'Sik</b>", ST["HeaderCover"]),
        Paragraph("<b>Departement de Mathematiques et Informatique</b>", ST["HeaderCover"]),
    ]
    hdr = Table([[fsbm, center_text, dept]],
                colWidths=[3.5 * cm, 10 * cm, 3.5 * cm])
    hdr.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 0.6 * cm))
    story.append(HRFlowable(width="100%", thickness=1.2, color=PRIMARY))
    story.append(Spacer(1, 0.6 * cm))

    # Bloc filiere
    story.append(Paragraph(
        "<b>Memoire de fin de module pour la validation du module Full-Stack</b>",
        ST["HeaderCover"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "<b>Filiere : Developpement Informatique - S6 (DEV-INFO S6)</b>",
        ST["BoldCenter"]))
    story.append(Spacer(1, 1.4 * cm))

    # Bloc sujet
    story.append(Paragraph("<b>Sujet :</b>", ST["TitleCover"]))
    story.append(Spacer(1, 0.4 * cm))

    # Cadre du titre
    titlebox = Table([[
        Paragraph(
            "<b>E-STORE</b>",
            ParagraphStyle("titleE", parent=ST["TitleCoverBig"],
                           fontSize=30, leading=36, textColor=PRIMARY))
    ], [
        Paragraph(
            "Conception et realisation d'une plateforme<br/>"
            "e-commerce full-stack a persistance hybride<br/>"
            "<i>(Spring Boot - Angular - JPA - MongoDB)</i>",
            ParagraphStyle("subti", parent=ST["SubTitleCover"],
                           fontSize=13, leading=18))
    ]], colWidths=[14 * cm])
    titlebox.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.5, PRIMARY),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fafbfd")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(titlebox)
    story.append(Spacer(1, 1.5 * cm))

    # Encadrant + auteurs
    enc_aut = Table([
        [Paragraph("<b>Encadre par :</b>", ST["BoldCenter"]),
         Paragraph("<b>Realise par :</b>", ST["BoldCenter"])],
        [Paragraph("Pr. <b>ZAHOUR Omar</b>", ST["HeaderCover"]),
         Paragraph("Akram <b>BELMOUSSA</b><br/>Nouhaila <b>BEN SOUMANE</b>",
                   ST["HeaderCover"])],
    ], colWidths=[8.5 * cm, 8.5 * cm])
    enc_aut.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))
    story.append(enc_aut)
    story.append(Spacer(1, 1 * cm))

    # Soutenance + jury
    story.append(Paragraph(
        "<b>Soutenu le 10 Mai 2026, devant le jury :</b>",
        ST["BoldCenter"]))
    story.append(Spacer(1, 0.3 * cm))

    jury = Table([
        ["Pr. ZAHOUR Omar",         "Encadrant"],
        ["Pr. BEN Lahmar El Habib", "Examinateur"],
        ["Pr. EL KANDALI Khalid",   "Examinateur"],
    ], colWidths=[8 * cm, 6 * cm])
    jury.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
    ]))
    story.append(jury)

    story.append(Spacer(1, 1.5 * cm))
    story.append(HRFlowable(width="100%", thickness=1.2, color=PRIMARY))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("<b>Annee universitaire : 2025 - 2026</b>",
                           ST["BoldCenter"]))
    story.append(PageBreak())


# =====================================================================
# PAGES LIMINAIRES
# =====================================================================
def dedicace(story):
    STATE.chapter_title = "Dedicace"
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Dedicace", ST["LiminaireTitle"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(
        "C'est avec profonde gratitude et sinceres mots, que nous dedions ce "
        "modeste travail de fin de module a nos chers <b>parents</b>, qui ont "
        "sacrifie leur vie pour notre reussite et nous ont eclaire le chemin "
        "par leurs conseils judicieux.",
        ST["LiminaireBody"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Nous esperons qu'un jour, nous serons leur source de fierte et de "
        "bonheur, et que Dieu leur prete une longue et heureuse vie.",
        ST["LiminaireBody"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Nous dedions egalement ce travail a nos <b>freres et soeurs</b>, "
        "a nos <b>familles</b>, a nos <b>amis</b>, et a tous nos "
        "<b>chers professeurs</b> qui nous ont accompagnes tout au long de "
        "notre parcours.",
        ST["LiminaireBody"]))
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("<i>Akram &amp; Nouhaila</i>",
                           ParagraphStyle("sig", parent=ST["LiminaireBody"],
                                          alignment=TA_RIGHT, fontSize=13)))
    story.append(PageBreak())


def remerciements(story):
    STATE.chapter_title = "Remerciements"
    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("Remerciements", ST["LiminaireTitle"]))
    story.append(Paragraph(
        "Au terme de ce projet, il nous est tres agreable d'exprimer nos "
        "sinceres remerciements a toutes les personnes qui ont contribue, "
        "de pres ou de loin, a la realisation de ce travail.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "Nous tenons en premier lieu a remercier <b>Allah</b> le tout puissant "
        "de nous avoir donne la sante, la volonte et le courage d'entamer et "
        "de terminer ce projet.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "Nous adressons nos plus vifs remerciements a notre encadrant pedagogique, "
        "<b>Pr. ZAHOUR Omar</b>, pour la qualite de son enseignement, sa "
        "disponibilite permanente, ses conseils avises et la rigueur "
        "scientifique qu'il a su nous transmettre tout au long de ce module. "
        "Ses orientations ont ete determinantes dans la definition du perimetre "
        "du projet et dans les choix techniques que nous avons operes.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "Nous remercions egalement l'ensemble du <b>corps professoral</b> du "
        "Departement de Mathematiques et Informatique de la Faculte des "
        "Sciences Ben M'Sik - Universite Hassan II de Casablanca, dont les "
        "enseignements anterieurs en programmation orientee objet, en bases "
        "de donnees, en genie logiciel et en architectures web ont constitue "
        "les fondations sur lesquelles ce travail a pu s'elever.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "Nos remerciements vont enfin a nos <b>familles</b> et a nos "
        "<b>camarades de promotion DEV-INFO S6</b>, pour leur soutien "
        "constant, leurs relectures attentives et l'emulation intellectuelle "
        "qui nous a tires vers le haut.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "Nous adressons enfin nos remerciements anticipes aux <b>membres du "
        "jury</b> qui nous font l'honneur d'evaluer ce travail.",
        ST["LiminaireBody"]))
    story.append(PageBreak())


def resume(story):
    STATE.chapter_title = "Resume"
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("Resume", ST["LiminaireTitle"]))
    story.append(Paragraph(
        "Ce memoire presente la conception et la realisation de <b>E-Store</b>, "
        "une application e-commerce complete developpee dans le cadre du "
        "module <i>Full-Stack</i> de la filiere DEV-INFO Semestre 6 a la "
        "Faculte des Sciences Ben M'Sik. Le projet adopte une architecture "
        "rigoureuse en trois couches techniques (presentation, logique metier, "
        "acces aux donnees) et un decoupage en cinq domaines fonctionnels "
        "suivant les principes du Domain-Driven Design.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "L'application implemente l'ensemble du parcours utilisateur d'un "
        "site marchand : inscription, authentification, navigation dans un "
        "catalogue, gestion d'un panier, validation transactionnelle de "
        "commandes et depot d'avis produits. La particularite technique "
        "majeure reside dans la mise en oeuvre d'une <b>persistance hybride</b> "
        "associant un systeme relationnel (MySQL ou H2) pour les donnees "
        "transactionnelles a un systeme documentaire (MongoDB) pour les avis "
        "utilisateurs.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "Le backend repose sur Spring Boot 3.3 et Spring Security 6 avec une "
        "authentification stateless par jeton JWT. Le frontend exploite les "
        "nouveautes d'Angular 17 (composants standalone, signals, lazy loading) "
        "et le framework Bootstrap 5. Une suite de neuf tests unitaires "
        "JUnit 5 / Mockito couvre les services metier critiques.",
        ST["LiminaireBody"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "<b>Mots-cles :</b> Spring Boot, Angular, JWT, MongoDB, Architecture "
        "en couches, Domain-Driven Design, Persistance hybride, ACID, REST, BCrypt.",
        ST["LiminaireBody"]))
    story.append(PageBreak())


def abstract(story):
    STATE.chapter_title = "Abstract"
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("Abstract", ST["LiminaireTitle"]))
    story.append(Paragraph(
        "This dissertation presents the design and implementation of "
        "<b>E-Store</b>, a complete e-commerce application developed as part "
        "of the Full-Stack module of the DEV-INFO S6 program at the Faculty "
        "of Sciences Ben M'Sik. The project follows a rigorous three-layer "
        "architecture (presentation, business logic, data access) combined "
        "with a five-domain decomposition inspired by Domain-Driven Design.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "The application covers the entire customer journey of a merchant "
        "website: registration, authentication, catalog navigation, cart "
        "management, transactional order validation and product review "
        "submission. The main technical originality lies in the use of a "
        "<b>hybrid persistence</b> model combining a relational database "
        "(MySQL or H2 in-memory) for transactional data with a document "
        "database (MongoDB) for user reviews.",
        ST["LiminaireBody"]))
    story.append(Paragraph(
        "The backend is built on Spring Boot 3.3 and Spring Security 6 with "
        "stateless authentication via JWT tokens. The frontend leverages the "
        "latest features of Angular 17 (standalone components, signals, lazy "
        "loading) combined with Bootstrap 5. A suite of nine unit tests "
        "(JUnit 5 / Mockito) ensures the reliability of the core business "
        "services.",
        ST["LiminaireBody"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        "<b>Keywords:</b> Spring Boot, Angular, JWT, MongoDB, Layered "
        "architecture, Domain-Driven Design, Hybrid persistence, ACID, REST, BCrypt.",
        ST["LiminaireBody"]))
    story.append(PageBreak())


def table_des_matieres(story):
    """Sommaire detaille manuel."""
    STATE.chapter_title = "Sommaire"
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph("Sommaire", ST["LiminaireTitle"]))

    entries = [
        ("Introduction generale", "1", False, 0),
        ("Chapitre 1 : Contexte et cahier des charges", "3", True, 0),
        ("1.1. Contexte academique", "3", False, 1),
        ("1.2. Etude du marche de l'e-commerce au Maroc", "4", False, 1),
        ("1.3. Cahier des charges fonctionnel", "5", False, 1),
        ("1.4. Cahier des charges non fonctionnel", "6", False, 1),
        ("1.5. Methodologie de travail", "7", False, 1),
        ("Chapitre 2 : Architecture et conception", "8", True, 0),
        ("2.1. Architecture en trois couches", "8", False, 1),
        ("2.2. Decoupage en domaines fonctionnels", "9", False, 1),
        ("2.3. Modele conceptuel de donnees", "10", False, 1),
        ("2.4. Modele documentaire MongoDB", "11", False, 1),
        ("2.5. Architecture de l'API REST", "12", False, 1),
        ("Chapitre 3 : Choix techniques", "13", True, 0),
        ("3.1. Backend : Java et Spring Boot", "13", False, 1),
        ("3.2. Persistance hybride MySQL + MongoDB", "14", False, 1),
        ("3.3. Frontend : Angular 17 standalone", "15", False, 1),
        ("Chapitre 4 : Realisation du backend", "16", True, 0),
        ("4.1. Structure du projet", "16", False, 1),
        ("4.2. Domaine customer (User, Profile, JWT)", "17", False, 1),
        ("4.3. Domaine catalog", "18", False, 1),
        ("4.4. Domaine inventory", "19", False, 1),
        ("4.5. Domaines shopping et billing", "19", False, 1),
        ("4.6. Domaine review (MongoDB)", "21", False, 1),
        ("4.7. Gestion globale des erreurs", "22", False, 1),
        ("Chapitre 5 : Securite", "23", True, 0),
        ("5.1. Hachage BCrypt des mots de passe", "23", False, 1),
        ("5.2. Authentification stateless par JWT", "23", False, 1),
        ("5.3. Autorisation par role", "25", False, 1),
        ("5.4. Configuration CORS", "25", False, 1),
        ("Chapitre 6 : Realisation du frontend", "26", True, 0),
        ("6.1. Structure de l'application Angular", "26", False, 1),
        ("6.2. Bootstrap de l'application", "27", False, 1),
        ("6.3. Routing et lazy loading", "27", False, 1),
        ("6.4. AuthInterceptor et ErrorInterceptor", "28", False, 1),
        ("6.5. AuthGuard et composants", "29", False, 1),
        ("Chapitre 7 : Tests et deploiement", "30", True, 0),
        ("7.1. Strategie de tests", "30", False, 1),
        ("7.2. Resultats d'execution", "31", False, 1),
        ("7.3. Conteneurisation Docker", "32", False, 1),
        ("Chapitre 8 : Difficultes et resultats", "33", True, 0),
        ("8.1. Difficultes rencontrees", "33", False, 1),
        ("8.2. Bilan fonctionnel et metriques", "35", False, 1),
        ("Conclusion generale et perspectives", "36", False, 0),
        ("Bibliographie", "38", False, 0),
        ("Annexes", "39", False, 0),
    ]

    rows = []
    for title, page, bold, level in entries:
        indent = "&nbsp;" * (4 * level)
        if bold:
            t = f"<b>{indent}{title}</b>"
            pg = f"<b>{page}</b>"
        else:
            t = f"{indent}{title}"
            pg = page
        style = ParagraphStyle("e", parent=ST["BodyNoIndent"],
                               fontSize=11, leading=15, spaceAfter=2)
        rows.append([Paragraph(t, style), Paragraph(pg, style)])

    tbl = Table(rows, colWidths=[14 * cm, 2 * cm])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(tbl)
    story.append(PageBreak())


def table_des_figures(story):
    """Liste des figures."""
    STATE.chapter_title = "Table des figures"
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("Table des figures", ST["LiminaireTitle"]))

    figs = [
        ("Figure 1 : Architecture en trois couches de l'application E-Store", "8"),
        ("Figure 2 : Les six domaines fonctionnels", "9"),
        ("Figure 3 : Modele conceptuel de donnees relationnel", "10"),
        ("Figure 4 : Structure d'un document Review (MongoDB)", "11"),
        ("Figure 5 : Cycle de vie d'un JWT", "24"),
        ("Figure 6 : Resultats d'execution des tests JUnit", "31"),
        ("Figure 7 : Organisation Docker Compose", "32"),
    ]
    tbls = [
        ("Tableau 1 : Cas d'usage fonctionnels couverts par E-Store", "5"),
        ("Tableau 2 : Matrice architecturale (couches x domaines)", "9"),
        ("Tableau 3 : Endpoints REST principaux", "12"),
        ("Tableau 4 : Comparaison MySQL vs MongoDB", "14"),
        ("Tableau 5 : Suite de tests unitaires", "30"),
        ("Tableau 6 : Metriques quantitatives du projet", "35"),
    ]

    for title, page in figs:
        style = ParagraphStyle("e", parent=ST["BodyNoIndent"],
                               fontSize=11, leading=15, spaceAfter=2)
        tbl = Table([[Paragraph(title, style), Paragraph(page, style)]],
                    colWidths=[14 * cm, 2 * cm])
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(tbl)

    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph("Liste des tableaux", ST["H1"]))
    story.append(Spacer(1, 0.3 * cm))
    for title, page in tbls:
        style = ParagraphStyle("e", parent=ST["BodyNoIndent"],
                               fontSize=11, leading=15, spaceAfter=2)
        tbl = Table([[Paragraph(title, style), Paragraph(page, style)]],
                    colWidths=[14 * cm, 2 * cm])
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        story.append(tbl)
    story.append(PageBreak())


def liste_abrev(story):
    """Liste des abreviations."""
    STATE.chapter_title = "Abreviations"
    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph("Liste des abreviations", ST["LiminaireTitle"]))

    rows = [
        ["ACID", "Atomicity, Consistency, Isolation, Durability"],
        ["API", "Application Programming Interface"],
        ["BCrypt", "Blowfish Crypt (algorithme de hachage)"],
        ["CRUD", "Create, Read, Update, Delete"],
        ["CORS", "Cross-Origin Resource Sharing"],
        ["DDD", "Domain-Driven Design"],
        ["DEV-INFO", "Developpement Informatique (filiere)"],
        ["DTO", "Data Transfer Object"],
        ["FSBM", "Faculte des Sciences Ben M'Sik"],
        ["H2", "Base de donnees relationnelle in-memory en Java"],
        ["HTTP", "HyperText Transfer Protocol"],
        ["IDE", "Integrated Development Environment"],
        ["JPA", "Jakarta Persistence API"],
        ["JSON", "JavaScript Object Notation"],
        ["JWT", "JSON Web Token"],
        ["MCD", "Modele Conceptuel de Donnees"],
        ["NoSQL", "Not Only SQL"],
        ["REST", "Representational State Transfer"],
        ["S6", "Semestre 6"],
        ["SGBD", "Systeme de Gestion de Bases de Donnees"],
        ["SPA", "Single Page Application"],
        ["UI/UX", "User Interface / User eXperience"],
    ]

    tbl = Table(rows, colWidths=[3 * cm, 13 * cm])
    tbl.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("TEXTCOLOR", (0, 0), (0, -1), PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
    ]))
    story.append(tbl)
    story.append(PageBreak())


# =====================================================================
# INTRODUCTION GENERALE
# =====================================================================
def introduction(story):
    STATE.pre_intro = False
    STATE.page_number = 1
    STATE.chapter_title = "Introduction generale"
    story.extend(chap_header("INTRO", "Introduction generale"))

    story.append(p(
        "L'avenement du commerce electronique a profondement remodele les "
        "pratiques commerciales mondiales. Selon les estimations de la "
        "Confederation Marocaine du Commerce Electronique, le volume des "
        "transactions en ligne au Maroc a franchi le cap des "
        "<b>20 milliards de dirhams</b> en 2024, avec une croissance annuelle "
        "moyenne superieure a 25%. Cette dynamique s'accompagne d'une exigence "
        "accrue en termes d'ergonomie, de performance et de securite des "
        "plateformes marchandes."))

    story.append(p(
        "Le module <b>Full-Stack</b> du <b>Semestre 6 de la filiere DEV-INFO</b>, "
        "dispense sous la direction du Pr. Omar Zahour, vise a doter les "
        "etudiants des competences necessaires a la conception et a la "
        "realisation de telles applications de bout en bout - du modele de "
        "donnees jusqu'a l'interface utilisateur, en passant par la logique "
        "metier, la securite et le deploiement."))

    story.append(p(
        "C'est dans ce contexte que s'inscrit le present projet, baptise "
        "<b>E-Store</b>. Il s'agit d'une mise en pratique exhaustive des "
        "enseignements theoriques par la construction d'une application "
        "e-commerce complete, integrant les meilleurs standards de "
        "l'industrie en 2026 : Spring Boot 3.3, Angular 17, persistance "
        "hybride relationnel/documentaire, authentification JWT, tests "
        "unitaires automatises et conteneurisation Docker."))

    story.append(section("1", "Objectifs du projet"))
    story.append(p("Ce projet poursuit cinq objectifs principaux :"))
    for b in [
        "<b>Maitriser une architecture full-stack moderne</b> en appliquant "
        "un decoupage en couches et en domaines fonctionnels rigoureux.",
        "<b>Illustrer la persistance hybride</b> en faisant cohabiter, au "
        "sein d'une meme application, un SGBD relationnel (MySQL) et un "
        "SGBD documentaire (MongoDB).",
        "<b>Appliquer les bonnes pratiques</b> de genie logiciel : DTOs, "
        "transactions, validation, gestion centralisee des erreurs, tests unitaires.",
        "<b>Securiser l'application</b> par un mecanisme stateless reposant "
        "sur Spring Security 6, BCrypt et JWT.",
        "<b>Produire une interface utilisateur reactive</b> avec Angular 17 "
        "en mode standalone, Bootstrap 5 et signals.",
    ]:
        story.append(bullet(b))

    story.append(section("2", "Plan du memoire"))
    story.append(p("Le present memoire s'articule autour de <b>huit chapitres</b> :"))
    for b in [
        "Le <b>chapitre 1</b> pose le contexte du projet et formalise le "
        "cahier des charges fonctionnel et non fonctionnel.",
        "Le <b>chapitre 2</b> decrit l'architecture generale, le decoupage "
        "en couches et en domaines, ainsi que la modelisation des donnees.",
        "Le <b>chapitre 3</b> justifie les choix techniques operes pour "
        "chaque brique de la stack.",
        "Les <b>chapitres 4 et 5</b> detaillent respectivement la realisation "
        "du backend et le module de securite.",
        "Le <b>chapitre 6</b> presente la realisation du frontend Angular.",
        "Le <b>chapitre 7</b> expose la strategie de tests et le deploiement Docker.",
        "Le <b>chapitre 8</b> relate les difficultes rencontrees et dresse "
        "le bilan quantitatif du travail.",
        "Une <b>conclusion generale</b> trace les perspectives d'evolution.",
    ]:
        story.append(bullet(b))

    story.append(PageBreak())


# =====================================================================
# CHAPITRE 1
# =====================================================================
def chap1(story):
    STATE.chapter_title = "Chapitre 1 - Contexte"
    story.extend(chap_header(1, "Contexte et cahier des charges"))

    story.append(section("1.1", "Contexte academique"))
    story.append(p(
        "Ce projet est realise dans le cadre du module Full-Stack du "
        "<b>Semestre 6 de la Licence Sciences Mathematiques et Informatique - "
        "option Developpement Informatique (DEV-INFO)</b>, dispense au "
        "Departement de Mathematiques et Informatique de la Faculte des "
        "Sciences Ben M'Sik. Ce module intervient en fin de cursus de "
        "licence, apres que les etudiants ont acquis les bases en "
        "programmation orientee objet, bases de donnees relationnelles, "
        "developpement web cote client et genie logiciel."))

    story.append(p("L'objectif pedagogique est triple :"))
    for b in [
        "<b>Integrer</b> les acquis des modules precedents au sein d'un "
        "projet de taille significative.",
        "<b>Decouvrir</b> les frameworks de production utilises dans "
        "l'industrie (Spring Boot, Angular).",
        "<b>Pratiquer</b> le travail en binome sur un depot Git partage, "
        "en respectant des conventions de nommage et de commit.",
    ]:
        story.append(bullet(b))

    story.append(section("1.2", "Etude du marche de l'e-commerce au Maroc"))
    story.append(p(
        "Le commerce electronique marocain connait une expansion soutenue. "
        "Les plateformes leaders du marche - Jumia, Avito, Marjane.ma, "
        "Decathlon.ma - partagent un ensemble de fonctionnalites-types "
        "qui constituent l'<i>etat de l'art</i> : authentification "
        "utilisateur, navigation dans un catalogue categorise, recherche "
        "textuelle et par filtres, gestion d'un panier persistant, processus "
        "de commande securise, suivi d'historique, depot et consultation "
        "d'avis clients, gestion de favoris."))

    story.append(subsection("1.2.1", "Analyse comparative"))
    story.append(p(
        "Le tableau ci-dessous resume une analyse comparative succincte des "
        "principales plateformes existantes au Maroc."))

    rows = [
        ["Critere", "Forces communes", "Faiblesses recurrentes"],
        ["Catalogue", "Richesse, pagination",
         "Filtres parfois lents, peu pertinents"],
        ["Panier", "Persistance, modification quantite",
         "Synchronisation multi-appareils inegale"],
        ["Securite", "HTTPS, JWT/OAuth",
         "Mots de passe faibles autorises"],
        ["Performance", "CDN, cache",
         "Surcharge en periode de soldes"],
        ["Avis", "Notation par etoiles",
         "Moderation absente ou tardive"],
    ]
    tbl = Table(rows, colWidths=[3.5 * cm, 6 * cm, 6.5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
    ]))
    story.append(tbl)
    story.append(tcaption("Analyse comparative succincte des plateformes existantes", 1))

    story.append(p(
        "<b>E-Store</b> ne pretend evidemment pas rivaliser avec ces geants, "
        "mais propose une maquette pedagogique fonctionnelle qui en reprend "
        "les fondamentaux dans un perimetre maitrisable."))

    story.append(section("1.3", "Cahier des charges fonctionnel"))
    story.append(subsection("1.3.1", "Acteurs du systeme"))
    story.append(p("L'application distingue deux profils d'utilisateurs :"))
    for b in [
        "<b>USER</b> (utilisateur standard) : peut s'inscrire, se connecter, "
        "consulter le catalogue, ajouter au panier, passer commande, "
        "consulter son historique et deposer des avis.",
        "<b>ADMIN</b> (administrateur) : dispose, en plus, des droits de "
        "creation, modification et suppression sur les categories, les "
        "produits et le stock.",
    ]:
        story.append(bullet(b))

    story.append(subsection("1.3.2", "Cas d'usage principaux"))
    story.append(p("Le tableau suivant recapitule les cas d'usage couverts :"))
    rows = [
        ["Cas d'usage", "Acteur", "Description"],
        ["Inscription", "Visiteur",
         "Email unique + mot de passe (≥ 6 caracteres)"],
        ["Connexion", "Utilisateur", "Authentification, retour d'un JWT 24h"],
        ["Profil", "USER", "Consultation et mise a jour du profil"],
        ["Catalogue", "Tous", "Liste paginee, recherche, filtre categorie"],
        ["Fiche produit", "Tous", "Detail, prix, stock, avis"],
        ["Panier", "USER", "Ajout, modification, suppression, vidage"],
        ["Commande", "USER", "Validation transactionnelle (ACID)"],
        ["Avis", "USER", "Depot (1-5 etoiles + commentaire)"],
        ["Categorie/Produit", "ADMIN", "CRUD complet"],
        ["Stock", "ADMIN", "Lecture publique, mise a jour reservee"],
    ]
    tbl = Table(rows, colWidths=[4 * cm, 2.5 * cm, 9.5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BG_LIGHT]),
    ]))
    story.append(tbl)
    story.append(tcaption("Cas d'usage fonctionnels couverts par E-Store", 2))

    story.append(section("1.4", "Cahier des charges non fonctionnel"))
    story.append(subsection("1.4.1", "Performance"))
    story.append(p(
        "Les pages doivent se charger en moins de <b>2 secondes</b> sur "
        "connexion nominale (4G ou Wi-Fi). Le bundle initial JavaScript doit "
        "rester sous <b>50 ko</b> grace au lazy loading."))

    story.append(subsection("1.4.2", "Securite"))
    for b in [
        "Mots de passe haches en <b>BCrypt</b> (jamais en clair).",
        "Authentification stateless par <b>JWT signe HMAC-SHA256</b>, "
        "expiration 24 heures.",
        "Endpoints d'administration proteges par <code>@PreAuthorize</code>.",
        "Validation systematique des entrees (Bean Validation).",
        "CORS restreint a l'origine localhost:4200 en developpement.",
    ]:
        story.append(bullet(b))

    story.append(subsection("1.4.3", "Maintenabilite"))
    for b in [
        "Code conforme aux conventions Java/TypeScript.",
        "Decoupage en cinq domaines fonctionnels autonomes.",
        "Au moins <b>neuf tests unitaires</b> couvrant les services critiques.",
        "Documentation interne (Javadoc, README, commentaires).",
    ]:
        story.append(bullet(b))

    story.append(subsection("1.4.4", "Portabilite"))
    for b in [
        "Demarrage possible <b>sans installation prealable</b> grace au "
        "profil <code>dev</code> (H2 in-memory).",
        "Demarrage Docker en une commande pour le profil <code>prod</code>.",
        "Compatibilite multi-OS (Windows, macOS, Linux).",
    ]:
        story.append(bullet(b))

    story.append(section("1.5", "Methodologie de travail"))
    story.append(p(
        "Nous avons retenu une approche <b>iterative legere</b>, inspiree "
        "d'Agile mais adaptee au contexte d'un binome etudiant. Le projet "
        "a ete decoupe en quinze etapes incrementales, chacune se concluant "
        "par un commit Git significatif. La repartition des roles a ete :"))
    for b in [
        "<b>Akram Belmoussa</b> : Backend (Spring Boot, JPA, securite JWT), "
        "integration MongoDB, tests unitaires.",
        "<b>Nouhaila Ben Soumane</b> : Frontend (Angular 17, Bootstrap), "
        "modelisation des donnees, documentation et redaction du rapport.",
        "<b>Travail commun</b> : architecture, design de l'API, debogage, "
        "revue de code, integration finale.",
    ]:
        story.append(bullet(b))

    story.append(PageBreak())


# =====================================================================
# CHAPITRE 2
# =====================================================================
def chap2(story):
    STATE.chapter_title = "Chapitre 2 - Architecture"
    story.extend(chap_header(2, "Architecture et conception"))

    story.append(section("2.1", "Architecture generale en trois couches"))
    story.append(p(
        "E-Store adopte une architecture n-tiers classique en trois couches, "
        "qui presente l'avantage de separer clairement les responsabilites "
        "et de faciliter la maintenance. La figure 1 en donne une vue "
        "synthetique."))

    # Diagramme 3 couches (table)
    layers = Table([
        ["COUCHE PRESENTATION",
         "Angular 17 standalone - Bootstrap 5 - TypeScript - RxJS / Signals"],
        ["COUCHE LOGIQUE METIER",
         "Spring Boot 3.3 - Controllers REST - Services - DTOs - Spring Security 6"],
        ["COUCHE ACCES AUX DONNEES",
         "Spring Data JPA - Spring Data MongoDB - MySQL 8 / H2 - MongoDB 7"],
    ], colWidths=[5.5 * cm, 10.5 * cm])
    layers.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), PRIMARY),
        ("TEXTCOLOR", (0, 0), (0, -1), white),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Times-Italic"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("GRID", (0, 0), (-1, -1), 0.4, GREY_LIGHT),
    ]))
    story.append(layers)
    story.append(caption("Architecture en trois couches de l'application E-Store", 1))

    story.append(subsection("2.1.1", "Couche presentation (frontend)"))
    story.append(p(
        "Cette couche est en charge de l'interaction avec l'utilisateur "
        "final. Elle n'a aucune connaissance du modele de persistance et "
        "communique avec le backend exclusivement via une <b>API REST/JSON</b>."))

    story.append(subsection("2.1.2", "Couche logique metier (backend)"))
    story.append(p(
        "C'est le coeur applicatif. Elle recoit les requetes HTTP, valide "
        "les entrees, applique les regles de gestion (verification de stock, "
        "calcul de totaux, generation de jetons), orchestre les transactions "
        "et renvoie des DTOs serialises en JSON."))

    story.append(subsection("2.1.3", "Couche d'acces aux donnees"))
    story.append(p(
        "Cette couche, masquee derriere les abstractions Spring Data, gere "
        "la persistance effective. Deux SGBD coexistent : <b>MySQL 8</b> "
        "(ou H2 en mode dev) pour les donnees strictement relationnelles "
        "(utilisateurs, produits, panier, commandes), et <b>MongoDB 7</b> "
        "pour les avis, donnees semi-structurees en forte croissance."))

    story.append(section("2.2", "Decoupage en domaines fonctionnels"))
    story.append(p(
        "Chaque couche est elle-meme decoupee en <b>cinq domaines "
        "fonctionnels</b> cohesifs, suivant les principes du Domain-Driven "
        "Design. Un sixieme domaine, <code>review</code>, gere la "
        "particularite MongoDB."))

    # 6 domaines en grille 2x3
    domains = Table([
        [Paragraph("<b>customer</b><br/><font size='9'>User, Profile, JWT, Auth</font>",
                   ST["BodyNoIndent"]),
         Paragraph("<b>catalog</b><br/><font size='9'>Category, Product, recherche</font>",
                   ST["BodyNoIndent"]),
         Paragraph("<b>inventory</b><br/><font size='9'>Stock par produit</font>",
                   ST["BodyNoIndent"])],
        [Paragraph("<b>shopping</b><br/><font size='9'>Cart, CartItem</font>",
                   ST["BodyNoIndent"]),
         Paragraph("<b>billing</b><br/><font size='9'>Order, OrderItem<br/>@Transactional</font>",
                   ST["BodyNoIndent"]),
         Paragraph("<b>review</b><br/><font size='9'>Avis (MongoDB)</font>",
                   ST["BodyNoIndent"])],
    ], colWidths=[5.3 * cm, 5.3 * cm, 5.3 * cm], rowHeights=[1.6*cm, 1.6*cm])
    domains.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(domains)
    story.append(caption("Les six domaines fonctionnels de l'application", 2))

    story.append(p(
        "Cette double organisation <i>couches x domaines</i> produit la "
        "matrice suivante qui donne une vue exhaustive du projet :"))

    rows = [
        ["Domaine", "Presentation", "Logique metier", "Donnees"],
        ["customer", "login.component.ts", "AuthService, JwtFilter",
         "users, profiles (JPA)"],
        ["catalog", "product-list", "ProductService, recherche",
         "products, categories"],
        ["inventory", "Indicateur UI", "InventoryService", "inventories"],
        ["shopping", "cart.component", "CartService", "carts, cart_items"],
        ["billing", "orders.component", "OrderService @Transactional",
         "orders, order_items"],
        ["review", "review-form", "ReviewService", "MongoDB reviews"],
    ]
    tbl = Table(rows, colWidths=[2.6 * cm, 3.8 * cm, 5 * cm, 4.6 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BG_LIGHT]),
    ]))
    story.append(tbl)
    story.append(tcaption("Matrice architecturale : 3 couches x 6 domaines", 2))

    story.append(section("2.3", "Modele conceptuel des donnees relationnel"))
    story.append(p(
        "Le modele relationnel comporte <b>neuf entites</b> reliees par des "
        "associations <i>one-to-one</i>, <i>one-to-many</i> et "
        "<i>many-to-one</i>. Les principales entites sont :"))
    for b in [
        "<b>User</b> : id, firstName, lastName, email (unique), password (BCrypt), role",
        "<b>Profile</b> : id, phone, address, city, country (one-to-one User)",
        "<b>Category</b> : id, name, description (one-to-many Product)",
        "<b>Product</b> : id, name, description, price, imageUrl (many-to-one Category)",
        "<b>Inventory</b> : id, quantity (one-to-one Product)",
        "<b>Cart</b> : id, createdAt, updatedAt (one-to-one User)",
        "<b>CartItem</b> : id, quantity, unitPrice (many-to-one Cart, Product)",
        "<b>Order</b> : id, orderDate, totalAmount, status (many-to-one User)",
        "<b>OrderItem</b> : id, quantity, unitPrice (many-to-one Order, Product)",
    ]:
        story.append(bullet(b))

    story.append(p(
        "Les contraintes sont strictement respectees : email unique, prix "
        "en <code>BigDecimal</code> (jamais en double), cle etrangere "
        "<code>NOT NULL</code> sur les associations many-to-one obligatoires, "
        "cascade <code>ALL</code> avec <code>orphanRemoval</code> sur les "
        "collections de l'agregat."))

    story.append(section("2.4", "Modele documentaire MongoDB"))
    story.append(p(
        "La collection <code>reviews</code> stocke les avis utilisateurs "
        "sous forme de documents JSON :"))
    story.append(code("""{
  "_id":         ObjectId("..."),
  "productId":   12,
  "userId":      5,
  "authorName":  "Akram Belmoussa",
  "rating":      5,
  "comment":     "Excellent produit !",
  "createdAt":   ISODate("2026-04-22T14:30:00Z")
}"""))
    story.append(caption("Structure d'un document de la collection reviews", 4))

    story.append(p(
        "Deux index secondaires sont crees via les annotations "
        "<code>@Indexed</code> sur les champs <code>productId</code> et "
        "<code>userId</code>, afin d'accelerer les requetes "
        "<code>findByProductId</code> et <code>findByUserId</code>."))

    story.append(section("2.5", "Architecture de l'API REST"))
    story.append(p(
        "Toute communication frontend/backend transite par une API REST "
        "respectant les standards : methodes HTTP appropriees (GET / POST / "
        "PUT / DELETE), codes de retour normalises (200, 201, 204, 400, 401, "
        "403, 404, 409), corps JSON encadre par une enveloppe "
        "<code>ApiResponse</code> standardisee, et versioning implicite par "
        "le prefixe <code>/api/</code>."))

    rows = [
        ["Verbe", "URL", "Description", "Auth."],
        ["POST", "/api/auth/register", "Inscription", "Public"],
        ["POST", "/api/auth/login", "Connexion (retourne JWT)", "Public"],
        ["GET", "/api/products", "Catalogue + filtres", "Public"],
        ["GET", "/api/products/{id}", "Fiche produit", "Public"],
        ["POST", "/api/products", "Creation produit", "ADMIN"],
        ["GET", "/api/categories", "Liste categories", "Public"],
        ["GET", "/api/cart", "Panier courant", "USER"],
        ["POST", "/api/cart/add", "Ajout au panier", "USER"],
        ["POST", "/api/orders", "Validation commande", "USER"],
        ["GET", "/api/orders", "Historique", "USER"],
        ["POST", "/api/reviews", "Depot d'avis", "USER"],
        ["GET", "/api/reviews/product/{id}", "Avis d'un produit", "Public"],
    ]
    tbl = Table(rows, colWidths=[1.5 * cm, 5.5 * cm, 6.5 * cm, 2.5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (1, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (3, 1), (3, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BG_LIGHT]),
    ]))
    story.append(tbl)
    story.append(tcaption("Endpoints REST principaux", 3))
    story.append(PageBreak())


# =====================================================================
# CHAPITRE 3
# =====================================================================
def chap3(story):
    STATE.chapter_title = "Chapitre 3 - Choix techniques"
    story.extend(chap_header(3, "Choix techniques et justifications"))

    story.append(section("3.1", "Backend : Java et Spring Boot"))
    story.append(subsection("3.1.1", "Pourquoi Java ?"))
    story.append(p(
        "Java demeure, en 2026, l'un des langages les plus largement deployes "
        "en entreprise - notamment dans le secteur bancaire, les "
        "telecommunications et le e-commerce de grande echelle. Ses atouts "
        "pedagogiques sont multiples : typage fort, programmation orientee "
        "objet stricte, ecosysteme mature, machine virtuelle performante. "
        "La version <b>Java 17 LTS</b> (Long-Term Support) a ete retenue "
        "pour sa stabilite et son adoption massive."))

    story.append(subsection("3.1.2", "Pourquoi Spring Boot ?"))
    story.append(p(
        "Spring Boot est le framework Java de reference pour la construction "
        "d'applications backend modernes. Il automatise la configuration et "
        "fournit une myriade de <i>starters</i> prets a l'emploi. Ses "
        "points forts sont :"))
    for b in [
        "<b>Auto-configuration</b> par convention plutot que par configuration explicite.",
        "<b>Embedded Tomcat</b> : deploiement en JAR auto-executable.",
        "<b>Spring Data</b> : abstraction puissante des SGBD.",
        "<b>Spring Security 6</b> : securisation standardisee.",
        "<b>Actuator</b> : observabilite prete a l'emploi.",
    ]:
        story.append(bullet(b))
    story.append(p(
        "La <b>version 3.3</b> a ete choisie car compatible Jakarta EE 10 "
        "et Java 17+, et stable depuis fin 2024."))

    story.append(section("3.2", "Persistance hybride : MySQL + MongoDB"))
    story.append(p(
        "Le choix d'un <b>double systeme de persistance</b> n'est pas un "
        "caprice : il repond a une realite du terrain. Toutes les donnees "
        "ne sont pas egales :"))
    for b in [
        "Les <b>transactions financieres</b> (commandes, panier, stock) "
        "exigent les proprietes ACID : atomicite, coherence, isolation, "
        "durabilite. Le SQL relationnel y excelle.",
        "Les <b>avis utilisateurs</b> ne necessitent ni jointures complexes, "
        "ni transactions ; ils croissent rapidement et sont consultes "
        "massivement en lecture. Le NoSQL documentaire les sert plus efficacement.",
    ]:
        story.append(bullet(b))

    rows = [
        ["Critere", "MySQL 8 (relationnel)", "MongoDB 7 (documentaire)"],
        ["Paradigme", "SQL, tables normalisees", "BSON, documents JSON"],
        ["Schema", "Strict, predefini", "Flexible"],
        ["Transactions", "ACID natives", "Limitees (multi-doc v4+)"],
        ["Joins", "Performants", "Rares ($lookup)"],
        ["Lectures massives", "Bonnes (index)", "Excellentes (replicas)"],
        ["Cas d'usage E-Store", "Users, Products, Orders", "Reviews"],
    ]
    tbl = Table(rows, colWidths=[4 * cm, 6 * cm, 6 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BG_LIGHT]),
    ]))
    story.append(tbl)
    story.append(tcaption("Comparaison MySQL vs MongoDB dans le contexte E-Store", 4))

    story.append(subsection("3.2.1", "Bascule H2 / MySQL via les profils"))
    story.append(p(
        "Le projet exploite la fonctionnalite Spring de <b>profils</b> "
        "(<code>application-dev.properties</code>, "
        "<code>application-prod.properties</code>) pour basculer entre H2 "
        "in-memory (developpement) et MySQL persistant (production)."))
    story.append(code("""# Profil dev : H2 in-memory
spring.datasource.url=jdbc:h2:mem:estore;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect

# Profil prod : MySQL
spring.datasource.url=jdbc:mysql://localhost:3306/estore
spring.datasource.username=root
spring.datasource.password=root"""))

    story.append(section("3.3", "Frontend : Angular 17 standalone"))
    story.append(subsection("3.3.1", "Pourquoi Angular ?"))
    story.append(p(
        "Trois frameworks dominent le developpement web SPA en 2026 : "
        "<b>Angular</b>, <b>React</b> et <b>Vue</b>. Angular se distingue "
        "par son approche <i>tout-en-un</i> (router, formulaires, HTTP, "
        "i18n inclus) et son langage TypeScript natif, qui apporte la "
        "rigueur du typage statique au JavaScript. Pour un projet "
        "pedagogique de fin de module, Angular offre l'environnement le "
        "plus structurant."))

    story.append(subsection("3.3.2", "Le mode standalone et les Signals"))
    story.append(p(
        "Depuis la version 14, et de maniere generalisee depuis la version "
        "17, Angular permet de s'affranchir des <code>NgModule</code> "
        "historiques au profit de <b>composants standalone</b>. Les "
        "<b>signals</b>, nouveaute majeure d'Angular 17, remplacent "
        "avantageusement les <code>Observable</code> RxJS pour la gestion "
        "d'etat simple. Dans E-Store, ils servent par exemple a afficher "
        "dynamiquement le badge du panier dans la barre de navigation."))
    story.append(code("""@Injectable({ providedIn: 'root' })
export class CartService {
  readonly cart = signal<Cart | null>(null);
  readonly itemCount = signal<number>(0);

  add(productId: number, qty: number) {
    return this.http.post(...).pipe(tap(r => this.update(r.data)));
  }
}"""))
    story.append(PageBreak())


# =====================================================================
# CHAPITRE 4 : Realisation Backend
# =====================================================================
def chap4(story):
    STATE.chapter_title = "Chapitre 4 - Backend"
    story.extend(chap_header(4, "Realisation du backend"))

    story.append(section("4.1", "Structure generale du projet"))
    story.append(p(
        "L'arborescence <code>estore-backend/src/main/java/com/estore/</code> "
        "reflete fidelement le decoupage en domaines :"))
    story.append(code("""com.estore/
  EstoreApplication.java        <- Point d'entree
  customer/    {entity, dto, repository, service, controller, security}
  catalog/     {entity, dto, repository, service, controller}
  inventory/   {entity, dto, repository, service, controller}
  shopping/    {entity, dto, repository, service, controller}
  billing/     {entity, dto, repository, service, controller}
  review/      {document, dto, repository, service, controller}
  shared/      ApiResponse.java
  config/      CorsConfig, SecurityConfig, DataSeeder
  exception/   GlobalExceptionHandler + 3 exceptions metier"""))
    story.append(p(
        "Chaque domaine est <b>autonome</b> : il ne peut dependre que des "
        "couches inferieures de son propre domaine, ou des composants "
        "partages. Les domaines communiquent exclusivement via leurs "
        "services publics."))

    story.append(section("4.2", "Domaine customer (User, Profile, JWT)"))
    story.append(p(
        "Ce domaine pivote autour de l'entite <code>User</code>, a laquelle "
        "est associe un <code>Profile</code> en relation "
        "<code>@OneToOne</code>."))
    story.append(code("""@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @JsonIgnore
    @Column(nullable = false)
    private String password;          // hash BCrypt, jamais en clair

    @Enumerated(EnumType.STRING)
    private Role role;                 // USER ou ADMIN

    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL,
              orphanRemoval = true, fetch = FetchType.LAZY)
    private Profile profile;
}"""))
    story.append(p(
        "L'annotation <code>@JsonIgnore</code> sur <code>password</code> "
        "empeche toute serialisation accidentelle. La cascade ALL sur "
        "<code>profile</code> garantit l'atomicite creation/suppression."))

    story.append(subsection("4.2.1", "AuthService"))
    story.append(p(
        "L'<code>AuthService</code> centralise la logique d'inscription et "
        "de connexion. La connexion delegue a Spring Security via "
        "l'<code>AuthenticationManager</code>, puis genere un JWT."))
    story.append(code("""@Transactional
public AuthResponseDto register(RegisterDto dto) {
    if (userRepository.existsByEmail(dto.getEmail()))
        throw new BusinessException("Cet email est deja utilise");

    User user = User.builder()
        .firstName(dto.getFirstName()).lastName(dto.getLastName())
        .email(dto.getEmail())
        .password(passwordEncoder.encode(dto.getPassword()))  // BCrypt
        .role(Role.USER).build();

    user.setProfile(Profile.builder().user(user).build());
    User saved = userRepository.save(user);

    String token = jwtService.generateToken(saved);
    return AuthResponseDto.builder()
        .token(token).user(UserDto.from(saved)).build();
}"""))

    story.append(section("4.3", "Domaine catalog"))
    story.append(p(
        "Le catalogue regroupe <code>Category</code> et <code>Product</code>. "
        "Le repository <code>ProductRepository</code> expose une methode "
        "personnalisee combinant recherche textuelle et filtre par "
        "categorie :"))
    story.append(code(
        "public interface ProductRepository extends JpaRepository<Product, Long> {\n"
        "    @Query(\"\"\"\n"
        "        SELECT p FROM Product p\n"
        "        WHERE (:categoryId IS NULL OR p.category.id = :categoryId)\n"
        "          AND (:q IS NULL OR LOWER(p.name) LIKE LOWER(CONCAT('%',:q,'%'))\n"
        "                          OR LOWER(p.description) LIKE LOWER(CONCAT('%',:q,'%')))\n"
        "    \"\"\")\n"
        "    Page<Product> search(@Param(\"categoryId\") Long categoryId,\n"
        "                         @Param(\"q\") String q, Pageable pageable);\n"
        "}"))
    story.append(p(
        "L'utilisation de JPQL plutot que de SQL natif garantit la "
        "portabilite H2/MySQL, et la pagination via "
        "<code>Pageable</code> evite le retour massif d'enregistrements."))

    story.append(section("4.4", "Domaine inventory"))
    story.append(p(
        "L'entite <code>Inventory</code> est mappee 1-1 avec "
        "<code>Product</code>. Le service expose deux operations "
        "essentielles : <code>checkAvailability</code> (lecture sans "
        "modification) et <code>decrement</code> (verification + "
        "decrement). Cette separation garantit que la verification "
        "amont du checkout ne modifie pas le stock."))

    story.append(section("4.5", "Domaines shopping et billing"))
    story.append(subsection("4.5.1", "Le panier (shopping)"))
    story.append(p(
        "L'entite <code>Cart</code> maintient une relation "
        "<code>@OneToMany</code> avec <code>CartItem</code>. A l'ajout "
        "d'un produit deja present, la quantite est incrementee plutot "
        "que dupliquee."))

    story.append(subsection("4.5.2", "Le checkout transactionnel (billing)"))
    story.append(p(
        "La validation de commande constitue <b>l'operation la plus "
        "critique</b> de l'application. Elle touche trois agregats (Cart, "
        "Order, Inventory) et doit etre strictement atomique."))
    story.append(code("""@Transactional
public OrderDto checkout() {
    User user = securityUtils.currentUser();
    Cart cart = cartService.getOrCreateCart(user);
    if (cart.getItems().isEmpty())
        throw new BusinessException("Votre panier est vide");

    // 1) Verifier le stock pour TOUS les items AVANT toute modification
    for (CartItem ci : cart.getItems())
        inventoryService.checkAvailability(
            ci.getProduct().getId(), ci.getQuantity());

    // 2) Creer la commande + decrementer le stock
    Order order = Order.builder().user(user).status(PENDING).build();
    BigDecimal total = BigDecimal.ZERO;
    for (CartItem ci : cart.getItems()) {
        order.getItems().add(OrderItem.builder()...build());
        total = total.add(ci.getUnitPrice()
            .multiply(BigDecimal.valueOf(ci.getQuantity())));
        inventoryService.decrement(
            ci.getProduct().getId(), ci.getQuantity());
    }
    order.setStatus(CONFIRMED);

    // 3) Sauvegarder + vider le panier
    Order saved = orderRepository.save(order);
    cartService.clearCart(cart);
    return OrderDto.from(saved);
}"""))

    story.append(p(
        "<b>L'annotation @Transactional</b> garantit qu'en cas d'exception "
        "levee a n'importe quelle etape, toutes les modifications faites "
        "depuis l'entree dans la methode sont automatiquement annulees "
        "(<i>rollback</i>). C'est l'atomicite ACID en action."))

    story.append(section("4.6", "Domaine review (MongoDB)"))
    story.append(p(
        "Le document <code>Review</code> est mappe sur la collection "
        "MongoDB eponyme :"))
    story.append(code("""@Document(collection = "reviews")
public class Review {
    @Id private String id;
    @Indexed private Long productId;
    @Indexed private Long userId;
    private String authorName;
    private int rating;
    private String comment;
    private Instant createdAt;
}

public interface ReviewRepository extends MongoRepository<Review, String> {
    List<Review> findByProductIdOrderByCreatedAtDesc(Long productId);
    List<Review> findByUserIdOrderByCreatedAtDesc(Long userId);
}"""))
    story.append(p(
        "Le repository tire profit de la <i>convention over configuration</i> "
        "de Spring Data : la simple declaration d'une methode au nom "
        "evocateur produit la requete correspondante."))

    story.append(section("4.7", "Gestion globale des erreurs"))
    story.append(p(
        "Plutot que de laisser remonter des exceptions Java brutes vers le "
        "client, l'application centralise leur traitement via un "
        "<code>@RestControllerAdvice</code>. Chaque exception metier est "
        "convertie en reponse JSON propre avec le code HTTP approprie."))
    story.append(code("""@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse<Void>> handleNotFound(...) {
        return ResponseEntity.status(NOT_FOUND)
            .body(ApiResponse.error(ex.getMessage()));
    }

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResponse<Void>> handleBusiness(...) {
        return ResponseEntity.status(CONFLICT)
            .body(ApiResponse.error(ex.getMessage()));
    }
    // ... + ValidationException, BadCredentials, AccessDenied
}"""))
    story.append(PageBreak())


# =====================================================================
# CHAPITRE 5 : Securite
# =====================================================================
def chap5(story):
    STATE.chapter_title = "Chapitre 5 - Securite"
    story.extend(chap_header(5, "Securite de l'application"))

    story.append(p(
        "La securite de toute application e-commerce est une exigence "
        "absolue. E-Store met en oeuvre une chaine complete depuis le "
        "hachage des mots de passe jusqu'a l'autorisation fine par role."))

    story.append(section("5.1", "Hachage BCrypt des mots de passe"))
    story.append(p(
        "Aucun mot de passe utilisateur n'est jamais stocke en clair. Tous "
        "transitent par l'algorithme <b>BCrypt</b>, un <i>one-way hash</i> "
        "avec sel aleatoire et facteur de cout ajustable. Le facteur 10 "
        "(par defaut Spring) est utilise, soit 2^10 = 1024 rounds."))
    story.append(code("""@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}"""))

    story.append(section("5.2", "Authentification stateless par JWT"))
    story.append(p(
        "L'authentification suit un modele <i>stateless</i> : aucun etat "
        "n'est conserve cote serveur entre deux requetes. Le client porte "
        "lui-meme la preuve de son identite, sous la forme d'un JSON Web "
        "Token signe."))

    story.append(subsection("5.2.1", "Structure d'un JWT"))
    story.append(p(
        "Un JWT est compose de trois parties separees par un point : "
        "<code>header.payload.signature</code>. Le payload de E-Store "
        "contient les <i>claims</i> suivants :"))
    for b in [
        "<code>sub</code> : email de l'utilisateur (subject)",
        "<code>uid</code> : identifiant numerique",
        "<code>role</code> : USER ou ADMIN",
        "<code>name</code> : nom complet (pour affichage UI)",
        "<code>iat</code> et <code>exp</code> : timestamps de creation et d'expiration",
    ]:
        story.append(bullet(b))

    story.append(subsection("5.2.2", "Cycle de vie complet"))
    rows = [
        ["#", "Etape", "Composant"],
        ["1", "Client envoie email + password", "POST /api/auth/login"],
        ["2", "Validation BCrypt", "passwordEncoder.matches()"],
        ["3", "Generation du token (HS256, 24h)", "JwtService"],
        ["4", "Stockage cote client", "localStorage 'estore.token'"],
        ["5", "Toute requete : Bearer <token>", "AuthInterceptor"],
        ["6", "Validation a chaque appel", "JwtAuthenticationFilter"],
        ["7", "Population SecurityContext", "SecurityContextHolder"],
    ]
    tbl = Table(rows, colWidths=[1 * cm, 9 * cm, 6 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 1), (2, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BG_LIGHT]),
    ]))
    story.append(tbl)
    story.append(caption("Cycle de vie d'un JWT dans E-Store", 5))

    story.append(subsection("5.2.3", "Generation et validation du token"))
    story.append(code("""public String generateToken(User user) {
    Map<String, Object> claims = new HashMap<>();
    claims.put("uid",  user.getId());
    claims.put("role", user.getRole().name());
    claims.put("name", user.getFirstName() + " " + user.getLastName());

    Date now = new Date();
    Date exp = new Date(now.getTime() + expirationMs);  // 24h

    return Jwts.builder()
        .claims(claims).subject(user.getEmail())
        .issuedAt(now).expiration(exp)
        .signWith(key)                  // HMAC-SHA256
        .compact();
}"""))

    story.append(section("5.3", "Autorisation par role"))
    story.append(p(
        "Les operations sensibles (creation/modification/suppression de "
        "categories et de produits, mise a jour du stock) sont protegees "
        "par <code>@PreAuthorize</code> :"))
    story.append(code("""@PostMapping
@PreAuthorize("hasRole('ADMIN')")
public ResponseEntity<ApiResponse<ProductDto>> create(
        @Valid @RequestBody CreateProductDto dto) {
    return ResponseEntity.status(CREATED)
        .body(ApiResponse.ok("Produit cree", productService.create(dto)));
}"""))
    story.append(p(
        "Tout appel a cet endpoint par un utilisateur non-ADMIN se solde "
        "par un HTTP 403 Forbidden, intercepte par le "
        "<code>GlobalExceptionHandler</code>."))

    story.append(section("5.4", "Configuration CORS"))
    story.append(p(
        "En developpement, le frontend tourne sur le port 4200 et le "
        "backend sur le port 8080. Cette difference d'origine declencherait "
        "une erreur CORS du navigateur sans configuration appropriee."))
    story.append(code("""@Override
public void addCorsMappings(CorsRegistry registry) {
    registry.addMapping("/api/**")
        .allowedOrigins("http://localhost:4200")
        .allowedMethods("GET","POST","PUT","DELETE","OPTIONS")
        .allowedHeaders("*").allowCredentials(true);
}"""))
    story.append(PageBreak())


# =====================================================================
# CHAPITRE 6 : Frontend
# =====================================================================
def chap6(story):
    STATE.chapter_title = "Chapitre 6 - Frontend"
    story.extend(chap_header(6, "Realisation du frontend"))

    story.append(section("6.1", "Structure de l'application Angular"))
    story.append(p(
        "Le projet Angular suit l'organisation <b>core / shared / features</b>, "
        "classique des applications Angular modernes :"))
    story.append(code("""src/app/
  app.component.ts          <- Composant racine
  app.config.ts             <- Configuration globale (providers)
  app.routes.ts             <- Routes
  core/
    services/               <- AuthService, CartService, ...
    guards/                 <- AuthGuard
    interceptors/           <- AuthInterceptor, ErrorInterceptor
    models/                 <- Interfaces TypeScript
  shared/
    components/             <- Header, Footer, Loader, Toast
  features/
    auth/                   <- Login, Register
    catalog/                <- ProductList, ProductDetail
    cart/                   <- Cart
    orders/                 <- Orders
    profile/                <- Profile
    reviews/                <- ReviewForm"""))

    story.append(section("6.2", "Bootstrap de l'application"))
    story.append(p(
        "Le fichier <code>main.ts</code> amorce l'application sans "
        "<code>NgModule</code>, en passant directement par "
        "<code>bootstrapApplication</code> :"))
    story.append(code("""import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.error(err));

// app.config.ts - configuration centralisee
export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([
      authInterceptor, errorInterceptor
    ]))
  ]
};"""))

    story.append(section("6.3", "Routing et lazy loading"))
    story.append(p(
        "Toutes les routes utilisent <code>loadComponent</code> pour un "
        "lazy loading natif, ce qui produit des bundles separes par "
        "fonctionnalite. Mesure : le bundle initial pese "
        "<b>13.84 ko</b>, et chaque feature ajoute en moyenne "
        "<b>8 ko</b> charges a la demande."))
    story.append(code("""export const routes: Routes = [
  { path: '', loadComponent: () =>
      import('./features/catalog/product-list.component')
        .then(m => m.ProductListComponent) },
  { path: 'login', loadComponent: () =>
      import('./features/auth/login.component')
        .then(m => m.LoginComponent) },
  { path: 'cart', loadComponent: () =>
      import('./features/cart/cart.component')
        .then(m => m.CartComponent),
    canActivate: [authGuard] }
];"""))

    story.append(section("6.4", "AuthInterceptor et ErrorInterceptor"))
    story.append(p(
        "L'<b>AuthInterceptor</b> attache silencieusement le JWT a chaque "
        "requete HTTP sortante. L'<b>ErrorInterceptor</b> centralise la "
        "gestion d'erreurs : 401 entraine la deconnexion automatique, "
        "4xx/5xx affichent un toast."))
    story.append(code("""export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = inject(AuthService).token;
  if (!token) return next(req);
  return next(req.clone({
    setHeaders: { Authorization: `Bearer ${token}` }
  }));
};

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  const auth = inject(AuthService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      if (err.status === 401) {
        auth.logout();
        router.navigate(['/login']);
        toast.error('Session expiree');
      } else if (err.status !== 0) {
        toast.error(err.error?.message || `Erreur ${err.status}`);
      }
      return throwError(() => err);
    })
  );
};"""))

    story.append(section("6.5", "AuthGuard et composants"))
    story.append(p(
        "Trois routes sont protegees par <code>authGuard</code> : "
        "<code>/cart</code>, <code>/orders</code> et <code>/profile</code>. "
        "Le panier d'un visiteur non connecte n'est donc jamais persiste "
        "cote serveur."))
    story.append(code("""export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  if (auth.isAuthenticated) return true;
  router.navigate(['/login']);
  return false;
};"""))
    story.append(p(
        "L'interface adopte les codes du e-commerce moderne : barre de "
        "navigation fixe en tete, grille de cartes produits responsive "
        "(1 / 2 / 4 colonnes selon la largeur d'ecran), badges colores "
        "indiquant la disponibilite stock. Bootstrap 5 fournit l'ossature "
        "CSS et les composants standards (modales, alertes, formulaires)."))
    story.append(PageBreak())


# =====================================================================
# CHAPITRE 7 : Tests et deploiement
# =====================================================================
def chap7(story):
    STATE.chapter_title = "Chapitre 7 - Tests"
    story.extend(chap_header(7, "Tests et deploiement"))

    story.append(section("7.1", "Strategie de tests"))
    story.append(p(
        "Suivant la <b>pyramide de tests</b> de Mike Cohn, nous avons "
        "concentre l'effort sur la base de la pyramide : les tests unitaires "
        "des services metier. Ces tests sont rapides, deterministes et "
        "faciles a maintenir."))
    story.append(p("Outils utilises :"))
    for b in [
        "<b>JUnit 5</b> (Jupiter) : framework de test",
        "<b>Mockito 5</b> : isolation des dependances",
        "<b>AssertJ</b> : assertions fluentes (assertThat...)",
        "<b>Spring Boot Test</b> : tests d'integration eventuels",
    ]:
        story.append(bullet(b))

    rows = [
        ["Suite", "Tests", "Statut", "Couverture"],
        ["ProductServiceTest", "4", "PASS",
         "findById (present/absent), recherche (avec/sans mot-cle)"],
        ["CartServiceTest", "2", "PASS",
         "Ajout avec stock suffisant et insuffisant"],
        ["OrderServiceTest", "3", "PASS",
         "Panier vide, validation complete, historique"],
        ["TOTAL", "9", "0 failure", "BUILD SUCCESS"],
    ]
    tbl = Table(rows, colWidths=[4 * cm, 1.5 * cm, 2 * cm, 8.5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), ACCENT_GREEN),
        ("TEXTCOLOR", (0, -1), (-1, -1), white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
    ]))
    story.append(tbl)
    story.append(tcaption("Suite de tests unitaires E-Store", 5))

    story.append(section("7.2", "Resultats d'execution"))
    story.append(code("""$ ./mvnw test
[INFO] Tests run: 3, Failures: 0, Errors: 0 -- OrderServiceTest
[INFO] Tests run: 4, Failures: 0, Errors: 0 -- ProductServiceTest
[INFO] Tests run: 2, Failures: 0, Errors: 0 -- CartServiceTest
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS"""))
    story.append(caption("Resultats d'execution des tests JUnit", 6))

    story.append(section("7.3", "Conteneurisation Docker"))
    story.append(p(
        "Le fichier <code>docker-compose.yml</code> orchestre quatre "
        "services :"))
    story.append(code("""services:
  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: estore
    ports: ["3306:3306"]
  mongo:
    image: mongo:7
    ports: ["27017:27017"]
  phpmyadmin:
    image: phpmyadmin:latest
    ports: ["8081:80"]
  mongo-express:
    image: mongo-express:latest
    ports: ["8082:8081"]"""))
    story.append(caption("Organisation des services Docker Compose", 7))
    story.append(p(
        "Une commande suffit alors a provisionner l'environnement complet : "
        "<code>docker compose up -d</code>."))

    story.append(subsection("7.3.1", "Demarrage en trois commandes"))
    story.append(code("""# 1. Bases de donnees (optionnel : profil prod uniquement)
docker compose up -d

# 2. Backend
cd estore-backend && ./mvnw spring-boot:run

# 3. Frontend
cd estore-frontend && npm install && npm start

# 4. Ouvrir http://localhost:4200"""))

    story.append(subsection("7.3.2", "Versionnement Git et publication GitHub"))
    story.append(p(
        "L'historique du projet est versionne par Git, organise en "
        "<b>21 commits</b> semantiques (feat, fix, docs, chore). "
        "Le projet est publie sur GitHub a l'adresse "
        "<code>github.com/akrambelmoussa-etu-byte/e-store</code>."))
    story.append(PageBreak())


# =====================================================================
# CHAPITRE 8 : Difficultes et resultats
# =====================================================================
def chap8(story):
    STATE.chapter_title = "Chapitre 8 - Difficultes"
    story.extend(chap_header(8, "Difficultes rencontrees et resultats"))

    story.append(p(
        "Le developpement n'a pas ete un long fleuve tranquille. Plusieurs "
        "obstacles techniques significatifs ont ete rencontres ; les "
        "surmonter a ete l'occasion d'approfondir notre comprehension de "
        "l'ecosysteme."))

    story.append(section("8.1", "Difficultes rencontrees"))

    story.append(subsection("8.1.1", "Strictness Mockito"))
    story.append(p(
        "Lors du premier lancement de <code>mvn test</code>, deux tests "
        "echouent avec le message <i>UnnecessaryStubbingException: "
        "Unnecessary stubbings detected</i>."))
    story.append(p(
        "<b>Cause :</b> Mockito 5 applique par defaut le mode strict. Toute "
        "instruction <code>when(...).thenReturn(...)</code> declaree mais "
        "non verifiee durant l'execution du test provoque une erreur."))
    story.append(p(
        "<b>Solution :</b> annoter chaque classe de test avec "
        "<code>@MockitoSettings(strictness = Strictness.LENIENT)</code>, "
        "ce qui relache la verification tout en conservant la securite "
        "d'ecriture."))

    story.append(subsection("8.1.2", "LazyInitializationException"))
    story.append(p(
        "Lors du retour d'une entite User via le controleur, Hibernate "
        "levait une <code>LazyInitializationException</code> sur le "
        "<code>Profile</code> charge en mode LAZY."))
    story.append(p(
        "<b>Cause :</b> la serialisation Jackson tentait de naviguer dans "
        "la relation apres la fermeture de la session JPA."))
    story.append(p(
        "<b>Solution :</b> adoption systematique du pattern <b>DTO</b>. "
        "Chaque endpoint renvoie un objet de transfert "
        "(<code>UserDetailsDto</code>), construit dans la couche service "
        "alors que la session est encore ouverte. Avantage collateral : "
        "les DTOs masquent les champs sensibles (password) et stabilisent "
        "l'API."))

    story.append(subsection("8.1.3", "Installation de Docker Desktop"))
    story.append(p(
        "Lors de l'installation de Docker Desktop sous Windows 11, l'erreur "
        "suivante bloque le processus :"))
    story.append(Paragraph(
        '<i>« For security reasons C:\\ProgramData\\DockerDesktop must be '
        'owned by an elevated account. »</i>', ST["Quote"]))
    story.append(p(
        "<b>Cause :</b> un dossier residuel d'une installation anterieure "
        "subsistait avec des permissions incorrectes."))
    story.append(p("<b>Solutions implementees :</b>"))
    story.append(bullet(
        "<b>Solution A (brute) :</b> suppression manuelle en mode "
        "administrateur via <code>rmdir /s /q</code>, puis reinstallation propre."))
    story.append(bullet(
        "<b>Solution B (elegante) :</b> mise en place d'un <b>profil dev</b> "
        "base sur H2 in-memory, qui permet de demarrer l'application sans "
        "aucune installation prealable. Cette dualite Docker/H2 a ete "
        "pensee des la conception et a fait ses preuves le jour de la "
        "demonstration."))

    story.append(subsection("8.1.4", "Encodage des tokens JWT"))
    story.append(p(
        "Lors de la generation du premier JWT, la bibliotheque jjwt levait "
        "une <code>WeakKeyException</code> : la cle secrete configuree "
        "comportait moins de 256 bits."))
    story.append(p(
        "<b>Solution :</b> implementer une logique de fallback : tenter "
        "d'abord un decodage Base64 de la cle, et en cas d'echec ou de "
        "longueur insuffisante, utiliser l'encodage UTF-8 brut."))
    story.append(code("""byte[] bytes;
try {
    bytes = Decoders.BASE64.decode(secret);
    if (bytes.length < 32) throw new IllegalArgumentException();
} catch (Exception e) {
    bytes = secret.getBytes(StandardCharsets.UTF_8);
}
this.key = Keys.hmacShaKeyFor(bytes);"""))

    story.append(section("8.2", "Bilan fonctionnel et metriques"))
    story.append(p(
        "L'application livree couvre integralement le perimetre du cahier "
        "des charges. Le tableau suivant en synthetise les fonctionnalites :"))

    rows = [
        ["Fonctionnalite", "Description", "Statut"],
        ["Inscription / Connexion", "Email + mot de passe, JWT 24h", "Livre"],
        ["Profil utilisateur", "Consultation et modification", "Livre"],
        ["Catalogue pagine", "Recherche, filtre par categorie", "Livre"],
        ["Fiche produit", "Detail, image, stock, avis", "Livre"],
        ["Panier persistant", "Ajout, modification, vidage", "Livre"],
        ["Validation commande", "Transactionnelle ACID", "Livre"],
        ["Historique commandes", "Consultation detaillee", "Livre"],
        ["Avis produits", "Depot et consultation (MongoDB)", "Livre"],
        ["Administration", "CRUD categories / produits / stock", "Livre"],
    ]
    tbl = Table(rows, colWidths=[5 * cm, 8.5 * cm, 2.5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("BACKGROUND", (2, 1), (2, -1), ACCENT_GREEN),
        ("TEXTCOLOR", (2, 1), (2, -1), white),
        ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
    ]))
    story.append(tbl)
    story.append(tcaption("Bilan fonctionnel des livrables", 7))

    story.append(p("Quelques metriques quantitatives :"))
    rows = [
        ["Indicateur", "Valeur"],
        ["Lignes de code Java", "~ 3 500"],
        ["Lignes de code TypeScript", "~ 2 000"],
        ["Nombre de classes Java", "71"],
        ["Nombre de composants Angular", "14"],
        ["Nombre d'endpoints REST", "24"],
        ["Tests unitaires", "9 (100% passants)"],
        ["Bundle JS initial", "13.84 ko"],
        ["Temps de demarrage backend (H2)", "≈ 4 secondes"],
        ["Temps de reponse API (mediane)", "≈ 30 ms"],
        ["Commits Git", "21"],
    ]
    tbl = Table(rows, colWidths=[10 * cm, 6 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, BG_LIGHT]),
    ]))
    story.append(tbl)
    story.append(tcaption("Metriques quantitatives du projet", 6))
    story.append(PageBreak())


# =====================================================================
# CONCLUSION + BIBLIOGRAPHIE + ANNEXES
# =====================================================================
def conclusion(story):
    STATE.chapter_title = "Conclusion"
    story.extend(chap_header("CONCL", "Conclusion generale et perspectives"))

    story.append(section("1", "Bilan"))
    story.append(p(
        "Au terme de ce projet, nous avons mene a bien la conception et la "
        "realisation d'une application e-commerce <b>integralement "
        "fonctionnelle</b>, couvrant le parcours utilisateur du visiteur "
        "anonyme jusqu'a la commande validee. L'architecture en "
        "<b>trois couches x cinq domaines</b> a ete rigoureusement "
        "respectee, fournissant une base saine pour toute evolution ulterieure."))

    story.append(p("Sur le plan technique, les objectifs initiaux ont tous ete atteints :"))
    for b in [
        "Architecture full-stack moderne avec Spring Boot 3.3 et Angular 17.",
        "Persistance hybride MySQL + MongoDB operationnelle.",
        "Securite robuste par BCrypt + JWT + @PreAuthorize.",
        "Suite de tests JUnit 5 / Mockito en BUILD SUCCESS.",
        "Conteneurisation Docker Compose, profil de fallback H2.",
    ]:
        story.append(bullet(b))

    story.append(p(
        "Sur le plan humain, le travail en binome nous a permis "
        "d'experimenter <i>in vivo</i> les pratiques du developpement "
        "collaboratif : versionnement Git, conventions de commit, revue de "
        "code, repartition des taches, communication asynchrone."))

    story.append(section("2", "Apports personnels"))
    story.append(p(
        "Au-dela de la technique, ce projet nous a confronte a la "
        "<b>realite de l'incertitude</b> qui caracterise tout developpement "
        "logiciel : choix d'architecture aux consequences durables, "
        "debogage de problemes inattendus, arbitrages entre elegance du "
        "code et delais. Apprendre a composer avec cette incertitude, "
        "plutot qu'a la fuir, est probablement le benefice le plus durable "
        "de cette experience."))

    story.append(section("3", "Perspectives"))
    story.append(p(
        "Le projet livre n'est pas un produit fini mais un <b>socle "
        "evolutif</b>. Plusieurs pistes d'extension ont ete identifiees :"))
    for b in [
        "<b>Paiement en ligne :</b> integration de Stripe ou des "
        "passerelles marocaines (CMI, Maroc Telecommerce).",
        "<b>Notifications transactionnelles :</b> envoi automatique d'emails "
        "(Spring Mail) ou de SMS (Twilio) lors de la confirmation de commande.",
        "<b>Recommandations :</b> suggestion produits basee sur "
        "l'historique d'achat (collaborative filtering).",
        "<b>Internationalisation :</b> passage du francais a l'arabe ou "
        "l'anglais via Angular i18n.",
        "<b>Deploiement cloud :</b> conteneurisation et deploiement sur "
        "Heroku, Render ou AWS Free Tier.",
        "<b>Application mobile :</b> portage Ionic ou Flutter consommant "
        "la meme API.",
        "<b>Observabilite :</b> integration Prometheus + Grafana pour les "
        "metriques applicatives.",
    ]:
        story.append(bullet(b))

    story.append(p(
        "Plus fondamentalement, l'architecture en couches et en domaines "
        "que nous avons mise en place rend ces evolutions <b>additives</b> : "
        "il sera possible de les introduire sans casser l'existant. C'est, "
        "a nos yeux, la preuve la plus convaincante que les choix "
        "architecturaux de depart etaient les bons."))
    story.append(PageBreak())


def bibliographie(story):
    STATE.chapter_title = "Bibliographie"
    story.extend(chap_header("BIB", "Bibliographie et webographie"))

    story.append(Paragraph("<b>Ouvrages :</b>", ST["H3"]))
    for i, ref in enumerate([
        "Craig Walls, <i>Spring Boot in Action</i>, 2nd edition, "
        "Manning Publications, 2024.",
        "Robert C. Martin, <i>Clean Code: A Handbook of Agile Software "
        "Craftsmanship</i>, Prentice Hall, 2008.",
        "Eric Evans, <i>Domain-Driven Design: Tackling Complexity in the "
        "Heart of Software</i>, Addison-Wesley, 2003.",
        "Martin Fowler, <i>Patterns of Enterprise Application "
        "Architecture</i>, Addison-Wesley, 2002.",
    ], start=1):
        story.append(p(f"[{i}] {ref}"))

    story.append(Paragraph("<b>Documentations officielles :</b>", ST["H3"]))
    for i, ref in enumerate([
        "Spring Framework Reference - docs.spring.io/spring-framework/",
        "Spring Boot Reference - docs.spring.io/spring-boot/",
        "Spring Data JPA - docs.spring.io/spring-data/jpa/",
        "Spring Data MongoDB - docs.spring.io/spring-data/mongodb/",
        "Angular Documentation - angular.dev",
        "MongoDB Manual - mongodb.com/docs/manual/",
        "RFC 7519 - JSON Web Token (JWT) - rfc-editor.org/rfc/rfc7519",
        "OWASP Authentication Cheat Sheet - cheatsheetseries.owasp.org",
    ], start=5):
        story.append(p(f"[{i}] {ref}"))

    story.append(Paragraph("<b>Articles et tutoriels :</b>", ST["H3"]))
    for i, ref in enumerate([
        "Baeldung - A Guide to JPA with Spring",
        "Baeldung - Spring Security with JWT",
        "Angular Blog - Introducing Angular Signals",
    ], start=13):
        story.append(p(f"[{i}] {ref}"))
    story.append(PageBreak())


def annexes(story):
    STATE.chapter_title = "Annexes"
    story.extend(chap_header("ANN", "Annexes"))

    story.append(section("A", "Configuration application.properties"))
    story.append(code("""# === application.properties (commun) ===
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
jwt.expiration=86400000"""))

    story.append(section("B", "Comptes de test"))
    story.append(p(
        "Le <code>DataSeeder</code> cree automatiquement deux comptes au "
        "premier demarrage si la base est vide :"))
    rows = [
        ["Role", "Email", "Mot de passe"],
        ["ADMIN", "admin@estore.ma", "Admin@123"],
        ["USER", "user@estore.ma", "User@123"],
    ]
    tbl = Table(rows, colWidths=[3 * cm, 6 * cm, 4 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (-1, -1), "Courier"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("GRID", (0, 0), (-1, -1), 0.3, GREY_LIGHT),
    ]))
    story.append(tbl)

    story.append(section("C", "Procedure de demarrage rapide"))
    story.append(code("""# 1. Cloner le depot
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


# =====================================================================
# MAIN
# =====================================================================
def build_rapport():
    global ST
    ST = build_styles()
    out = os.path.join(OUT_DIR, "Rapport-E-Store.pdf")

    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2.5 * cm, bottomMargin=2.5 * cm,
        title="E-Store - Memoire de fin de module - DEV-INFO S6",
        author="Akram BELMOUSSA & Nouhaila BEN SOUMANE",
        subject="Memoire de fin de module - Full-Stack - FSBM - 10 Mai 2026"
    )

    story = []

    # === COVER ===
    STATE.show_header_footer = False
    cover_page(story)

    # === LIMINAIRES (numerotation romaine) ===
    STATE.show_header_footer = True
    STATE.pre_intro = True
    dedicace(story)
    remerciements(story)
    resume(story)
    abstract(story)
    table_des_matieres(story)
    table_des_figures(story)
    liste_abrev(story)

    # === CORPS (numerotation arabe) ===
    STATE.pre_intro = False
    introduction(story)
    chap1(story)
    chap2(story)
    chap3(story)
    chap4(story)
    chap5(story)
    chap6(story)
    chap7(story)
    chap8(story)
    conclusion(story)
    bibliographie(story)
    annexes(story)

    # Build avec callback header/footer different pour la page de garde
    def first_page(canvas, doc):
        # Cover : juste un cadre subtil
        canvas.saveState()
        # Cadre fin
        canvas.setStrokeColor(PRIMARY)
        canvas.setLineWidth(0.6)
        canvas.rect(1.5 * cm, 1.5 * cm, A4[0] - 3 * cm, A4[1] - 3 * cm)
        # Annee en bas a droite
        canvas.restoreState()

    # Counter pour pages — STATE.page_number incremente
    def all_pages(canvas, doc):
        # Sur la cover, pas de header
        if doc.page == 1:
            first_page(canvas, doc)
            return
        # Liminaires : pagination romaine
        # Corps : pagination arabe, redemarrant a 1
        if not STATE.pre_intro:
            STATE.page_number = doc.page - 8  # cover + 7 liminaires
            if STATE.page_number < 1:
                STATE.page_number = 1
        header_footer(canvas, doc)

    doc.build(story, onFirstPage=all_pages, onLaterPages=all_pages)
    return out


if __name__ == "__main__":
    print("=" * 70)
    print(" Generation du rapport E-Store (PDF)")
    print(" Style : Memoire de fin de module FSBM")
    print(" Date : 10 Mai 2026 - Filiere DEV-INFO S6")
    print("=" * 70)
    out = build_rapport()
    size_kb = os.path.getsize(out) // 1024
    print(f"\n  [OK] {os.path.basename(out)}  ({size_kb} ko)")
    print(f"\n  Chemin : {out}")
    print("=" * 70)
