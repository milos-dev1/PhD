"""LaTeX conversion utilities for thesis content."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def strip_manual_number(heading: str) -> str:
  """Remove leading manual numbers (e.g. '2.1 Title') — LaTeX numbers sections."""
  return re.sub(r"^\d+(\.\d+)+\s+", "", heading).strip()


def escape_latex(text: str) -> str:
  text = str(text)
  text = text.replace("—", "---").replace("–", "--")
  # Subscripts: PK_C -> PK\textsubscript{C}
  text = re.sub(r"([A-Za-z0-9]+)_([A-Za-z0-9]+)", r"\1\\textsubscript{\2}", text)
  replacements = (
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
  )
  for old, new in replacements:
    text = text.replace(old, new)
  return text


def render_paragraph(text: str, *, indent: bool = True) -> str:
  prefix = r"\indent " if indent else ""
  return f"{prefix}{escape_latex(text)}\n\n"


def render_table(table: dict[str, Any]) -> str:
  headers = table["headers"]
  rows = table["rows"]
  caption = escape_latex(table["caption"])
  cols = "l" * len(headers)
  lines = [
    r"\begin{table}[htbp]",
    r"\centering",
    rf"\begin{{tabular}}{{{cols}}}",
    r"\toprule",
    " & ".join(escape_latex(h) for h in headers) + r" \\",
    r"\midrule",
  ]
  for row in rows:
    lines.append(" & ".join(escape_latex(c) for c in row) + r" \\")
  lines.extend([r"\bottomrule", r"\end{tabular}", rf"\caption{{{caption}}}", r"\end{table}", ""])
  return "\n".join(lines)


def render_figure(caption: str, figure_map: dict[str, str]) -> str:
  img: str | None = None
  for key, path in figure_map.items():
    if key in caption:
      img = path
      break
  cap = escape_latex(caption)
  if img:
    return (
      r"\begin{figure}[htbp]" + "\n"
      r"\centering" + "\n"
      rf"\includegraphics[width=0.92\linewidth]{{{img}}}" + "\n"
      rf"\caption{{{cap}}}" + "\n"
      r"\end{figure}" + "\n\n"
    )
  return rf"% [Figure not found: {cap}]" + "\n\n"


def render_sections(
  sections: list[dict[str, Any]],
  figure_map: dict[str, str] | None = None,
  section_cmd: str = "section",
  subsection_cmd: str = "subsection",
) -> str:
  figure_map = figure_map or {}
  parts: list[str] = []
  for section in sections:
    parts.append(rf"\{section_cmd}{{{escape_latex(strip_manual_number(section['heading']))}}}")
    parts.append("")
    for para in section.get("paragraphs", []):
      parts.append(render_paragraph(para))
    for sub in section.get("subsections", []):
      parts.append(rf"\{subsection_cmd}{{{escape_latex(strip_manual_number(sub['heading']))}}}")
      parts.append("")
      for para in sub.get("paragraphs", []):
        parts.append(render_paragraph(para))
      if "table" in sub:
        parts.append(render_table(sub["table"]))
      if "figure" in sub:
        parts.append(render_figure(sub["figure"], figure_map))
  return "".join(parts)


def merge_expansions(base_sections: list[dict], expansions: list[dict]) -> list[dict]:
  merged_sections = []
  for section in base_sections:
    merged = dict(section)
    extra = [
      s
      for e in expansions
      if e.get("parent_section") == section["heading"]
      for s in e.get("subsections", [])
    ]
    if extra:
      merged["subsections"] = list(section.get("subsections", [])) + extra
    merged_sections.append(merged)
  return merged_sections


def write_tex(path: Path, content: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(content, encoding="utf-8")
