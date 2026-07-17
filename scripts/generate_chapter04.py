"""Generate Chapter 4 Word document (B5, 11pt)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from thesis_doc import add_figure, add_paragraph, add_table, create_thesis_document, save_document

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "thesis" / "figures"
FIGURE_MAP = {
    "Figure 4.1": FIG / "fig_4_1_architecture.png",
    "Figure 4.2": FIG / "fig_4_2_flow.png",
    "Figure 4.3": FIG / "fig_4_3_dtb_modules.png",
    "Figure 4.4": FIG / "fig_4_4_hise_modules.png",
    "Figure 4.5": FIG / "fig_4_5_deployment.png",
}


def render_sections(doc, sections) -> None:
    for section in sections:
        doc.add_heading(section["heading"], level=2)
        for para in section.get("paragraphs", []):
            add_paragraph(doc, para, indent=True)
        for sub in section.get("subsections", []):
            doc.add_heading(sub["heading"], level=3)
            for para in sub.get("paragraphs", []):
                add_paragraph(doc, para, indent=True)
            if "table" in sub:
                t = sub["table"]
                add_table(doc, t["headers"], t["rows"], t["caption"])
            if "figure" in sub:
                cap = sub["figure"]
                img = next((v for k, v in FIGURE_MAP.items() if k in cap), None)
                add_figure(doc, img, cap)


def build_sections():
    import chapter04 as ch4
    from chapter04_expansion import EXPANSION

    sections = []
    for section in ch4.SECTIONS:
        merged = dict(section)
        extra = [s for e in EXPANSION if e["parent_section"] == section["heading"] for s in e["subsections"]]
        if extra:
            merged["subsections"] = list(section.get("subsections", [])) + extra
        sections.append(merged)
    return ch4, sections


def generate_chapter04() -> Path:
    ch4, sections = build_sections()
    doc = create_thesis_document()
    doc.add_heading(ch4.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch4.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_sections(doc, sections)
    out = ROOT / "thesis" / "05_chapter04.docx"
    save_document(doc, out)
    return out


if __name__ == "__main__":
    print(f"Saved: {generate_chapter04()}")
