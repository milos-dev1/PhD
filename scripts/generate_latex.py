"""Generate complete LaTeX thesis (all chapters, citations, TOC, references)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from latex_utils import (
    escape_latex,
    merge_expansions,
    render_bibliography,
    render_paragraph,
    render_sections,
    write_tex,
)

ROOT = Path(__file__).resolve().parent.parent
LATEX = ROOT / "Latex"

FIGURE_MAP_CH1 = {
    "Figure 1.1": "fig_1_1_attack_lifecycle.png",
    "Figure 1.2": "fig_1_2_client_auth_flow.png",
    "Figure 1.3": "fig_1_3_server_mesh.png",
    "Figure 1.4": "fig_1_4_data_layers.png",
    "Figure 1.5": "fig_1_5_threat_model.png",
}
FIGURE_MAP_CH2 = {
    "Figure 2.1": "fig_2_1_protocol_sequence.png",
    "Figure 2.2": "fig_2_2_key_derivation.png",
    "Figure 2.3": "fig_2_3_benchmark_chart.png",
}
FIGURE_MAP_CH3 = {
    "Figure 3.1": "fig_3_1_hierarchy.png",
    "Figure 3.2": "fig_3_2_envelope.png",
    "Figure 3.3": "fig_3_3_verify_flow.png",
    "Figure 3.4": "fig_3_4_benchmark.png",
}
FIGURE_MAP_CH4 = {
    "Figure 4.1": "fig_4_1_architecture.png",
    "Figure 4.2": "fig_4_2_flow.png",
    "Figure 4.3": "fig_4_3_dtb_modules.png",
    "Figure 4.4": "fig_4_4_hise_modules.png",
    "Figure 4.5": "fig_4_5_deployment.png",
}
FIGURE_MAP_CH5 = {
    "Figure 5.1": "fig_5_1_attack_matrix.png",
    "Figure 5.2": "fig_5_2_combined_benchmark.png",
    "Figure 5.3": "fig_5_3_tls_handshake.png",
    "Figure 5.4": "fig_5_4_oauth_pkce.png",
    "Figure 5.5": "fig_5_5_mtls.png",
    "Figure 5.6": "fig_5_6_tls_vs_envelope.png",
    "Figure 5.7": "fig_5_7_merkle_compare.png",
}

THESIS_TITLE = (
    "A Dual-Layer ECC Methodology for Client-Server Authentication "
    "and Server-Server Data Protection in Electronic Finance Systems"
)

ABSTRACT = (
    "This dissertation investigates information security challenges in electronic banking and "
    "electronic finance service systems, with particular emphasis on authentication, key exchange, "
    "data encryption, and integrity protection. A comprehensive analysis of contemporary attack "
    "mechanisms---including phishing, man-in-the-middle attacks, replay attacks, session hijacking, "
    "credential stuffing, and insider threats---establishes the threat landscape and identifies "
    "critical limitations in existing security mechanisms. Two novel elliptic curve cryptography "
    "(ECC) based schemes are proposed: ECC-DTB-AKA (Device- and Transaction-Bound Authenticated "
    "Key Agreement) for client-server channels, and ECC-HISE (Hierarchical Integrity-preserving "
    "Secure Envelope) for server-server batch data transfer. Both schemes are formally analyzed, "
    "quantitatively evaluated against established baselines, and implemented in a working software "
    "prototype. Experimental results demonstrate that ECC-DTB-AKA achieves mutual authentication "
    "in three communication rounds with device and transaction binding, while ECC-HISE provides "
    "hierarchical key management with Merkle-tree audit chains enabling efficient batch integrity "
    "verification."
)


def fig_map(name_map: dict[str, str]) -> dict[str, str]:
    return {k: v for k, v in name_map.items()}  # graphicspath handles directory


def generate_preamble() -> Path:
    content = r"""\documentclass[11pt,b5paper,twoside,openright]{book}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{mathptmx}
\usepackage[margin=25mm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage{graphicx}
\graphicspath{{../thesis/figures/}{figures/}}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{caption}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{microtype}
\usepackage{xcolor}

% Hyperlinks: clickable TOC, citations, figures
\usepackage[hidelinks]{hyperref}
\usepackage{bookmark}
\hypersetup{
  colorlinks=true,
  linkcolor=blue!50!black,
  citecolor=blue!50!black,
  urlcolor=blue,
  bookmarks=true,
  bookmarksnumbered=true,
  pdftitle={E-Banking ECC Security Thesis},
  pdfauthor={PhD Dissertation},
}

\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}

\usepackage{titlesec}
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries}{\chaptertitlename\ \thechapter}{20pt}{\Huge}
\titleformat{\section}{\normalfont\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\large\bfseries}{\thesubsection}{1em}{}

% Page numbers (centered footer)
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
}

