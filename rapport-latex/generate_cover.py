# -*- coding: utf-8 -*-
"""
Genere la page de garde du rapport E-Store au format PDF, en respectant
le modele du Pr. Zahour (cf. Rapport Pfe[1] exemple.pdf).

USAGE :
  1. (Optionnel) Sauvegarder les logos dans rapport-latex/images/ :
       - logo-fsbm.png      (logo de la Faculte des Sciences Ben M'Sick)
       - logo-dept.png      (logo Departement Mathematiques & Informatique)
  2. Lancer : python generate_cover.py
  3. Le fichier page-de-garde-estore.pdf est genere.

Si les logos ne sont pas presents, le script dessine des placeholders.
"""
import os, sys, io

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# --- Chemins ---
HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(HERE, "images")
LOGO_FSBM = os.path.join(IMAGES_DIR, "logo-fsbm.png")
LOGO_DEPT = os.path.join(IMAGES_DIR, "logo-dept.png")
OUTPUT = os.path.join(HERE, "page-de-garde-estore.pdf")

# --- Couleurs ---
DARK_NAVY = HexColor("#1F3A68")     # Bleu universite
PRIMARY = HexColor("#0D6EFD")       # Bleu projet
TEAL = HexColor("#1FA98F")          # Vert turquoise du logo dept
DARK = HexColor("#212529")
GREY = HexColor("#6C757D")


def draw_fsbm_placeholder(c, x, y, w, h):
    """Dessine un placeholder du logo FSBM (style hexagones empiles)."""
    c.saveState()
    # Texte arabe (placeholder)
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x + w/2, y + h - 0.4*cm, "Universite Hassan II - Casablanca")
    c.drawCentredString(x + w/2, y + h - 0.75*cm, "Faculte des Sciences Ben M'Sick")
    # Bloc UH2 + FSBM
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(x + 0.4*cm, y + h/2 - 0.5*cm, "UH2")
    c.setStrokeColor(DARK_NAVY)
    c.setLineWidth(1.2)
    c.line(x + 2.2*cm, y + h/2 - 1.0*cm, x + 2.2*cm, y + h/2 + 0.6*cm)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(x + 2.4*cm, y + h/2 - 0.5*cm, "FSBM")
    # Sous-titre
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(DARK_NAVY)
    c.drawCentredString(x + w/2, y + 0.55*cm, "FACULTE DES SCIENCES BEN M'SICK")
    c.setFillColor(GREY)
    c.drawCentredString(x + w/2, y + 0.20*cm, "UNIVERSITE HASSAN II DE CASABLANCA")
    c.restoreState()


def draw_dept_placeholder(c, x, y, w, h):
    """Dessine un placeholder du logo Departement Maths & Info."""
    c.saveState()
    cx = x + w/2
    cy = y + h*0.55
    # Symbole infini stylise (deux cercles)
    c.setStrokeColor(TEAL)
    c.setLineWidth(2.2)
    c.circle(cx - 0.7*cm, cy, 0.5*cm, stroke=1, fill=0)
    c.circle(cx + 0.7*cm, cy, 0.5*cm, stroke=1, fill=0)
    # Petit texte "0101" autour
    c.setFillColor(TEAL)
    c.setFont("Courier-Bold", 6)
    c.drawString(cx - 1.6*cm, cy + 0.7*cm, "01010110")
    c.drawString(cx + 0.4*cm, cy + 0.7*cm, "10010101")
    # Texte sous le symbole
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(cx, y + 0.55*cm, "MATHEMATIQUES")
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(cx, y + 0.18*cm, "& INFORMATIQUE")
    c.restoreState()


def draw_logo(c, path, fallback_fn, x, y, w, h):
    """Dessine un logo image si present, sinon un placeholder."""
    if os.path.exists(path):
        try:
            img = ImageReader(path)
            iw, ih = img.getSize()
            ratio = min(w/iw, h/ih)
            new_w, new_h = iw*ratio, ih*ratio
            cx = x + (w - new_w) / 2
            cy = y + (h - new_h) / 2
            c.drawImage(img, cx, cy, width=new_w, height=new_h,
                        preserveAspectRatio=True, mask='auto')
            return
        except Exception as e:
            print(f"[warn] impossible de charger {path}: {e}")
    fallback_fn(c, x, y, w, h)


