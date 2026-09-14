"""Verify citation hyperlinks and bookmarks in full_thesis.docx."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "thesis" / "full_thesis.docx"
xml = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8", "ignore")
anchors = set(re.findall(r'w:anchor="(ref_\d+)"', xml))
bookmarks = set(re.findall(r'w:name="(ref_\d+)"', xml))
print("hyperlinks", len(re.findall(r"w:hyperlink", xml)))
print("cite anchors", len(anchors))
print("ref bookmarks", len(bookmarks))
print("anchors missing bookmarks", sorted(anchors - bookmarks))
print("bookmarks unused", sorted(bookmarks - anchors)[:20], "..." if len(bookmarks - anchors) > 20 else "")
print("has TOC", "sec_table_of_contents" in xml)
print("has References bookmark", "sec_references" in xml)
print("MB", round(p.stat().st_size / 1e6, 2))