"""
    out = LATEX / "preamble.tex"
    write_tex(out, content)
    return out


def generate_titlepage() -> Path:
    content = (
        r"\begin{titlepage}" + "\n"
        r"\centering" + "\n"
        r"\vspace*{3cm}" + "\n"
        rf"{{\Huge\bfseries {escape_latex(THESIS_TITLE)}\par}}" + "\n"
        r"\vspace{1.5cm}" + "\n"
        r"{\Large PhD Dissertation in Information Security\par}" + "\n"
        r"\vspace{4cm}" + "\n"
        r"{\large Submitted in partial fulfillment of the requirements" + "\n"
        r"for the degree of Doctor of Philosophy\par}" + "\n"
        r"\vfill" + "\n"
        r"{\large \today\par}" + "\n"
        r"\end{titlepage}" + "\n"
    )
    out = LATEX / "frontmatter" / "titlepage.tex"
    write_tex(out, content)
    return out


def generate_abstract() -> Path:
    content = (
        r"\chapter*{Abstract}" + "\n"
        r"\addcontentsline{toc}{chapter}{Abstract}" + "\n"
        r"\label{ch:abstract}" + "\n\n"
        + render_paragraph(ABSTRACT.replace("---", "—"), auto_cite=False)
    )
    out = LATEX / "frontmatter" / "abstract.tex"
    write_tex(out, content)
    return out


def chapter_file(
    path: Path,
    chapter_title: str,
    subtitle: str,
    label: str,
    body: str,
) -> Path:
    # Drop redundant "Chapter N" if present — book class adds it
    display = chapter_title
    if display.lower().startswith("chapter "):
        # Keep as unnumbered? No — use chapter with short title from subtitle or clean
        # Prefer using the descriptive subtitle as the chapter title for LaTeX numbering
        display = subtitle if subtitle else chapter_title
    content = (
        rf"\chapter{{{escape_latex(display)}}}" + "\n"
        rf"\label{{{label}}}" + "\n\n"
        + body
    )
    write_tex(path, content)
    return path


def generate_preface() -> Path:
    import preface as pf
    from phase1_expansion import PREFACE_DEEP, PREFACE_EXPANSION
    from phase1_expansion2 import EXTRA_PREFACE

    sections = pf.SECTIONS + PREFACE_EXPANSION + [PREFACE_DEEP] + EXTRA_PREFACE
    body = render_sections(sections)
    content = (
        r"\chapter*{Preface}" + "\n"
        r"\addcontentsline{toc}{chapter}{Preface}" + "\n"
        r"\label{ch:preface}" + "\n"
        r"\markboth{Preface}{Preface}" + "\n\n"
        + body
    )
    out = LATEX / "chapters" / "preface.tex"
    write_tex(out, content)
    return out


def generate_chapter01() -> Path:
    import chapter01 as ch1
    from phase1_expansion import CHAPTER01_DEEP, CHAPTER01_EXPANSION
    from phase1_expansion2 import EXTRA_CHAPTER01

    sections = merge_expansions(ch1.SECTIONS, CHAPTER01_EXPANSION + CHAPTER01_DEEP + EXTRA_CHAPTER01)
    body = (
        rf"\noindent\textit{{{escape_latex(ch1.CHAPTER_SUBTITLE)}}}\par\vspace{{1em}}" + "\n\n"
        + render_sections(sections, figure_map=fig_map(FIGURE_MAP_CH1))
    )
    return chapter_file(
        LATEX / "chapters" / "chapter01.tex",
        "Threat Landscape and Security Gaps",
        ch1.CHAPTER_SUBTITLE,
        "ch:chapter01",
        body,
    )


def generate_chapter02() -> Path:
    import chapter02 as ch2
    from chapter02_expansion import EXPANSION
    from chapter02_expansion2 import EXPANSION2

    sections = merge_expansions(ch2.SECTIONS, EXPANSION + EXPANSION2)
    body = (
        rf"\noindent\textit{{{escape_latex(ch2.CHAPTER_SUBTITLE)}}}\par\vspace{{1em}}" + "\n\n"
        + render_sections(sections, figure_map=fig_map(FIGURE_MAP_CH2))
    )
    return chapter_file(
        LATEX / "chapters" / "chapter02.tex",
        "ECC-DTB-AKA Authenticated Key Agreement",
        ch2.CHAPTER_SUBTITLE,
        "ch:chapter02",
        body,
    )


def generate_chapter03() -> Path:
    import chapter03 as ch3
    from chapter03_expansion import EXPANSION, EXPANSION2

    sections = merge_expansions(ch3.SECTIONS, EXPANSION + EXPANSION2)
    body = (
        rf"\noindent\textit{{{escape_latex(ch3.CHAPTER_SUBTITLE)}}}\par\vspace{{1em}}" + "\n\n"
        + render_sections(sections, figure_map=fig_map(FIGURE_MAP_CH3))
    )
    return chapter_file(
        LATEX / "chapters" / "chapter03.tex",
        "ECC-HISE Secure Envelope",
        ch3.CHAPTER_SUBTITLE,
        "ch:chapter03",
        body,
    )


def generate_chapter04() -> Path:
    import chapter04 as ch4
    from chapter04_expansion import EXPANSION

    sections = merge_expansions(ch4.SECTIONS, EXPANSION)
    body = (
        rf"\noindent\textit{{{escape_latex(ch4.CHAPTER_SUBTITLE)}}}\par\vspace{{1em}}" + "\n\n"
        + render_sections(sections, figure_map=fig_map(FIGURE_MAP_CH4))
    )
    return chapter_file(
        LATEX / "chapters" / "chapter04.tex",
        "Architecture and Implementation",
        ch4.CHAPTER_SUBTITLE,
        "ch:chapter04",
        body,
    )


def generate_chapter05() -> Path:
    import chapter05 as ch5
    from chapter05_expansion import EXPANSION

    sections = merge_expansions(ch5.SECTIONS, EXPANSION)
    body = (
        rf"\noindent\textit{{{escape_latex(ch5.CHAPTER_SUBTITLE)}}}\par\vspace{{1em}}" + "\n\n"
        + render_sections(sections, figure_map=fig_map(FIGURE_MAP_CH5))
    )
    return chapter_file(
        LATEX / "chapters" / "chapter05.tex",
        "Evaluation and Prior Work",
        ch5.CHAPTER_SUBTITLE,
        "ch:chapter05",
        body,
    )


def generate_conclusions() -> Path:
    import conclusions as conc

    body = render_sections(conc.SECTIONS)
    content = (
        r"\chapter*{Conclusions}" + "\n"
        r"\addcontentsline{toc}{chapter}{Conclusions}" + "\n"
        r"\label{ch:conclusions}" + "\n"
        r"\markboth{Conclusions}{Conclusions}" + "\n\n"
        + body
    )
    out = LATEX / "chapters" / "conclusions.tex"
    write_tex(out, content)
    return out


def generate_appendix() -> Path:
    import appendix as app

    body = render_sections(app.SECTIONS)
    content = (
        r"\chapter{Appendix}" + "\n"
        r"\label{ch:appendix}" + "\n\n"
        + body
    )
    out = LATEX / "chapters" / "appendix.tex"
    write_tex(out, content)
    return out


def generate_references() -> Path:
    import references as refs

    content = (
        r"\clearpage" + "\n"
        r"\phantomsection" + "\n"
        r"\addcontentsline{toc}{chapter}{References}" + "\n"
        r"\label{ch:references}" + "\n\n"
        + render_bibliography(refs.REFERENCES)
    )
    out = LATEX / "chapters" / "references.tex"
    write_tex(out, content)
    return out


def generate_scheme_design() -> Path:
    import scheme_design as sd

    body = render_sections(sd.SECTIONS)
    content = (
        r"\chapter{Scheme Design Document}" + "\n"
        r"\label{ch:scheme-design}" + "\n\n"
        rf"\noindent\textit{{{escape_latex(sd.SUBTITLE)}}}\par\vspace{{1em}}" + "\n\n"
        + body
    )
    out = LATEX / "chapters" / "scheme_design.tex"
    write_tex(out, content)
    return out


def generate_main() -> Path:
    content = r"""\input{preamble.tex}

