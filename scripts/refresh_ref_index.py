"""Refresh references/pdfs README + manifest from on-disk files."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "references" / "pdfs"

# Thesis bibliography titles (1-based), short form
TITLES = {
    1: "RFC 8446 — TLS 1.3",
    2: "NIST SP 800-38D — GCM",
    3: "NIST SP 800-57 Part 1 Rev. 5 — Key management",
    4: "RFC 5280 — X.509 PKI",
    5: "Krawczyk — HKDF (CRYPTO 2010)",
    6: "RFC 5869 — HKDF",
    7: "Bellare & Rogaway — Entity authentication",
    8: "Canetti & Krawczyk — Key-exchange analysis",
    9: "Johnson et al. — ECDSA",
    10: "RFC 8032 — Ed25519 / EdDSA",
    11: "SEC 1 — Elliptic Curve Cryptography",
    12: "ANSI X9.63",
    13: "RFC 6749 — OAuth 2.0",
    14: "RFC 8252 — OAuth for native apps",
    15: "W3C WebAuthn Level 2",
    16: "EMVCo Book 2",
    17: "PCI DSS v4.0",
    18: "EU PSD2 (Directive 2015/2366)",
    19: "ISO/IEC 27001:2022",
    20: "SWIFT CSP",
    21: "IBM Cost of a Data Breach 2024",
    22: "Verizon DBIR 2024",
    23: "OWASP API Security Top 10 (2023 commentary PDF)",
    24: "Bangladesh Bank SWIFT heist",
    25: "Kaspersky — Carbanak",
    26: "FIPS 186-5 — Digital signatures",
    27: "FIPS 180-4 — Secure Hash Standard",
    28: "NIST SP 800-52 Rev. 2 — TLS",
    29: "NIST SP 800-56A Rev. 3 — Key establishment",
    30: "Merkle — Digital signature / hash trees (CRYPTO 1987)",
    31: "Bitcoin whitepaper",
    32: "Corda introductory whitepaper",
    33: "Diffie & Hellman — New Directions in Cryptography",
    34: "Miller — Use of Elliptic Curves in Cryptography",
    35: "Koblitz — Elliptic Curve Cryptosystems",
    36: "Boneh & Franklin — IBE",
    37: "Bellare & Namprempre — Authenticated encryption",
    38: "Dolev & Yao — Public-key protocols (Stanford TR)",
    39: "Wagner/Gennaro et al. — SSL 3.0 analysis",
    40: "Rescorla — SSL and TLS (book)",
    41: "Handbook of Applied Cryptography (free chapters)",
    42: "Katz & Lindell — Modern Cryptography (book)",
    43: "Stallings — Cryptography and Network Security (book)",
    44: "Anderson — Security Engineering (author PDF)",
    45: "Schneier — Applied Cryptography (book)",
    46: "Ferguson et al. — Cryptography Engineering (book)",
    47: "Gordon et al. — Breaches / stock market",
    48: "Ponemon / Accenture cyber cost study",
    49: "BIS — Principles for Financial Market Infrastructures",
    50: "ECB — Guide to internal models",
    51: "Basel — Operational risk sound practices",
    52: "Open Banking UK — security profile (HTML)",
    53: "CSA Cloud Security Guidance v4",
    54: "NIST PQC — FIPS 203 ML-KEM (+ FIPS 204 companion)",
    55: "Bernstein — Curve25519",
    56: "IEEE 1363a — ECIES",
    57: "ANSI X9.102 — Key wrap",
    58: "RFC 5652 — CMS",
    59: "RFC 8017 — PKCS #1",
    60: "Goodrich & Tamassia — Algorithm Design (book)",
    61: "Camenisch & Lysyanskaya — Anonymous credentials",
    62: "Bhargavan et al. — Triple handshakes / TLS",
    63: "Dennis et al. — E-banking security survey",
    64: "Aloul et al. — Online banking security",
    65: "de Ruiter & Poll — TLS state fuzzing",
    66: "Cremers et al. — TAMARIN",
    67: "Blanchet — ProVerif survey",
}

SKIP = {
    12: "Paywalled ANSI standard",
    16: "EMVCo registration required",
    17: "PCI DSS download portal / bot protection",
    18: "EUR-Lex PDF blocked from this network (try browser manually)",
    19: "Paywalled ISO standard",
    20: "SWIFT portal access required",
    21: "IBM gated marketing download",
    24: "No single canonical public investigation PDF",
    40: "Commercial book",
    42: "Commercial book",
    43: "Commercial book",
    45: "Commercial book",
    46: "Commercial book",
    47: "Paywalled journal article",
    48: "Vendor-gated report",
    50: "ECB PDF URL changed / blocked",
    53: "CSA gated download",
    56: "Paywalled IEEE standard",
    57: "Paywalled ANSI standard",
    60: "Commercial book",
    63: "Paywalled journal article",
    64: "Author PDF not reachable (403/HTML)",
}


def is_usable(path: Path) -> bool:
    data = path.read_bytes()
    if path.suffix.lower() == ".pdf":
        return data[:4] == b"%PDF" and len(data) > 5000
    if path.suffix.lower() == ".html":
        return len(data) > 50_000
    return False


def main() -> None:
    by_ref: dict[int, list[dict]] = {}
    for path in sorted(OUT.iterdir()):
        if not path.is_file():
            continue
        if path.name in {"README.md", "manifest.json"}:
            continue
        if path.suffix.lower() == ".txt":
            continue  # keep RFC txt but don't list as primary
        if path.name.startswith("41b_") or path.name.startswith("41c_") or path.name.startswith("54b_"):
            # companions under parent ref
            parent = 41 if path.name.startswith("41") else 54
            by_ref.setdefault(parent, [])
            if is_usable(path):
                by_ref[parent].append(
                    {"file": path.name, "bytes": path.stat().st_size, "companion": True}
                )
            continue
        if not path.name[:2].isdigit():
            continue
        ref = int(path.name[:2])
        if not is_usable(path):
            continue
        by_ref.setdefault(ref, []).append(
            {"file": path.name, "bytes": path.stat().st_size, "companion": False}
        )

    results = []
    for ref in range(1, 68):
        title = TITLES.get(ref, "")
        files = by_ref.get(ref, [])
        if files:
            primary = next((f for f in files if not f.get("companion")), files[0])
            results.append(
                {
                    "ref": ref,
                    "ok": True,
                    "skipped": False,
                    "title": title,
                    "file": primary["file"],
                    "bytes": primary["bytes"],
                    "companions": [f["file"] for f in files if f.get("companion")],
                }
            )
        else:
            results.append(
                {
                    "ref": ref,
                    "ok": False,
                    "skipped": ref in SKIP,
                    "title": title,
                    "file": None,
                    "detail": SKIP.get(ref, "Download failed / no open URL"),
                }
            )

    ok = [r for r in results if r["ok"]]
    skipped = [r for r in results if r.get("skipped")]
    failed = [r for r in results if not r["ok"] and not r.get("skipped")]

    lines = [
        "# Thesis Reference Downloads",
        "",
        f"Bibliography size: **67**. Usable local files: **{len(ok)}**.",
        f"Skipped (paywall / commercial / gated): **{len(skipped)}**.",
        f"Failed (open source expected but unreachable): **{len(failed)}**.",
        "",
        "Folder: `references/pdfs/`",
        "",
        "## Downloaded",
        "",
        "| Ref | File | Title |",
        "|-----|------|-------|",
    ]
    for r in ok:
        extra = ""
        if r.get("companions"):
            extra = " (+ " + ", ".join(f"`{c}`" for c in r["companions"]) + ")"
        lines.append(f"| [{r['ref']}] | `{r['file']}`{extra} | {r['title']} |")

    lines += ["", "## Skipped (not freely downloadable)", "", "| Ref | Title | Reason |", "|-----|-------|--------|"]
    for r in skipped:
        lines.append(f"| [{r['ref']}] | {r['title']} | {r['detail']} |")

    if failed:
        lines += ["", "## Failed", "", "| Ref | Title | Detail |", "|-----|-------|--------|"]
        for r in failed:
            lines.append(f"| [{r['ref']}] | {r['title']} | {r['detail']} |")

    lines += [
        "",
        "## Notes",
        "",
        "- RFC PDFs use the rfc.fr mirror of the official IETF PDF renderings.",
        "- `[41]` includes free HAC chapter PDFs from the University of Waterloo (not the full commercial book).",
        "- `[54]` includes FIPS 203; companion `54b_NIST_FIPS204_ML-DSA.pdf` is also saved.",
        "- `[23]` is a detailed 2023 OWASP API Top 10 examination PDF (Wallarm); official OWASP sources are primarily HTML/Markdown.",
        "- `[38]` is the Stanford technical report version of Dolev–Yao (equivalent content).",
        "",
    ]

    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"OK={len(ok)} SKIP={len(skipped)} FAIL={len(failed)}")


if __name__ == "__main__":
    main()
