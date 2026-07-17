"""Appendix content for the PhD thesis."""

TITLE = "Appendix"

SECTIONS = [
    {
        "heading": "A. Algorithm Listings",
        "paragraphs": [
            "Algorithm A.1 (ECC-DTB-AKA Client Handshake): See Section 2.3.7. "
            "Algorithm A.2 (ECC-DTB-AKA Server Handshake): See Section 2.3.8. "
            "Algorithm A.3 (ECC-HISE Batch Envelope Construction): See Section 3.4.1–3.4.2. "
            "Algorithm A.4 (Merkle Root and Proof Verification): See prototype/ecc_hise/merkle.py.",
        ],
    },
    {
        "heading": "B. API Specification",
        "paragraphs": [
            "Prototype REST API (prototype/api/app.py): "
            "GET /health — returns status and supported schemes. "
            "POST /auth/register — body: {device_id}; registers client key. "
            "POST /auth/handshake/init — body: {device_id}; returns session_id and handshake data. "
            "POST /auth/handshake/complete — body: {session_id, txn_nonce_hex}; completes authentication. "
            "POST /settlement/submit-batch — body: {batch_id, domain_id, records[]}; submits and verifies batch.",
        ],
    },
    {
        "heading": "C. Benchmark Raw Data",
        "paragraphs": [
            "Chapter 2 benchmarks: thesis/benchmarks/chapter2_benchmarks.json. "
            "Chapter 3 benchmarks: thesis/benchmarks/chapter3_benchmarks.json. "
            "Reproduce via: python -m prototype.benchmarks.bench_dtb_aka && python -m prototype.benchmarks.bench_hise.",
        ],
    },
    {
        "heading": "D. Prototype Module Index",
        "paragraphs": [
            "prototype/common/crypto_utils.py — SHA-256, HKDF, ECDH, ECDSA utilities. "
            "prototype/ecc_dtb_aka/protocol.py — ECC-DTB-AKA client/server protocol. "
            "prototype/ecc_hise/hierarchy.py — hierarchical key derivation. "
            "prototype/ecc_hise/merkle.py — Merkle tree construction and proofs. "
            "prototype/ecc_hise/envelope.py — secure batch envelope. "
            "prototype/api/app.py — FastAPI integration. "
            "prototype/benchmarks/ — timing and size measurement scripts.",
        ],
    },
]