\begin{document}

\frontmatter
\input{frontmatter/titlepage.tex}
\input{frontmatter/abstract.tex}

% Clickable table of contents, list of figures, list of tables
\tableofcontents
\listoffigures
\listoftables
\clearpage

\mainmatter
\input{chapters/preface.tex}
\input{chapters/chapter01.tex}
\input{chapters/chapter02.tex}
\input{chapters/chapter03.tex}
\input{chapters/chapter04.tex}
\input{chapters/chapter05.tex}
\input{chapters/conclusions.tex}

\appendix
\input{chapters/appendix.tex}
\input{chapters/scheme_design.tex}

% Bibliography with clickable [n] targets
\input{chapters/references.tex}

\end{document}
"""
    out = LATEX / "main.tex"
    write_tex(out, content)
    return out


def generate_readme() -> Path:
    content = """# LaTeX Thesis (Full)

B5 paper, 11pt Times, 1.5 line spacing.

## Contents

- Title page, Abstract
- Clickable Table of Contents / List of Figures / List of Tables (`hyperref`)
- Preface, Chapters 1--5, Conclusions, Appendix
- References (67 entries) with clickable in-text `[n]` citations (`\\hyperref`)
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
"""
    out = LATEX / "README.md"
    write_tex(out, content)
    return out


def main() -> None:
    LATEX.mkdir(parents=True, exist_ok=True)
    (LATEX / "chapters").mkdir(exist_ok=True)
    (LATEX / "frontmatter").mkdir(exist_ok=True)

    files = [
        generate_preamble(),
        generate_titlepage(),
        generate_abstract(),
        generate_preface(),
        generate_chapter01(),
        generate_chapter02(),
        generate_chapter03(),
        generate_chapter04(),
        generate_chapter05(),
        generate_conclusions(),
        generate_appendix(),
        generate_scheme_design(),
        generate_references(),
        generate_main(),
        generate_readme(),
    ]
    for f in files:
        print(f"Saved: {f}")
    print(f"\nBuild: cd Latex && pdflatex main.tex && pdflatex main.tex")


if __name__ == "__main__":
    main()
