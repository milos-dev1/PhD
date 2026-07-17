"""Scheme Design Document content for ECC-DTB-AKA and ECC-HISE."""

TITLE = "Scheme Design Document"
SUBTITLE = "Novel ECC-Based Security Schemes for E-Banking Systems"

SECTIONS = [
    {
        "heading": "1. Overview",
        "paragraphs": [
            "This document specifies two original cryptographic schemes proposed in this dissertation: "
            "(A) ECC-DTB-AKA — Device- and Transaction-Bound Authenticated Key Agreement for client-server "
            "e-banking communication, and (B) ECC-HISE — Hierarchical Integrity-preserving Secure Envelope for "
            "server-server inter-bank data exchange. Both schemes employ elliptic curve cryptography (ECC) as "
            "the foundational primitive, selected for its superior security-per-bit ratio compared to RSA and "
            "its widespread adoption in modern financial infrastructure standards including EMV, FIDO2, and "
            "TLS 1.3.",
            "The schemes are designed to address distinct vulnerability classes identified in Chapter 1: "
            "ECC-DTB-AKA targets authentication and session-key establishment weaknesses in client-server "
            "channels (Section 1.2), while ECC-HISE targets data confidentiality, integrity, and auditability "
            "weaknesses in server-server settlement and record-transfer channels (Section 1.3).",
        ],
    },
    {
        "heading": "2. Scheme A: ECC-DTB-AKA",
        "paragraphs": [
            "ECC-DTB-AKA establishes a mutually authenticated session key between a banking client C and "
            "banking server S, with the session key further bound to a device fingerprint and a transaction "
            "nonce to enable per-transaction key derivation without additional round trips.",
        ],
        "subsections": [
            {
                "heading": "2.1 Notation",
                "paragraphs": [
                    "Let E be an elliptic curve over a finite field with base point G of prime order q. "
                    "Let H denote SHA-256, and HKDF denote RFC 5869 key derivation. "
                    "Denote scalar multiplication as [k]G. "
                    "Entities: Client C with long-term key pair (sk_C, PK_C = [sk_C]G); "
                    "Server S with certificate chain rooted in bank CA; "
                    "device_fp = H(hardware_attributes) truncated to 128 bits; "
                    "ephemeral pairs (ek_C, EK_C) and (ek_S, EK_S) generated per session.",
                ],
            },
            {
                "heading": "2.2 Protocol Steps (3-Round Handshake)",
                "paragraphs": [
                    "Round 1 (Client Init): C generates ephemeral (ek_C, EK_C), samples nonce_c ← {0,1}^128, "
                    "computes t_C = H(EK_C || PK_C || device_fp || nonce_c), "
                    "and sends MSG1 = (EK_C, PK_C, device_fp, nonce_c, Sig_C(sk_C, t_C)).",
                    "Round 2 (Server Response): S verifies Sig_C and PK_C against customer registry. "
                    "S generates (ek_S, EK_S), samples nonce_s, computes "
                    "Z = [ek_S]EK_C = [ek_C]EK_S, "
                    "MSK = HKDF(Z || device_fp || nonce_c || nonce_s || 'ECC-DTB-AKA-v1', 256), "
                    "and sends MSG2 = (EK_S, nonce_s, Cert_S, Sig_S(sk_S, H(EK_S || nonce_s || MSK))).",
                    "Round 3 (Client Confirm): C verifies Cert_S and Sig_S, recomputes MSK, "
                    "derives TBK_txn = HKDF(MSK || txn_nonce || 'TBK', 256) for a specific transaction, "
                    "and sends MSG3 = (HMAC(TBK_txn, txn_nonce), Sig_C(sk_C, H(MSK || 'confirm'))).",
                    "Upon successful verification, both parties hold MSK (master session key) and can derive "
                    "transaction-bound keys TBK_txn on demand.",
                ],
            },
            {
                "heading": "2.3 Security Properties",
                "paragraphs": [
                    "Authenticity: Mutual authentication via ECDSA signatures and server certificate validation.",
                    "Forward secrecy: Compromise of long-term keys does not reveal past MSK values due to ECDH ephemerals.",
                    "Device binding: device_fp included in HKDF salt prevents session transfer to unauthorized devices.",
                    "Transaction binding: TBK_txn incorporates txn_nonce, limiting replay to single transaction context.",
                    "Resistance: Replay (nonces + timestamps), MITM (signatures + cert chain), session hijacking (device_fp binding).",
                ],
            },
        ],
    },
    {
        "heading": "3. Scheme B: ECC-HISE",
        "paragraphs": [
            "ECC-HISE provides encrypted, signed, and auditable envelopes for batch financial records "
            "transferred between server nodes in an inter-bank or intra-bank settlement network.",
        ],
        "subsections": [
            {
                "heading": "3.1 Key Hierarchy",
                "paragraphs": [
                    "Level 0 — Master Key (MK): Stored in HSM at clearing-house authority; MK ∈ Z_q.",
                    "Level 1 — Domain Keys: DK_i = HKDF([MK]G || domain_id || 'DK', 256) for each business domain "
                    "(retail, corporate, settlement).",
                    "Level 2 — Session Keys: SK_batch = HKDF(DK_i || batch_id || epoch || 'SK', 256) rotated per batch.",
                ],
            },
            {
                "heading": "3.2 Envelope Construction",
                "paragraphs": [
                    "For each record r_j in batch B = {r_1, ..., r_n}: "
                    "(1) Generate ephemeral eph_j; compute shared Z_j via ECDH(eph_j, PK_receiver). "
                    "(2) Derive K_enc = HKDF(Z_j || SK_batch, 256); split into K_aes (128-bit) and K_mac (128-bit). "
                    "(3) ciphertext_j = AES-256-GCM(K_aes, IV_j, r_j). "
                    "(4) sig_j = Ed25519(sk_sender, H(ciphertext_j || batch_id || j)). "
                    "(5) leaf_j = H(ciphertext_j || sig_j || metadata_j). "
                    "Merkle root Root = Merkle(leaf_1, ..., leaf_n) is included in batch header. "
                    "Header = (batch_id, epoch, PK_eph, Root, Sig_header, timestamp).",
                ],
            },
            {
                "heading": "3.3 Verification and Audit",
                "paragraphs": [
                    "Receiver verifies Sig_header, reconstructs Merkle root from received records, "
                    "decrypts each record, and validates sig_j. Any tampering breaks Merkle root or GCM authentication tag. "
                    "Audit log stores (batch_id, Root, timestamp) immutably for regulatory compliance.",
                ],
            },
        ],
    },
    {
        "heading": "4. Comparison Baselines",
        "paragraphs": [
            "ECC-DTB-AKA will be compared against: TLS 1.3 full handshake + application-layer OTP; "
            "standard ECDH without device/transaction binding; OAuth 2.0 PKCE flow.",
            "ECC-HISE will be compared against: TLS record layer only; AES-GCM with static pre-shared keys; "
            "standard ECIES without hierarchical keys or Merkle audit chain.",
            "Metrics: authentication latency (ms), ciphertext overhead (bytes), round-trip count, "
            "and qualitative attack-resistance matrix.",
        ],
    },
    {
        "heading": "5. Implementation Mapping",
        "paragraphs": [
            "Prototype modules: prototype/ecc_dtb_aka/ (client, server, protocol), "
            "prototype/ecc_hise/ (envelope, merkle, hierarchy), "
            "prototype/benchmarks/ (timing and size measurements).",
            "Cryptographic library: Python cryptography (OpenSSL backend), curves: SECP256R1 and Ed25519.",
        ],
    },
]
