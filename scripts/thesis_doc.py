"""Word document utilities for B5 thesis (11pt)."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

# ISO B5
B5_WIDTH = Mm(176)
B5_HEIGHT = Mm(250)
BODY_FONT = "Times New Roman"
BODY_SIZE = Pt(11)
HEADING_COLOR = RGBColor(0, 0, 0)


def create_thesis_document() -> Document:
    doc = Document()
    section = doc.sections[0]
    section.page_width = B5_WIDTH
    section.page_height = B5_HEIGHT
    section.top_margin = Mm(25)
    section.bottom_margin = Mm(25)
    section.left_margin = Mm(25)
    section.right_margin = Mm(25)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = BODY_SIZE
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    normal.paragraph_format.space_after = Pt(6)

    for level, size in [(1, 16), (2, 14), (3, 12)]:
        style = doc.styles[f"Heading {level}"]
        style.font.name = BODY_FONT
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = HEADING_COLOR
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(6)

    return doc


def add_title_page(doc: Document, title: str, subtitle: str, degree: str) -> None:
    for _ in range(6):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(16)
    run.font.name = BODY_FONT

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run(subtitle)
    r2.font.size = Pt(12)
    r2.font.name = BODY_FONT

    for _ in range(8):
        doc.add_paragraph()
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run(degree)
    r3.font.size = Pt(12)
    r3.font.name = BODY_FONT
    doc.add_page_break()


def add_paragraph(doc: Document, text: str, *, bold: bool = False, indent: bool = False) -> None:
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.first_line_indent = Mm(10)
    run = p.add_run(text)
    run.font.name = BODY_FONT
    run.font.size = BODY_SIZE
    run.bold = bold


def add_bullet(doc: Document, text: str) -> None:
    p = doc.add_paragraph(text, style="List Bullet")
    for run in p.runs:
        run.font.name = BODY_FONT
        run.font.size = BODY_SIZE


def add_numbered(doc: Document, text: str) -> None:
    p = doc.add_paragraph(text, style="List Number")
    for run in p.runs:
        run.font.name = BODY_FONT
        run.font.size = BODY_SIZE


def add_figure(doc: Document, image_path: Path | None, caption: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if image_path and image_path.exists():
        run = p.add_run()
        run.add_picture(str(image_path), width=Mm(140))
    else:
        run = p.add_run(f"[Figure: {caption}]")
        run.italic = True
        run.font.size = Pt(10)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr = cap.add_run(caption)
    cr.font.size = Pt(10)
    cr.font.name = BODY_FONT
    cr.italic = True


def add_figure_placeholder(doc: Document, caption: str) -> None:
    add_figure(doc, None, caption)


def add_table(doc: Document, headers: list[str], rows: list[list[str]], caption: str) -> None:
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(10)
                r.font.name = BODY_FONT
    for ri, row in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, val in enumerate(row):
            cells[ci].text = val
            for p in cells[ci].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
                    r.font.name = BODY_FONT
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr = cap.add_run(caption)
    cr.font.size = Pt(10)
    cr.font.name = BODY_FONT
    cr.italic = True
    doc.add_paragraph()


def save_document(doc: Document, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
