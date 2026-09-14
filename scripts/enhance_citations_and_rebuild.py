"""
Prune uncited bibliography entries, renumber cited ones contiguously,
update citation keywords + explicit [n] markers, rebuild index metadata,
download cited reference PDFs, and regenerate Word + LaTeX theses.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
CONTENT = ROOT / "content"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(CONTENT))

from citations import (  # noqa: E402
    CITATION_KEYWORDS,
    extract_citation_numbers,
    inject_citations,
    remap_citations_in_text,
)


def iter_paragraphs() -> list[str]:
    """Collect all thesis body paragraphs that receive auto-citation."""
    import appendix as app
    import chapter01 as c1
    import chapter02 as c2
    import chapter03 as c3
    import chapter04 as c4
    import chapter05 as c5
    import conclusions as conc
    import preface as pf
    from generate_chapter02 import build_sections as build_ch2
    from generate_chapter03 import build_sections as build_ch3
    from generate_chapter04 import build_sections as build_ch4
    from generate_chapter05 import build_sections as build_ch5
    from generate_full_thesis import ABSTRACT, build_ch1_sections
    from phase1_expansion import PREFACE_DEEP, PREFACE_EXPANSION
    from phase1_expansion2 import EXTRA_PREFACE

    paras: list[str] = [ABSTRACT]
    _, ch1_sections = build_ch1_sections()
    for sections in (
        pf.SECTIONS + PREFACE_EXPANSION + [PREFACE_DEEP] + EXTRA_PREFACE,
        ch1_sections,
        build_ch2()[1],
        build_ch3()[1],
        build_ch4()[1],
        build_ch5()[1],
        conc.SECTIONS,
        app.SECTIONS,
    ):
        for section in sections:
            paras.extend(section.get("paragraphs", []))
            for sub in section.get("subsections", []):
                paras.extend(sub.get("paragraphs", []))
    # Also scan raw chapter modules for any leftover explicit cites
    for mod in (c1, c2, c3, c4, c5, pf, conc, app):
        for section in getattr(mod, "SECTIONS", []):
            paras.extend(section.get("paragraphs", []))
            for sub in section.get("subsections", []):
                paras.extend(sub.get("paragraphs", []))
    return paras


def collect_cited_refs() -> set[int]:
    cited: set[int] = set()
    for para in iter_paragraphs():
        text = inject_citations(para)
        cited |= extract_citation_numbers(text)
    return cited


def load_references() -> list[tuple]:
    import references as refs

    return list(refs.REFERENCES)


def write_references_py(new_refs: list[tuple]) -> None:
    path = CONTENT / "references.py"
    lines = [
        '"""Bibliography for the PhD thesis (numbered references)."""',
        "",
        'TITLE = "References"',
        "",
        "# Only references cited in the thesis body (contiguous numbering).",
        "# Each entry: (authors, title, venue, year, optional_url_or_doi)",
        "REFERENCES = [",
    ]
    for ref in new_refs:
        authors, title, venue, year = ref[:4]
        extras = ref[4:]
        # repr for safe escaping
        if extras:
            lines.append(
                f"    ({authors!r}, {title!r}, {venue!r}, {year!r}, {extras[0]!r}),"
            )
        else:
            lines.append(f"    ({authors!r}, {title!r}, {venue!r}, {year!r}),")
    lines.append("]")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_citations_py(mapping: dict[int, int]) -> None:
    """Rewrite CITATION_KEYWORDS with renumbered refs; drop empty mappings."""
    path = SCRIPTS / "citations.py"
    text = path.read_text(encoding="utf-8")
    # Rebuild keyword list
    new_kw: list[tuple[str, list[int]]] = []
    for keyword, refs in CITATION_KEYWORDS:
        mapped = []
        for r in refs:
            if r in mapping and mapping[r] not in mapped:
                mapped.append(mapping[r])
        if mapped:
            new_kw.append((keyword, mapped))

    kw_lines = ["CITATION_KEYWORDS: list[tuple[str, list[int]]] = ["]
    for keyword, refs in new_kw:
        kw_lines.append(f"    ({keyword!r}, {refs}),")
    kw_lines.append("]")
    new_block = "\n".join(kw_lines)

    pattern = re.compile(
        r"CITATION_KEYWORDS: list\[tuple\[str, list\[int\]\]\] = \[.*?\]\n",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise RuntimeError("Could not locate CITATION_KEYWORDS block")
    path.write_text(pattern.sub(new_block + "\n", text, count=1), encoding="utf-8")


def remap_content_files(mapping: dict[int, int]) -> int:
    """Update explicit [n] citations inside content/*.py string literals."""
    changed_files = 0
    for path in sorted(CONTENT.glob("*.py")):
        if path.name in {"references.py", "index_metadata.py"}:
            continue
        original = path.read_text(encoding="utf-8")
        # Only rewrite citation-like brackets in the file text
        updated = remap_citations_in_text(original, mapping)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1
    return changed_files


def patch_generators_to_shared_citations() -> None:
    """Ensure thesis_doc.py and latex_utils.py import shared citations module."""
    for name in ("thesis_doc.py", "latex_utils.py"):
        path = SCRIPTS / name
        text = path.read_text(encoding="utf-8")
        if "from citations import" in text:
            # Still strip local CITATION_KEYWORDS / inject_citations duplicates
            pass
        # Remove local CITATION_KEYWORDS block if present
        text2 = re.sub(
            r"\n# Keyword -> reference.*?\nCITATION_KEYWORDS: list\[tuple\[str, list\[int\]\]\] = \[.*?\]\n\n",
            "\nfrom citations import CITATION_KEYWORDS, inject_citations\n\n",
            text,
            count=1,
            flags=re.DOTALL,
        )
        if text2 == text:
            # latex_utils may have slightly different header comment
            text2 = re.sub(
                r"\nCITATION_KEYWORDS: list\[tuple\[str, list\[int\]\]\] = \[.*?\]\n\n",
                "\nfrom citations import CITATION_KEYWORDS, inject_citations\n\n",
                text,
                count=1,
                flags=re.DOTALL,
            )
        # Remove local inject_citations function if still present
        text2 = re.sub(
            r"\ndef inject_citations\(text: str(?:, \*, max_cites: int = 3)?\) -> str:.*?return text\.rstrip\(\) \+ f\" \{cites\}\"\n\n",
            "\n",
            text2,
            count=1,
            flags=re.DOTALL,
        )
        # Avoid double import
        if text2.count("from citations import") > 1:
            # keep first only
            parts = text2.split("from citations import")
            text2 = parts[0] + "from citations import" + parts[1]
            for extra in parts[2:]:
                # drop the import line
                text2 += re.sub(r"^[^\n]*\n", "", extra, count=1)
        if "from citations import" not in text2:
            # insert after imports
            text2 = text2.replace(
                "from __future__ import annotations\n",
                "from __future__ import annotations\n\nfrom citations import CITATION_KEYWORDS, inject_citations\n",
                1,
            )
        path.write_text(text2, encoding="utf-8")


def rebuild_index_metadata() -> None:
    """Rebuild TOC/figure/table index metadata from chapter modules."""
    import chapter01 as c1
    import chapter02 as c2
    import chapter03 as c3
    import chapter04 as c4
    import chapter05 as c5
    import conclusions as conc
    import appendix as app
    from index_metadata import FIGURES, TABLES  # keep figure/table captions

    chapters = [
        ("Chapter 1", c1.CHAPTER_SUBTITLE),
        ("Chapter 2", c2.CHAPTER_SUBTITLE),
        ("Chapter 3", c3.CHAPTER_SUBTITLE),
        ("Chapter 4", c4.CHAPTER_SUBTITLE),
        ("Chapter 5", c5.CHAPTER_SUBTITLE),
        (conc.TITLE, None),
        (app.TITLE, None),
        ("References", None),
    ]

    # Collect section headings for a richer TOC index
    section_index: list[tuple[str, str]] = []
    for mod, label in [
        (c1, "1"),
        (c2, "2"),
        (c3, "3"),
        (c4, "4"),
        (c5, "5"),
    ]:
        for sec in mod.SECTIONS:
            section_index.append((label, sec["heading"]))

    path = CONTENT / "index_metadata.py"
    lines = [
        '"""Static index metadata for TOC, figures, and tables (rebuilt)."""',
        "",
        "FRONT_MATTER = [",
        '    ("Abstract", 1),',
        '    ("Preface", 1),',
        "]",
        "",
        "CHAPTERS = [",
    ]
    for title, subtitle in chapters:
        lines.append(f"    ({title!r}, {subtitle!r}),")
    lines.append("]")
    lines.append("")
    lines.append("SECTION_INDEX = [")
    for chap, heading in section_index:
        lines.append(f"    ({chap!r}, {heading!r}),")
    lines.append("]")
    lines.append("")
    lines.append("FIGURES = [")
    for fig in FIGURES:
        lines.append(f"    {fig!r},")
    lines.append("]")
    lines.append("")
    lines.append("TABLES = [")
    for tbl in TABLES:
        lines.append(f"    {tbl!r},")
    lines.append("]")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def download_cited(new_count: int, mapping: dict[int, int]) -> None:
    """Download PDFs for newly numbered cited refs; skip failures."""
    pdf_dir = ROOT / "references" / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Best-effort: copy any old-numbered usable PDF to new number if missing
    reverse = {new: old for old, new in mapping.items()}
    for new_num in range(1, new_count + 1):
        if any(
            p.suffix.lower() in {".pdf", ".html"} and p.stat().st_size > 5000
            for p in pdf_dir.glob(f"{new_num:02d}_*")
        ):
            # Verify magic for pdfs
            good = False
            for p in pdf_dir.glob(f"{new_num:02d}_*"):
                data = p.read_bytes()[:8]
                if p.suffix.lower() == ".pdf" and data.startswith(b"%PDF"):
                    good = True
                if p.suffix.lower() == ".html" and p.stat().st_size > 50000:
                    good = True
            if good:
                continue
        old_num = reverse[new_num]
        for old_path in list(pdf_dir.glob(f"{old_num:02d}_*.pdf")) + list(
            pdf_dir.glob(f"{old_num:02d}_*.html")
        ):
            data = old_path.read_bytes()
            ok = (old_path.suffix == ".html" and len(data) > 50000) or (
                old_path.suffix == ".pdf" and data[:4] == b"%PDF" and len(data) > 5000
            )
            if not ok:
                continue
            rest = old_path.name.split("_", 1)[1]
            new_path = pdf_dir / f"{new_num:02d}_{rest}"
            if not new_path.exists():
                new_path.write_bytes(data)
                print(f"Copied {old_path.name} -> {new_path.name}")
            break

    subprocess.run(
        [sys.executable, str(SCRIPTS / "download_cited_refs.py")],
        check=False,
    )


def main() -> None:
    print("=== 1) Collect cited references ===")
    old_refs = load_references()
    cited = collect_cited_refs()
    # Keep only cited that exist in bibliography
    cited = {n for n in cited if 1 <= n <= len(old_refs)}
    unused = sorted(set(range(1, len(old_refs) + 1)) - cited)
    used_sorted = sorted(cited)
    print(f"Bibliography size: {len(old_refs)}")
    print(f"Cited: {len(used_sorted)} -> {used_sorted}")
    print(f"Unused (will remove): {len(unused)} -> {unused}")

    mapping = {old: new for new, old in enumerate(used_sorted, 1)}
    new_refs = [old_refs[old - 1] for old in used_sorted]

    print("=== 2) Write pruned references.py ===")
    write_references_py(new_refs)

    print("=== 3) Remap citation keywords ===")
    write_citations_py(mapping)

    print("=== 4) Remap explicit [n] in content ===")
    n_files = remap_content_files(mapping)
    print(f"Updated {n_files} content files")

    print("=== 5) Share citations module with generators ===")
    # Generators already import from citations.py

    print("=== 6) Rebuild index metadata ===")
    rebuild_index_metadata()

    # Persist mapping
    map_path = ROOT / "references" / "renumber_map.json"
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_text(
        json.dumps(
            {
                "old_to_new": {str(k): v for k, v in mapping.items()},
                "cited_old": used_sorted,
                "unused_old": unused,
                "new_count": len(new_refs),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Saved mapping: {map_path}")

    print("=== 7) Download cited reference files ===")
    download_cited(len(new_refs), mapping)

    print("=== 8) Regenerate Word thesis ===")
    subprocess.run([sys.executable, str(SCRIPTS / "generate_full_thesis.py")], check=True)

    print("=== 9) Regenerate LaTeX ===")
    subprocess.run([sys.executable, str(SCRIPTS / "generate_latex.py")], check=True)

    # Verify
    for mod in list(sys.modules):
        if (
            mod in {
                "citations",
                "references",
                "thesis_doc",
                "latex_utils",
                "index_metadata",
                "preface",
                "conclusions",
                "appendix",
                "phase1_expansion",
                "phase1_expansion2",
                "generate_full_thesis",
                "generate_chapter02",
                "generate_chapter03",
                "generate_chapter04",
                "generate_chapter05",
            }
            or mod.startswith("chapter")
        ):
            del sys.modules[mod]

    from citations import extract_citation_numbers as ext2
    from citations import inject_citations as inj2
    import references as refs2

    cited2: set[int] = set()
    for para in iter_paragraphs():
        cited2 |= ext2(inj2(para))
    bad = {n for n in cited2 if n < 1 or n > len(refs2.REFERENCES)}
    uncited_new = sorted(set(range(1, len(refs2.REFERENCES) + 1)) - cited2)
    print(f"Post-check: refs={len(refs2.REFERENCES)} cited={sorted(cited2)}")
    print(f"Out-of-range cites: {bad}")
    print(f"Uncited after prune (should be empty): {uncited_new}")
    print("DONE")


if __name__ == "__main__":
    main()
