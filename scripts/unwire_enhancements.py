"""Unwire expansion/enhancement imports; chapters are self-contained."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

for n in (2, 3, 4, 5):
    p = ROOT / f"generate_chapter0{n}.py"
    text = p.read_text(encoding="utf-8")
    start = text.find("def build_sections():")
    end = text.find("\ndef generate_chapter")
    if start < 0 or end < 0:
        raise SystemExit(f"bad markers chapter {n}")
    new_fn = (
        "def build_sections():\n"
        f"    import chapter0{n} as ch\n"
        "    return ch, list(ch.SECTIONS)\n\n\n"
    )
    p.write_text(text[:start] + new_fn + text[end + 1 :], encoding="utf-8")
    print("patched", p.name)

latex = (ROOT / "generate_latex.py").read_text(encoding="utf-8")

replacements = [
    (
        """def generate_chapter01() -> Path:
    import chapter01 as ch1
    from phase1_expansion import CHAPTER01_DEEP, CHAPTER01_EXPANSION
    from phase1_expansion2 import EXTRA_CHAPTER01

    sections = merge_expansions(ch1.SECTIONS, CHAPTER01_EXPANSION + CHAPTER01_DEEP + EXTRA_CHAPTER01)
    try:
        from chapter01_enhancement import EXPANSION as CH1_ENH
        sections = merge_expansions(sections, CH1_ENH)
    except ImportError:
        pass""",
        """def generate_chapter01() -> Path:
    import chapter01 as ch1

    sections = list(ch1.SECTIONS)""",
    ),
    (
        """def generate_chapter02() -> Path:
    import chapter02 as ch2
    from chapter02_expansion import EXPANSION
    from chapter02_expansion2 import EXPANSION2

    sections = merge_expansions(ch2.SECTIONS, EXPANSION + EXPANSION2)
    try:
        from chapter02_enhancement import EXPANSION as ENH
        sections = merge_expansions(sections, ENH)
    except ImportError:
        pass""",
        """def generate_chapter02() -> Path:
    import chapter02 as ch2

    sections = list(ch2.SECTIONS)""",
    ),
    (
        """def generate_chapter03() -> Path:
    import chapter03 as ch3
    from chapter03_expansion import EXPANSION, EXPANSION2

    sections = merge_expansions(ch3.SECTIONS, EXPANSION + EXPANSION2)
    try:
        from chapter03_enhancement import EXPANSION as ENH
        sections = merge_expansions(sections, ENH)
    except ImportError:
        pass""",
        """def generate_chapter03() -> Path:
    import chapter03 as ch3

    sections = list(ch3.SECTIONS)""",
    ),
    (
        """def generate_chapter04() -> Path:
    import chapter04 as ch4
    from chapter04_expansion import EXPANSION

    sections = merge_expansions(ch4.SECTIONS, EXPANSION)
    try:
        from chapter04_enhancement import EXPANSION as ENH
        sections = merge_expansions(sections, ENH)
    except ImportError:
        pass""",
        """def generate_chapter04() -> Path:
    import chapter04 as ch4

    sections = list(ch4.SECTIONS)""",
    ),
    (
        """def generate_chapter05() -> Path:
    import chapter05 as ch5
    from chapter05_expansion import EXPANSION

    sections = merge_expansions(ch5.SECTIONS, EXPANSION)
    try:
        from chapter05_enhancement import EXPANSION as ENH
        sections = merge_expansions(sections, ENH)
    except ImportError:
        pass""",
        """def generate_chapter05() -> Path:
    import chapter05 as ch5

    sections = list(ch5.SECTIONS)""",
    ),
    (
        """def generate_conclusions() -> Path:
    import conclusions as conc
    from conclusions_enhancement import EXTRA_SECTIONS

    body = render_sections(list(conc.SECTIONS) + EXTRA_SECTIONS)""",
        """def generate_conclusions() -> Path:
    import conclusions as conc

    body = render_sections(list(conc.SECTIONS))""",
    ),
]

for old, new in replacements:
    if old not in latex:
        raise SystemExit(f"block not found:\n{old[:80]}")
    latex = latex.replace(old, new)

(ROOT / "generate_latex.py").write_text(latex, encoding="utf-8")
print("patched generate_latex.py")

full = (ROOT / "generate_full_thesis.py").read_text(encoding="utf-8")
old_ch1 = """def build_ch1_sections():
    import chapter01 as ch1
    from phase1_expansion import CHAPTER01_DEEP, CHAPTER01_EXPANSION
    from phase1_expansion2 import EXTRA_CHAPTER01

    all_exp = CHAPTER01_EXPANSION + CHAPTER01_DEEP + EXTRA_CHAPTER01
    try:
        from chapter01_enhancement import EXPANSION as CH1_ENH
        all_exp = all_exp + CH1_ENH
    except ImportError:
        pass
    sections = []
    for section in ch1.SECTIONS:
        merged = dict(section)
        extra = [s for e in all_exp if e[\"parent_section\"] == section[\"heading\"] for s in e[\"subsections\"]]
        if extra:
            merged[\"subsections\"] = list(section.get(\"subsections\", [])) + extra
        sections.append(merged)
    return ch1, sections"""
# fix quotes - the file uses normal quotes
old_ch1 = old_ch1.replace('\\"', '"')
new_ch1 = """def build_ch1_sections():
    import chapter01 as ch1
    return ch1, list(ch1.SECTIONS)"""
if old_ch1 not in full:
    raise SystemExit("build_ch1_sections not found")
full = full.replace(old_ch1, new_ch1)

old_conc = """    add_heading_bookmarked(doc, conc.TITLE, level=1)
    from conclusions_enhancement import EXTRA_SECTIONS as CONC_EXTRA

    render_sections(doc, list(conc.SECTIONS) + CONC_EXTRA)"""
new_conc = """    add_heading_bookmarked(doc, conc.TITLE, level=1)
    render_sections(doc, list(conc.SECTIONS))"""
if old_conc not in full:
    raise SystemExit("conclusions block not found")
full = full.replace(old_conc, new_conc)

(ROOT / "generate_full_thesis.py").write_text(full, encoding="utf-8")
print("patched generate_full_thesis.py")
print("done")
