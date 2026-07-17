"""Generate conclusions and appendix Word documents."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "content"))

from generate_phase1 import render_sections
from thesis_doc import create_thesis_document, save_document

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    import appendix as app
    import conclusions as conc

    for mod, name in [(conc, "07_conclusions.docx"), (app, "08_appendix.docx")]:
        doc = create_thesis_document()
        doc.add_heading(mod.TITLE, level=1)
        render_sections(doc, mod.SECTIONS)
        path = ROOT / "thesis" / name
        save_document(doc, path)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