def build_cover():
    c = canvas.Canvas(OUTPUT, pagesize=A4)
    page_w, page_h = A4

    # ─── Logos (en haut) ────────────────────────────────────────────
    logo_h = 3.0 * cm
    logo_w_left = 6.5 * cm
    logo_w_right = 5.5 * cm
    margin = 1.8 * cm

    draw_logo(c, LOGO_FSBM, draw_fsbm_placeholder,
              margin, page_h - margin - logo_h, logo_w_left, logo_h)
    draw_logo(c, LOGO_DEPT, draw_dept_placeholder,
              page_w - margin - logo_w_right, page_h - margin - logo_h,
              logo_w_right, logo_h)

    # ─── Trait de separation ────────────────────────────────────────
    sep_y = page_h - margin - logo_h - 0.5 * cm
    c.setStrokeColor(DARK_NAVY)
    c.setLineWidth(0.4)
    c.line(margin, sep_y, page_w - margin, sep_y)

    # ─── En-tete textuel (universite, faculte, departement) ─────────
    y = sep_y - 0.7 * cm
    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, y, "Universite Hassan II de Casablanca")
    y -= 0.55 * cm
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(page_w/2, y, "Faculte des Sciences Ben M'Sick")
    y -= 0.55 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w/2, y, "Departement de Mathematiques et Informatique")

    # ─── Type de document ───────────────────────────────────────────
    y -= 1.4 * cm
    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 12.5)
    c.drawCentredString(page_w/2,
        y, "Memoire de fin d'etude pour l'obtention de la Licence Sciences")
    y -= 0.5 * cm
    c.drawCentredString(page_w/2,
        y, "Mathematiques et Informatique  -  Option : Genie Logiciel")

    # ─── Boite SUJET ────────────────────────────────────────────────
    y -= 1.3 * cm
    box_x = margin + 1*cm
    box_w = page_w - 2*margin - 2*cm
    box_h = 3.6 * cm

    # Fond
    c.setFillColor(HexColor("#F5F7FA"))
    c.setStrokeColor(PRIMARY)
    c.setLineWidth(1.2)
    c.roundRect(box_x, y - box_h, box_w, box_h, 6, fill=1, stroke=1)

    # Label "Sujet :"
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(box_x + 0.6*cm, y - 0.7*cm, "Sujet :")

    # Titre projet
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_w/2, y - 1.7*cm, "E-STORE")
    c.setFont("Helvetica", 13)
    c.drawCentredString(page_w/2, y - 2.4*cm,
        "Conception et realisation d'une plateforme e-commerce")
    c.drawCentredString(page_w/2, y - 2.95*cm,
        "full-stack a persistance hybride (SQL + NoSQL)")

    # ─── Encadrant ──────────────────────────────────────────────────
    y -= box_h + 0.9 * cm
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w/2, y, "Encadre par : Pr. ZAHOUR OMAR")

    # ─── Realise par ────────────────────────────────────────────────
    y -= 0.9 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w/2, y, "Realise par :")
    y -= 0.55 * cm
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, y,
        "Akram BELMOUSSA  -  Nouhaila BEN SOUMANE")

    # ─── Soutenu devant le jury ─────────────────────────────────────
    y -= 1.0 * cm
    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(page_w/2, y, "Soutenu en juin 2026, devant le jury :")

    # Tableau jury
    jury = [
        ("Pr. Omar ZAHOUR",          "Encadrant"),
        ("Pr. [Nom du President]",   "President du jury"),
        ("Pr. [Nom de l'Examinateur]", "Examinateur"),
    ]
    y -= 0.7 * cm
    c.setFont("Helvetica", 11)
    for name, role in jury:
        c.setFillColor(DARK)
        c.drawString(margin + 3*cm, y, name)
        c.setFillColor(GREY)
        c.drawRightString(page_w - margin - 3*cm, y, role)
        y -= 0.5 * cm

    # ─── Annee universitaire ────────────────────────────────────────
    c.setStrokeColor(DARK_NAVY)
    c.setLineWidth(0.4)
    c.line(margin + 4*cm, 1.7*cm, page_w - margin - 4*cm, 1.7*cm)

    c.setFillColor(DARK_NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(page_w/2, 1.1*cm, "Annee universitaire : 2025 - 2026")

    c.showPage()
    c.save()
    return OUTPUT


if __name__ == "__main__":
    print("=" * 60)
    print("Generation de la page de garde E-Store")
    print("=" * 60)
    out = build_cover()
    size_kb = os.path.getsize(out) // 1024
    print(f"  [OK] {os.path.basename(out)}  ({size_kb} ko)")

    # Avertissements logos
    if not os.path.exists(LOGO_FSBM):
        print()
        print("  [!] Aucun logo FSBM detecte (placeholder utilise).")
        print(f"      Pour un rendu reel, sauvegardez le logo en :")
        print(f"      {LOGO_FSBM}")
    if not os.path.exists(LOGO_DEPT):
        print()
        print("  [!] Aucun logo Departement detecte (placeholder utilise).")
        print(f"      Pour un rendu reel, sauvegardez le logo en :")
        print(f"      {LOGO_DEPT}")
    print()
    print(f"Fichier genere : {out}")
