"""Generate thesis Word documents (B5, 11pt)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from thesis_doc import (
    add_figure,
    add_paragraph,
    add_table,
    add_title_page,
    create_thesis_document,
    save_document,
)

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "thesis" / "figures"
FIGURE_MAP = {
    "Figure 1.1": FIG / "fig_1_1_attack_lifecycle.png",
    "Figure 1.2": FIG / "fig_1_2_client_auth_flow.png",
    "Figure 1.3": FIG / "fig_1_3_server_mesh.png",
    "Figure 1.4": FIG / "fig_1_4_data_layers.png",
    "Figure 1.5": FIG / "fig_1_5_threat_model.png",
}
sys.path.insert(0, str(ROOT / "content"))


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


def generate_preface() -> Path:
    import preface as pf
    from phase1_expansion import PREFACE_DEEP, PREFACE_EXPANSION
    from phase1_expansion2 import EXTRA_PREFACE

    doc = create_thesis_document()
    doc.add_heading(pf.TITLE, level=1)
    render_sections(doc, pf.SECTIONS + PREFACE_EXPANSION + [PREFACE_DEEP] + EXTRA_PREFACE)
    out = ROOT / "thesis" / "01_preface.docx"
    save_document(doc, out)
    return out


def generate_chapter01() -> Path:
    import chapter01 as ch1
    from phase1_expansion import CHAPTER01_DEEP, CHAPTER01_EXPANSION
    from phase1_expansion2 import EXTRA_CHAPTER01

    all_exp = CHAPTER01_EXPANSION + CHAPTER01_DEEP + EXTRA_CHAPTER01
    ch1_sections = []
    for section in ch1.SECTIONS:
        merged = dict(section)
        extra_subs = [s for e in all_exp if e["parent_section"] == section["heading"] for s in e["subsections"]]
        if extra_subs:
            merged["subsections"] = list(section.get("subsections", [])) + extra_subs
        ch1_sections.append(merged)

    doc = create_thesis_document()
    doc.add_heading(ch1.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch1.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_sections(doc, ch1_sections)
    out = ROOT / "thesis" / "02_chapter01.docx"
    save_document(doc, out)
    return out


def generate_combined_phase1() -> Path:
    import chapter01 as ch1
    import preface as pf
    from phase1_expansion import (
        CHAPTER01_DEEP,
        CHAPTER01_EXPANSION,
        PREFACE_DEEP,
        PREFACE_EXPANSION,
    )
    from phase1_expansion2 import EXTRA_CHAPTER01, EXTRA_PREFACE

    # Merge expansion into preface
    pf_sections = pf.SECTIONS + PREFACE_EXPANSION + [PREFACE_DEEP] + EXTRA_PREFACE

    # Merge expansion into chapter01 sections by parent heading
    ch1_sections = []
    all_ch1_exp = CHAPTER01_EXPANSION + CHAPTER01_DEEP + EXTRA_CHAPTER01
    for section in ch1.SECTIONS:
        merged = dict(section)
        extra_subs = []
        for exp in all_ch1_exp:
            if exp["parent_section"] == section["heading"]:
                extra_subs.extend(exp["subsections"])
        if extra_subs:
            merged["subsections"] = list(section.get("subsections", [])) + extra_subs
        ch1_sections.append(merged)

    doc = create_thesis_document()
    add_title_page(
        doc,
        "A Dual-Layer ECC Methodology for Client-Server Authentication\n"
        "and Server-Server Data Protection in Electronic Finance Systems",
        "PhD Dissertation in Information Security",
        "Submitted in partial fulfillment of the requirements\nfor the degree of Doctor of Philosophy",
    )

    doc.add_heading("Abstract", level=1)
    abstract = (
        "This dissertation investigates information security challenges in electronic banking and "
        "electronic finance service systems, with particular emphasis on authentication, key exchange, "
        "data encryption, and integrity protection. A comprehensive analysis of contemporary attack "
        "mechanisms—including phishing, man-in-the-middle attacks, replay attacks, session hijacking, "
        "credential stuffing, and insider threats—establishes the threat landscape and identifies "
        "critical limitations in existing security mechanisms. Two novel elliptic curve cryptography "
        "(ECC) based schemes are proposed: ECC-DTB-AKA (Device- and Transaction-Bound Authenticated "
        "Key Agreement) for client-server channels, and ECC-HISE (Hierarchical Integrity-preserving "
        "Secure Envelope) for server-server batch data transfer. Both schemes are formally analyzed, "
        "quantitatively evaluated against established baselines, and implemented in a working software "
        "prototype. Experimental results demonstrate that ECC-DTB-AKA achieves mutual authentication "
        "in three communication rounds with device and transaction binding, while ECC-HISE provides "
        "hierarchical key management with Merkle-tree audit chains enabling efficient batch integrity "
        "verification. The dissertation contributes original methodologies, algorithms, and implementation "
        "artifacts that advance the state of the art in e-banking cryptographic security."
    )
    add_paragraph(doc, abstract, indent=True)
    doc.add_page_break()

    doc.add_heading(pf.TITLE, level=1)
    render_sections(doc, pf_sections)
    doc.add_page_break()

    doc.add_heading(ch1.CHAPTER_TITLE, level=1)
    add_paragraph(doc, ch1.CHAPTER_SUBTITLE, bold=True)
    doc.add_paragraph()
    render_sections(doc, ch1_sections)

    out = ROOT / "thesis" / "phase1_preface_chapter01.docx"
    save_document(doc, out)
    return out


if __name__ == "__main__":
    p1 = generate_preface()
    p2 = generate_chapter01()
    p3 = generate_combined_phase1()
    print(f"Saved: {p1}")
    print(f"Saved: {p2}")
    print(f"Saved: {p3}")
