# LaTeX Thesis (Full)

B5 paper, 11pt Times, 1.5 line spacing.

## Contents

- Title page, Abstract
- Clickable Table of Contents / List of Figures / List of Tables (`hyperref`)
- Preface, Chapters 1--5, Conclusions, Appendix
- References (67 entries) with clickable in-text `[n]` citations (`\hyperref`)
- Page numbers (centered footer)

## Build PDF

```bash
cd Latex
pdflatex main.tex
pdflatex main.tex   # second pass for TOC and cross-refs
```

Or from project root:

```bash
python scripts/generate_latex.py
cd Latex && pdflatex main.tex && pdflatex main.tex
```

Figures are loaded from `../thesis/figures/`.

## Regenerate from content

```bash
python scripts/generate_latex.py
```
