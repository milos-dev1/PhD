# E-Banking Security Thesis

PhD dissertation on ECC-based security for e-banking systems.

**Format:** B5 paper, Times New Roman 11pt, 1.5 line spacing  
**Target:** 150+ pages total

## Project Structure

```
e-banking-security-thesis/
├── content/          # Chapter text (Python modules)
├── scripts/          # Word/figure generators
├── thesis/           # Output .docx files and figures/
├── prototype/        # Implementation (Chapters 2–4)
└── references/       # Bibliography
```

## Page Budget (B5, 11pt)

| Deliverable | Target Pages | Status |
|-------------|-------------|--------|
| Scheme Design | ~5 | Done |
| Preface + Ch.1 | ~38 | Done |
| Chapter 2 (ECC-DTB-AKA + prototype) | ~32 | **Done** |
| Chapter 3 (ECC-HISE + prototype) | ~32 | **Done** |
| Chapter 4 (implementation) | ~28 | **Done** |
| Chapter 5 | ~30 | **Done** |
| Conclusions + Appendix | ~18 | **Done** |
| **Full merge** | `full_thesis.docx` | **Done** |

## Final Assembly

```bash
python scripts/generate_full_thesis.py
# or
python scripts/assemble_all.py
```

**Main output:** `thesis/full_thesis.docx` (or `full_thesis_assembled.docx` if the file is open in Word)

Includes:
- Title page, Abstract
- **Table of Contents** (all chapters + sections)
- **List of Figures** (23 figures)
- **List of Tables** (17 tables)
- Preface, Chapters 1–5, Conclusions, Appendix
- **References** (67 numbered citations)

Close `full_thesis.docx` in Word before regenerating. If locked, output goes to `full_thesis_assembled.docx`.

## Generate Individual Chapters

### Word (B5, 11pt)

```bash
pip install -r requirements.txt
python scripts/generate_phase1.py
python scripts/generate_figures_ch2.py
python scripts/generate_chapter02.py
python scripts/generate_figures_ch3.py
python scripts/generate_chapter03.py
python scripts/generate_figures_ch4.py
python scripts/generate_chapter05.py
python scripts/generate_conclusions.py
python scripts/generate_full_thesis.py
```

Output:
- `thesis/phase1_preface_chapter01.docx`
- `thesis/03_chapter02.docx` … `thesis/06_chapter05.docx`
- `thesis/07_conclusions.docx`, `thesis/08_appendix.docx`
- **`thesis/full_thesis_assembled.docx`** — all chapters merged

### LaTeX (B5, 11pt) — full thesis

```bash
python scripts/generate_figures_ch1.py
python scripts/generate_figures_ch2.py
python scripts/generate_figures_ch3.py
python scripts/generate_figures_ch4.py
python scripts/generate_figures_ch5.py
python scripts/generate_latex.py
cd Latex
pdflatex main.tex
pdflatex main.tex
```

Includes: Preface, Ch.1–5, Conclusions, Appendix, References (67), clickable TOC/LOF/LOT, hyperlinked `[n]` citations, page numbers.

Output: `Latex/main.tex` (see `Latex/README.md`).

## Schemes

- **ECC-DTB-AKA** — Client-server authenticated key agreement (Chapter 2)
- **ECC-HISE** — Server-server hierarchical secure envelope (Chapter 3)

See `thesis/00_scheme_design.docx` for full specification.
