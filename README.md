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
| Chapter 3 (ECC-HISE + prototype) | ~32 | Pending |
| Chapter 4 | ~28 | Pending |
| Chapter 5 | ~30 | Pending |
| Conclusions + Appendix | ~18 | Pending |

## Generate Documents

### Word (B5, 11pt)

```bash
pip install -r requirements.txt
python scripts/generate_phase1.py
python scripts/generate_figures_ch2.py
python scripts/generate_chapter02.py
python -m prototype.benchmarks.bench_dtb_aka
```

Output:
- `thesis/phase1_preface_chapter01.docx`
- `thesis/03_chapter02.docx`

### LaTeX (B5, 11pt)

```bash
python scripts/generate_figures_ch1.py
python scripts/generate_figures_ch2.py
python scripts/generate_latex.py
cd Latex
pdflatex main.tex
pdflatex main.tex
```

Output: `Latex/main.tex` and chapter `.tex` files (see `Latex/README.md`).

## Schemes

- **ECC-DTB-AKA** — Client-server authenticated key agreement (Chapter 2)
- **ECC-HISE** — Server-server hierarchical secure envelope (Chapter 3)

See `thesis/00_scheme_design.docx` for full specification.
