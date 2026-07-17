# LaTeX Thesis

B5 paper, 11pt Times (mathptmx), 1.5 line spacing.

## Build

```bash
cd Latex
pdflatex main.tex
pdflatex main.tex   # second pass for TOC/references
```

Or from project root:

```bash
python scripts/generate_latex.py
cd Latex && pdflatex main.tex && pdflatex main.tex
```

## Structure

```
Latex/
  main.tex              # Master document
  preamble.tex          # Packages, B5 geometry, styling
  frontmatter/
    titlepage.tex
    abstract.tex
  chapters/
    preface.tex
    chapter01.tex
    chapter02.tex
    scheme_design.tex   # Appendix
```

Figures are loaded from `../thesis/figures/`.

## Regenerate from content

Content lives in `content/*.py`. Regenerate LaTeX after edits:

```bash
python scripts/generate_latex.py
```
