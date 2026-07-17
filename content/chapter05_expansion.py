"""Expansion content for Chapter 5."""

EXPANSION = [
    {
        "parent_section": "5.2 Prior Work on Authentication and Key Exchange",
        "subsections": [
            {
                "heading": "5.2.6 EMV and Card-Present Authentication",
                "paragraphs": [
                    "EMV (Europay, Mastercard, Visa) chip cards use ECDSA on secp256r1 for offline and "
                    "online transaction authentication. Contactless payments add relay-attack vulnerabilities "
                    "addressed by distance-bounding protocols under research. EMV addresses card-present "
                    "channels; ECC-DTB-AKA addresses remote digital banking channels with similar ECC "
                    "foundations but different binding requirements (device_fp, txn_nonce).",
                ],
            },
        ],
    },
    {
        "parent_section": "5.3 Prior Work on Data Encryption, Security, and Integrity",
        "subsections": [
            {
                "heading": "5.3.6 Database TDE and Column-Level Encryption",
                "paragraphs": [
                    "Transparent Data Encryption (TDE) protects data at rest in Oracle, SQL Server, and "
                    "PostgreSQL extensions. Column-level encryption targets sensitive fields (PAN, SSN). "
                    "These mechanisms protect storage but not data in transit between services or audit "
                    "integrity of exported settlement batches. ECC-HISE complements TDE by protecting "
                    "inter-service batch transfer with verifiable integrity chains.",
                ],
            },
        ],
    },
    {
        "parent_section": "5.4 Synthesis: Vulnerabilities and Research Contributions",
        "subsections": [
            {
                "heading": "5.4.4 Alignment with Regulatory Requirements",
                "paragraphs": [
                    "PCI DSS Requirement 4 mandates strong cryptography for transmission; Requirement 3 for "
                    "storage. PSD2 Strong Customer Authentication aligns with ECC-DTB-AKA mutual authentication. "
                    "SWIFT CSP controls for integrity and non-repudiation align with ECC-HISE signed Merkle "
                    "batch headers. The proposed schemes support compliance objectives while exceeding minimum "
                    "baselines through integrated device binding and cryptographic audit.",
                ],
            },
        ],
    },
]
