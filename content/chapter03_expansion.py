"""Expansion content for Chapter 3."""

EXPANSION = [
    {
        "parent_section": "3.3 Hierarchical Key Management",
        "subsections": [
            {
                "heading": "3.3.3 Comparison with Flat Key Management",
                "paragraphs": [
                    "Traditional e-banking data encryption deploys a small number of long-lived data-encryption "
                    "keys (DEKs) wrapped by infrequently rotated key-encryption keys (KEKs). If a DEK is "
                    "compromised, all data encrypted under that key is exposed—potentially years of settlement "
                    "records. ECC-HISE's hierarchical derivation limits exposure to a single batch within a "
                    "single domain. The quantitative overhead of hierarchical derivation (two HKDF operations "
                    "per batch) is negligible compared to per-record encryption and signing.",
                ],
            },
        ],
    },
    {
        "parent_section": "3.5 Security Analysis",
        "subsections": [
            {
                "heading": "3.5.3 Addressing Section 1.3.3 Limitations",
                "paragraphs": [
                    "L1 (Flat key hierarchy): Resolved via MK → DK_i → SK_batch derivation.",
                    "L2 (Disconnected audit): Resolved — Merkle root is embedded in signed batch header.",
                    "L3 (Batch verification cost): Resolved — O(log n) Merkle proofs vs O(n) full reprocess.",
                    "L4 (Static PSKs): Resolved — per-batch session keys derived from domain keys.",
                    "L5 (Service-boundary gaps): Resolved — envelope integrity persists beyond TLS.",
                    "L6 (Audit friction): Resolved — cryptographic audit chain for regulators.",
                ],
            },
        ],
    },
]

EXPANSION2 = [
    {
        "parent_section": "3.4 Secure Envelope Construction",
        "subsections": [
            {
                "heading": "3.4.4 Deployment in Inter-Bank Settlement",
                "paragraphs": [
                    "In a representative deployment, Bank A's settlement server constructs an ECC-HISE "
                    "batch from end-of-day payment records and transmits the envelope to Bank B's settlement "
                    "server over mTLS. Bank B verifies the batch header signature, Merkle root, and each "
                    "record signature before posting to its core banking ledger. The clearing-house authority "
                    "receives (batch_id, Root, timestamp) for regulatory archive. This workflow satisfies "
                    "SWIFT CSP controls for data integrity and non-repudiation while adding cryptographic "
                    "audit efficiency not present in file-transfer-only approaches.",
                ],
            },
        ],
    },
    {
        "parent_section": "3.6 Effectiveness Analysis and Quantitative Evaluation",
        "subsections": [
            {
                "heading": "3.6.5 Scalability Projection",
                "paragraphs": [
                    "Linear scaling in record count dominates ECC-HISE processing time due to per-record "
                    "encryption and signing. For million-record national settlement files, parallel batch "
                    "partitioning (multiple ECC-HISE envelopes of 10,000 records each) enables "
                    "multi-core processing. Merkle roots of sub-batches can themselves form a meta-Merkle "
                    "tree for hierarchical audit—a straightforward extension not required for regional-bank "
                    "workloads but available for central-bank scale.",
                ],
            },
        ],
    },
]
