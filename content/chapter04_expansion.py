"""Expansion content for Chapter 4."""

EXPANSION = [
    {
        "parent_section": "4.2 Programmatic Implementation of ECC-DTB-AKA (Chapter 2)",
        "subsections": [
            {
                "heading": "4.2.5 Key Derivation Implementation Details",
                "paragraphs": [
                    "The HKDF implementation uses cryptography.hazmat.primitives.kdf.hkdf.HKDF with "
                    "SHA-256 as the hash function. MSK derivation concatenates device_fp, nonce_c, and "
                    "nonce_s as salt with info string 'ECC-DTB-AKA-v1'. TBK derivation uses txn_nonce "
                    "as salt with info string 'TBK'. These domain-separated info strings prevent "
                    "cross-protocol key reuse if additional derivation functions are added.",
                ],
            },
        ],
    },
    {
        "parent_section": "4.3 Programmatic Implementation of ECC-HISE (Chapter 3)",
        "subsections": [
            {
                "heading": "4.3.5 Merkle Tree Implementation",
                "paragraphs": [
                    "The Merkle tree implementation (merkle.py) uses SHA-256 for internal nodes. Odd-length "
                    "layers duplicate the last node (Bitcoin-style) to ensure deterministic root computation. "
                    "Proof generation handles odd-layer promotion with self-pairing. Verification reconstructs "
                    "the path from leaf to root in O(log n) hashes. For n=100 records, proof length is 7 hashes "
                    "(224 bytes), enabling compact audit evidence.",
                ],
            },
        ],
    },
]
