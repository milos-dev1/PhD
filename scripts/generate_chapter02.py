"""Generate Chapter 2 Word document (B5, 11pt)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from thesis_doc import add_figure, add_paragraph, add_table, create_thesis_document, save_document

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "thesis" / "figures"
FIGURE_MAP = {
    "Figure 2.1": FIG / "fig_2_1_protocol_sequence.png",
    "Figure 2.2": FIG / "fig_2_2_key_derivation.png",
    "Figure 2.3": FIG / "fig_2_3_benchmark_chart.png",
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
    import chapter02 as ch
    return ch, list(ch.SECTIONS)


def generate_chapter02() -> Path:
    ch2, sections = build_sections()
    doc = create_thesis_document()
    doc.add_heading(ch2.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch2.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_sections(doc, sections)
    out = ROOT / "thesis" / "03_chapter02.docx"
    save_document(doc, out)
    return out


if __name__ == "__main__":
    path = generate_chapter02()
    print(f"Saved: {path}")
