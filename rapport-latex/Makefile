# Makefile pour la compilation du rapport LaTeX E-Store
# Usage : make           (compile en PDF)
#         make clean     (supprime les fichiers auxiliaires)
#         make rebuild   (clean + compile)

MAIN = rapport-estore
LATEX = pdflatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean rebuild view

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	$(LATEX) $(LATEX_FLAGS) $(MAIN).tex
	@echo "------------------------------------------------------------"
	@echo "  PDF genere : $(MAIN).pdf"
	@echo "------------------------------------------------------------"

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz

rebuild: clean all

view: $(MAIN).pdf
	@echo "Ouverture de $(MAIN).pdf..."
	@cmd.exe /c start $(MAIN).pdf 2>/dev/null || open $(MAIN).pdf 2>/dev/null || xdg-open $(MAIN).pdf
