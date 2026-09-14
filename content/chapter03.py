"""Chapter 3: ECC-HISE — Hierarchical Integrity-preserving Secure Envelope."""

import json
from pathlib import Path

_BENCH = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks" / "chapter3_benchmarks.json"
if _BENCH.exists():
    _ALL = json.loads(_BENCH.read_text())
    def _get(scheme: str, n: int) -> dict:
        return next(d for d in _ALL if d["scheme"] == scheme and d["records"] == n)
    HISE_100 = _get("ECC-HISE", 100)
    STATIC_100 = _get("Static AES-GCM PSK", 100)
    TLS_100 = _get("TLS record layer only", 100)
    HISE_500 = _get("ECC-HISE", 500)
else:
    HISE_100 = {"latency_ms_mean": 23.32, "batch_bytes_mean": 37823}
    STATIC_100 = {"latency_ms_mean": 0.22, "batch_bytes_mean": 28400}
    TLS_100 = {"latency_ms_mean": 0.24, "batch_bytes_mean": 28905}
    HISE_500 = {"latency_ms_mean": 245.53, "batch_bytes_mean": 189023}

CHAPTER_TITLE = "Chapter 3"
CHAPTER_SUBTITLE = (
    "ECC-HISE: Hierarchical Integrity-preserving Secure Envelope "
    "for Server-Server E-Finance Data Transfer"
)

