"""LaTeX conversion utilities for thesis content."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# Same keyword map as Word thesis_doc for consistent auto-citations
CITATION_KEYWORDS: list[tuple[str, list[int]]] = [
    ("TLS 1.3", [1]),
    ("TLS", [1, 28]),
    ("AES-GCM", [2]),
    ("AES-256", [2]),
    ("key management", [3]),
    ("X.509", [4]),
    ("certificate", [4]),
    ("HKDF", [5, 6]),
    ("authenticated key", [7, 8]),
    ("ECDSA", [9, 26]),
    ("Ed25519", [10]),
    ("EdDSA", [10]),
    ("elliptic curve", [11, 34, 35]),
    ("ECDH", [12, 29]),
    ("OAuth", [13, 14]),
    ("PKCE", [14]),
    ("FIDO", [15]),
    ("WebAuthn", [15]),
    ("EMV", [16]),
    ("PCI DSS", [17]),
    ("PSD2", [18]),
    ("ISO/IEC 27001", [19]),
    ("SWIFT", [20, 24]),
    ("data breach", [21, 22]),
    ("OWASP", [23]),
    ("Bangladesh", [24]),
    ("Carbanak", [25]),
    ("SHA-256", [27]),
    ("Merkle", [30]),
    ("Bitcoin", [31]),
    ("blockchain", [31, 32]),
    ("Corda", [32]),
    ("Diffie-Hellman", [33]),
    ("post-quantum", [54]),
    ("Curve25519", [55]),
    ("ECIES", [56]),
    ("ProVerif", [66]),
    ("Tamarin", [65]),
    ("e-banking", [63, 64]),
    ("phishing", [22]),
    ("forward secrecy", [1, 8]),
]


def strip_manual_number(heading: str) -> str:
    return re.sub(r"^\d+(\.\d+)+\s+", "", heading).strip()


def inject_citations(text: str) -> str:
    if re.search(r"\[\d+", text):
        return text
    found: list[int] = []
    lower = text.lower()
    for keyword, refs in CITATION_KEYWORDS:
        if keyword.lower() in lower:
            for r in refs:
                if r not in found:
                    found.append(r)
            if len(found) >= 3:
                break
    if not found:
        return text
    cites = "".join(f"[{n}]" for n in found[:3])
    if text.rstrip().endswith("."):
        return text.rstrip()[:-1] + f" {cites}."
    return text.rstrip() + f" {cites}"


def escape_latex(text: str) -> str:
    text = str(text)
    text = text.replace("—", "---").replace("–", "--")
    text = text.replace("→", r"$\rightarrow$").replace("←", r"$\leftarrow$")
    text = text.replace("×", r"$\times$").replace("≈", r"$\approx$")
    text = text.replace("∈", r"$\in$").replace("≤", r"$\leq$").replace("≥", r"$\geq$")
    # Subscripts: PK_C -> PK\textsubscript{C} (before escaping remaining _)
    text = re.sub(r"([A-Za-z0-9]+)_([A-Za-z0-9]+)", r"\1\\textsubscript{\2}", text)
    replacements = (
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    )
    # Protect already-inserted LaTeX commands from escaping
    placeholders: list[str] = []

    def protect(m: re.Match) -> str:
        placeholders.append(m.group(0))
        return f"<<<PH{len(placeholders) - 1}>>>"

    text = re.sub(
        r"\\(?:textsubscript|textbackslash|textasciitilde|textasciicircum|rightarrow|leftarrow|times|approx|in|leq|geq)(?:\{[^}]*\})?",
        protect,
        text,
    )
    text = re.sub(r"\$[^$]+\$", protect, text)

    for old, new in replacements:
        text = text.replace(old, new)

    for i, ph in enumerate(placeholders):
        text = text.replace(f"<<<PH{i}>>>", ph)
    return text


def convert_citations(text: str) -> str:
    """Turn [1] or [1,2] into clickable \\hyperref links to bibliography."""

    def repl(m: re.Match) -> str:
        nums = [int(x.strip()) for x in m.group(1).split(",")]
        parts = []
        for i, n in enumerate(nums):
            if i > 0:
                parts.append(",")
            parts.append(rf"\hyperref[ref:{n}]{{[{n}]}}")
        return "".join(parts)

    return re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", repl, text)


def render_paragraph(text: str, *, indent: bool = True, auto_cite: bool = True) -> str:
    if auto_cite:
        text = inject_citations(text)
    # Escape first, but protect citation markers then convert
    # Split on citations so we don't escape inside hyperref commands
    parts = re.split(r"(\[\d+(?:\s*,\s*\d+)*\])", text)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if re.fullmatch(r"\[\d+(?:\s*,\s*\d+)*\]", part):
            out.append(convert_citations(part))
        else:
            out.append(escape_latex(part))
    body = "".join(out)
    prefix = r"\indent " if indent else ""
    return f"{prefix}{body}\n\n"


def render_table(table: dict[str, Any]) -> str:
    headers = table["headers"]
    rows = table["rows"]
    caption = escape_latex(table["caption"])
    label = ""
    m = re.search(r"Table\s+(\d+)\.(\d+)", table["caption"], re.I)
    if m:
        label = rf"\label{{tbl:{m.group(1)}.{m.group(2)}}}"
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
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            rf"\caption{{{caption}}}{label}",
            r"\end{table}",
            "",
        ]
    )
    return "\n".join(lines)


def render_figure(caption: str, figure_map: dict[str, str]) -> str:
    img: str | None = None
    for key, path in figure_map.items():
        if key in caption:
            img = path
            break
    cap = escape_latex(caption)
    label = ""
    m = re.search(r"Figure\s+(\d+)\.(\d+)", caption, re.I)
    if m:
        label = rf"\label{{fig:{m.group(1)}.{m.group(2)}}}"
    if img:
        return (
            r"\begin{figure}[htbp]" + "\n"
            r"\centering" + "\n"
            rf"\includegraphics[width=0.92\linewidth]{{{img}}}" + "\n"
            rf"\caption{{{cap}}}{label}" + "\n"
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
        title = escape_latex(strip_manual_number(section["heading"]))
        parts.append(rf"\{section_cmd}{{{title}}}" + "\n\n")
        for para in section.get("paragraphs", []):
            parts.append(render_paragraph(para))
        for sub in section.get("subsections", []):
            st = escape_latex(strip_manual_number(sub["heading"]))
            parts.append(rf"\{subsection_cmd}{{{st}}}" + "\n\n")
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


def render_bibliography(references: list[tuple]) -> str:
    lines = [r"\begin{thebibliography}{99}", ""]
    for i, ref in enumerate(references, 1):
        authors, title, venue, year = ref[:4]
        extra = ref[4] if len(ref) > 4 else ""
        entry = (
            f"{escape_latex(authors)}. ``{escape_latex(title)}.'' "
            f"{escape_latex(venue)}, {escape_latex(year)}."
        )
        if extra:
            entry += f" {escape_latex(extra)}"
        lines.append(rf"\bibitem[{i}]{{ref{i}}}")
        lines.append(rf"\phantomsection\label{{ref:{i}}}")
        lines.append(entry)
        lines.append("")
    lines.append(r"\end{thebibliography}")
    lines.append("")
    return "\n".join(lines)
