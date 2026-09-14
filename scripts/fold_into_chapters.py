"""Fold expansion/enhancement modules into content/chapter0x.py (one-shot)."""
from __future__ import annotations

import pprint
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
sys.path.insert(0, str(CONTENT))
sys.path.insert(0, str(ROOT / "scripts"))

from latex_utils import merge_expansions  # noqa: E402


def word_count(sections: list) -> int:
    words = 0

    def walk(obj):
        nonlocal words
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "paragraphs" and isinstance(v, list):
                    words += sum(len(p.split()) for p in v)
                else:
                    walk(v)
        elif isinstance(obj, list):
            for x in obj:
                walk(x)

    walk(sections)
    return words


def rewrite_sections(mod_name: str, expansions: list, deep_extra: list | None = None) -> int:
    mod = __import__(mod_name)
    sections = list(mod.SECTIONS)
    if expansions:
        sections = merge_expansions(sections, expansions)
    if deep_extra:
        sections = merge_expansions(sections, deep_extra)
    words = word_count(sections)
    src = (CONTENT / f"{mod_name}.py").read_text(encoding="utf-8")
    marker = "SECTIONS = "
    idx = src.find(marker)
    if idx < 0:
        raise SystemExit(f"no SECTIONS in {mod_name}")
    preamble = src[:idx]
    dumped = pprint.pformat(sections, width=100, sort_dicts=False)
    (CONTENT / f"{mod_name}.py").write_text(preamble + marker + dumped + "\n", encoding="utf-8")
    return words


DEEP4 = [
    {
        "parent_section": "4.1 Security System Architecture of an E-Financial Service System",
        "subsections": [
            {
                "heading": "4.1.6 Operational Security Controls Complementary to Cryptography",
                "paragraphs": [
                    "Cryptographic schemes do not replace operational security. Rate limiting on "
                    "handshake endpoints, anomaly detection on verification-failure rates, "
                    "certificate revocation checking, and segregation of duties for HSM "
                    "administrators remain mandatory. The architecture places these controls "
                    "adjacent to ECC-DTB-AKA and ECC-HISE services so that cryptographic "
                    "failures and operational signals can be correlated in a common SIEM pipeline.",
                    "Change-management procedures for HKDF label strings, envelope version bytes, "
                    "and Merkle algorithm identifiers must be treated as security-relevant "
                    "configuration. Silent drift between sender and receiver encodings produces "
                    "systemic verification failures that can be mistaken for attacks; therefore "
                    "configuration is versioned and signed alongside application releases.",
                ],
            },
            {
                "heading": "4.1.7 Regulatory and Assurance Alignment",
                "paragraphs": [
                    "The dual-layer architecture aligns with assurance themes common to PCI DSS "
                    "(protect cardholder data in transit and at rest), PSD2 strong customer "
                    "authentication (possession factors for remote payments), and SWIFT Customer "
                    "Security Programme controls on interface integrity. ECC-DTB-AKA strengthens "
                    "possession of a client authenticator bound to session keys; ECC-HISE "
                    "strengthens integrity and auditability of inter-institution data exchanges.",
                    "The dissertation does not claim automatic compliance certification. Rather, "
                    "it provides cryptographic mechanisms that map cleanly onto control objectives "
                    "auditors already expect, reducing reliance on procedural compensating "
                    "controls for session binding and batch integrity.",
                ],
            },
        ],
    },
    {
        "parent_section": "4.2 Programmatic Implementation of ECC-DTB-AKA (Chapter 2)",
        "subsections": [
            {
                "heading": "4.2.9 Logging, Observability, and Secrets Hygiene",
                "paragraphs": [
                    "Prototype logging records handshake outcomes, client identifiers, and "
                    "truncated nonce digests, never raw ECDH scalars, MSK, or TBK. Production "
                    "deployments should emit structured events suitable for fraud correlation "
                    "while retaining cryptographic material exclusively in HSM or sealed memory.",
                    "Distributed tracing spans may carry session_id handles but must not carry "
                    "material that enables offline analysis of long-term keys. Clock skew beyond "
                    "a configured window causes handshakes to fail closed with a distinct error "
                    "code distinguishing configuration faults from replay attempts.",
                ],
            },
        ],
    },
    {
        "parent_section": "4.3 Programmatic Implementation of ECC-HISE (Chapter 3)",
        "subsections": [
            {
                "heading": "4.3.8 Scaling and Parallelism Considerations",
                "paragraphs": [
                    "Per-record AES-GCM encryption and Ed25519 signing dominate ECC-HISE latency "
                    "and parallelize naturally across CPU cores. Merkle tree construction is a "
                    "barrier after leaves are ready; for large batches, a forest of subtrees with "
                    "a top-level meta-root can preserve O(log n) proofs while enabling segmented "
                    "construction.",
                    "Memory pressure for million-record national settlement files motivates "
                    "streaming leaf hashing and spill-to-disk for intermediate layers. The "
                    "prototype demonstrates correctness at hundreds of records; larger volumes "
                    "are an engineering path discussed as future work.",
                ],
            },
        ],
    },
    {
        "parent_section": "4.4 Integrated System Demonstration",
        "subsections": [
            {
                "heading": "4.4.5 Failure Modes and Recovery",
                "paragraphs": [
                    "Integrated failure modes include: client handshake timeout (retry with fresh "
                    "nonces); TBK HMAC mismatch (reject payment, alert fraud); ECC-HISE quarantine "
                    "(hold settlement, notify operations); and audit proof mismatch (escalate as "
                    "integrity incident). Recovery never skips verification to restore availability; "
                    "degraded modes may queue outbound batches offline but do not accept unverified "
                    "inbound envelopes.",
                    "Disaster-recovery drills should include restoring MK from HSM backup ceremonies "
                    "and re-deriving domain keys under dual control, verifying that archived "
                    "envelopes remain decryptable under recorded key_version identifiers.",
                ],
            },
        ],
    },
]