SECTIONS = [{'heading': '3.1 Introduction and Motivation',
  'paragraphs': ['Chapter 2 addressed authentication and key-exchange limitations in client-server '
                 'e-banking channels through ECC-DTB-AKA. This chapter takes a fundamentally '
                 'different approach, targeting the data-security limitations identified in '
                 'Section 1.3.3 for server-server communication in electronic banking and '
                 'electronic finance systems.',
                 'Inter-bank and intra-bank settlement operations transfer large batches of '
                 'financial records between server nodes: end-of-day reconciliation files, '
                 'regulatory reporting payloads, payment clearing batches, and cross-border '
                 'remittance instructions. These transfers require confidentiality (unauthorized '
                 'parties must not read records), integrity (any modification must be detectable), '
                 'non-repudiation (senders cannot deny transmission), and auditability (regulators '
                 'must verify completeness and ordering without reprocessing entire batches).',
                 'Current practice relies on TLS for transport encryption, static pre-shared keys '
                 'for file encryption, or per-message digital signatures without efficient batch '
                 'verification. Each approach exhibits limitations cataloged in Section 1.3.3: '
                 'flat key hierarchies, disconnected encryption and audit subsystems, inefficient '
                 'batch integrity verification, static PSKs in server-server channels, lack of '
                 'end-to-end integrity across service boundaries, and regulatory audit friction.',
                 'ECC-HISE (Elliptic Curve Cryptography — Hierarchical Integrity-preserving Secure '
                 'Envelope) proposes a unified methodology combining hierarchical ECC key '
                 'derivation, AES-256-GCM authenticated encryption, Ed25519 per-record signatures, '
                 'and Merkle-tree audit chains. The scheme is designed for server-server channels '
                 'and complements ECC-DTB-AKA, which secures client-server authentication.'],
  'subsections': [{'heading': '3.1.1 Server-Server Threats Beyond Transport Security',
                   'paragraphs': ['Client-server channels in e-banking have received '
                                  'disproportionate attention in both academic literature and '
                                  'commercial security products. Server-server channels—settlement '
                                  'feeds, clearing-house submissions, card authorization backends, '
                                  'and intra-bank microservice mesh traffic—often rely on mutually '
                                  'authenticated TLS (mTLS) or static file encryption with '
                                  'long-lived pre-shared keys. While mTLS authenticates endpoints '
                                  'and encrypts bytes on the wire, it does not provide persistent '
                                  'integrity once data leaves the TLS session: decrypted payloads '
                                  'may be stored, forwarded, or transformed without cryptographic '
                                  'evidence of origin, completeness, or ordering.',
                                  'Consider an end-of-day settlement batch of n payment records '
                                  'transmitted from Bank A to Bank B. Under mTLS alone, Bank B '
                                  'learns that some TLS peer holding a valid certificate sent a '
                                  'stream of bytes. Bank B cannot, without additional application '
                                  'cryptography, prove to a regulator six months later that record '
                                  'j was present, unmodified, and correctly ordered relative to '
                                  'the batch as a whole. Static PSK file encryption improves '
                                  'confidentiality at rest but typically uses a single key for '
                                  'many batches, creating catastrophic blast radius on key '
                                  'compromise and offering no structured audit proof.',
                                  'ECC-HISE addresses this gap by treating each settlement batch '
                                  'as a cryptographic object: hierarchical keys limit exposure; '
                                  'per-record authenticated encryption and signatures provide '
                                  'origin authenticity; a Merkle tree binds records into a '
                                  'tamper-evident set; and a signed batch header carries the '
                                  'Merkle root as a compact, independently verifiable audit '
                                  'commitment.']},
                  {'heading': '3.1.2 Relationship to Chapter 2 and Dual-Layer Methodology',
                   'paragraphs': ['The dual-layer methodology of this dissertation pairs '
                                  'ECC-DTB-AKA (Chapter 2) for client-server authentication with '
                                  'ECC-HISE for server-server data protection. The layers are '
                                  'complementary rather than redundant. ECC-DTB-AKA binds a '
                                  'human-facing session to a device and transaction; ECC-HISE '
                                  'binds an institutional batch to a domain key hierarchy and an '
                                  'integrity tree. Both use ECC primitives (ECDH/ECDSA or '
                                  'Ed25519), HKDF domain separation, and explicit adversarial '
                                  'models, enabling unified security reasoning across the '
                                  'e-finance stack.',
                                  'Importantly, ECC-HISE does not replace mTLS. Transport security '
                                  'remains necessary to protect metadata, thwart passive '
                                  'eavesdropping on network paths, and satisfy baseline compliance '
                                  'controls. ECC-HISE adds an application-layer envelope that '
                                  'survives TLS termination at API gateways, message queues, and '
                                  'archival systems—precisely where Chapter 1 identified integrity '
                                  'gaps.']}]},
 {'heading': '3.2 Design Goals and Requirements',
  'paragraphs': ['ECC-HISE addresses security requirements SR5–SR7 from Section 1.4.5:',
                 'G1 (Hierarchical Key Management): Keys must be scoped to business domains and '
                 'individual batches, limiting compromise blast radius.',
                 'G2 (Confidentiality): Records must be encrypted with semantic security under '
                 'chosen-ciphertext attack.',
                 'G3 (Integrity and Non-repudiation): Per-record and batch-level integrity proofs '
                 'must detect tampering.',
                 'G4 (Efficient Batch Audit): Verification of individual record inclusion must '
                 'require O(log n) operations.',
                 'G5 (Domain Separation): Retail, corporate, and settlement domains must use '
                 'cryptographically isolated keys.',
                 'G6 (ECC Alignment): Key hierarchy and envelope encryption must use elliptic '
                 'curve primitives consistent with Chapter 2 and industry standards.'],
  'subsections': [{'heading': '3.2.1 Formalization of Integrity and Non-Repudiation Goals',
                   'paragraphs': ['Beyond the high-level goals stated above, ECC-HISE targets the '
                                  'following precise properties for a batch B = (r_1, ..., r_n) '
                                  'produced by sender S for receiver R under domain D:',
                                  'I1 (Record confidentiality): Without SK_batch (or ancestor keys '
                                  'that derive it), an adversary learns negligible information '
                                  'about plaintext r_j from ciphertext_j.',
                                  'I2 (Record authenticity): R accepts record j only if an Ed25519 '
                                  "signature under S's signing key verifies over the ciphertext "
                                  'and batch context.',
                                  'I3 (Batch binding): Any modification, deletion, insertion, or '
                                  'reordering of records changes the Merkle root with overwhelming '
                                  'probability, causing header verification to fail when the '
                                  'signed root is checked.',
                                  'I4 (Selective audit): A third party holding the signed header '
                                  'and a Merkle proof for index j can verify inclusion of '
                                  'ciphertext_j without receiving the entire batch.',
                                  'I5 (Key isolation): Compromise of SK_batch for one batch does '
                                  "not yield SK_batch' for another batch under the same domain, "
                                  'assuming HKDF behaves as a PRF.',
                                  'These properties map directly to SR5–SR8 from Chapter 1 and to '
                                  'SWIFT CSP-style controls requiring integrity and '
                                  'non-repudiation for high-value payment flows.']}]},
 {'heading': '3.3 Hierarchical Key Management',
  'paragraphs': ['The ECC-HISE key hierarchy comprises three levels, derived using HKDF-SHA256 '
                 'with domain-separated info strings.'],
  'subsections': [{'heading': '3.3.1 Master, Domain, and Session Keys',
                   'paragraphs': ['Level 0 — Master Key (MK): A 256-bit key generated within an '
                                  'HSM at the clearing-house authority. MK is the root of trust '
                                  'for all derived keys and is never transmitted.',
                                  'Level 1 — Domain Key (DK_i): For each business domain i '
                                  '(retail, corporate, settlement), DK_i = HKDF(MK, salt = H(MK || '
                                  "domain_id), info = 'ECC-HISE-DK', 256). Domain keys isolate "
                                  'cryptographic material between business units.',
                                  'Level 2 — Session Key (SK_batch): For each batch transfer '
                                  'identified by batch_id and epoch timestamp, SK_batch = '
                                  "HKDF(DK_i, salt = batch_id || epoch, info = 'ECC-HISE-SK', "
                                  '256). Session keys rotate per batch, ensuring that compromise '
                                  'of one batch key does not affect other batches.'],
                   'figure': 'ECC-HISE three-level key hierarchy: Master Key, Domain Keys, Session '
                             'Keys (Figure 3.1).'},
                  {'heading': '3.3.2 Key Rotation and Revocation',
                   'paragraphs': ['Domain keys rotate on a scheduled basis (quarterly recommended) '
                                  'by updating domain_id version suffix (e.g., settlement-v2). '
                                  'Session keys rotate automatically per batch. Revocation of a '
                                  'compromised domain key requires re-derivation from MK with a '
                                  'new domain_id; unaffected domains remain secure. The '
                                  'hierarchical structure ensures revocation scope is limited to '
                                  'the compromised domain rather than the entire institution.']},
                  {'heading': '3.3.3 Comparison with Flat Key Management',
                   'paragraphs': ['Traditional e-banking data encryption deploys a small number of '
                                  'long-lived data-encryption keys (DEKs) wrapped by infrequently '
                                  'rotated key-encryption keys (KEKs). If a DEK is compromised, '
                                  'all data encrypted under that key is exposed—potentially years '
                                  "of settlement records. ECC-HISE's hierarchical derivation "
                                  'limits exposure to a single batch within a single domain. The '
                                  'quantitative overhead of hierarchical derivation (two HKDF '
                                  'operations per batch) is negligible compared to per-record '
                                  'encryption and signing.']},
                  {'heading': '3.3.4 Threat Analysis of Key Hierarchy Compromise',
                   'paragraphs': ['Hierarchical keying concentrates risk at higher levels by '
                                  'design: compromise of the master key MK is catastrophic for all '
                                  'domains, while compromise of DK_i affects only domain i. '
                                  'Operational practice must therefore protect MK in an HSM or '
                                  'equivalent hardware boundary, issue DK_i under dual control, '
                                  'and rotate domain keys on a defined schedule or after suspected '
                                  'incident.',
                                  'An adversary who obtains SK_batch can decrypt and forge within '
                                  'that batch only if they also possess the sender signing key—or '
                                  'if verification is incorrectly implemented to skip signature '
                                  'checks. ECC-HISE deliberately separates confidentiality keys '
                                  '(HKDF-derived) from authenticity keys (Ed25519), so that a '
                                  'confidentiality breach does not automatically yield forgery '
                                  'capability.',
                                  'Revocation proceeds by discontinuing derivation under a '
                                  'compromised DK_i and re-wrapping subsequent batches under a new '
                                  'domain key. Historical batches remain verifiable using archived '
                                  'headers and the public verification key, even after domain-key '
                                  'rotation, provided signature keys are managed with a documented '
                                  'certificate or key-lifecycle policy.']},
                  {'heading': '3.3.5 Domain Separation and Cross-Protocol Safety',
                   'paragraphs': ["HKDF info labels in ECC-HISE ('ECC-HISE-DK', 'ECC-HISE-SK', "
                                  "'ECC-HISE-AES') implement cryptographic domain separation: keys "
                                  'derived for one purpose cannot be substituted for another even '
                                  'if salts collide. This practice follows recommendations in the '
                                  'HKDF analysis literature and prevents accidental key reuse '
                                  'between ECC-DTB-AKA transaction keys and ECC-HISE batch keys '
                                  'when both schemes coexist in one institution.',
                                  'Salts incorporate domain identifiers and batch identifiers so '
                                  'that identical plaintexts in different domains produce '
                                  'independent keys and ciphertexts. This property supports '
                                  'multi-tenant clearing platforms where logical isolation must be '
                                  'enforced cryptographically, not merely by access-control '
                                  'lists.']}]},
 {'heading': '3.4 Secure Envelope Construction',
  'paragraphs': ['Each batch B = {r_1, ..., r_n} of financial records is packaged into a secure '
                 'envelope comprising a signed batch header and a collection of encrypted, signed '
                 'record envelopes.'],
  'subsections': [{'heading': '3.4.1 Record Envelope Algorithm',
                   'paragraphs': ['For each record r_j at index j in batch B with batch_id and '
                                  'session key SK_batch: (1) Derive K_enc_j = HKDF(SK_batch, salt '
                                  "= str(j), info = 'ECC-HISE-AES', 256). (2) Sample IV_j ← "
                                  '{0,1}^96. (3) ciphertext_j = AES-256-GCM.Enc(K_enc_j, IV_j, '
                                  'r_j, AAD = batch_id). (4) sig_j = Ed25519.Sign(sk_sender, '
                                  'H(ciphertext_j || batch_id || j)). (5) metadata_j = JSON(index, '
                                  'batch_id, timestamp). (6) leaf_j = H(ciphertext_j || sig_j || '
                                  'metadata_j).',
                                  'The use of index-derived encryption keys ensures that '
                                  'compromise of K_enc_j does not reveal other records in the '
                                  'batch. GCM authenticated encryption provides both '
                                  'confidentiality and integrity at the record level.']},
                  {'heading': '3.4.2 Batch Header and Merkle Root',
                   'paragraphs': ['The batch header binds all records cryptographically: Root = '
                                  'Merkle(leaf_1, ..., leaf_n). Header = (batch_id, epoch, '
                                  'domain_id, Root, PK_sender, Sig_header, timestamp, n). '
                                  'Sig_header = Ed25519.Sign(sk_sender, batch_id || epoch || '
                                  'Root).',
                                  'The Merkle root provides O(1) batch-level integrity evidence: '
                                  'any modification to any record changes the root hash. '
                                  'Individual record inclusion can be proven with O(log n) hash '
                                  'computations via Merkle authentication paths.'],
                   'figure': 'ECC-HISE secure envelope structure with Merkle audit chain (Figure '
                             '3.2).'},
                  {'heading': '3.4.3 Verification and Decryption',
                   'paragraphs': ['The receiver executes the following steps: (1) Verify '
                                  "Sig_header using sender's Ed25519 public key. (2) Recompute "
                                  'Merkle root from received leaf hashes; compare with '
                                  'Header.Root. (3) For each record j: verify sig_j, derive '
                                  'K_enc_j from SK_batch, decrypt ciphertext_j with AES-256-GCM, '
                                  'verify GCM authentication tag. (4) Optionally verify Merkle '
                                  'inclusion proof for audit sampling. (5) Log (batch_id, Root, '
                                  'timestamp) to immutable audit store.',
                                  'Any failure at steps 1–3 indicates tampering, key mismatch, or '
                                  'data corruption. The receiver rejects the entire batch on '
                                  'header verification failure; individual record failures are '
                                  'logged and flagged without silently skipping.'],
                   'figure': 'Server-server batch verification and audit flow (Figure 3.3).'},
                  {'heading': '3.4.4 Deployment in Inter-Bank Settlement',
                   'paragraphs': ["In a representative deployment, Bank A's settlement server "
                                  'constructs an ECC-HISE batch from end-of-day payment records '
                                  "and transmits the envelope to Bank B's settlement server over "
                                  'mTLS. Bank B verifies the batch header signature, Merkle root, '
                                  'and each record signature before posting to its core banking '
                                  'ledger. The clearing-house authority receives (batch_id, Root, '
                                  'timestamp) for regulatory archive. This workflow satisfies '
                                  'SWIFT CSP controls for data integrity and non-repudiation while '
                                  'adding cryptographic audit efficiency not present in '
                                  'file-transfer-only approaches.']},
                  {'heading': '3.4.5 Why Per-Record Keys and Per-Record Signatures',
                   'paragraphs': ['Encrypting an entire batch under one AES-GCM key is simpler but '
                                  'couples confidentiality failure modes: a single IV misuse or '
                                  'partial leak can affect all records. Index-derived keys K_enc_j '
                                  '= HKDF(SK_batch, salt=str(j), ...) ensure that compromise of '
                                  'one record key does not decrypt siblings. Combined with unique '
                                  'IVs per record, this design reduces the blast radius of '
                                  'implementation mistakes at the cost of n HKDF '
                                  'expansions—negligible relative to AES-GCM and Ed25519 for '
                                  'typical settlement sizes.',
                                  'Per-record signatures enable receivers to reject individual '
                                  'malformed records while still validating the batch structure, '
                                  'and they support selective disclosure to auditors. A design '
                                  'using only a single signature over the Merkle root would '
                                  'authenticate the set of ciphertexts but would not bind each '
                                  'ciphertext to the sender independently of the tree; ECC-HISE '
                                  'uses both so that leaf authenticity and set integrity are dual '
                                  'checks.']},
                  {'heading': '3.4.6 Failure Modes and Safe Abort Behavior',
                   'paragraphs': ['Verification must be constant-time with respect to early abort '
                                  'on signature failure where feasible, and must never decrypt '
                                  'before authenticity checks succeed (encrypt-then-sign / '
                                  'sign-over-ciphertext discipline). If the batch header signature '
                                  'fails, the receiver aborts without processing leaves. If the '
                                  'Merkle root mismatches, the receiver aborts even if individual '
                                  'signatures verify—indicating a spliced or reordered set. If a '
                                  'single leaf fails, implementations may quarantine that index '
                                  'while accepting the remainder only when policy explicitly '
                                  'allows partial settlement; the default secure posture is '
                                  'fail-closed for the entire batch.',
                                  'Clock skew, duplicate batch_id replay, and stale domain keys '
                                  'are handled by application policy: batch_id uniqueness stores, '
                                  'timestamp windows, and key-version fields in the header. '
                                  'ECC-HISE provides the cryptographic substrate; operational '
                                  'replay databases remain necessary, analogous to TLS session '
                                  'ticket tracking.']}]},
 {'heading': '3.5 Security Analysis',
  'paragraphs': ['This section analyzes the security properties of ECC-HISE under standard '
                 'cryptographic assumptions.'],
  'subsections': [{'heading': '3.5.1 Security Properties',
                   'paragraphs': ['Theorem 3.1 (Record Confidentiality): Under IND-CCA2 security '
                                  'of AES-256-GCM and PRF security of HKDF, an adversary without '
                                  'SK_batch cannot distinguish ciphertext_j from random. Proof '
                                  'sketch: SK_batch is derived via HKDF from MK; without MK or '
                                  'domain key, SK_batch is computationally indistinguishable from '
                                  'random.',
                                  'Theorem 3.2 (Record Integrity): Under EUF-CMA security of '
                                  'Ed25519 and collision resistance of SHA-256, an adversary '
                                  'cannot forge (ciphertext_j, sig_j) for a new or modified record '
                                  "without the sender's private key.",
                                  'Theorem 3.3 (Batch Integrity): Under collision resistance of '
                                  'SHA-256, an adversary cannot produce a valid Header with Root '
                                  'consistent with a modified set of records. Any record '
                                  'alteration changes its leaf hash, propagating to a different '
                                  'Merkle root.',
                                  'Theorem 3.4 (Audit Soundness): A Merkle inclusion proof for '
                                  'record j verifies only if leaf_j is included in the batch '
                                  'committed by Root. Proof follows from Merkle tree binding '
                                  'properties.']},
                  {'heading': '3.5.2 Attack Resistance',
                   'paragraphs': ['Table 3.1 maps ECC-HISE resistance to server-server attack '
                                  'vectors relevant to e-finance data transfer.'],
                   'table': {'headers': ['Threat', 'Mechanism', 'Resistance', 'Basis'],
                             'rows': [['Data tampering',
                                       'Modify record in transit',
                                       'High',
                                       'GCM tag + Ed25519 + Merkle'],
                                      ['Record injection',
                                       'Add fake record',
                                       'High',
                                       'Merkle root mismatch'],
                                      ['Record deletion',
                                       'Omit record',
                                       'High',
                                       'Merkle root mismatch'],
                                      ['Reorder attack',
                                       'Permute records',
                                       'High',
                                       'Index-bound keys + Merkle'],
                                      ['Key compromise',
                                       'Steal static PSK',
                                       'Medium-High',
                                       'Per-batch key rotation'],
                                      ['Repudiation',
                                       'Deny sending batch',
                                       'High',
                                       'Sig_header + per-record sigs']],
                             'caption': 'Table 3.1: ECC-HISE resistance to server-server data '
                                        'attacks.'}},
                  {'heading': '3.5.3 Addressing Section 1.3.3 Limitations',
                   'paragraphs': ['L1 (Flat key hierarchy): Resolved via MK → DK_i → SK_batch '
                                  'derivation.',
                                  'L2 (Disconnected audit): Resolved — Merkle root is embedded in '
                                  'signed batch header.',
                                  'L3 (Batch verification cost): Resolved — O(log n) Merkle proofs '
                                  'vs O(n) full reprocess.',
                                  'L4 (Static PSKs): Resolved — per-batch session keys derived '
                                  'from domain keys.',
                                  'L5 (Service-boundary gaps): Resolved — envelope integrity '
                                  'persists beyond TLS.',
                                  'L6 (Audit friction): Resolved — cryptographic audit chain for '
                                  'regulators.']},
                  {'heading': '3.5.4 Adversarial Model for Server-Server Channels',
                   'paragraphs': ['We consider a network adversary who can eavesdrop, drop, delay, '
                                  'inject, and reorder messages on the institutional network, plus '
                                  'a stronger adversary who compromises a receiving host after TLS '
                                  'termination (honest-but-curious gateway). The second adversary '
                                  'models API gateways and message brokers that see plaintext '
                                  'after mTLS decryption—precisely the setting where envelope '
                                  'cryptography is required.',
                                  "We assume the sender's Ed25519 private key remains "
                                  'uncompromised during batch production, HKDF-SHA-256 behaves as '
                                  'a dual PRF in the usual way, AES-GCM is secure under unique '
                                  'nonces, and SHA-256 is collision-resistant for Merkle tree '
                                  'nodes. Under these assumptions, forging a batch header or '
                                  'substituting a leaf while preserving the signed root is '
                                  'infeasible.']},
                  {'heading': '3.5.5 Comparison with Sign-Then-Encrypt and CMS Detached Signatures',
                   'paragraphs': ['Cryptographic Message Syntax (CMS) and related S/MIME profiles '
                                  'can sign and encrypt files, and are used in some banking '
                                  'document exchanges. ECC-HISE differs by (1) hierarchical '
                                  'batch-scoped keys rather than per-message certificate '
                                  'encryption for every record, (2) explicit Merkle audit proofs '
                                  'optimized for selective verification, and (3) index-bound keys '
                                  'that encode ordering into the key schedule. CMS remains '
                                  'valuable for document workflows; ECC-HISE targets high-volume '
                                  'structured settlement batches where audit efficiency and key '
                                  'hierarchy matter.',
                                  'Sign-then-encrypt without a Merkle layer authenticates messages '
                                  'but forces auditors to re-process entire files to confirm '
                                  'membership. Encrypt-then-MAC with a single batch MAC detects '
                                  'modification but does not support compact inclusion proofs. '
                                  "ECC-HISE's combination of AEAD, signatures, and Merkle "
                                  'commitments is chosen specifically for regulatory auditability '
                                  'at scale.']}]},
 {'heading': '3.6 Effectiveness Analysis and Quantitative Evaluation',
  'paragraphs': ['This section presents quantitative evaluation of ECC-HISE against static AES-GCM '
                 'with pre-shared keys and TLS record-layer-only encryption, using the prototype '
                 'implementation and benchmark suite (prototype/benchmarks/bench_hise.py).'],
  'subsections': [{'heading': '3.6.1 Experimental Setup',
                   'paragraphs': ['Benchmarks measure batch encryption, signing, Merkle '
                                  'construction, verification, and decryption for record counts n '
                                  '∈ {10, 100, 500}. Each record is 256 bytes, representative of a '
                                  'compact settlement entry. Measurements are averaged over 50 '
                                  'iterations on Intel x64 hardware with Python 3.11 and '
                                  'OpenSSL-backed cryptography.']},
                  {'heading': '3.6.2 Throughput and Latency',
                   'paragraphs': ['For n = 100 records, ECC-HISE completes batch '
                                  'protect-and-verify in 23.32 ms (mean), compared to 0.22 ms for '
                                  'static AES-GCM PSK and 0.24 ms for TLS record-layer-only '
                                  'encryption. The ECC-HISE premium arises from Ed25519 signing '
                                  'per record, Merkle tree construction, and hierarchical key '
                                  'derivation—operations that baselines omit entirely.',
                                  'For n = 500 records, ECC-HISE requires 245.53 ms, processing '
                                  'approximately 2,040 records per second. This throughput exceeds '
                                  'typical end-of-day settlement batch requirements for regional '
                                  'banks (hundreds to low thousands of records per batch), with '
                                  'horizontal scaling available via parallel batch processing.'],
                   'figure': 'Batch processing latency and size comparison across schemes (Figure '
                             '3.4).'},
                  {'heading': '3.6.3 Storage and Bandwidth Overhead',
                   'paragraphs': ['For n = 100 records of 256 bytes each (25,600 bytes plaintext), '
                                  'ECC-HISE produces batches averaging 37823 bytes, a 48% '
                                  'overhead. Static AES-GCM produces 28400 bytes (11% overhead) '
                                  'without signatures or Merkle audit data. TLS record-layer-only '
                                  'produces 28905 bytes.',
                                  'The additional overhead of ECC-HISE (~33% over static AES-GCM '
                                  'for n=100) purchases per-record non-repudiation, batch-level '
                                  'Merkle audit chain, hierarchical key isolation, and '
                                  'domain-separated key management—properties unavailable in '
                                  'baseline schemes at any overhead.'],
                   'table': {'headers': ['Scheme',
                                         'n=100 latency (ms)',
                                         'n=100 size (B)',
                                         'Merkle audit',
                                         'Hierarchy',
                                         'Signatures'],
                             'rows': [['ECC-HISE', '23.32', '37823', 'Yes', 'Yes', 'Yes'],
                                      ['Static AES-GCM', '0.22', '28400', 'No', 'No', 'No'],
                                      ['TLS record only', '0.24', '28905', 'No', 'No', 'No']],
                             'caption': 'Table 3.2: Quantitative comparison for 100-record '
                                        'settlement batches (n=50 iterations).'}},
                  {'heading': '3.6.4 Audit Efficiency',
                   'paragraphs': ['Merkle inclusion proof verification requires ⌈log_2(n)⌉ hash '
                                  'operations per record. For n = 100, each proof verifies in 7 '
                                  'hashes (~0.001 ms). A regulator sampling 10% of records for '
                                  'audit performs 10 × 7 = 70 hash operations instead of '
                                  'reprocessing all 100 records, reducing audit computation by '
                                  '90%. For n = 500, proofs require 9 hashes each, maintaining '
                                  'logarithmic scaling.',
                                  'Compared to per-record RSA signatures with full-batch '
                                  'recomputation for audit, ECC-HISE reduces audit cost from O(n) '
                                  'to O(k log n) for k sampled records, a significant improvement '
                                  'for million-record settlement files.']},
                  {'heading': '3.6.5 Scalability Projection',
                   'paragraphs': ['Linear scaling in record count dominates ECC-HISE processing '
                                  'time due to per-record encryption and signing. For '
                                  'million-record national settlement files, parallel batch '
                                  'partitioning (multiple ECC-HISE envelopes of 10,000 records '
                                  'each) enables multi-core processing. Merkle roots of '
                                  'sub-batches can themselves form a meta-Merkle tree for '
                                  'hierarchical audit—a straightforward extension not required for '
                                  'regional-bank workloads but available for central-bank scale.']},
                  {'heading': '3.6.6 Interpretation of Prototype Measurements',
                   'paragraphs': ['Prototype benchmarks in this chapter measure cryptographic core '
                                  'costs on commodity hardware without network latency or HSM '
                                  'round-trips. Absolute milliseconds therefore understate '
                                  'production latency but fairly compare relative overhead among '
                                  'ECC-HISE, flat AES-GCM batch encryption, and sign-only '
                                  'baselines. The dominant costs are per-record AEAD and Ed25519 '
                                  'signatures; Merkle hashing is comparatively cheap.',
                                  'For regional banks with batches of hundreds to thousands of '
                                  'records, ECC-HISE completes well within typical settlement '
                                  'windows. For national switches processing millions of records, '
                                  "the chapter's partitioning strategy—multiple envelopes under a "
                                  'meta-Merkle root—keeps per-envelope latency bounded and enables '
                                  'parallel verification. These engineering projections are '
                                  'consistent with the linear complexity observed in the prototype '
                                  'curves.']},
                  {'heading': '3.6.7 Storage Overhead and Archival Economics',
                   'paragraphs': ['Each record carries ciphertext expansion (GCM tag), an Ed25519 '
                                  'signature (64 bytes), and metadata. The batch header adds a '
                                  'constant-size signature and root. Relative overhead shrinks as '
                                  'average record size grows: for compact payment messages of a '
                                  'few hundred bytes, signature overhead is noticeable; for richer '
                                  'ISO 20022 payloads, it is modest. Institutions already store '
                                  'redundant settlement copies for compliance; replacing one '
                                  'redundant cleartext archive with a cryptographically verifiable '
                                  'envelope archive can improve assurance without proportional '
                                  'storage growth.']}]},
 {'heading': '3.7 Comparison with Chapter 2 and Prior Approaches',
  'paragraphs': ['ECC-HISE and ECC-DTB-AKA address complementary security layers in e-finance '
                 'systems. Chapter 2 secures who is communicating and establishes session keys in '
                 'client-server channels; Chapter 3 secures what data is transferred and provides '
                 'audit evidence in server-server channels. Together they form the dual-layer ECC '
                 'methodology of this dissertation.',
                 'Compared to ECIES-only encryption, ECC-HISE adds hierarchical keys and Merkle '
                 'audit. Compared to blockchain-based audit trails, ECC-HISE avoids consensus '
                 'overhead while providing cryptographic integrity guarantees sufficient for '
                 'regulated settlement. Compared to TLS-only protection, ECC-HISE provides '
                 'persistent integrity proofs that survive TLS termination at service boundaries.'],
  'subsections': [{'heading': '3.7.1 Dual-Layer Coverage Matrix',
                   'paragraphs': ['Table-style reasoning clarifies complementary coverage: session '
                                  'hijacking and device transfer attacks are primarily mitigated '
                                  'by ECC-DTB-AKA; batch tampering, selective record deletion, and '
                                  'post-TLS integrity loss are mitigated by ECC-HISE. Neither '
                                  "scheme alone closes Chapter 1's full gap list. Deploying both "
                                  'yields defense-in-depth with shared ECC/HKDF implementation '
                                  'skills and HSM policies.',
                                  'Prior approaches such as blockchain settlement pilots provide '
                                  'strong shared audit logs but introduce consensus latency, '
                                  'governance complexity, and often weaker confidentiality. '
                                  'ECC-HISE retains bilateral (or multilateral clearing-house) '
                                  'topologies familiar to banks while offering Merkle-style audit '
                                  'commitments without distributed consensus.']}]},
 {'heading': '3.8 Chapter Summary',
  'paragraphs': ['This chapter proposed ECC-HISE, a hierarchical integrity-preserving secure '
                 'envelope for server-server data transfer in e-banking and e-finance systems. The '
                 'scheme addresses six data-security limitations from Section 1.3.3 through '
                 'hierarchical ECC key derivation, AES-256-GCM record encryption, Ed25519 '
                 'signatures, and Merkle-tree audit chains. Security analysis establishes '
                 'confidentiality, integrity, and audit soundness under standard assumptions. '
                 'Quantitative evaluation demonstrates 23.32 ms batch processing for 100 records '
                 'with 37823-byte envelopes, providing audit and non-repudiation capabilities '
                 'absent in static PSK and TLS-only baselines. Chapter 4 describes the integrated '
                 'system architecture and programmatic implementation of both ECC-DTB-AKA and '
                 'ECC-HISE.'],
  'subsections': [{'heading': '3.8.1 Forward Links',
                   'paragraphs': ['Chapter 4 implements ECC-HISE as executable modules and '
                                  'integrates them with a settlement API alongside ECC-DTB-AKA. '
                                  'Chapter 5 revisits prior work on ECIES, TLS record protection, '
                                  'static PSK encryption, and ledger-based audit, positioning '
                                  'ECC-HISE among these alternatives with quantitative and '
                                  'qualitative comparison.']}]}]
