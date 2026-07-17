"""Static index metadata for TOC, figures, and tables."""

FRONT_MATTER = [
    ("Abstract", 1),
    ("Preface", 1),
]

CHAPTERS = [
    ("Chapter 1", "Attack Mechanisms, Threat Landscape, and Security Gaps in E-Banking Systems"),
    ("Chapter 2", "ECC-DTB-AKA: Device- and Transaction-Bound Authenticated Key Agreement"),
    ("Chapter 3", "ECC-HISE: Hierarchical Integrity-preserving Secure Envelope"),
    ("Chapter 4", "Security System Architecture and Programmatic Implementation"),
    ("Chapter 5", "Evaluation, Prior Work Analysis, and Vulnerability Synthesis"),
    ("Conclusions", None),
    ("Appendix", None),
    ("References", None),
]

FIGURES = [
    "Figure 1.1: Attack lifecycle in e-banking systems",
    "Figure 1.2: Current client-server authentication flow",
    "Figure 1.3: Server-server mTLS service mesh architecture",
    "Figure 1.4: Data protection layers in e-banking systems",
    "Figure 1.5: Threat model for e-banking system",
    "Figure 2.1: ECC-DTB-AKA three-round handshake",
    "Figure 2.2: Key derivation hierarchy in ECC-DTB-AKA",
    "Figure 2.3: Quantitative comparison of authentication schemes",
    "Figure 3.1: ECC-HISE hierarchical key structure",
    "Figure 3.2: ECC-HISE secure envelope with Merkle audit chain",
    "Figure 3.3: Server-server batch verification and audit flow",
    "Figure 3.4: ECC-HISE quantitative comparison",
    "Figure 4.1: Integrated e-financial service system architecture",
    "Figure 4.2: End-to-end transaction and settlement flow",
    "Figure 4.3: ECC-DTB-AKA software module diagram",
    "Figure 4.4: ECC-HISE software module diagram",
    "Figure 4.5: Deployment topology for prototype services",
    "Figure 5.1: Comparative attack resistance overview",
    "Figure 5.2: Combined quantitative performance of proposed schemes",
    "Figure 5.3: TLS 1.3 full handshake flow",
    "Figure 5.4: OAuth 2.0 PKCE authorization flow",
    "Figure 5.5: mTLS service mesh authentication",
    "Figure 5.6: TLS record layer vs. persistent envelope integrity",
    "Figure 5.7: Merkle audit — blockchain vs. ECC-HISE",
]

TABLES = [
    "Table 1.1: Taxonomy of attack mechanisms against e-banking systems",
    "Table 1.2: Limitations of current authentication and key-exchange mechanisms",
    "Table 1.3: Limitations of current data security mechanisms",
    "Table 1.4: Comparative overview of authentication protocols for e-banking",
    "Table 2.1: ECC-DTB-AKA resistance to e-banking attack mechanisms",
    "Table 2.2: Quantitative comparison of authentication schemes",
    "Table 2.3: ECC-DTB-AKA message field specification",
    "Table 2.4: Projected end-to-end authentication time for ECC-DTB-AKA",
    "Table 3.1: ECC-HISE resistance to server-server data attacks",
    "Table 3.2: Quantitative comparison for 100-record settlement batches",
    "Table 4.1: Architecture components and technology mapping",
    "Table 4.2: ECC-DTB-AKA prototype test results",
    "Table 4.3: ECC-HISE prototype test results",
    "Table 5.1: Attack resistance matrix for proposed schemes vs. baselines",
    "Table 5.2: Authentication and key-exchange prior work vs. ECC-DTB-AKA",
    "Table 5.3: Data encryption and integrity prior work vs. ECC-HISE",
    "Table 5.4: Vulnerabilities in existing e-banking systems and dissertation responses",
]
