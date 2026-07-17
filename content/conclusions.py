"""Concluding remarks for the PhD thesis."""

TITLE = "Conclusions"

SECTIONS = [
    {
        "heading": "Summary of Approach",
        "paragraphs": [
            "This dissertation investigated information security in electronic banking and electronic "
            "finance service systems, with emphasis on elliptic curve cryptography for authentication, "
            "key exchange, and data protection. A systematic threat analysis (Chapter 1) established "
            "the attack landscape and identified critical limitations in deployed authentication "
            "mechanisms (Section 1.2) and data-security mechanisms (Section 1.3).",
            "Two novel ECC-based methodologies were proposed, analyzed, implemented, and evaluated: "
            "ECC-DTB-AKA for client-server authenticated key agreement with device and transaction "
            "binding (Chapter 2), and ECC-HISE for server-server hierarchical secure envelopes with "
            "Merkle audit chains (Chapter 3). Chapter 4 demonstrated integrated architecture and "
            "programmatic implementation. Chapter 5 evaluated effectiveness against network attacks, "
            "reviewed prior work, and synthesized vulnerability findings.",
        ],
    },
    {
        "heading": "Contributions",
        "paragraphs": [
            "The principal contributions of this research are:",
            "First, the design and formal analysis of ECC-DTB-AKA, a three-round protocol achieving "
            "mutual authentication, forward secrecy, device binding, and per-transaction key derivation "
            "using SECP256R1 ECDH, ECDSA, and HKDF.",
            "Second, the design and formal analysis of ECC-HISE, a hierarchical envelope scheme "
            "combining domain-separated key derivation, AES-256-GCM encryption, Ed25519 signatures, "
            "and Merkle-tree batch integrity for inter-bank settlement.",
            "Third, a dual-layer integrated security architecture unifying both schemes in an "
            "e-financial service system with defined trust boundaries and component interactions.",
            "Fourth, a working software prototype with REST APIs, benchmark suites, and end-to-end "
            "integration tests providing reproducible quantitative evaluation.",
            "Fifth, comprehensive prior-work analysis positioning the proposed schemes relative to "
            "TLS 1.3, OAuth 2.0 PKCE, FIDO2, ECIES, static PSK, and blockchain audit approaches.",
        ],
    },
    {
        "heading": "Limitations",
        "paragraphs": [
            "This research has limitations that should be acknowledged. The prototype uses software "
            "key storage rather than hardware security modules. Formal security proofs are presented "
            "as structured proof sketches rather than machine-verified derivations. Certificate "
            "management is simplified compared to production PKI. The settlement demonstration "
            "performs sender and receiver verification in a single process. These limitations do "
            "not invalidate the cryptographic designs but indicate areas requiring hardening for "
            "production deployment.",
        ],
    },
    {
        "heading": "Future Work",
        "paragraphs": [
            "Future research directions include: integration of NIST post-quantum algorithms (ML-KEM, "
            "ML-DSA) for long-term confidentiality; HSM-backed key storage and FIPS 140-3 validation; "
            "formal verification using ProVerif or Tamarin provers; field trials with partner "
            "financial institutions; meta-Merkle hierarchies for million-record national settlement; "
            "and composition with FIDO2/WebAuthn for phishing-resistant client key enrollment.",
        ],
    },
]
