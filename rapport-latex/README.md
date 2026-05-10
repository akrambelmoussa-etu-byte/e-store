# Rapport LaTeX — E-Store

Rapport académique du projet E-Store au format LaTeX, structuré selon les
standards des rapports de fin de module à la Faculté des Sciences Ben M'Sick.

## 📄 Contenu du rapport

- **40+ pages** structurées en 10 chapitres
- Page de garde formelle (université, faculté, encadrant)
- Remerciements, dédicaces, résumé
- Table des matières, liste des figures, liste des tableaux, abréviations
- 4 schémas TikZ (architecture 3 couches, 6 domaines, MCD, flux JWT)
- 8 tableaux structurés (matrice architecturale, endpoints REST, métriques)
- 25+ extraits de code Java / TypeScript / properties
- Boîtes colorées (info, astuce, attention)
- Bibliographie / webographie
- 4 annexes (configuration, endpoints complets, comptes test, démarrage rapide)

## 🎯 Méthode 1 (recommandée) — Compilation sur Overleaf

**Pas d'installation locale, compilation en ligne, gratuit.**

1. Aller sur [https://www.overleaf.com](https://www.overleaf.com) (créer un compte gratuit)
2. Cliquer **New Project** → **Upload Project**
3. Compresser le dossier `rapport-latex/` en ZIP, puis l'uploader
4. Overleaf détecte automatiquement le fichier principal `rapport-estore.tex`
5. Cliquer **Recompile** → le PDF est généré en quelques secondes
6. Télécharger le PDF avec le bouton de téléchargement

> **Astuce :** Overleaf permet aussi le partage en temps réel — pratique
> pour la rédaction à deux (Akram + Nouhaila).

## 🎯 Méthode 2 — Compilation locale (Windows)

### Pré-requis

Installer **MiKTeX** : [https://miktex.org/download](https://miktex.org/download)

→ Lors de l'installation, cocher **"Install missing packages on the fly: Yes"**

### Compilation

Ouvrir un terminal dans le dossier `rapport-latex/` :

```cmd
pdflatex rapport-estore.tex
pdflatex rapport-estore.tex
```

Deux passes sont nécessaires pour que les références (table des matières,
liste des figures, numéros de pages) soient correctement résolues.

Le fichier `rapport-estore.pdf` est alors généré dans le même dossier.

### Compilation avec le Makefile

```cmd
make
```

Ou pour nettoyer les fichiers auxiliaires :

```cmd
make clean
```

## 🎯 Méthode 3 — VS Code + LaTeX Workshop

1. Installer **MiKTeX** (voir Méthode 2)
2. Installer l'extension **LaTeX Workshop** dans VS Code
3. Ouvrir `rapport-estore.tex`
4. Appuyer sur **Ctrl+Alt+B** pour compiler
5. Aperçu PDF intégré : **Ctrl+Alt+V**

## 📦 Dépendances LaTeX utilisées

Tous les packages utilisés sont **standards** et inclus par défaut dans
MiKTeX et TeX Live :

| Package | Rôle |
| --- | --- |
| `babel` (french) | Localisation française |
| `geometry` | Marges et mise en page |
| `xcolor` | Couleurs |
| `listings` | Coloration syntaxique du code |
| `tcolorbox` | Boîtes colorées (info, tip, warn) |
| `tikz` | Schémas vectoriels |
| `hyperref` | Liens cliquables |
| `titlesec`, `fancyhdr` | Mise en forme titres et en-têtes |
| `booktabs`, `longtable`, `tabularx` | Tableaux |

## 🛠️ Personnalisation

### Modifier les auteurs / encadrant

Éditer en haut du fichier `rapport-estore.tex` la **page de garde** (ligne 215)
et les **remerciements** (ligne 270).

### Ajouter des captures d'écran

1. Placer les images PNG dans un sous-dossier `images/`
2. Insérer dans le rapport avec :
   ```latex
   \begin{figure}[htbp]
   \centering
   \includegraphics[width=0.8\textwidth]{images/screenshot-catalogue.png}
   \caption{Page d'accueil du catalogue}
   \label{fig:catalogue}
   \end{figure}
   ```

### Changer la couleur principale

Dans le préambule (ligne 38), modifier :

```latex
\definecolor{primaryblue}{HTML}{0D6EFD}  % Bleu Bootstrap (défaut)
% Exemples :
% \definecolor{primaryblue}{HTML}{198754}  % Vert
% \definecolor{primaryblue}{HTML}{6610F2}  % Violet
% \definecolor{primaryblue}{HTML}{D63384}  % Rose
```

## 📝 Notes de rédaction

- **Volume estimé** : 40-45 pages (page de garde incluse)
- **Format** : A4, Latin Modern 11pt, interligne 1.5
- **Bibliographie** : style numéroté simple (sans biblatex)
- **Code** : style "leftline" avec barre bleue à gauche
- **Schémas** : entièrement en TikZ — modifiables sans logiciel externe

## ❓ FAQ

### « Je n'ai pas LaTeX installé »
→ Utiliser Overleaf (Méthode 1).

### « Le compilateur ne trouve pas un package »
→ Sur MiKTeX, accepter l'installation à la volée. Sur Overleaf, c'est automatique.

### « Comment ajouter un nouveau chapitre ? »
→ Dupliquer un `\chapter{...}` existant et adapter le contenu.

### « Comment changer la langue en arabe ? »
→ Remplacer `[french]` par `[arabic]` dans `\usepackage{babel}` et passer à
XeLaTeX (compiler avec `xelatex` au lieu de `pdflatex`). Police arabe :
`\setmainfont{Amiri}`.
