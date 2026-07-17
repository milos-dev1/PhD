"""Convert downloaded RFC .txt files to PDF; remove failed HTML downloads."""

from __future__ import annotations

import json
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "references" / "pdfs"

FAKE = [
    "01_RFC8446_TLS_1.3.pdf",
    "06_RFC5869_HKDF.pdf",
    "10_RFC8032_Ed25519.pdf",
    "05_Krawczyk_HKDF_CRYPTO2010.pdf",
]

CONVERSIONS = [
    ("01_RFC8446_TLS_1.3.txt", "01_RFC8446_TLS_1.3.pdf"),
    ("06_RFC5869_HKDF.txt", "06_RFC5869_HKDF.pdf"),
    ("10_RFC8032_Ed25519.txt", "10_RFC8032_Ed25519.pdf"),
]

NOTES = {
    1: "TLS 1.3 — client-server transport baseline (from official RFC text)",
    2: "AES-GCM — authenticated encryption used in ECC-HISE",
    3: "Key management guidance — hierarchical keys",
    6: "HKDF — key derivation in ECC-DTB-AKA and ECC-HISE (from official RFC text)",
    8: "CK/AKE model — security analysis foundation for Ch.2",
    10: "Ed25519 — signatures in ECC-HISE (from official RFC text)",
    11: "SEC 1 — ECC / ECIES standards basis",
    26: "FIPS 186-5 — ECDSA digital signatures",
    29: "ECDH key establishment — NIST guidance",
    31: "Bitcoin / Merkle trees — audit-chain prior art (Ch.3/5)",
}


def txt_to_pdf(txt_path: Path, pdf_path: Path) -> None:
    text = txt_path.read_text(encoding="utf-8", errors="replace")
    pdf = FPDF(format="A4", unit="mm")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Courier", size=7)
    safe = text.encode("latin-1", errors="replace").decode("latin-1")
    # Form feeds / control chars break layout
    safe = "".join(ch if (ch == "\n" or ord(ch) >= 32) else " " for ch in safe)
    width = pdf.epw
    for raw in safe.splitlines():
        line = raw.rstrip() or " "
        while line:
            chunk = line[:95]
            line = line[95:]
            pdf.set_x(pdf.l_margin)
            pdf.cell(width, 3.2, chunk, new_x="LMARGIN", new_y="NEXT")
    pdf.output(str(pdf_path))


def main() -> None:
    for name in FAKE:
        p = OUT / name
        if p.exists():
            head = p.read_bytes()[:5]
            if not head.startswith(b"%PDF"):
                p.unlink()
                print(f"removed fake {name}")

    for txt_name, pdf_name in CONVERSIONS:
        txt_path = OUT / txt_name
        pdf_path = OUT / pdf_name
        if not txt_path.exists():
            print(f"missing {txt_name}")
            continue
        txt_to_pdf(txt_path, pdf_path)
        print(f"wrote {pdf_name} ({pdf_path.stat().st_size} bytes)")

    files = []
    for p in sorted(OUT.glob("*.pdf")):
        head = p.read_bytes()[:5]
        ok = head.startswith(b"%PDF")
        print(f"{'OK' if ok else 'BAD'} {p.name}: {p.stat().st_size}")
        if ok:
            num = int(p.name.split("_", 1)[0])
            files.append(
                {
                    "ref": num,
                    "file": p.name,
                    "bytes": p.stat().st_size,
                    "note": NOTES.get(num, ""),
                }
            )

    (OUT / "manifest.json").write_text(
        json.dumps(files, indent=2), encoding="utf-8"
    )

    lines = [
        "# Downloaded Reference PDFs",
        "",
        "Mapped to thesis bibliography numbers. Ten key open-access sources.",
        "",
        "| Ref | File | Topic |",
        "|-----|------|-------|",
    ]
    for f in files:
        lines.append(f"| [{f['ref']}] | `{f['file']}` | {f['note']} |")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- RFC PDFs `[1]`, `[6]`, `[10]` were generated from official IETF `.txt` "
            "sources (`rfc-editor.org`) because PDF mirrors returned HTML error pages.",
            "- Original `.txt` files are kept alongside those PDFs.",
            "- `[8]` Canetti–Krawczyk and `[11]` SEC 1 use publisher / archive PDFs.",
            "",
            "## Sources",
            "",
            "- **[1]** https://www.rfc-editor.org/rfc/rfc8446.txt",
            "- **[2]** https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf",
            "- **[3]** https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf",
            "- **[6]** https://www.rfc-editor.org/rfc/rfc5869.txt",
            "- **[8]** EUROCRYPT / IACR archive PDF",
            "- **[10]** https://www.rfc-editor.org/rfc/rfc8032.txt",
            "- **[11]** https://www.secg.org/sec1-v2.pdf (via Wayback if needed)",
            "- **[26]** https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf",
            "- **[29]** https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Ar3.pdf",
            "- **[31]** https://bitcoin.org/bitcoin.pdf",
            "",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nTotal valid PDFs: {len(files)}")


if __name__ == "__main__":
    main()
