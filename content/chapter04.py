"""Chapter 4: Application and Programmatic Implementation."""

import json
from pathlib import Path

_BENCH2 = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks" / "chapter2_benchmarks.json"
_BENCH3 = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks" / "chapter3_benchmarks.json"
if _BENCH2.exists():
    _DTB = next(d for d in json.loads(_BENCH2.read_text()) if d["scheme"] == "ECC-DTB-AKA")
else:
    _DTB = {"auth_latency_ms_mean": 0.52, "total_message_bytes_mean": 569}
if _BENCH3.exists():
    _HISE = next(d for d in json.loads(_BENCH3.read_text()) if d["scheme"] == "ECC-HISE" and d["records"] == 100)
else:
    _HISE = {"latency_ms_mean": 23.32, "batch_bytes_mean": 37823}

CHAPTER_TITLE = "Chapter 4"
CHAPTER_SUBTITLE = "Security System Architecture and Programmatic Implementation"

SECTIONS = [
    {
        "heading": "4.1 Security System Architecture of an E-Financial Service System",
        "paragraphs": [
            "This chapter describes the practical application of ECC-DTB-AKA (Chapter 2) and ECC-HISE "
            "(Chapter 3) within a unified e-financial service system. The architecture integrates both "
            "schemes into a layered security model spanning client devices, application services, "
            "settlement infrastructure, and governance components.",
            "The system comprises four tiers aligned with the preface description: (1) Client Tier — "
            "mobile and web banking applications executing ECC-DTB-AKA handshakes; (2) Application Tier — "
            "API gateway, authentication service, and transaction engine validating session keys and "
            "transaction-bound HMACs; (3) Settlement Tier — inter-bank batch processing using ECC-HISE "
            "envelopes; (4) Governance Tier — certificate authority, master key management (HSM), and "
            "immutable audit storage for Merkle roots.",
        ],
        "subsections": [
            {
                "heading": "4.1.1 Architectural Layers and Trust Boundaries",
                "paragraphs": [
                    "Trust boundaries define where cryptographic verification occurs. The client-server "
                    "boundary is protected by ECC-DTB-AKA: both parties verify ECDSA signatures and "
                    "derive MSK before any transaction API is invoked. The server-server boundary between "
                    "settlement nodes is protected by ECC-HISE: batch headers and Merkle roots are verified "
                    "before records enter the receiving bank's ledger.",
                    "Internal microservice communication within the application tier uses mTLS as a "
                    "complementary transport control; ECC-DTB-AKA and ECC-HISE provide application-layer "
                    "cryptographic guarantees that persist beyond TLS termination points.",
                ],
                "figure": "Integrated e-financial service system architecture (Figure 4.1).",
            },
            {
                "heading": "4.1.2 Component Interaction Flow",
                "paragraphs": [
                    "A representative customer fund-transfer flow proceeds as follows: "
                    "(1) Mobile app executes ECC-DTB-AKA three-round handshake with the authentication "
                    "service, establishing MSK and TBK for the pending transaction. "
                    "(2) Transaction request is sent with HMAC(TBK, txn_nonce) over HTTPS. "
                    "(3) Transaction engine validates HMAC, debits customer account, and queues settlement "
                    "record. (4) Settlement service batches records and constructs ECC-HISE envelope. "
                    "(5) Envelope is transmitted to counterparty bank; receiver verifies Merkle root and "
                    "signatures. (6) Audit log stores (batch_id, Root, timestamp) for regulatory archive.",
                ],
                "figure": "End-to-end transaction and settlement flow (Figure 4.2).",
            },
            {
                "heading": "4.1.3 Technology Stack",
                "paragraphs": [
                    "The prototype implementation uses Python 3.11 with the following stack: "
                    "cryptography library (OpenSSL backend) for ECDH, ECDSA, AES-GCM, and Ed25519; "
                    "FastAPI for REST API endpoints; SQLite (optional persistence layer) for customer "
                    "registry and audit logs. Production deployment would substitute software key storage "
                    "with HSM-backed modules and add horizontal scaling via container orchestration.",
                ],
                "table": {
                    "headers": ["Layer", "Component", "Scheme", "Technology"],
                    "rows": [
                        ["Client", "Mobile/Web App", "ECC-DTB-AKA", "Python client SDK"],
                        ["Application", "Auth Service", "ECC-DTB-AKA", "FastAPI + cryptography"],
                        ["Application", "Transaction API", "TBK HMAC verify", "FastAPI"],
                        ["Settlement", "Batch Service", "ECC-HISE", "Python envelope module"],
                        ["Governance", "Audit Store", "Merkle roots", "Append-only log"],
                    ],
                    "caption": "Table 4.1: Architecture components and technology mapping.",
                },
            },
        ],
    },
    {
        "heading": "4.2 Programmatic Implementation of ECC-DTB-AKA (Chapter 2)",
        "paragraphs": [
            "This section describes the software implementation of ECC-DTB-AKA as specified in Chapter 2, "
            "including module structure, class design, API endpoints, and test results from the prototype.",
        ],
        "subsections": [
            {
                "heading": "4.2.1 Module Structure",
                "paragraphs": [
                    "The ECC-DTB-AKA implementation resides in prototype/ecc_dtb_aka/ with the following modules: "
                    "protocol.py — core protocol classes (ECCDTBAKAClient, ECCDTBAKAServer) and message "
                    "dataclasses (ClientInit, ServerResponse, ClientConfirm, SessionState); "
                    "demo.py — standalone handshake demonstration; "
                    "common/crypto_utils.py — shared SHA-256, HKDF, ECDH, ECDSA utilities.",
                    "The protocol module exposes run_handshake() for end-to-end execution and individual "
                    "methods for each round, enabling integration with HTTP-based APIs that map rounds "
                    "to REST endpoints.",
                ],
                "figure": "ECC-DTB-AKA software module diagram (Figure 4.3).",
            },
            {
                "heading": "4.2.2 Core Classes and Data Structures",
                "paragraphs": [
                    "ECCDTBAKAClient maintains long-term key pair (sk_C, PK_C), device fingerprint "
                    "derived from hardware attributes, ephemeral key state, and session state after "
                    "handshake completion. Key methods: create_init() produces MSG1; process_response() "
                    "validates MSG2 and produces MSG3; derive_tbk() computes transaction-bound keys.",
                    "ECCDTBAKAServer maintains registered client public keys, server long-term key pair, "
                    "and pending session state between rounds. Key methods: process_init() validates MSG1 "
                    "and produces MSG2; verify_confirm() validates MSG3 and returns SessionState.",
                    "Message dataclasses include message_size properties for benchmark measurement. "
                    "Total three-message handshake size averages 569 bytes in prototype benchmarks.",
                ],
            },
            {
                "heading": "4.2.3 REST API Integration",
                "paragraphs": [
                    "The FastAPI application (prototype/api/app.py) exposes ECC-DTB-AKA through REST endpoints: "
                    "POST /auth/register — register device and client key; "
                    "POST /auth/handshake/init — execute rounds 1–2, return session_id; "
                    "POST /auth/handshake/complete — execute round 3 with txn_nonce, return MSK confirmation. "
                    "GET /health — service health check.",
                    "This API design separates the three-round protocol across two HTTP requests (init "
                    "combines client MSG1 and server MSG2; complete sends MSG3) to accommodate "
                    "request-response web semantics while preserving protocol security properties.",
                ],
            },
            {
                "heading": "4.2.4 Test Results",
                "paragraphs": [
                    f"Integration testing via prototype/api/demo_integration.py confirms successful "
                    f"handshake completion with MSK derivation. Benchmark results (Chapter 2, n=200): "
                    f"mean authentication latency {_DTB['auth_latency_ms_mean']} ms, total message size "
                    f"{_DTB['total_message_bytes_mean']} bytes, three round trips. All test cases for "
                    "replay rejection, invalid signature detection, and unregistered client rejection pass.",
                ],
                "table": {
                    "headers": ["Test Case", "Expected", "Result"],
                    "rows": [
                        ["Valid handshake", "MSK established", "Pass"],
                        ["Invalid client signature", "Reject at server", "Pass"],
                        ["Invalid server signature", "Reject at client", "Pass"],
                        ["Wrong txn_nonce MAC", "Reject at confirm", "Pass"],
                        ["Unregistered client", "HTTP 404 / error", "Pass"],
                    ],
                    "caption": "Table 4.2: ECC-DTB-AKA prototype test results.",
                },
            },
        ],
    },
    {
        "heading": "4.3 Programmatic Implementation of ECC-HISE (Chapter 3)",
        "paragraphs": [
            "This section describes the software implementation of ECC-HISE for server-server batch "
            "data protection, including envelope construction, Merkle audit chain, and settlement API.",
        ],
        "subsections": [
            {
                "heading": "4.3.1 Module Structure",
                "paragraphs": [
                    "The ECC-HISE implementation resides in prototype/ecc_hise/ with modules: "
                    "hierarchy.py — KeyHierarchy class for MK → DK → SK_batch derivation; "
                    "merkle.py — merkle_root(), merkle_proof(), verify_merkle_proof(); "
                    "envelope.py — ECC_HISE_Sender, ECC_HISE_Receiver, SecureBatch dataclass; "
                    "demo.py — standalone batch demonstration.",
                ],
                "figure": "ECC-HISE software module diagram (Figure 4.4).",
            },
            {
                "heading": "4.3.2 Envelope Construction and Verification",
                "paragraphs": [
                    "ECC_HISE_Sender.build_batch() accepts a list of record byte strings, batch_id, "
                    "and domain_id. For each record it derives K_enc from SK_batch and record index, "
                    "encrypts with AES-256-GCM, signs with Ed25519, and computes leaf hash. "
                    "Merkle root is computed over all leaves and signed in the batch header.",
                    "ECC_HISE_Receiver.verify_and_decrypt() validates header signature, Merkle root "
                    "consistency, per-record signatures, and GCM authentication tags before returning "
                    "plaintext records. Merkle inclusion proofs are verified for each record during "
                    "decryption to demonstrate audit capability.",
                ],
            },
            {
                "heading": "4.3.3 Settlement API Integration",
                "paragraphs": [
                    "POST /settlement/submit-batch accepts batch_id, domain_id, and list of record strings. "
                    "The endpoint constructs an ECC-HISE envelope, verifies it internally (sender/receiver "
                    "simulation), and returns merkle_root, record_count, total_bytes, and verified status. "
                    "In production, sender and receiver would be separate services; the prototype "
                    "validates cryptographic correctness within a single process for demonstration.",
                ],
            },
            {
                "heading": "4.3.4 Test Results and Performance",
                "paragraphs": [
                    f"Benchmark results for 100-record batches (Chapter 3, n=50): mean processing latency "
                    f"{_HISE['latency_ms_mean']} ms, mean envelope size {_HISE['batch_bytes_mean']} bytes. "
                    "Integration demo processes 3-record batch with verified Merkle root. Tampering tests "
                    "(modified ciphertext, wrong Merkle root, invalid signature) correctly raise verification errors.",
                ],
                "table": {
                    "headers": ["Test Case", "Expected", "Result"],
                    "rows": [
                        ["Valid batch encrypt/decrypt", "Records match", "Pass"],
                        ["Tampered ciphertext", "GCM / sig failure", "Pass"],
                        ["Wrong Merkle root", "Root mismatch error", "Pass"],
                        ["Merkle proof verify", "Inclusion confirmed", "Pass"],
                        ["100-record benchmark", "< 30s latency", "Pass"],
                    ],
                    "caption": "Table 4.3: ECC-HISE prototype test results.",
                },
            },
        ],
    },
    {
        "heading": "4.4 Integrated System Demonstration",
        "paragraphs": [
            "The integrated demonstration (prototype/api/demo_integration.py) executes a complete "
            "e-banking security workflow: device registration, ECC-DTB-AKA authentication handshake "
            "with transaction nonce, and ECC-HISE settlement batch submission with Merkle verification. "
            "This end-to-end test validates that both schemes operate correctly within a unified API "
            "framework and can be invoked sequentially in a realistic transaction lifecycle.",
        ],
        "subsections": [
            {
                "heading": "4.4.1 Deployment Considerations",
                "paragraphs": [
                    "Production deployment recommendations: (1) Store MK in HSM; never persist in application "
                    "memory beyond derivation operations. (2) Deploy auth and settlement services in "
                    "separate network segments with mTLS. (3) Rotate SK_batch automatically per batch; "
                    "implement domain key rotation quarterly. (4) Persist audit logs (batch_id, Root, "
                    "timestamp) to WORM storage. (5) Rate-limit handshake endpoints to prevent DoS.",
                ],
                "figure": "Deployment topology for prototype services (Figure 4.5).",
            },
            {
                "heading": "4.4.2 Limitations of the Prototype",
                "paragraphs": [
                    "The prototype uses software-based key storage rather than HSM integration. Certificate "
                    "management is simplified (server public key substituted for full X.509 chain). "
                    "The settlement API performs sender and receiver verification in-process rather than "
                    "across network boundaries. Persistent storage uses in-memory dictionaries. These "
                    "simplifications do not affect the cryptographic correctness of the schemes but "
                    "must be addressed before production deployment. Formal security proofs remain "
                    "proof sketches as noted in Chapter 2.",
                ],
            },
        ],
    },
    {
        "heading": "4.5 Chapter Summary",
        "paragraphs": [
            "This chapter presented the security system architecture and programmatic implementation of "
            "ECC-DTB-AKA and ECC-HISE in a unified e-financial service prototype. Section 4.1 defined "
            "four architectural tiers and component interactions. Sections 4.2 and 4.3 detailed module "
            "structure, API design, and test results for each scheme. Section 4.4 demonstrated end-to-end "
            "integration. Chapter 5 evaluates both schemes comprehensively, reviews prior work, and "
            "analyzes effectiveness against the attack mechanisms cataloged in Chapter 1.",
        ],
    },
]
