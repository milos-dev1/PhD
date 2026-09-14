"""Shared citation keywords and helpers for Word + LaTeX generators."""

from __future__ import annotations

import re

# Specific phrases MUST appear before broader ones (e.g. ECIES before "elliptic curve").
CITATION_KEYWORDS: list[tuple[str, list[int]]] = [
    ('TLS 1.3', [1]),
    ('forward secrecy', [1, 8]),
    ('mTLS', [1, 28]),
    ('AES-GCM', [2]),
    ('AES-256', [2]),
    ('authenticated encryption', [36, 2]),
    ('GCM', [2]),
    ('key management', [3]),
    ('X.509', [4]),
    ('certificate', [4]),
    ('HKDF', [5, 6]),
    ('key derivation', [5, 6]),
    ('authenticated key', [7, 8]),
    ('Canetti', [8]),
    ('key exchange', [8, 29]),
    ('ECDSA', [9, 26]),
    ('Ed25519', [10]),
    ('EdDSA', [10]),
    ('ECIES', [41]),
    ('IEEE 1363', [41]),
    ('Curve25519', [40]),
    ('ProVerif', [45, 44]),
    ('Tamarin', [44, 45]),
    ('TAMARIN', [44, 45]),
    ('formal verification', [44, 45]),
    ('SEC 1', [11]),
    ('elliptic curve', [11, 34, 35]),
    ('ECDH', [12, 29]),
    ('PKCE', [14]),
    ('OAuth', [13, 14]),
    ('WebAuthn', [15]),
    ('FIDO', [15]),
    ('EMV', [16]),
    ('PCI DSS', [17]),
    ('PSD2', [18]),
    ('ISO/IEC 27001', [19]),
    ('ISO 27001', [19]),
    ('Bangladesh', [24]),
    ('Carbanak', [25]),
    ('SWIFT', [20, 24]),
    ('DBIR', [22]),
    ('data breach', [21, 22]),
    ('OWASP', [23]),
    ('FIPS 186', [26]),
    ('digital signature', [26, 9]),
    ('SHA-256', [27]),
    ('SHA-2', [27]),
    ('SP 800-52', [28]),
    ('SP 800-56', [29]),
    ('Merkle', [30]),
    ('Corda', [32]),
    ('Bitcoin', [31]),
    ('blockchain', [31, 32]),
    ('Diffie-Hellman', [33]),
    ('Diffie–Hellman', [33]),
    ('Dolev-Yao', [37]),
    ('Dolev–Yao', [37]),
    ('Open Banking', [38]),
    ('ML-KEM', [39]),
    ('ML-DSA', [39]),
    ('post-quantum', [39]),
    ('online banking', [42, 43]),
    ('e-banking', [42, 43]),
    ('phishing', [22]),
    ('TLS', [1, 28]),
]


def inject_citations(text: str, *, max_cites: int = 4) -> str:
    """Append citation markers for matching keywords if none already present."""
    if re.search(r"\[\d+", text):
        return text
    found: list[int] = []
    lower = text.lower()
    for keyword, refs in CITATION_KEYWORDS:
        if keyword.lower() not in lower:
            continue
        # Always take the full ref group for a matched keyword, then stop if full.
        for r in refs:
            if r not in found:
                found.append(r)
        if len(found) >= max_cites:
            break
    if not found:
        return text
    cites = "".join(f"[{n}]" for n in found[:max_cites])
    if text.rstrip().endswith("."):
        return text.rstrip()[:-1] + f" {cites}."
    return text.rstrip() + f" {cites}"


def extract_citation_numbers(text: str) -> set[int]:
    nums: set[int] = set()
    for m in re.finditer(r"\[(\d+(?:\s*,\s*\d+)*)\]", text):
        for part in m.group(1).split(","):
            nums.add(int(part.strip()))
    return nums


def remap_citations_in_text(text: str, mapping: dict[int, int]) -> str:
    """Rewrite [old] citation markers using old->new mapping."""

    def repl(m: re.Match) -> str:
        nums = []
        for part in m.group(1).split(","):
            old = int(part.strip())
            if old in mapping:
                nums.append(str(mapping[old]))
        if not nums:
            return ""
        if len(nums) == 1:
            return f"[{nums[0]}]"
        return "[" + ",".join(nums) + "]"

    return re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", repl, text)
