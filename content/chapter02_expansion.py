"""Expansion content for Chapter 2 depth."""

EXPANSION = [
    {
        "parent_section": "2.3 Protocol Specification",
        "subsections": [
            {
                "heading": "2.3.6 Message Format Summary",
                "paragraphs": [
                    "Table 2.3 summarizes the wire-format fields for each protocol message. All integer "
                    "fields are encoded in big-endian. Public keys use X9.62 uncompressed point format "
                    "(65 bytes for P-256). Signatures are DER-encoded ECDSA (typically 70–72 bytes).",
                    "The total payload for a complete handshake is approximately 569 bytes as measured "
                    "in the prototype, making ECC-DTB-AKA suitable for bandwidth-constrained mobile "
                    "networks. By comparison, a typical TLS 1.3 handshake with a 2 KB certificate chain "
                    "exceeds 3 KB before application data.",
                ],
                "table": {
                    "headers": ["Message", "Field", "Size (bytes)", "Description"],
                    "rows": [
                        ["MSG1", "EK_C", "65", "Client ephemeral public key"],
                        ["MSG1", "PK_C", "65", "Client long-term public key"],
                        ["MSG1", "device_fp", "16", "Device fingerprint"],
                        ["MSG1", "nonce_c", "16", "Client nonce"],
                        ["MSG1", "σ_C", "~72", "ECDSA signature"],
                        ["MSG2", "EK_S", "65", "Server ephemeral public key"],
                        ["MSG2", "nonce_s", "16", "Server nonce"],
                        ["MSG2", "Cert_S", "65", "Server public key (prototype)"],
                        ["MSG2", "σ_S", "~72", "ECDSA signature"],
                        ["MSG3", "τ", "32", "HMAC-SHA256 transaction tag"],
                        ["MSG3", "txn_nonce", "16", "Transaction nonce"],
                        ["MSG3", "σ_confirm", "~72", "Client confirmation signature"],
                    ],
                    "caption": "Table 2.3: ECC-DTB-AKA message field specification.",
                },
            },
        ],
    },
    {
        "parent_section": "2.4 Security Analysis",
        "subsections": [
            {
                "heading": "2.4.4 Session Lifecycle and Key Erasure",
                "paragraphs": [
                    "Secure session lifecycle management is essential for limiting the window of exposure "
                    "after key establishment. ECC-DTB-AKA mandates the following lifecycle policies: "
                    "(1) Ephemeral private keys ek_C and ek_S are erased from memory immediately after "
                    "MSK derivation; (2) MSK is retained only for the session duration (configurable, "
                    "default 15 minutes for retail banking); (3) TBK_txn values are erased after "
                    "transaction completion or timeout; (4) Session termination requires an explicit "
                    "MSG_end or timeout, after which MSK is erased and a new handshake is required.",
                    "These policies ensure that the number of transactions protected by a single MSK is "
                    "bounded, and that ephemeral key material does not persist in memory beyond its "
                    "useful lifetime. In the prototype implementation, Python's garbage collector "
                    "handles key erasure; a production deployment would use secure memory allocation "
                    "and explicit zeroization, ideally within a trusted execution environment.",
                ],
            },
        ],
    },
    {
        "parent_section": "2.5 Effectiveness Analysis and Quantitative Evaluation",
        "subsections": [
            {
                "heading": "2.5.6 Resistance to Limitations from Section 1.2.3",
                "paragraphs": [
                    "Mapping the quantitative and qualitative evaluation results to the six limitations "
                    "identified in Section 1.2.3 confirms that ECC-DTB-AKA addresses each limitation:",
                    "L1 (Decoupled auth layers): Resolved — user and server authentication occur within "
                    "the key-exchange protocol via ECDSA signatures on handshake transcripts.",
                    "L2 (No device binding): Resolved — device_fp is included in HKDF salt for MSK derivation.",
                    "L3 (No per-txn key derivation): Resolved — TBK_txn derived locally without extra rounds.",
                    "L4 (Bearer token vulnerability): Mitigated — session state is bound to cryptographic "
                    "keys rather than opaque bearer tokens.",
                    "L5 (No message-level integrity): Partially addressed at session level; full "
                    "message-level integrity for server-server data is addressed by ECC-HISE in Chapter 3.",
                    "L6 (Legacy TLS configurations): Avoided — protocol specifies fixed algorithms with "
                    "no downgrade-negotiation surface.",
                ],
            },
        ],
    },
]
