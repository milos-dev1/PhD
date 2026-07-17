"""Generate LaTeX thesis files from content modules."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from latex_utils import escape_latex, merge_expansions, render_paragraph, render_sections, write_tex

ROOT = Path(__file__).resolve().parent.parent
LATEX = ROOT / "Latex"
FIG = ROOT / "thesis" / "figures"

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
    "verification. The dissertation contributes original methodologies, algorithms, and implementation "
    "artifacts that advance the state of the art in e-banking cryptographic security."
)


def figure_map_for_latex(name_map: dict[str, str]) -> dict[str, str]:
  return {k: f"../thesis/figures/{v}" for k, v in name_map.items()}


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
\usepackage{hyperref}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{microtype}

\hypersetup{
  colorlinks=true,
  linkcolor=black,
  citecolor=black,
  urlcolor=blue,
  pdftitle={E-Banking ECC Security Thesis},
}

\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}

% Chapter title formatting
\usepackage{titlesec}
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries}{\chaptertitlename\ \thechapter}{20pt}{\Huge}
\titleformat{\section}{\normalfont\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\large\bfseries}{\thesubsection}{1em}{}

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
    + render_paragraph(ABSTRACT.replace("---", "—"))
  )
  out = LATEX / "frontmatter" / "abstract.tex"
  write_tex(out, content)
  return out


def generate_preface() -> Path:
  import preface as pf
  from phase1_expansion import PREFACE_DEEP, PREFACE_EXPANSION
  from phase1_expansion2 import EXTRA_PREFACE

  sections = pf.SECTIONS + PREFACE_EXPANSION + [PREFACE_DEEP] + EXTRA_PREFACE
  body = render_sections(sections, section_cmd="section", subsection_cmd="subsection")
  content = (
    r"\chapter{Preface}" + "\n"
    r"\label{ch:preface}" + "\n\n"
    + body
  )
  out = LATEX / "chapters" / "preface.tex"
  write_tex(out, content)
  return out


def generate_chapter01() -> Path:
  import chapter01 as ch1
  from phase1_expansion import CHAPTER01_DEEP, CHAPTER01_EXPANSION
  from phase1_expansion2 import EXTRA_CHAPTER01

  all_exp = CHAPTER01_EXPANSION + CHAPTER01_DEEP + EXTRA_CHAPTER01
  sections = merge_expansions(ch1.SECTIONS, all_exp)
  fig_map = figure_map_for_latex(FIGURE_MAP_CH1)
  body = render_sections(sections, figure_map=fig_map)
  content = (
    rf"\chapter{{{escape_latex(ch1.CHAPTER_TITLE)}}}" + "\n"
    rf"\chaptermark{{{escape_latex(ch1.CHAPTER_TITLE)}}}" + "\n"
    rf"\label{{ch:chapter01}}" + "\n\n"
    rf"\noindent\textbf{{{escape_latex(ch1.CHAPTER_SUBTITLE)}}}\par" + "\n\n"
    + body
  )
  out = LATEX / "chapters" / "chapter01.tex"
  write_tex(out, content)
  return out


def generate_chapter02() -> Path:
  import chapter02 as ch2
  from chapter02_expansion import EXPANSION
  from chapter02_expansion2 import EXPANSION2

  sections = merge_expansions(ch2.SECTIONS, EXPANSION + EXPANSION2)
  fig_map = figure_map_for_latex(FIGURE_MAP_CH2)
  body = render_sections(sections, figure_map=fig_map)
  content = (
    rf"\chapter{{{escape_latex(ch2.CHAPTER_TITLE)}}}" + "\n"
    rf"\chaptermark{{{escape_latex(ch2.CHAPTER_TITLE)}}}" + "\n"
    rf"\label{{ch:chapter02}}" + "\n\n"
    rf"\noindent\textbf{{{escape_latex(ch2.CHAPTER_SUBTITLE)}}}\par" + "\n\n"
    + body
  )
  out = LATEX / "chapters" / "chapter02.tex"
  write_tex(out, content)
  return out


def generate_scheme_design() -> Path:
  import scheme_design as sd

  body = render_sections(sd.SECTIONS, section_cmd="section", subsection_cmd="subsection")
  content = (
    r"\chapter{Scheme Design Document}" + "\n"
    r"\label{ch:scheme-design}" + "\n\n"
    rf"\noindent\textbf{{{escape_latex(sd.SUBTITLE)}}}\par" + "\n\n"
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
\tableofcontents
\listoffigures
\listoftables
\clearpage

\mainmatter
\input{chapters/preface.tex}
\input{chapters/chapter01.tex}
\input{chapters/chapter02.tex}

\appendix
\input{chapters/scheme_design.tex}

% Placeholders for upcoming chapters
% \input{chapters/chapter03.tex}
% \input{chapters/chapter04.tex}
% \input{chapters/chapter05.tex}
% \input{chapters/conclusions.tex}

\end{document}
"""
  out = LATEX / "main.tex"
  write_tex(out, content)
  return out


def main() -> None:
  LATEX.mkdir(parents=True, exist_ok=True)
  files = [
    generate_preamble(),
    generate_titlepage(),
    generate_abstract(),
    generate_preface(),
    generate_chapter01(),
    generate_chapter02(),
    generate_scheme_design(),
    generate_main(),
  ]
  for f in files:
    print(f"Saved: {f}")


if __name__ == "__main__":
  main()
