"""Generate Scheme Design Document (Word, B5, 11pt)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from thesis_doc import add_paragraph, create_thesis_document, save_document

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "content"))
import scheme_design as sd


def main() -> None:
    doc = create_thesis_document()
    doc.add_heading(sd.TITLE, level=1)
    add_paragraph(doc, sd.SUBTITLE, bold=True)
    doc.add_paragraph()

    for section in sd.SECTIONS:
        doc.add_heading(section["heading"], level=2)
        for para in section["paragraphs"]:
            add_paragraph(doc, para, indent=True)
        for sub in section.get("subsections", []):
            doc.add_heading(sub["heading"], level=3)
            for para in sub["paragraphs"]:
                add_paragraph(doc, para, indent=True)

    out = ROOT / "thesis" / "00_scheme_design.docx"
    save_document(doc, out)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
