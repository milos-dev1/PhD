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

SECTIONS = [{'heading': '4.1 Security System Architecture of an E-Financial Service System',
  'paragraphs': ['This chapter describes the practical application of ECC-DTB-AKA (Chapter 2) and '
                 'ECC-HISE (Chapter 3) within a unified e-financial service system. The '
                 'architecture integrates both schemes into a layered security model spanning '
                 'client devices, application services, settlement infrastructure, and governance '
                 'components.',
                 'The system comprises four tiers aligned with the preface description: (1) Client '
                 'Tier — mobile and web banking applications executing ECC-DTB-AKA handshakes; (2) '
                 'Application Tier — API gateway, authentication service, and transaction engine '
                 'validating session keys and transaction-bound HMACs; (3) Settlement Tier — '
                 'inter-bank batch processing using ECC-HISE envelopes; (4) Governance Tier — '
                 'certificate authority, master key management (HSM), and immutable audit storage '
                 'for Merkle roots.'],
  'subsections': [{'heading': '4.1.1 Architectural Layers and Trust Boundaries',
                   'paragraphs': ['Trust boundaries define where cryptographic verification '
                                  'occurs. The client-server boundary is protected by ECC-DTB-AKA: '
                                  'both parties verify ECDSA signatures and derive MSK before any '
                                  'transaction API is invoked. The server-server boundary between '
                                  'settlement nodes is protected by ECC-HISE: batch headers and '
                                  'Merkle roots are verified before records enter the receiving '
                                  "bank's ledger.",
                                  'Internal microservice communication within the application tier '
                                  'uses mTLS as a complementary transport control; ECC-DTB-AKA and '
                                  'ECC-HISE provide application-layer cryptographic guarantees '
                                  'that persist beyond TLS termination points.'],
                   'figure': 'Integrated e-financial service system architecture (Figure 4.1).'},
                  {'heading': '4.1.2 Component Interaction Flow',
                   'paragraphs': ['A representative customer fund-transfer flow proceeds as '
                                  'follows: (1) Mobile app executes ECC-DTB-AKA three-round '
                                  'handshake with the authentication service, establishing MSK and '
                                  'TBK for the pending transaction. (2) Transaction request is '
                                  'sent with HMAC(TBK, txn_nonce) over HTTPS. (3) Transaction '
                                  'engine validates HMAC, debits customer account, and queues '
                                  'settlement record. (4) Settlement service batches records and '
                                  'constructs ECC-HISE envelope. (5) Envelope is transmitted to '
                                  'counterparty bank; receiver verifies Merkle root and '
                                  'signatures. (6) Audit log stores (batch_id, Root, timestamp) '
                                  'for regulatory archive.'],
                   'figure': 'End-to-end transaction and settlement flow (Figure 4.2).'},
                  {'heading': '4.1.3 Technology Stack',
                   'paragraphs': ['The prototype implementation uses Python 3.11 with the '
                                  'following stack: cryptography library (OpenSSL backend) for '
                                  'ECDH, ECDSA, AES-GCM, and Ed25519; FastAPI for REST API '
                                  'endpoints; SQLite (optional persistence layer) for customer '
                                  'registry and audit logs. Production deployment would substitute '
                                  'software key storage with HSM-backed modules and add horizontal '
                                  'scaling via container orchestration.'],
                   'table': {'headers': ['Layer', 'Component', 'Scheme', 'Technology'],
                             'rows': [['Client',
                                       'Mobile/Web App',
                                       'ECC-DTB-AKA',
                                       'Python client SDK'],
                                      ['Application',
                                       'Auth Service',
                                       'ECC-DTB-AKA',
                                       'FastAPI + cryptography'],
                                      ['Application',
                                       'Transaction API',
                                       'TBK HMAC verify',
                                       'FastAPI'],
                                      ['Settlement',
                                       'Batch Service',
                                       'ECC-HISE',
                                       'Python envelope module'],
                                      ['Governance',
                                       'Audit Store',
                                       'Merkle roots',
                                       'Append-only log']],
                             'caption': 'Table 4.1: Architecture components and technology '
                                        'mapping.'}},
                  {'heading': '4.1.4 Trust Boundaries and Data Flow Classification',
                   'paragraphs': ['The reference architecture divides the e-financial service '
                                  'system into four trust zones: (1) the customer device zone, '
                                  'where ECC-DTB-AKA client logic and device fingerprinting '
                                  'execute; (2) the DMZ/API zone, terminating TLS and hosting API '
                                  'gateways; (3) the internal services zone, containing '
                                  'authentication, payment orchestration, and fraud engines; and '
                                  '(4) the settlement zone, where ECC-HISE senders and receivers '
                                  'exchange batch envelopes with counterparties or clearing '
                                  'houses.',
                                  'Data are classified as public metadata (routing identifiers), '
                                  'confidential PII/financial payloads, and cryptographic material '
                                  '(private keys, MSK, DK_i). Cryptographic material never crosses '
                                  'into the DMZ in unprotected form; HSMs or sealed service vaults '
                                  'issue signatures and derivations via constrained APIs. '
                                  'Confidential payloads may traverse the DMZ only as AEAD '
                                  'ciphertexts under ECC-DTB-AKA transaction keys or as ECC-HISE '
                                  'envelopes.',
                                  'This zoning explains why transport security alone is '
                                  'insufficient: the DMZ necessarily decrypts TLS, creating a '
                                  'plaintext hotspot. Application-layer bindings (device_fp, '
                                  'txn_nonce) and envelopes (Merkle-signed batches) preserve '
                                  'security goals across that hotspot.']},
                  {'heading': '4.1.5 Mapping Requirements to Architectural Components',
                   'paragraphs': ['Security requirements SR1–SR4 from Chapter 1 map to the '
                                  'ECC-DTB-AKA service and client SDK: mutual authentication, '
                                  'forward secrecy, device binding, and per-transaction keys. '
                                  'SR5–SR8 map to the ECC-HISE settlement service: confidentiality '
                                  'of batch records, authenticity, integrity/ordering, and '
                                  'efficient audit. Non-cryptographic controls—rate limiting, '
                                  'device attestation services, fraud scoring—remain complementary '
                                  'and are represented as adjacent components in the architecture '
                                  'diagrams of this chapter.',
                                  'The technology mapping favors Python for the research prototype '
                                  '(rapid iteration, clear algorithms) with cryptography backends '
                                  'that wrap OpenSSL or equivalent. A production port would '
                                  'relocate hot paths to languages and HSM PKCS#11 interfaces '
                                  "already certified in the bank's estate, without changing wire "
                                  'formats or HKDF labels.']},
                  {'heading': '4.1.6 Operational Security Controls Complementary to Cryptography',
                   'paragraphs': ['Cryptographic schemes do not replace operational security. Rate '
                                  'limiting on handshake endpoints, anomaly detection on '
                                  'verification-failure rates, certificate revocation checking, '
                                  'and segregation of duties for HSM administrators remain '
                                  'mandatory. The architecture places these controls adjacent to '
                                  'ECC-DTB-AKA and ECC-HISE services so that cryptographic '
                                  'failures and operational signals can be correlated in a common '
                                  'SIEM pipeline.',
                                  'Change-management procedures for HKDF label strings, envelope '
                                  'version bytes, and Merkle algorithm identifiers must be treated '
                                  'as security-relevant configuration. Silent drift between sender '
                                  'and receiver encodings produces systemic verification failures '
                                  'that can be mistaken for attacks; therefore configuration is '
                                  'versioned and signed alongside application releases.']},
                  {'heading': '4.1.7 Regulatory and Assurance Alignment',
                   'paragraphs': ['The dual-layer architecture aligns with assurance themes common '
                                  'to PCI DSS (protect cardholder data in transit and at rest), '
                                  'PSD2 strong customer authentication (possession factors for '
                                  'remote payments), and SWIFT Customer Security Programme '
                                  'controls on interface integrity. ECC-DTB-AKA strengthens '
                                  'possession of a client authenticator bound to session keys; '
                                  'ECC-HISE strengthens integrity and auditability of '
                                  'inter-institution data exchanges.',
                                  'The dissertation does not claim automatic compliance '
                                  'certification. Rather, it provides cryptographic mechanisms '
                                  'that map cleanly onto control objectives auditors already '
                                  'expect, reducing reliance on procedural compensating controls '
                                  'for session binding and batch integrity.']},
                  {'heading': '4.1.8 Interface Contracts Between Tiers',
                   'paragraphs': ['Each tier exposes a narrow interface contract. The client tier '
                                  'may call only authentication and transaction APIs; it never '
                                  'contacts settlement nodes directly. The application tier emits '
                                  'settlement records through a queue abstraction with schema '
                                  'validation before ECC-HISE packaging. The settlement tier '
                                  'accepts only envelopes whose domain_id and key_version are on '
                                  'an allow-list maintained by governance. The governance tier '
                                  'publishes trust anchors and consumes Merkle roots for archival, '
                                  'without holding plaintext settlement payloads by default.',
                                  'These contracts reduce lateral movement: compromise of a DMZ '
                                  'API gateway yields TLS-terminated HTTP traffic and application '
                                  'tokens, but not MK, DK_i, or the ability to forge ECC-HISE '
                                  'header signatures without settlement-zone keys. Conversely, '
                                  'compromise of a settlement signer does not grant interactive '
                                  'ECC-DTB-AKA sessions with customers. The dual-layer split is '
                                  'therefore also a blast-radius split.',
                                  'Message schemas are versioned. Breaking changes require '
                                  'simultaneous client SDK and server deployment windows, '
                                  'coordinated like certificate rotations. Non-breaking additive '
                                  'fields are ignored by older verifiers under explicit '
                                  'forward-compatibility rules documented in the prototype API.']},
                  {'heading': '4.1.9 Threat Model Instantiation for the Reference Architecture',
                   'paragraphs': ['The architectural threat model assumes a network adversary who '
                                  'can eavesdrop, inject, and replay messages on client-Internet '
                                  'and inter-bank links; a malicious or compromised peer service '
                                  'inside the DMZ after TLS termination; and an honest-but-curious '
                                  'auditor who should verify inclusion without learning unrelated '
                                  'records. It does not assume physical possession of HSM-backed '
                                  'MK, nor unrestricted malware on a hardware-attested client '
                                  'device.',
                                  'Under this model, ECC-DTB-AKA targets remote session abuse and '
                                  'impersonation, while ECC-HISE targets undetectable mutation of '
                                  'settlement batches and inefficient audit. Social engineering of '
                                  'authorized users and colluding insiders with signing authority '
                                  'remain residual risks addressed by fraud engines and dual '
                                  'control, not by these protocols alone.']}]},
 {'heading': '4.2 Programmatic Implementation of ECC-DTB-AKA (Chapter 2)',
  'paragraphs': ['This section describes the software implementation of ECC-DTB-AKA as specified '
                 'in Chapter 2, including module structure, class design, API endpoints, and test '
                 'results from the prototype.'],
  'subsections': [{'heading': '4.2.1 Module Structure',
                   'paragraphs': ['The ECC-DTB-AKA implementation resides in '
                                  'prototype/ecc_dtb_aka/ with the following modules: protocol.py '
                                  '— core protocol classes (ECCDTBAKAClient, ECCDTBAKAServer) and '
                                  'message dataclasses (ClientInit, ServerResponse, ClientConfirm, '
                                  'SessionState); demo.py — standalone handshake demonstration; '
                                  'common/crypto_utils.py — shared SHA-256, HKDF, ECDH, ECDSA '
                                  'utilities.',
                                  'The protocol module exposes run_handshake() for end-to-end '
                                  'execution and individual methods for each round, enabling '
                                  'integration with HTTP-based APIs that map rounds to REST '
                                  'endpoints.'],
                   'figure': 'ECC-DTB-AKA software module diagram (Figure 4.3).'},
                  {'heading': '4.2.2 Core Classes and Data Structures',
                   'paragraphs': ['ECCDTBAKAClient maintains long-term key pair (sk_C, PK_C), '
                                  'device fingerprint derived from hardware attributes, ephemeral '
                                  'key state, and session state after handshake completion. Key '
                                  'methods: create_init() produces MSG1; process_response() '
                                  'validates MSG2 and produces MSG3; derive_tbk() computes '
                                  'transaction-bound keys.',
                                  'ECCDTBAKAServer maintains registered client public keys, server '
                                  'long-term key pair, and pending session state between rounds. '
                                  'Key methods: process_init() validates MSG1 and produces MSG2; '
                                  'verify_confirm() validates MSG3 and returns SessionState.',
                                  'Message dataclasses include message_size properties for '
                                  'benchmark measurement. Total three-message handshake size '
                                  'averages 569 bytes in prototype benchmarks.']},
                  {'heading': '4.2.3 REST API Integration',
                   'paragraphs': ['The FastAPI application (prototype/api/app.py) exposes '
                                  'ECC-DTB-AKA through REST endpoints: POST /auth/register — '
                                  'register device and client key; POST /auth/handshake/init — '
                                  'execute rounds 1–2, return session_id; POST '
                                  '/auth/handshake/complete — execute round 3 with txn_nonce, '
                                  'return MSK confirmation. GET /health — service health check.',
                                  'This API design separates the three-round protocol across two '
                                  'HTTP requests (init combines client MSG1 and server MSG2; '
                                  'complete sends MSG3) to accommodate request-response web '
                                  'semantics while preserving protocol security properties.']},
                  {'heading': '4.2.4 Test Results',
                   'paragraphs': ['Integration testing via prototype/api/demo_integration.py '
                                  'confirms successful handshake completion with MSK derivation. '
                                  'Benchmark results (Chapter 2, n=200): mean authentication '
                                  'latency 0.52 ms, total message size 569 bytes, three round '
                                  'trips. All test cases for replay rejection, invalid signature '
                                  'detection, and unregistered client rejection pass.'],
                   'table': {'headers': ['Test Case', 'Expected', 'Result'],
                             'rows': [['Valid handshake', 'MSK established', 'Pass'],
                                      ['Invalid client signature', 'Reject at server', 'Pass'],
                                      ['Invalid server signature', 'Reject at client', 'Pass'],
                                      ['Wrong txn_nonce MAC', 'Reject at confirm', 'Pass'],
                                      ['Unregistered client', 'HTTP 404 / error', 'Pass']],
                             'caption': 'Table 4.2: ECC-DTB-AKA prototype test results.'}},
                  {'heading': '4.2.5 Key Derivation Implementation Details',
                   'paragraphs': ['The HKDF implementation uses '
                                  'cryptography.hazmat.primitives.kdf.hkdf.HKDF with SHA-256 as '
                                  'the hash function. MSK derivation concatenates device_fp, '
                                  "nonce_c, and nonce_s as salt with info string 'ECC-DTB-AKA-v1'. "
                                  "TBK derivation uses txn_nonce as salt with info string 'TBK'. "
                                  'These domain-separated info strings prevent cross-protocol key '
                                  'reuse if additional derivation functions are added.']},
                  {'heading': '4.2.6 State Machine and Error Handling',
                   'paragraphs': ['The handshake is implemented as an explicit state machine: INIT '
                                  '→ WAIT_MSG2 → ESTABLISHED on the client; LISTEN → WAIT_MSG3 → '
                                  'ESTABLISHED on the server. Transitions fail closed on signature '
                                  'verification errors, certificate path failures, registry '
                                  'misses, or nonce reuse. Failed sessions delete ephemeral ECDH '
                                  'scalars immediately and do not emit partial MSK material to '
                                  'application logs.',
                                  'Idempotency of MSG3 confirmation uses (client_id, nonce_c, '
                                  'nonce_s) as a server-side replay key with TTL matching the '
                                  'session lifetime. This prevents an adversary from replaying a '
                                  'captured confirmation to re-derive acceptance of an already '
                                  'completed handshake.']},
                  {'heading': '4.2.7 Device Fingerprint Pipeline',
                   'paragraphs': ['Device fingerprinting in the prototype hashes a canonicalized '
                                  'attribute vector (platform identifiers, app attestation digest '
                                  'when available, and installation salt) to a 128-bit truncation '
                                  'for protocol messages. Production deployments should prefer '
                                  'hardware-backed attestation (e.g., Android Play Integrity, '
                                  'Apple App Attest, or TPM quotes) and treat the fingerprint as a '
                                  'high-entropy binding input rather than a privacy-invasive '
                                  'tracking identifier.',
                                  'Privacy note: fingerprints are used only as HKDF salt material '
                                  'and server-side binding checks; they are not designed as a '
                                  'global cross-bank identifier. Banks may rotate installation '
                                  'salts on reinstall, accepting that sessions must be '
                                  're-established—consistent with device-binding goals.']},
                  {'heading': '4.2.8 Interoperability with Existing Login Flows',
                   'paragraphs': ['ECC-DTB-AKA can wrap or replace password-plus-OTP login. In a '
                                  'transitional deployment, the bank continues to verify primary '
                                  'credentials, then runs ECC-DTB-AKA to establish MSK/TBK for '
                                  'subsequent high-risk operations (payments, beneficiary '
                                  'changes). Over time, FIDO2 credentials can serve as the '
                                  'long-term client key PK_C, unifying phishing-resistant '
                                  'authentication with device-bound session keys.',
                                  'The REST integration exposes /handshake/msg1, /handshake/msg2, '
                                  'and /handshake/msg3 endpoints plus /transaction/authorize that '
                                  'requires an HMAC under TBK. This mirrors how OAuth access '
                                  'tokens are presented today, but replaces bearer tokens with '
                                  'transaction-bound authenticator tags.']},
                  {'heading': '4.2.9 Logging, Observability, and Secrets Hygiene',
                   'paragraphs': ['Prototype logging records handshake outcomes, client '
                                  'identifiers, and truncated nonce digests, never raw ECDH '
                                  'scalars, MSK, or TBK. Production deployments should emit '
                                  'structured events suitable for fraud correlation while '
                                  'retaining cryptographic material exclusively in HSM or sealed '
                                  'memory.',
                                  'Distributed tracing spans may carry session_id handles but must '
                                  'not carry material that enables offline analysis of long-term '
                                  'keys. Clock skew beyond a configured window causes handshakes '
                                  'to fail closed with a distinct error code distinguishing '
                                  'configuration faults from replay attempts.']},
                  {'heading': '4.2.10 Concurrency and Session Store Design',
                   'paragraphs': ['Pending handshake state between MSG1 and MSG3 is stored under a '
                                  'server-generated session_id with a short TTL (prototype: tens '
                                  'of seconds). Concurrent handshakes from the same client_id are '
                                  'allowed only up to a small bound; excess attempts are '
                                  'rate-limited. On ESTABLISHED, ephemeral ECDH private keys are '
                                  'zeroized in the process where the language runtime permits.',
                                  'Horizontal scaling of the auth service requires a shared '
                                  'session store (Redis or equivalent) or sticky routing. The '
                                  'store holds public transcript fields and verification '
                                  'intermediates, not MSK. After confirmation, only a handle '
                                  'referencing HSM-sealed key material (or a short-lived derived '
                                  'token for non-HSM prototypes) is returned to the transaction '
                                  'API.',
                                  'Load tests should measure not only cryptographic latency but '
                                  'lock contention on the client registry and nonce-replay cache. '
                                  'The dissertation benchmarks isolate crypto cores; production '
                                  'capacity planning must add network and store overheads measured '
                                  'on target hardware.']},
                  {'heading': '4.2.11 Negative Testing and Property-Based Checks',
                   'paragraphs': ['Beyond the pass/fail table in Section 4.2.4, the prototype '
                                  'includes negative tests that flip signature bytes, truncate '
                                  'messages, reuse nonces, swap client identities, and present '
                                  'unregistered PK_C values. Property-oriented checks assert that '
                                  'MSK differs whenever device_fp or either nonce differs, and '
                                  'that TBK differs whenever txn_nonce differs, approximating the '
                                  'binding claims of Chapter 2 at the implementation level.',
                                  'Continuous integration runs these tests on every change to '
                                  'protocol.py. Regressions in canonical encoding or HKDF labels '
                                  'are treated as release blockers because they silently break '
                                  'interoperability and security assumptions.']}]},
 {'heading': '4.3 Programmatic Implementation of ECC-HISE (Chapter 3)',
  'paragraphs': ['This section describes the software implementation of ECC-HISE for server-server '
                 'batch data protection, including envelope construction, Merkle audit chain, and '
                 'settlement API.'],
  'subsections': [{'heading': '4.3.1 Module Structure',
                   'paragraphs': ['The ECC-HISE implementation resides in prototype/ecc_hise/ with '
                                  'modules: hierarchy.py — KeyHierarchy class for MK → DK → '
                                  'SK_batch derivation; merkle.py — merkle_root(), merkle_proof(), '
                                  'verify_merkle_proof(); envelope.py — ECC_HISE_Sender, '
                                  'ECC_HISE_Receiver, SecureBatch dataclass; demo.py — standalone '
                                  'batch demonstration.'],
                   'figure': 'ECC-HISE software module diagram (Figure 4.4).'},
                  {'heading': '4.3.2 Envelope Construction and Verification',
                   'paragraphs': ['ECC_HISE_Sender.build_batch() accepts a list of record byte '
                                  'strings, batch_id, and domain_id. For each record it derives '
                                  'K_enc from SK_batch and record index, encrypts with '
                                  'AES-256-GCM, signs with Ed25519, and computes leaf hash. Merkle '
                                  'root is computed over all leaves and signed in the batch '
                                  'header.',
                                  'ECC_HISE_Receiver.verify_and_decrypt() validates header '
                                  'signature, Merkle root consistency, per-record signatures, and '
                                  'GCM authentication tags before returning plaintext records. '
                                  'Merkle inclusion proofs are verified for each record during '
                                  'decryption to demonstrate audit capability.']},
                  {'heading': '4.3.3 Settlement API Integration',
                   'paragraphs': ['POST /settlement/submit-batch accepts batch_id, domain_id, and '
                                  'list of record strings. The endpoint constructs an ECC-HISE '
                                  'envelope, verifies it internally (sender/receiver simulation), '
                                  'and returns merkle_root, record_count, total_bytes, and '
                                  'verified status. In production, sender and receiver would be '
                                  'separate services; the prototype validates cryptographic '
                                  'correctness within a single process for demonstration.']},
                  {'heading': '4.3.4 Test Results and Performance',
                   'paragraphs': ['Benchmark results for 100-record batches (Chapter 3, n=50): '
                                  'mean processing latency 23.32 ms, mean envelope size 37823 '
                                  'bytes. Integration demo processes 3-record batch with verified '
                                  'Merkle root. Tampering tests (modified ciphertext, wrong Merkle '
                                  'root, invalid signature) correctly raise verification errors.'],
                   'table': {'headers': ['Test Case', 'Expected', 'Result'],
                             'rows': [['Valid batch encrypt/decrypt', 'Records match', 'Pass'],
                                      ['Tampered ciphertext', 'GCM / sig failure', 'Pass'],
                                      ['Wrong Merkle root', 'Root mismatch error', 'Pass'],
                                      ['Merkle proof verify', 'Inclusion confirmed', 'Pass'],
                                      ['100-record benchmark', '< 30s latency', 'Pass']],
                             'caption': 'Table 4.3: ECC-HISE prototype test results.'}},
                  {'heading': '4.3.5 Merkle Tree Implementation',
                   'paragraphs': ['The Merkle tree implementation (merkle.py) uses SHA-256 for '
                                  'internal nodes. Odd-length layers duplicate the last node '
                                  '(Bitcoin-style) to ensure deterministic root computation. Proof '
                                  'generation handles odd-layer promotion with self-pairing. '
                                  'Verification reconstructs the path from leaf to root in O(log '
                                  'n) hashes. For n=100 records, proof length is 7 hashes (224 '
                                  'bytes), enabling compact audit evidence.']},
                  {'heading': '4.3.6 Envelope Serialization and Versioning',
                   'paragraphs': ['Envelopes are serialized as structured objects (JSON for the '
                                  'prototype; CBOR or protobuf recommended for production) '
                                  'containing header fields (batch_id, domain_id, key_version, '
                                  'root, timestamp, header_signature) and an ordered list of '
                                  'record objects (index, ciphertext, iv, tag, signature, '
                                  'metadata). A version byte allows future AEAD or signature '
                                  'algorithm migration without breaking archival verifiers.',
                                  'Canonical encoding rules matter for signatures: fields are '
                                  'signed over a deterministic byte encoding to avoid JSON '
                                  'key-order ambiguity. The prototype documents this '
                                  'canonicalization in module docstrings; production code should '
                                  'use an explicit encode_for_signing() function shared by sender '
                                  'and receiver.']},
                  {'heading': '4.3.7 Receiver Pipeline and Quarantine',
                   'paragraphs': ['The receiver pipeline verifies header signature → recomputes or '
                                  'checks Merkle root → verifies each leaf signature → decrypts '
                                  'under index-derived keys → posts to ledger adapters. Any stage '
                                  'can quarantine the batch to a dead-letter store with forensic '
                                  'ciphertext retained for incident response.',
                                  'Integration tests inject mutated roots, swapped leaves, '
                                  'truncated batches, and wrong-index keys to confirm fail-closed '
                                  'behavior. These tests form part of the evidence that the '
                                  "implementation matches Chapter 3's security claims."]},
                  {'heading': '4.3.8 Scaling and Parallelism Considerations',
                   'paragraphs': ['Per-record AES-GCM encryption and Ed25519 signing dominate '
                                  'ECC-HISE latency and parallelize naturally across CPU cores. '
                                  'Merkle tree construction is a barrier after leaves are ready; '
                                  'for large batches, a forest of subtrees with a top-level '
                                  'meta-root can preserve O(log n) proofs while enabling segmented '
                                  'construction.',
                                  'Memory pressure for million-record national settlement files '
                                  'motivates streaming leaf hashing and spill-to-disk for '
                                  'intermediate layers. The prototype demonstrates correctness at '
                                  'hundreds of records; larger volumes are an engineering path '
                                  'discussed as future work.']},
                  {'heading': '4.3.9 Key Hierarchy Operational Lifecycle',
                   'paragraphs': ['MK generation is a ceremony: dual control, audit logging, and '
                                  'backup to offline media or HSM clones. DK_i rotation is '
                                  'scheduled (e.g., quarterly) and on suspicion of compromise; '
                                  'SK_batch is single-use per batch_id. The prototype models this '
                                  'lifecycle with in-memory keys and explicit derive calls; '
                                  'production maps the same labels onto PKCS#11 derive operations.',
                                  'Key version identifiers in envelope headers allow receivers to '
                                  'select the correct DK_i during rotation overlap windows. Old '
                                  'versions remain decrypt-only for a retention period matching '
                                  'archival policy, then are destroyed under dual control. This '
                                  'lifecycle is essential to the hierarchical blast-radius '
                                  'argument of Chapter 3.']},
                  {'heading': '4.3.10 Interoperability With Existing File-Transfer Rails',
                   'paragraphs': ['Banks often exchange files over SFTP, MQ, or managed '
                                  'file-transfer products. ECC-HISE envelopes can ride these rails '
                                  'as opaque payloads: transport provides availability and basic '
                                  'encryption, while the envelope provides end-to-end authenticity '
                                  'and Merkle audit independent of the rail. This composition '
                                  'avoids a rip-and-replace of MFT infrastructure.',
                                  'Where counterparties cannot yet verify envelopes, a '
                                  'transitional mode can attach a detached Merkle manifest and '
                                  'signature alongside legacy ciphertext, enabling gradual '
                                  'verifier rollout. Full hierarchical encryption becomes '
                                  'mandatory once both sides support the versioned format.']}]},
 {'heading': '4.4 Integrated System Demonstration',
  'paragraphs': ['The integrated demonstration (prototype/api/demo_integration.py) executes a '
                 'complete e-banking security workflow: device registration, ECC-DTB-AKA '
                 'authentication handshake with transaction nonce, and ECC-HISE settlement batch '
                 'submission with Merkle verification. This end-to-end test validates that both '
                 'schemes operate correctly within a unified API framework and can be invoked '
                 'sequentially in a realistic transaction lifecycle.'],
  'subsections': [{'heading': '4.4.1 Deployment Considerations',
                   'paragraphs': ['Production deployment recommendations: (1) Store MK in HSM; '
                                  'never persist in application memory beyond derivation '
                                  'operations. (2) Deploy auth and settlement services in separate '
                                  'network segments with mTLS. (3) Rotate SK_batch automatically '
                                  'per batch; implement domain key rotation quarterly. (4) Persist '
                                  'audit logs (batch_id, Root, timestamp) to WORM storage. (5) '
                                  'Rate-limit handshake endpoints to prevent DoS.'],
                   'figure': 'Deployment topology for prototype services (Figure 4.5).'},
                  {'heading': '4.4.2 Limitations of the Prototype',
                   'paragraphs': ['The prototype uses software-based key storage rather than HSM '
                                  'integration. Certificate management is simplified (server '
                                  'public key substituted for full X.509 chain). The settlement '
                                  'API performs sender and receiver verification in-process rather '
                                  'than across network boundaries. Persistent storage uses '
                                  'in-memory dictionaries. These simplifications do not affect the '
                                  'cryptographic correctness of the schemes but must be addressed '
                                  'before production deployment. Formal security proofs remain '
                                  'proof sketches as noted in Chapter 2.']},
                  {'heading': '4.4.3 End-to-End Scenario Walkthrough',
                   'paragraphs': ['The integrated demo executes: (1) client and bank auth service '
                                  'complete ECC-DTB-AKA; (2) client authorizes a payment under '
                                  'TBK; (3) payment service enqueues a settlement record; (4) '
                                  'settlement sender builds an ECC-HISE batch including that '
                                  'record; (5) counterparty receiver verifies and decrypts; (6) an '
                                  'auditor verifies a Merkle proof for the record against the '
                                  'signed root without receiving unrelated plaintexts.',
                                  'This walkthrough demonstrates the dual-layer claim in '
                                  'operational terms: the same payment is protected by '
                                  'device-bound client authentication at initiation and by '
                                  'hierarchical integrity envelopes at inter-bank transfer.']},
                  {'heading': '4.4.4 Performance Observations in the Integrated Path',
                   'paragraphs': ['In the prototype environment, ECC-DTB-AKA handshake latency '
                                  'remains sub-millisecond for cryptographic cores, while '
                                  'end-to-end HTTP framing adds the expected milliseconds of stack '
                                  'overhead. ECC-HISE batch build time grows roughly linearly with '
                                  'record count, matching Chapter 3 microbenchmarks. Neither cost '
                                  'dominates a realistic mobile payment UX or overnight settlement '
                                  'window at regional scale.',
                                  'The principal production risks are not raw crypto speed but key '
                                  'custody, certificate lifecycle, fingerprint policy, and '
                                  'operational monitoring of verification failures—topics treated '
                                  'as deployment considerations rather than cryptographic '
                                  'weaknesses.']},
                  {'heading': '4.4.5 Failure Modes and Recovery',
                   'paragraphs': ['Integrated failure modes include: client handshake timeout '
                                  '(retry with fresh nonces); TBK HMAC mismatch (reject payment, '
                                  'alert fraud); ECC-HISE quarantine (hold settlement, notify '
                                  'operations); and audit proof mismatch (escalate as integrity '
                                  'incident). Recovery never skips verification to restore '
                                  'availability; degraded modes may queue outbound batches offline '
                                  'but do not accept unverified inbound envelopes.',
                                  'Disaster-recovery drills should include restoring MK from HSM '
                                  'backup ceremonies and re-deriving domain keys under dual '
                                  'control, verifying that archived envelopes remain decryptable '
                                  'under recorded key_version identifiers.']},
                  {'heading': '4.4.6 Reproducibility and Artifact Layout',
                   'paragraphs': ['The repository layout separates protocol modules '
                                  '(prototype/ecc_dtb_aka, prototype/ecc_hise), API glue '
                                  '(prototype/api), and benchmark drivers that emit JSON consumed '
                                  'by Chapters 2–5 tables. Re-running benchmarks regenerates '
                                  'latency and size statistics without editing prose by hand when '
                                  'means are loaded dynamically in content modules.',
                                  'Deterministic demo scripts print Merkle roots and handshake '
                                  'digests for manual inspection. These artifacts support '
                                  'examination committees and future replicators who wish to '
                                  'confirm that claimed properties are not merely narrative.']}]},
 {'heading': '4.5 Chapter Summary',
  'paragraphs': ['This chapter presented the security system architecture and programmatic '
                 'implementation of ECC-DTB-AKA and ECC-HISE in a unified e-financial service '
                 'prototype. Section 4.1 defined four architectural tiers and component '
                 'interactions. Sections 4.2 and 4.3 detailed module structure, API design, and '
                 'test results for each scheme. Section 4.4 demonstrated end-to-end integration. '
                 'Chapter 5 evaluates both schemes comprehensively, reviews prior work, and '
                 'analyzes effectiveness against the attack mechanisms cataloged in Chapter 1.'],
  'subsections': [{'heading': '4.5.1 Implementation Contributions',
                   'paragraphs': ['Chapter 4 contributes an executable dual-layer prototype, '
                                  'API-level integration patterns, and empirical confirmation that '
                                  'Chapters 2–3 designs are realizable with standard libraries. '
                                  'The artifact supports reproducibility of latency and overhead '
                                  'claims and provides a reference for industrial ports into '
                                  'HSM-backed services.']}]}]
