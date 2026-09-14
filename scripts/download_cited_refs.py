"""Download PDFs for currently cited bibliography. Skip failures. No fuzzy reuse."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "references" / "pdfs"
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "content"))

import references as refs  # noqa: E402

MAP_PATH = ROOT / "references" / "renumber_map.json"

URL_RULES: list[tuple[str, list[str]]] = [
    ("TLS Protocol Version 1.3", ["http://www.rfc.fr/rfc/en/rfc8446.pdf"]),
    ("Galois/Counter Mode", ["https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf"]),
    ("Key Management: Part 1", ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf"]),
    ("X.509 Public Key Infrastructure", ["http://www.rfc.fr/rfc/en/rfc5280.pdf"]),
    ("Cryptographic Extraction and Key Derivation", ["https://link.springer.com/content/pdf/10.1007/978-3-642-14623-7_35.pdf"]),
    ("HMAC-based Extract-and-Expand", ["http://www.rfc.fr/rfc/en/rfc5869.pdf"]),
    ("Entity Authentication and Key Distribution", ["https://cseweb.ucsd.edu/~mihir/papers/eakd.pdf"]),
    ("Analysis of Key-Exchange Protocols", ["https://eprint.iacr.org/2001/040.pdf"]),
    ("Elliptic Curve Digital Signature Algorithm (ECDSA)", ["https://cacr.uwaterloo.ca/techreports/1999/corr99-34.pdf"]),
    ("Edwards-Curve Digital Signature", ["http://www.rfc.fr/rfc/en/rfc8032.pdf"]),
    ("SEC 1: Elliptic Curve Cryptography", ["https://www.secg.org/sec1-v2.pdf"]),
    ("OAuth 2.0 Authorization Framework", ["http://www.rfc.fr/rfc/en/rfc6749.pdf"]),
    ("OAuth 2.0 for Native Apps", ["http://www.rfc.fr/rfc/en/rfc8252.pdf"]),
    ("Web Authentication", ["https://www.w3.org/TR/webauthn-2/"]),
    ("Data Breach Investigations Report", ["https://www.verizon.com/business/resources/TXlp/reports/2024-dbir-data-breach-investigations-report.pdf"]),
    ("OWASP API Security", ["https://hubspot.wallarm.com/hubfs/2023%20OWASP%20API%20Security%20Top%2010.pdf"]),
    ("Carbanak", ["https://media.kasperskycontenthub.com/wp-content/uploads/sites/43/2018/03/08064518/Carbanak_APT_eng.pdf"]),
    ("Digital Signature Standard", ["https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf"]),
    ("Secure Hash Standard", ["https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf"]),
    ("Use of TLS Implementations", ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf"]),
    ("Pair-Wise Key Establishment", ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Ar3.pdf"]),
    ("Digital Signature Based on a Conventional", ["https://link.springer.com/content/pdf/10.1007/3-540-48184-2_32.pdf"]),
    ("Bitcoin", ["https://bitcoin.org/bitcoin.pdf"]),
    ("Corda", ["https://web.archive.org/web/20180101000000/https://docs.corda.net/_static/corda-introductory-whitepaper.pdf"]),
    ("New Directions in Cryptography", ["https://ee.stanford.edu/~hellman/publications/24.pdf"]),
    ("Use of Elliptic Curves in Cryptography", ["https://link.springer.com/content/pdf/10.1007/3-540-39757-4_20.pdf"]),
    ("Elliptic Curve Cryptosystems", ["https://web.archive.org/web/20160304122911id_/http://www.ams.org/journals/mcom/1987-48-177/S0025-5718-1987-0866109-5/S0025-5718-1987-0866109-5.pdf"]),
    ("Authenticated Encryption: Relations", ["https://link.springer.com/content/pdf/10.1007/3-540-44448-3_40.pdf"]),
    ("Security of Public Key Protocols", ["http://i.stanford.edu/pub/cstr/reports/cs/tr/81/854/CS-TR-81-854.pdf"]),
    ("Open Banking", ["https://standards.openbanking.org.uk/"]),
    ("Post-Quantum Cryptography", ["https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf"]),
    ("Curve25519", ["https://cr.yp.to/ecdh/curve25519-20060209.pdf"]),
    ("TAMARIN Prover", ["https://tamarin-prover.github.io/manual/tex/tamarin-manual.pdf"]),
    ("ProVerif", ["https://bblanche.gitlabpages.inria.fr/publications/BlanchetFnTPS16.pdf"]),
    ("Cost of a Data Breach", ["https://www.ibm.com/reports/data-breach"]),
]


def slugify(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", title)[:60].strip("_")
    return s or "ref"


def distinctive_tokens(title: str) -> list[str]:
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "using", "based",
        "standard", "security", "protocol", "protocols", "cryptography", "public",
        "key", "data", "report", "version", "digital", "system", "systems",
    }
    parts = re.findall(r"[A-Za-z0-9]+", title.lower())
    return [p for p in parts if len(p) >= 5 and p not in stop]


def is_usable(path: Path) -> bool:
    if not path.exists():
        return False
    data = path.read_bytes()
    if path.suffix.lower() == ".pdf":
        return data[:4] == b"%PDF" and len(data) > 5000
    if path.suffix.lower() == ".html":
        return len(data) > 80000 and b"<html" in data[:500].lower()
    return False


def filename_matches(path: Path, title: str) -> bool:
    tokens = distinctive_tokens(title)
    if not tokens:
        return False
    name = path.stem.lower()
    hits = sum(1 for t in tokens if t in name)
    # Prefer 2+ distinctive hits; allow 1 if token is very specific (>=8 chars)
    if hits >= 2:
        return True
    return hits == 1 and any(len(t) >= 8 and t in name for t in tokens)


def curl_get(url: str, dest: Path) -> tuple[bool, str]:
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = [
        "curl.exe", "-sL",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "-o", str(tmp), "--connect-timeout", "25", "--max-time", "120",
        "-w", "%{http_code}", url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        code = (proc.stdout or "").strip()
        if not tmp.exists():
            return False, f"HTTP {code} no file"
        data = tmp.read_bytes()
        tmp.unlink(missing_ok=True)
        if data[:4] == b"%PDF" and len(data) > 5000:
            dest.write_bytes(data)
            return True, f"PDF {len(data)} bytes"
        if (b"<html" in data[:500].lower() or b"<!doctype" in data[:500].lower()) and len(data) > 80000:
            html_dest = dest.with_suffix(".html")
            html_dest.write_bytes(data)
            return True, f"HTML {len(data)} bytes -> {html_dest.name}"
        return False, f"HTTP {code} not usable ({len(data)} bytes)"
    except Exception as e:
        tmp.unlink(missing_ok=True)
        return False, str(e)


def urls_for(title: str, venue: str) -> list[str]:
    blob = f"{title} {venue}"
    for needle, urls in URL_RULES:
        if needle.lower() in blob.lower():
            return urls
    m = re.search(r"RFC\s*(\d+)", venue, re.I) or re.search(r"RFC\s*(\d+)", title, re.I)
    if m:
        return [f"http://www.rfc.fr/rfc/en/rfc{m.group(1)}.pdf"]
    return []


def old_to_new() -> dict[int, int]:
    if not MAP_PATH.exists():
        return {}
    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    return {int(k): int(v) for k, v in data.get("old_to_new", {}).items()}


def copy_from_old_number(new_num: int, title: str, mapping: dict[int, int]) -> Path | None:
    reverse = {v: k for k, v in mapping.items()}
    old = reverse.get(new_num)
    if old is None:
        return None
    for p in list(OUT.glob(f"{old:02d}_*.pdf")) + list(OUT.glob(f"{old:02d}_*.html")):
        if not is_usable(p):
            continue
        if filename_matches(p, title) or _alias_match(p, title):
            dest = OUT / f"{new_num:02d}_{slugify(title)}{p.suffix.lower()}"
            if p.resolve() != dest.resolve():
                dest.write_bytes(p.read_bytes())
            return dest
    return None


ALIASES: dict[str, list[str]] = {
    "TLS Protocol Version 1.3": ["rfc8446", "tls_1_3", "tls_1.3"],
    "Galois/Counter Mode": ["sp800-38d", "800-38d", "gcm"],
    "Key Management: Part 1": ["800-57", "key_management"],
    "X.509": ["rfc5280", "x509", "x_509"],
    "Cryptographic Extraction and Key Derivation": ["krawczyk", "hkdf_crypto", "crypto2010"],
    "HMAC-based Extract-and-Expand": ["rfc5869"],
    "Entity Authentication": ["bellare_rogaway", "eakd"],
    "Analysis of Key-Exchange": ["canetti"],
    "Elliptic Curve Digital Signature Algorithm (ECDSA)": ["johnson", "ecdsa"],
    "Edwards-Curve": ["rfc8032", "ed25519"],
    "SEC 1": ["sec1"],
    "OAuth 2.0 Authorization": ["rfc6749"],
    "OAuth 2.0 for Native": ["rfc8252"],
    "Web Authentication": ["webauthn"],
    "Data Breach Investigations": ["dbir", "verizon"],
    "OWASP API Security": ["owasp"],
    "Carbanak": ["carbanak"],
    "Digital Signature Standard": ["fips186", "186-5"],
    "Secure Hash Standard": ["fips180", "180-4"],
    "Use of TLS Implementations": ["800-52", "sp800-52"],
    "Pair-Wise Key Establishment": ["800-56", "sp800-56"],
    "Digital Signature Based on a Conventional": ["merkle"],
    "Bitcoin": ["bitcoin"],
    "Corda": ["corda"],
    "New Directions in Cryptography": ["diffie"],
    "Use of Elliptic Curves in Cryptography": ["miller"],
    "Elliptic Curve Cryptosystems": ["koblitz"],
    "Authenticated Encryption: Relations": ["namprempre", "authenticated_encryption"],
    "Security of Public Key Protocols": ["dolev"],
    "Open Banking": ["open_banking"],
    "Post-Quantum": ["fips203", "ml-kem", "pqc", "nist_pqc"],
    "Curve25519": ["curve25519"],
    "TAMARIN": ["tamarin", "cremers"],
    "ProVerif": ["proverif", "blanchet"],
    "Cost of a Data Breach": ["data_breach"],
}


def _alias_match(path: Path, title: str) -> bool:
    name = path.stem.lower().replace("-", "_")
    for needle, aliases in ALIASES.items():
        if needle.lower() in title.lower():
            return any(a.replace("-", "_") in name for a in aliases)
    return False


def main() -> None:
    mapping = old_to_new()
    results = []
    for i, ref in enumerate(refs.REFERENCES, 1):
        title, venue = ref[1], ref[2]
        # Prefer already-correct new-numbered file
        kept = None
        for p in sorted(OUT.glob(f"{i:02d}_*")):
            if is_usable(p) and filename_matches(p, title):
                kept = p
                break
        if kept:
            print(f"[{i:02d}] KEEP {kept.name}")
            results.append({"ref": i, "ok": True, "file": kept.name, "detail": "already present"})
            continue

        copied = copy_from_old_number(i, title, mapping)
        if copied:
            print(f"[{i:02d}] COPY {copied.name}")
            results.append({"ref": i, "ok": True, "file": copied.name, "detail": "copied from prior download"})
            continue

        urls = urls_for(title, venue)
        if not urls:
            print(f"[{i:02d}] SKIP no open URL — {title[:60]}")
            results.append({"ref": i, "ok": False, "skipped": True, "detail": "no open URL / paywalled", "title": title})
            continue

        dest = OUT / f"{i:02d}_{slugify(title)}.pdf"
        ok = False
        detail = "failed"
        for url in urls:
            print(f"[{i:02d}] GET {url}")
            ok, detail = curl_get(url, dest)
            print(f"       {detail}")
            if ok:
                fname = dest.name if dest.exists() else dest.with_suffix(".html").name
                results.append({"ref": i, "ok": True, "file": fname, "url": url, "detail": detail})
                break
        if not ok:
            results.append({"ref": i, "ok": False, "skipped": False, "detail": detail, "title": title})

    ok_items = [r for r in results if r.get("ok")]
    skip_items = [r for r in results if not r.get("ok")]
    lines = [
        "# Cited Reference Downloads",
        "",
        f"Bibliography entries cited in thesis: **{len(results)}**",
        f"Local files obtained: **{len(ok_items)}**",
        f"Skipped / unavailable: **{len(skip_items)}**",
        "",
        "| Ref | File |",
        "|-----|------|",
    ]
    for r in ok_items:
        lines.append(f"| [{r['ref']}] | `{r.get('file')}` |")
    lines += ["", "## Skipped", ""]
    for r in skip_items:
        lines.append(f"- **[{r['ref']}]** {r.get('title','')} — {r.get('detail')}")
    lines.append("")
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "cited_manifest.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nCited refs with files: {len(ok_items)}/{len(results)}")


if __name__ == "__main__":
    main()
