"""Generate Chapter 3 Word document (B5, 11pt)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from thesis_doc import add_figure, add_paragraph, add_table, create_thesis_document, save_document

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "thesis" / "figures"
FIGURE_MAP = {
    "Figure 3.1": FIG / "fig_3_1_hierarchy.png",
    "Figure 3.2": FIG / "fig_3_2_envelope.png",
    "Figure 3.3": FIG / "fig_3_3_verify_flow.png",
    "Figure 3.4": FIG / "fig_3_4_benchmark.png",
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
    import chapter03 as ch
    return ch, list(ch.SECTIONS)


def generate_chapter03() -> Path:
    ch3, sections = build_sections()
    doc = create_thesis_document()
    doc.add_heading(ch3.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch3.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_sections(doc, sections)
    out = ROOT / "thesis" / "04_chapter03.docx"
    save_document(doc, out)
    return out


if __name__ == "__main__":
    print(f"Saved: {generate_chapter03()}")
