"""Concluding remarks for the PhD thesis."""

TITLE = "Conclusions"

SECTIONS = [{'heading': 'Summary of Approach',
  'paragraphs': ['This dissertation investigated information security in electronic banking and '
                 'electronic finance service systems, with emphasis on elliptic curve cryptography '
                 'for authentication, key exchange, and data protection. A systematic threat '
                 'analysis (Chapter 1) established the attack landscape and identified critical '
                 'limitations in deployed authentication mechanisms (Section 1.2) and '
                 'data-security mechanisms (Section 1.3).',
                 'Two novel ECC-based methodologies were proposed, analyzed, implemented, and '
                 'evaluated: ECC-DTB-AKA for client-server authenticated key agreement with device '
                 'and transaction binding (Chapter 2), and ECC-HISE for server-server hierarchical '
                 'secure envelopes with Merkle audit chains (Chapter 3). Chapter 4 demonstrated '
                 'integrated architecture and programmatic implementation. Chapter 5 evaluated '
                 'effectiveness against network attacks, reviewed prior work, and synthesized '
                 'vulnerability findings.',
                 'Across these chapters, the dissertation maintains a consistent methodological '
                 'stance: identify security gaps at architectural boundaries, encode banking '
                 'semantics (device, transaction, batch audit) into cryptographic constructions, '
                 'implement executable prototypes, and evaluate both qualitatively against attack '
                 'catalogues and quantitatively against protocol baselines.']},
 {'heading': 'Contributions',
  'paragraphs': ['The principal contributions of this research are:',
                 'First, the design and formal analysis of ECC-DTB-AKA, a three-round protocol '
                 'achieving mutual authentication, forward secrecy, device binding, and '
                 'per-transaction key derivation using SECP256R1 ECDH, ECDSA, and HKDF.',
                 'Second, the design and formal analysis of ECC-HISE, a hierarchical envelope '
                 'scheme combining domain-separated key derivation, AES-256-GCM encryption, '
                 'Ed25519 signatures, and Merkle-tree batch integrity for inter-bank settlement.',
                 'Third, a dual-layer integrated security architecture unifying both schemes in an '
                 'e-financial service system with defined trust boundaries and component '
                 'interactions.',
                 'Fourth, a working software prototype with REST APIs, benchmark suites, and '
                 'end-to-end integration tests providing reproducible quantitative evaluation.',
                 'Fifth, comprehensive prior-work analysis positioning the proposed schemes '
                 'relative to TLS 1.3, OAuth 2.0 PKCE, FIDO2, ECIES, static PSK, and blockchain '
                 'audit approaches.']},
 {'heading': 'Limitations',
  'paragraphs': ['This research has limitations that should be acknowledged. The prototype uses '
                 'software key storage rather than hardware security modules. Formal security '
                 'proofs are presented as structured proof sketches rather than machine-verified '
                 'derivations. Certificate management is simplified compared to production PKI. '
                 'The settlement demonstration performs sender and receiver verification in a '
                 'single process. These limitations do not invalidate the cryptographic designs '
                 'but indicate areas requiring hardening for production deployment.',
                 'Additionally, user experience studies of device-binding friction, large-scale '
                 'multi-institution interoperability trials, and machine-checked protocol proofs '
                 'are outside the present evaluation envelope. Quantitative benchmarks reflect a '
                 'research prototype stack (Python, software keys) and should be re-measured on '
                 'production-grade runtimes before capacity planning.']},
 {'heading': 'Future Work',
  'paragraphs': ['Future research directions include: integration of NIST post-quantum algorithms '
                 '(ML-KEM, ML-DSA) for long-term confidentiality; HSM-backed key storage and FIPS '
                 '140-3 validation; formal verification using ProVerif or Tamarin provers; field '
                 'trials with partner financial institutions; meta-Merkle hierarchies for '
                 'million-record national settlement; and composition with FIDO2/WebAuthn for '
                 'phishing-resistant client key enrollment.',
                 'A staged industrial roadmap would (1) deploy transaction-bound MACs under '
                 'existing session keys, (2) introduce Merkle manifests for settlement files, (3) '
                 'migrate to full ECC-DTB-AKA and hierarchical ECC-HISE with HSM custody, and (4) '
                 'pursue post-quantum hybridization once standards and HSM support mature.']},
 {'heading': 'Synthesis of the Dual-Layer Methodology',
  'paragraphs': ['This dissertation began from a systems observation: e-banking security failures '
                 'frequently arise at boundaries—between transport and application authentication, '
                 'between sessions and transactions, and between TLS termination and persistent '
                 'settlement data. The dual-layer methodology responds with two ECC-centered '
                 'schemes that encode banking semantics directly into key derivation and integrity '
                 'structures.',
                 'ECC-DTB-AKA shows that device and transaction binding can be integrated into '
                 'authenticated key agreement without abandoning standards-based curves and HKDF. '
                 'ECC-HISE shows that hierarchical keys plus Merkle-authenticated envelopes can '
                 'deliver confidentiality, authenticity, and efficient audit for server-server '
                 'batches without requiring global consensus ledgers. Chapter 4 demonstrated that '
                 'both can be implemented and composed; Chapter 5 showed that together they cover '
                 'the requirement set SR1–SR8 more completely than any single prior baseline '
                 'examined.']},
 {'heading': 'Implications for Research and Practice',
  'paragraphs': ['For researchers, the work argues that protocol design for finance should treat '
                 'device binding, transaction binding, and batch auditability as first-class goals '
                 'alongside classical AKE properties. For practitioners, the schemes offer '
                 'incremental adoption paths: transaction-bound authorizers atop existing '
                 'channels; Merkle manifests atop existing encrypted settlement files; later, full '
                 'hierarchical keying and handshake integration.',
                 'The prototype is a research artifact, not a product. Industrial deployment '
                 'requires HSM integration, attestation policy, certificate lifecycle alignment, '
                 'and rigorous operational monitoring. Those engineering tasks are outside the '
                 "dissertation's evaluation scope but are enabled by the explicit wire formats and "
                 'domain-separated labels specified herein.']},
 {'heading': 'Closing Remarks',
  'paragraphs': ['Electronic finance will continue to digitize and to attract capable adversaries. '
                 'Cryptography cannot eliminate fraud, but it can remove entire classes of remote '
                 'abuse that depend on portable bearer sessions and silently mutable batches. By '
                 'unifying ECC-based client-server authentication and server-server integrity '
                 'under one methodological umbrella, this dissertation contributes concrete '
                 'protocols, analyses, and implementations toward that narrower—and '
                 'achievable—goal.']}]
