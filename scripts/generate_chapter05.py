"""Generate Chapter 5 Word document (B5, 11pt)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from thesis_doc import add_figure, add_paragraph, add_table, create_thesis_document, save_document

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "thesis" / "figures"
FIGURE_MAP = {
    "Figure 5.1": FIG / "fig_5_1_attack_matrix.png",
    "Figure 5.2": FIG / "fig_5_2_combined_benchmark.png",
    "Figure 5.3": FIG / "fig_5_3_tls_handshake.png",
    "Figure 5.4": FIG / "fig_5_4_oauth_pkce.png",
    "Figure 5.5": FIG / "fig_5_5_mtls.png",
    "Figure 5.6": FIG / "fig_5_6_tls_vs_envelope.png",
    "Figure 5.7": FIG / "fig_5_7_merkle_compare.png",
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
    import chapter05 as ch
    return ch, list(ch.SECTIONS)


def generate_chapter05() -> Path:
    ch5, sections = build_sections()
    doc = create_thesis_document()
    doc.add_heading(ch5.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch5.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_sections(doc, sections)
    out = ROOT / "thesis" / "06_chapter05.docx"
    save_document(doc, out)
    return out


if __name__ == "__main__":
    print(f"Saved: {generate_chapter05()}")
