"""Assemble final thesis with clickable TOC, citations, page numbers, and references."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from generate_chapter02 import FIGURE_MAP as FIG2, build_sections as build_ch2
from generate_chapter03 import FIGURE_MAP as FIG3, build_sections as build_ch3
from generate_chapter04 import FIGURE_MAP as FIG4, build_sections as build_ch4
from generate_chapter05 import FIGURE_MAP as FIG5, build_sections as build_ch5
from thesis_doc import (
    add_figure,
    add_heading_bookmarked,
    add_paragraph,
    add_references,
    add_clickable_list,
    add_clickable_toc,
    add_table,
    add_title_page,
    bookmark_name_for_figure,
    bookmark_name_for_heading,
    bookmark_name_for_table,
    create_thesis_document,
    save_document,
    update_word_fields,
)

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "thesis" / "figures"
FIG1 = {
    "Figure 1.1": FIG / "fig_1_1_attack_lifecycle.png",
    "Figure 1.2": FIG / "fig_1_2_client_auth_flow.png",
    "Figure 1.3": FIG / "fig_1_3_server_mesh.png",
    "Figure 1.4": FIG / "fig_1_4_data_layers.png",
    "Figure 1.5": FIG / "fig_1_5_threat_model.png",
}

THESIS_TITLE = (
    "A Dual-Layer ECC Methodology for Client-Server Authentication\n"
    "and Server-Server Data Protection in Electronic Finance Systems"
)

ABSTRACT = (
    "This dissertation investigates information security challenges in electronic banking and "
    "electronic finance service systems, with particular emphasis on authentication, key exchange, "
    "data encryption, and integrity protection. A comprehensive analysis of contemporary attack "
    "mechanisms establishes the threat landscape and identifies critical limitations in existing "
    "security mechanisms. Two novel elliptic curve cryptography (ECC) based schemes are proposed: "
    "ECC-DTB-AKA (Device- and Transaction-Bound Authenticated Key Agreement) for client-server "
    "channels, and ECC-HISE (Hierarchical Integrity-preserving Secure Envelope) for server-server "
    "batch data transfer. Both schemes are formally analyzed, quantitatively evaluated against "
    "established baselines, and implemented in a working software prototype."
)


def render_sections(doc, sections) -> None:
    for section in sections:
        add_heading_bookmarked(doc, section["heading"], level=2)
        for para in section.get("paragraphs", []):
            add_paragraph(doc, para, indent=True)
        for sub in section.get("subsections", []):
            add_heading_bookmarked(doc, sub["heading"], level=3)
            for para in sub.get("paragraphs", []):
                add_paragraph(doc, para, indent=True)


def render_with_figures(doc, sections, figure_map) -> None:
    for section in sections:
        add_heading_bookmarked(doc, section["heading"], level=2)
        for para in section.get("paragraphs", []):
            add_paragraph(doc, para, indent=True)
        for sub in section.get("subsections", []):
            add_heading_bookmarked(doc, sub["heading"], level=3)
            for para in sub.get("paragraphs", []):
                add_paragraph(doc, para, indent=True)
            if "table" in sub:
                t = sub["table"]
                add_table(doc, t["headers"], t["rows"], t["caption"])
            if "figure" in sub:
                cap = sub["figure"]
                img = next((v for k, v in figure_map.items() if k in cap), None)
                add_figure(doc, img, cap)


def build_ch1_sections():
    import chapter01 as ch1
    return ch1, list(ch1.SECTIONS)


def build_full_toc_entries() -> list[tuple[str, str | None, str]]:
    """(display, subtitle, bookmark)."""
    import chapter01 as c1
    import chapter02 as c2
    import chapter03 as c3
    import chapter04 as c4
    import chapter05 as c5
    import conclusions as conc
    import appendix as app

    entries: list[tuple[str, str | None, str]] = [
        ("Abstract", None, bookmark_name_for_heading("Abstract")),
        ("Preface", None, bookmark_name_for_heading("Preface")),
    ]
    for mod, subtitle in [
        (c1, c1.CHAPTER_SUBTITLE),
        (c2, c2.CHAPTER_SUBTITLE),
        (c3, c3.CHAPTER_SUBTITLE),
        (c4, c4.CHAPTER_SUBTITLE),
        (c5, c5.CHAPTER_SUBTITLE),
    ]:
        entries.append((mod.CHAPTER_TITLE, subtitle, bookmark_name_for_heading(mod.CHAPTER_TITLE)))
        for sec in mod.SECTIONS:
            entries.append((f"  {sec['heading']}", None, bookmark_name_for_heading(sec["heading"])))
    entries.append((conc.TITLE, None, bookmark_name_for_heading(conc.TITLE)))
    entries.append((app.TITLE, None, bookmark_name_for_heading(app.TITLE)))
    entries.append(("References", None, "sec_references"))
    return entries


def build_lof_lot():
    from index_metadata import FIGURES, TABLES

    figs = []
    for cap in FIGURES:
        bm = bookmark_name_for_figure(cap)
        if bm:
            figs.append((cap, bm))
    tbls = []
    for cap in TABLES:
        bm = bookmark_name_for_table(cap)
        if bm:
            tbls.append((cap, bm))
    return figs, tbls


def generate_final_thesis() -> Path:
    import appendix as app
    import conclusions as conc
    import preface as pf
    import references as refs
    from phase1_expansion import PREFACE_DEEP, PREFACE_EXPANSION
    from phase1_expansion2 import EXTRA_PREFACE

    ch1, ch1_sections = build_ch1_sections()
    ch2, ch2_sections = build_ch2()
    ch3, ch3_sections = build_ch3()
    ch4, ch4_sections = build_ch4()
    ch5, ch5_sections = build_ch5()
    pf_sections = pf.SECTIONS + PREFACE_EXPANSION + [PREFACE_DEEP] + EXTRA_PREFACE
    figs, tbls = build_lof_lot()

    doc = create_thesis_document()

    add_title_page(
        doc,
        THESIS_TITLE,
        "PhD Dissertation in Information Security",
        "Submitted in partial fulfillment of the requirements\nfor the degree of Doctor of Philosophy",
    )

    add_heading_bookmarked(doc, "Abstract", level=1)
    add_paragraph(doc, ABSTRACT, indent=True)
    doc.add_page_break()

    add_clickable_toc(doc, build_full_toc_entries())
    add_clickable_list(doc, "List of Figures", figs)
    add_clickable_list(doc, "List of Tables", tbls)

    add_heading_bookmarked(doc, "Preface", level=1)
    render_sections(doc, pf_sections)
    doc.add_page_break()

    add_heading_bookmarked(doc, ch1.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch1.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_with_figures(doc, ch1_sections, FIG1)
    doc.add_page_break()

    add_heading_bookmarked(doc, ch2.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch2.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_with_figures(doc, ch2_sections, FIG2)
    doc.add_page_break()

    add_heading_bookmarked(doc, ch3.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch3.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_with_figures(doc, ch3_sections, FIG3)
    doc.add_page_break()

    add_heading_bookmarked(doc, ch4.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch4.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_with_figures(doc, ch4_sections, FIG4)
    doc.add_page_break()

    add_heading_bookmarked(doc, ch5.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch5.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_with_figures(doc, ch5_sections, FIG5)
    doc.add_page_break()

    add_heading_bookmarked(doc, conc.TITLE, level=1)
    render_sections(doc, list(conc.SECTIONS))
    doc.add_page_break()

    add_heading_bookmarked(doc, app.TITLE, level=1)
    render_sections(doc, app.SECTIONS)
    doc.add_page_break()

    add_references(doc, refs.REFERENCES)

    out = ROOT / "thesis" / "full_thesis.docx"
    try:
        save_document(doc, out)
    except PermissionError:
        out = ROOT / "thesis" / "full_thesis_assembled.docx"
        save_document(doc, out)
    return out


def main() -> None:
    from generate_figures_ch1 import (
        fig_1_1_attack_lifecycle,
        fig_1_2_client_auth_flow,
        fig_1_3_server_mesh,
        fig_1_4_data_layers,
        fig_1_5_threat_model,
    )

    for fn in [
        fig_1_1_attack_lifecycle,
        fig_1_2_client_auth_flow,
        fig_1_3_server_mesh,
        fig_1_4_data_layers,
        fig_1_5_threat_model,
    ]:
        try:
            fn()
        except Exception:
            pass

    for s in [
        "generate_figures_ch2.py",
        "generate_figures_ch3.py",
        "generate_figures_ch4.py",
        "generate_figures_ch5.py",
    ]:
        subprocess.run([sys.executable, str(ROOT / "scripts" / s)], check=False)

    path = generate_final_thesis()
    print(f"Saved: {path}")
    print("Features: page numbers, clickable TOC/LOF/LOT, hyperlinked [n] citations -> References")

    if update_word_fields(path):
        print("Updated PAGE fields via Microsoft Word.")
    else:
        print("Tip: In Word press Ctrl+A then F9 to refresh page numbers.")


if __name__ == "__main__":
    main()