DEEP5 = [
    {
        "parent_section": "5.1 Effectiveness of Proposed Methods Against Network Attacks",
        "subsections": [
            {
                "heading": "5.1.6 Threat Coverage Relative to Chapter 1 Catalogue",
                "paragraphs": [
                    "Mapping Table 5.1 back to Section 1.1 shows strong coverage for MITM, replay, "
                    "session hijacking, and batch tampering—the remote network and post-termination "
                    "integrity threats that dominate the dissertation scope. Credential stuffing is "
                    "out of scope for ECC-DTB-AKA once PKI client keys replace passwords; where "
                    "passwords remain, PAKE or FIDO enrollment is the appropriate prior control.",
                    "Insider threats with legitimate signing keys are only partially mitigated: "
                    "ECC-HISE provides non-repudiation and audit trails that increase detection "
                    "probability and forensic clarity, but organizational key custody remains "
                    "essential. This boundary is stated explicitly so effectiveness claims are "
                    "not overstated.",
                ],
            },
        ],
    },
    {
        "parent_section": "5.2 Prior Work on Authentication and Key Exchange",
        "subsections": [
            {
                "heading": "5.2.10 EMV Card-Present Binding Versus Remote Channels",
                "paragraphs": [
                    "EMV chip protocols bind payments to a physical card and issuer-authorized "
                    "cryptograms in card-present environments. Remote e-banking lacks an equivalent "
                    "hardware cryptogram path unless FIDO or secure elements are used. ECC-DTB-AKA "
                    "borrows the binding intuition—authorization should not be a transferable "
                    "bearer string—while operating over Internet channels with ECC key agreement.",
                    "The comparison clarifies novelty relative to retail payments research: the "
                    "contribution is not inventing binding in the abstract, but integrating device "
                    "and transaction binding into a mutual AKE suitable for mobile and web banking "
                    "APIs evaluated against TLS and OAuth baselines.",
                ],
            },
        ],
    },
    {
        "parent_section": "5.3 Prior Work on Data Encryption, Security, and Integrity",
        "subsections": [
            {
                "heading": "5.3.10 Transparent Data Encryption and Column Encryption",
                "paragraphs": [
                    "Database TDE and column-level encryption protect data at rest within a bank "
                    "estate. They do not authenticate membership of records in an inter-bank "
                    "settlement batch after export, nor do they provide counterparty-verifiable "
                    "Merkle commitments. ECC-HISE addresses the export and exchange path that TDE "
                    "leaves unprotected once files leave the encrypted database boundary.",
                    "Composition is natural: systems may keep TDE for storage, tokenize sensitive "
                    "fields, and wrap exported batches in ECC-HISE envelopes for transmission and "
                    "archival audit.",
                ],
            },
        ],
    },
    {
        "parent_section": "5.4 Synthesis: Vulnerabilities and Research Contributions",
        "subsections": [
            {
                "heading": "5.4.7 Regulatory Mapping Sketch",
                "paragraphs": [
                    "At a high level, ECC-DTB-AKA supports SCA-style possession factors and reduces "
                    "reliance on SMS OTP; ECC-HISE supports integrity and audit evidence expected "
                    "under SWIFT CSP and internal governance for settlement systems. Detailed "
                    "control-by-control mapping is institution-specific and left as future applied "
                    "work; the dissertation supplies the cryptographic substrate such mappings require.",
                ],
            },
        ],
    },
]


def main() -> None:
    from chapter01_enhancement import EXPANSION as h1
    from phase1_expansion import CHAPTER01_DEEP, CHAPTER01_EXPANSION
    from phase1_expansion2 import EXTRA_CHAPTER01
    from chapter02_enhancement import EXPANSION as h2
    from chapter02_expansion import EXPANSION as e2
    from chapter02_expansion2 import EXPANSION2 as e22
    from chapter03_enhancement import EXPANSION as h3
    from chapter03_expansion import EXPANSION as e3
    from chapter03_expansion import EXPANSION2 as e32
    from chapter04_enhancement import EXPANSION as h4
    from chapter04_expansion import EXPANSION as e4
    from chapter05_enhancement import EXPANSION as h5
    from chapter05_expansion import EXPANSION as e5
    from conclusions_enhancement import EXTRA_SECTIONS as cextra
    import conclusions as conc

    w1 = rewrite_sections(
        "chapter01", CHAPTER01_EXPANSION + CHAPTER01_DEEP + EXTRA_CHAPTER01 + h1
    )
    w2 = rewrite_sections("chapter02", e2 + e22 + h2)
    w3 = rewrite_sections("chapter03", e3 + e32 + h3)
    w4 = rewrite_sections("chapter04", e4 + h4, deep_extra=DEEP4)
    w5 = rewrite_sections("chapter05", e5 + h5, deep_extra=DEEP5)

    deep_conc = list(conc.SECTIONS)
    for sec in deep_conc:
        if sec["heading"] == "Summary of Approach":
            sec["paragraphs"].append(
                "Across these chapters, the dissertation maintains a consistent methodological "
                "stance: identify security gaps at architectural boundaries, encode banking "
                "semantics (device, transaction, batch audit) into cryptographic constructions, "
                "implement executable prototypes, and evaluate both qualitatively against attack "
                "catalogues and quantitatively against protocol baselines."
            )
        if sec["heading"] == "Limitations":
            sec["paragraphs"].append(
                "Additionally, user experience studies of device-binding friction, large-scale "
                "multi-institution interoperability trials, and machine-checked protocol proofs "
                "are outside the present evaluation envelope. Quantitative benchmarks reflect a "
                "research prototype stack (Python, software keys) and should be re-measured on "
                "production-grade runtimes before capacity planning."
            )
        if sec["heading"] == "Future Work":
            sec["paragraphs"].append(
                "A staged industrial roadmap would (1) deploy transaction-bound MACs under "
                "existing session keys, (2) introduce Merkle manifests for settlement files, "
                "(3) migrate to full ECC-DTB-AKA and hierarchical ECC-HISE with HSM custody, and "
                "(4) pursue post-quantum hybridization once standards and HSM support mature."
            )
    deep_conc = deep_conc + list(cextra)
    src = (CONTENT / "conclusions.py").read_text(encoding="utf-8")
    idx = src.find("SECTIONS = ")
    preamble = src[:idx]
    (CONTENT / "conclusions.py").write_text(
        preamble + "SECTIONS = " + pprint.pformat(deep_conc, width=100, sort_dicts=False) + "\n",
        encoding="utf-8",
    )

    print(f"words ch1={w1} ch2={w2} ch3={w3} ch4={w4} ch5={w5} conc={word_count(deep_conc)}")
    print("folded OK")


if __name__ == "__main__":
    main()
