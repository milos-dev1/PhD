"""Chapter 5: Evaluation, Prior Work, and Vulnerability Synthesis."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks"
_B2 = json.loads((ROOT / "chapter2_benchmarks.json").read_text()) if (ROOT / "chapter2_benchmarks.json").exists() else []
_B3 = json.loads((ROOT / "chapter3_benchmarks.json").read_text()) if (ROOT / "chapter3_benchmarks.json").exists() else []

def _b2(name): return next((d for d in _B2 if d["scheme"] == name), {})
def _b3(name, n=100): return next((d for d in _B3 if d["scheme"] == name and d["records"] == n), {})

DTB = _b2("ECC-DTB-AKA") or {"auth_latency_ms_mean": 0.52, "total_message_bytes_mean": 569, "round_trips": 3}
TLS = _b2("TLS 1.3 (crypto core)") or {"auth_latency_ms_mean": 0.21, "total_message_bytes_mean": 2800}
ECDH = _b2("Standard ECDH") or {"auth_latency_ms_mean": 0.11, "total_message_bytes_mean": 130}
HISE = _b3("ECC-HISE") or {"latency_ms_mean": 23.32, "batch_bytes_mean": 37823}
STATIC = _b3("Static AES-GCM PSK") or {"latency_ms_mean": 0.22, "batch_bytes_mean": 28400}

CHAPTER_TITLE = "Chapter 5"
CHAPTER_SUBTITLE = "Evaluation, Prior Work Analysis, and Vulnerability Synthesis"

SECTIONS = [{'heading': '5.1 Effectiveness of Proposed Methods Against Network Attacks',
  'paragraphs': ['This section evaluates the effectiveness of ECC-DTB-AKA and ECC-HISE against the '
                 'attack mechanisms cataloged in Chapter 1 (Section 1.1), using both qualitative '
                 'security analysis from Chapters 2 and 3 and quantitative measurements from the '
                 'prototype implementation in Chapter 4.'],
  'subsections': [{'heading': '5.1.1 Attack Resistance Matrix',
                   'paragraphs': ['Table 5.1 consolidates resistance ratings for both proposed '
                                  'schemes against the six primary attack categories defined in '
                                  'Section 1.1.1. Ratings reflect cryptographic analysis, '
                                  'prototype test results, and comparison with baseline schemes '
                                  'that lack device binding, transaction binding, or Merkle audit '
                                  'capabilities.'],
                   'table': {'headers': ['Attack category',
                                         'ECC-DTB-AKA',
                                         'ECC-HISE',
                                         'Baseline (TLS/PSK)'],
                             'rows': [['MITM / impersonation',
                                       'High',
                                       'High (sig chain)',
                                       'Medium (server-only)'],
                                      ['Replay', 'High (nonces)', 'High (Merkle+nonce)', 'Medium'],
                                      ['Session hijacking',
                                       'High (device_fp)',
                                       'N/A (server-server)',
                                       'Low (bearer token)'],
                                      ['Credential stuffing',
                                       'N/A (PKI-based)',
                                       'N/A',
                                       'Low (password)'],
                                      ['Data tampering',
                                       'Medium (HMAC txn)',
                                       'High (GCM+sig+Merkle)',
                                       'Low (TLS only)'],
                                      ['Insider / audit evasion',
                                       'Medium',
                                       'High (Merkle audit)',
                                       'Low']],
                             'caption': 'Table 5.1: Attack resistance matrix for proposed schemes '
                                        'vs. baselines.'},
                   'figure': 'Comparative attack resistance overview (Figure 5.1).'},
                  {'heading': '5.1.2 Quantitative Authentication Performance',
                   'paragraphs': ['ECC-DTB-AKA achieves mutual authentication in 3 round trips '
                                  'with 0.52 ms mean cryptographic latency and 569 bytes total '
                                  'message overhead. Compared to TLS 1.3 (0.21 ms, 2800 bytes), '
                                  'ECC-DTB-AKA trades one additional round trip and smaller '
                                  'absolute latency for mutual authentication, device binding, and '
                                  'transaction binding—properties TLS does not provide natively.',
                                  'For server-server batch protection, ECC-HISE processes 100 '
                                  'records in 23.32 ms with 37823-byte envelopes versus 0.22 ms '
                                  'and 28400 bytes for static PSK. The 106× latency premium '
                                  'purchases hierarchical keys, per-record Ed25519 signatures, and '
                                  'Merkle audit chains absent in static encryption.'],
                   'figure': 'Combined quantitative comparison of both schemes (Figure 5.2).'},
                  {'heading': '5.1.3 Case-Based Effectiveness Assessment',
                   'paragraphs': ['Against the Bangladesh Bank heist scenario (Section 1.1.2), '
                                  'ECC-HISE would require valid Ed25519 header signatures and '
                                  'consistent Merkle roots for fraudulent SWIFT messages to pass '
                                  'verification—raising the bar beyond local terminal compromise '
                                  "alone. Against credential-stuffing campaigns, ECC-DTB-AKA's "
                                  'PKI-based client authentication eliminates password guessing '
                                  'entirely when deployed with hardware-backed client keys. '
                                  'Against session hijacking via stolen JWTs, device_fp binding in '
                                  'MSK derivation prevents session transfer to attacker-controlled '
                                  'devices without valid client signatures.']},
                  {'heading': '5.1.4 Residual Risks and Non-Goals',
                   'paragraphs': ['No cryptographic protocol eliminates fraud. ECC-DTB-AKA does '
                                  'not stop an authorized user on a bound device from initiating a '
                                  'socially engineered payment; ECC-HISE does not detect '
                                  'semantically incorrect but correctly signed settlement amounts. '
                                  'Fraud analytics, beneficiary confirmation, and organizational '
                                  'controls remain necessary.',
                                  'Similarly, malware with full control of a device can '
                                  'potentially subvert fingerprint inputs unless hardware '
                                  'attestation is enforced. The schemes raise the bar for remote '
                                  'attackers who rely on stolen bearer tokens, replayed sessions, '
                                  'or undetectable batch tampering after TLS termination—the '
                                  'dominant remote patterns identified in Chapter 1—without '
                                  'claiming omnipotent endpoint security.']},
                  {'heading': '5.1.5 Combined Dual-Layer Effectiveness Narrative',
                   'paragraphs': ['Viewed as a methodology, the dual-layer design closes '
                                  'complementary gaps: authentication decoupling and bearer-token '
                                  'abuse on the client path; flat keys and audit friction on the '
                                  'server path. Quantitative results show acceptable overhead '
                                  'relative to baselines; qualitative analysis shows coverage of '
                                  'SR1–SR8. The remainder of this chapter situates these claims '
                                  'against prior protocols and systems.']},
                  {'heading': '5.1.6 Threat Coverage Relative to Chapter 1 Catalogue',
                   'paragraphs': ['Mapping Table 5.1 back to Section 1.1 shows strong coverage for '
                                  'MITM, replay, session hijacking, and batch tampering—the remote '
                                  'network and post-termination integrity threats that dominate '
                                  'the dissertation scope. Credential stuffing is out of scope for '
                                  'ECC-DTB-AKA once PKI client keys replace passwords; where '
                                  'passwords remain, PAKE or FIDO enrollment is the appropriate '
                                  'prior control.',
                                  'Insider threats with legitimate signing keys are only partially '
                                  'mitigated: ECC-HISE provides non-repudiation and audit trails '
                                  'that increase detection probability and forensic clarity, but '
                                  'organizational key custody remains essential. This boundary is '
                                  'stated explicitly so effectiveness claims are not overstated.']},
                  {'heading': '5.1.7 Cost–Benefit Interpretation of Benchmarks',
                   'paragraphs': ['Raw latency comparisons can mislead if security properties '
                                  'differ. ECC-DTB-AKA is slower than bare ECDH and uses more '
                                  'round trips than a TLS resumption path, yet it purchases mutual '
                                  'authentication with device and transaction binding that those '
                                  'baselines omit. ECC-HISE is orders of magnitude slower than '
                                  'static PSK encryption of the same records, yet static PSK '
                                  'provides neither signatures nor Merkle audit.',
                                  'In e-banking, authentication events are relatively rare '
                                  'compared with page views, and settlement batches are scheduled '
                                  'offline relative to interactive UX. Therefore absolute '
                                  'millisecond costs observed in the prototype are operationally '
                                  'acceptable when weighed against fraud and integrity incident '
                                  'costs that Chapter 1 case studies illustrate.',
                                  'The appropriate managerial question is not whether the schemes '
                                  'match the cheapest baseline, but whether the incremental cost '
                                  'is justified by coverage of SR1–SR8. Chapter 5 answers '
                                  'affirmatively for the evaluated threat classes, with residual '
                                  'risks acknowledged in Section 5.1.4.']}]},
 {'heading': '5.2 Prior Work on Authentication and Key Exchange',
  'paragraphs': ['This section reviews prior research and deployed protocols for authentication '
                 'and key exchange in client-server and server-server environments of e-banking '
                 'and e-finance services, expanding the overview presented in Section 1.2 with '
                 'detailed algorithmic descriptions and comparative analysis against ECC-DTB-AKA.'],
  'subsections': [{'heading': '5.2.1 TLS 1.3 Handshake Protocol',
                   'paragraphs': ['TLS 1.3 (RFC 8446) is the dominant transport security protocol '
                                  'for e-banking. The full handshake operates as: (1) ClientHello '
                                  'with key_share (typically X25519 or P-256); (2) ServerHello, '
                                  'EncryptedExtensions, Certificate, CertificateVerify, Finished; '
                                  '(3) Client Finished. Application traffic keys are derived via '
                                  'HKDF from the ECDH shared secret. Forward secrecy is mandatory; '
                                  '0-RTT resumption is optional but vulnerable to replay.',
                                  'Limitations for e-banking: server-only authentication at the '
                                  'TLS layer; user identity established separately via application '
                                  'credentials; no device or transaction binding in key '
                                  'derivation. ECC-DTB-AKA addresses these by integrating user '
                                  'authentication and binding into the key agreement protocol '
                                  'itself.'],
                   'figure': 'TLS 1.3 full handshake flow (Figure 5.3).'},
                  {'heading': '5.2.2 OAuth 2.0 and Open Banking (PKCE)',
                   'paragraphs': ['OAuth 2.0 with PKCE (RFC 7636) enables third-party providers to '
                                  'access bank APIs with customer consent. Flow: (1) Client '
                                  'generates code_verifier and code_challenge; (2) Authorization '
                                  'request redirects customer to bank; (3) Customer authenticates '
                                  'and grants consent; (4) Authorization code returned; (5) Token '
                                  'exchange with code_verifier; (6) Access token used for API '
                                  'calls. PKCE prevents authorization code interception.',
                                  'Limitations: bearer access tokens; no cryptographic binding to '
                                  'transaction context; token theft enables API abuse until '
                                  "expiration. ECC-DTB-AKA's TBK-derived HMAC provides "
                                  'per-transaction authorization without bearer semantics.'],
                   'figure': 'OAuth 2.0 PKCE authorization flow for open banking (Figure 5.4).'},
                  {'heading': '5.2.3 FIDO2 / WebAuthn',
                   'paragraphs': ['FIDO2 combines WebAuthn (browser API) and CTAP2 (authenticator '
                                  'protocol) for phishing-resistant authentication. Registration: '
                                  'server sends challenge, authenticator generates credential key '
                                  'pair, returns attestation. Authentication: server sends '
                                  'challenge with rpId, authenticator signs with credential '
                                  'private key. The rpId binding prevents credential use on '
                                  'phishing domains.',
                                  'Relation to ECC-DTB-AKA: FIDO2 credential public key can serve '
                                  'as PK_C in ECC-DTB-AKA, combining phishing resistance with '
                                  'device/transaction-bound session keys. FIDO2 alone does not '
                                  'establish encrypted session keys or per-transaction '
                                  'derivation.']},
                  {'heading': '5.2.4 Server-Server Key Exchange (mTLS and SWIFT BKE)',
                   'paragraphs': ['Mutual TLS uses X.509 client and server certificates for '
                                  'bidirectional authentication at the transport layer. '
                                  'Certificate rotation, OCSP stapling, and short-lived certs '
                                  '(24h) are best practices in microservice meshes. SWIFT '
                                  'bilateral key exchange (BKE) distributes symmetric keys for '
                                  'message authentication in the SWIFT network.',
                                  'Limitations: mTLS does not provide message-level integrity '
                                  'after TLS termination; SWIFT BKE relies on symmetric keys with '
                                  'manual distribution. ECC-DTB-AKA extends client-server auth; '
                                  'ECC-HISE extends server-server data protection beyond '
                                  'transport.'],
                   'figure': 'mTLS service mesh authentication in banking microservices (Figure '
                             '5.5).'},
                  {'heading': '5.2.5 Comparative Summary',
                   'paragraphs': ['Table 5.2 summarizes authentication and key-exchange prior work '
                                  'against ECC-DTB-AKA across security properties and efficiency '
                                  'metrics from prototype benchmarks.'],
                   'table': {'headers': ['Protocol',
                                         'Mutual auth',
                                         'Device bind',
                                         'Txn bind',
                                         'RTT',
                                         'Latency (ms)'],
                             'rows': [['TLS 1.3', 'Server', 'No', 'No', '1', '0.21'],
                                      ['OAuth 2.0 PKCE', 'Delegated', 'No', 'No', '3+', 'N/A'],
                                      ['FIDO2/WebAuthn', 'User', 'Partial', 'No', '2', 'N/A'],
                                      ['Standard ECDH', 'No', 'No', 'No', '2', '0.11'],
                                      ['ECC-DTB-AKA', 'Yes', 'Yes', 'Yes', '3', '0.52']],
                             'caption': 'Table 5.2: Authentication and key-exchange prior work vs. '
                                        'ECC-DTB-AKA.'}},
                  {'heading': '5.2.6 EMV and Card-Present Authentication',
                   'paragraphs': ['EMV (Europay, Mastercard, Visa) chip cards use ECDSA on '
                                  'secp256r1 for offline and online transaction authentication. '
                                  'Contactless payments add relay-attack vulnerabilities addressed '
                                  'by distance-bounding protocols under research. EMV addresses '
                                  'card-present channels; ECC-DTB-AKA addresses remote digital '
                                  'banking channels with similar ECC foundations but different '
                                  'binding requirements (device_fp, txn_nonce).']},
                  {'heading': '5.2.7 Password-Authenticated Key Exchange and Banking Reality',
                   'paragraphs': ['PAKE protocols (SRP, OPAQUE, etc.) protect password-based login '
                                  'against pre-computation and some server compromise scenarios. '
                                  'They are valuable upgrades for password verifiers but do not, '
                                  'by themselves, bind sessions to devices or derive '
                                  'per-transaction keys for payment authorization. ECC-DTB-AKA '
                                  'assumes a public-key client identity (which may be provisioned '
                                  'after PAKE or FIDO enrollment) and focuses on post-login '
                                  'channel binding.']},
                  {'heading': '5.2.8 5G AKA and Telecom Auth as Contrasting Domain',
                   'paragraphs': ['Mobile network AKA protocols bind authentication to subscriber '
                                  'modules (SIM/USIM) with sequence numbers and '
                                  'operator-controlled key hierarchies. They illustrate how '
                                  'another high-value industry solved device-subscription binding. '
                                  'E-banking cannot simply reuse 5G AKA because trust anchors, '
                                  'identity models, and transaction semantics differ; however, the '
                                  "analogy supports the dissertation's insistence on cryptographic "
                                  'binding to a client-held authenticator rather than to a bearer '
                                  'cookie alone.']},
                  {'heading': '5.2.9 Gaps Remaining in Industry Deployments',
                   'paragraphs': ['Despite TLS 1.3, OAuth PKCE, and FIDO adoption, many banks '
                                  'still operate legacy app versions, SMS OTP fallbacks, and '
                                  'long-lived refresh tokens. Server meshes may use mTLS with '
                                  'certificates that authenticate clusters rather than logical '
                                  'settlement roles. These deployment gaps motivate '
                                  'application-layer protocols that encode banking '
                                  'semantics—device and transaction binding; batch audit '
                                  'commitments—rather than relying solely on continual perfection '
                                  'of the transport and identity platforms.']},
                  {'heading': '5.2.10 EMV Card-Present Binding Versus Remote Channels',
                   'paragraphs': ['EMV chip protocols bind payments to a physical card and '
                                  'issuer-authorized cryptograms in card-present environments. '
                                  'Remote e-banking lacks an equivalent hardware cryptogram path '
                                  'unless FIDO or secure elements are used. ECC-DTB-AKA borrows '
                                  'the binding intuition—authorization should not be a '
                                  'transferable bearer string—while operating over Internet '
                                  'channels with ECC key agreement.',
                                  'The comparison clarifies novelty relative to retail payments '
                                  'research: the contribution is not inventing binding in the '
                                  'abstract, but integrating device and transaction binding into a '
                                  'mutual AKE suitable for mobile and web banking APIs evaluated '
                                  'against TLS and OAuth baselines.']},
                  {'heading': '5.2.11 Session Tokens, DPoP, and Emerging Binding Trends',
                   'paragraphs': ['Industry movement toward sender-constrained tokens (e.g., OAuth '
                                  'DPoP) and certificate-bound access tokens reflects growing '
                                  'recognition that bearer tokens are insufficient. ECC-DTB-AKA is '
                                  'philosophically aligned with that trend but binds at '
                                  'key-agreement time with device_fp and txn_nonce in HKDF, rather '
                                  'than only constraining presentation of an already-issued access '
                                  'token.',
                                  'DPoP and ECC-DTB-AKA can coexist: DPoP may protect general API '
                                  'access while TBK-HMAC authorizes high-risk payments. The '
                                  'dissertation positions ECC-DTB-AKA as a banking-semantic AKE, '
                                  'not as a wholesale replacement for the OAuth ecosystem.']},
                  {'heading': '5.2.12 Formal Methods Landscape for AKE',
                   'paragraphs': ['Modern AKE research often uses the eCK model, GJM model, or '
                                  'automated tools (ProVerif, Tamarin, CryptoVerif). This '
                                  'dissertation provides structured proof sketches mapping goals '
                                  'to reductions and game hops, sufficient for doctoral '
                                  'argumentation but short of machine-checked proofs. Related work '
                                  'that fully mechanizes TLS or Signal illustrates the '
                                  'aspirational bar for future verification of ECC-DTB-AKA.',
                                  'Choosing sketches over full mechanization was a deliberate '
                                  'scope decision to prioritize dual-layer systems contributions '
                                  'and prototype evaluation. The sketches identify oracle '
                                  'interfaces and adversary capabilities clearly enough to guide a '
                                  'subsequent Tamarin encoding.']}]},
 {'heading': '5.3 Prior Work on Data Encryption, Security, and Integrity',
  'paragraphs': ['This section reviews prior approaches to data encryption, security, and '
                 'integrity in e-banking and e-finance server-server channels, distinct from the '
                 'authentication focus of Section 5.2, and compares them with ECC-HISE.'],
  'subsections': [{'heading': '5.3.1 TLS Record Layer Protection',
                   'paragraphs': ['TLS record layer encrypts application data using AEAD ciphers '
                                  '(AES-128-GCM or ChaCha20-Poly1305) with keys derived from the '
                                  'handshake. Protection ends at TLS termination: load balancers, '
                                  'API gateways, and service meshes decrypt and re-encrypt traffic '
                                  'at each hop. Stored or forwarded messages after termination '
                                  'lack persistent integrity proofs.'],
                   'figure': 'TLS record layer vs. persistent envelope integrity (Figure 5.6).'},
                  {'heading': '5.3.2 ECIES and Hybrid Encryption',
                   'paragraphs': ['Elliptic Curve Integrated Encryption Scheme (ECIES, SEC 1 / '
                                  'IEEE 1363a) combines ECDH key agreement with symmetric '
                                  'encryption and MAC. Standard ECIES encrypts individual messages '
                                  'but does not provide hierarchical key management, batch Merkle '
                                  'audit, or domain-separated key derivation. ECC-HISE extends '
                                  'ECIES concepts with batch-level Merkle roots and three-level '
                                  'HKDF hierarchy.']},
                  {'heading': '5.3.3 Static Pre-Shared Key File Encryption',
                   'paragraphs': ['Inter-bank file transfer historically uses PGP/GPG or '
                                  'proprietary tools with symmetric keys distributed annually via '
                                  'secure courier. Keys remain valid for extended periods; '
                                  'compromise exposes all files encrypted under that key. '
                                  'Benchmark: static AES-GCM PSK achieves 0.22 ms for 100 records '
                                  'but provides no signatures, Merkle audit, or key hierarchy.']},
                  {'heading': '5.3.4 Blockchain and Distributed Ledger Audit',
                   'paragraphs': ['Blockchain systems (Bitcoin, Ethereum, R3 Corda, Hyperledger '
                                  'Fabric) provide tamper-evident audit via Merkle trees and '
                                  'consensus. JPMorgan Onyx and similar platforms pilot '
                                  'distributed ledgers for settlement. Limitations: consensus '
                                  'latency, throughput constraints, and operational complexity. '
                                  'ECC-HISE adopts Merkle audit without distributed consensus, '
                                  'suitable for traditional settlement workflows.'],
                   'figure': 'Merkle audit: blockchain vs. ECC-HISE envelope (Figure 5.7).'},
                  {'heading': '5.3.5 Comparative Summary',
                   'paragraphs': ['Table 5.3 compares data-protection prior work with ECC-HISE for '
                                  '100-record batches.'],
                   'table': {'headers': ['Approach',
                                         'Hierarchy',
                                         'Merkle audit',
                                         'Per-record sig',
                                         'Latency (ms)',
                                         'Size (B)'],
                             'rows': [['TLS record only', 'No', 'No', 'No', '0.24', '28905'],
                                      ['Static AES-GCM PSK', 'No', 'No', 'No', '0.22', '28400'],
                                      ['Standard ECIES', 'No', 'No', 'Optional', 'N/A', 'N/A'],
                                      ['Blockchain audit',
                                       'Varies',
                                       'Yes (consensus)',
                                       'Varies',
                                       'High',
                                       'High'],
                                      ['ECC-HISE', 'Yes', 'Yes', 'Yes', '23.32', '37823']],
                             'caption': 'Table 5.3: Data encryption and integrity prior work vs. '
                                        'ECC-HISE.'}},
                  {'heading': '5.3.6 Database TDE and Column-Level Encryption',
                   'paragraphs': ['Transparent Data Encryption (TDE) protects data at rest in '
                                  'Oracle, SQL Server, and PostgreSQL extensions. Column-level '
                                  'encryption targets sensitive fields (PAN, SSN). These '
                                  'mechanisms protect storage but not data in transit between '
                                  'services or audit integrity of exported settlement batches. '
                                  'ECC-HISE complements TDE by protecting inter-service batch '
                                  'transfer with verifiable integrity chains.']},
                  {'heading': '5.3.7 Merkle Trees Outside Cryptocurrencies',
                   'paragraphs': ['Merkle trees predate Bitcoin and appear in certificate '
                                  'transparency logs, backup systems, and authenticated data '
                                  'structures. ECC-HISE applies them to bilateral settlement '
                                  'batches with hierarchical keying and per-record AEAD—an '
                                  'application packing that is rarely presented as an integrated '
                                  'e-banking envelope scheme. Certificate transparency inspires '
                                  'public auditability; ECC-HISE keeps commitments verifiable by '
                                  'counterparties and regulators without requiring global public '
                                  'logs.']},
                  {'heading': '5.3.8 Format-Preserving and Tokenization Approaches',
                   'paragraphs': ['Payment ecosystems widely use tokenization (e.g., replacing PAN '
                                  'with tokens) and format-preserving encryption for legacy '
                                  'fields. These reduce PCI scope but do not authenticate batch '
                                  'membership or provide Merkle audit proofs for settlement files. '
                                  'ECC-HISE can carry already-tokenized payloads as plaintext '
                                  'records before envelope encryption, composing cleanly with '
                                  'tokenization programs.']},
                  {'heading': '5.3.9 Confidential Computing and Its Limits',
                   'paragraphs': ['Trusted execution environments can protect plaintext during '
                                  'processing inside enclaves. They complement but do not replace '
                                  'ECC-HISE: envelopes still matter when data leave enclaves for '
                                  'counterparties, archives, or non-enclave consumers. A '
                                  'defense-in-depth posture may combine enclave processing with '
                                  'ECC-HISE export formats.']},
                  {'heading': '5.3.10 Transparent Data Encryption and Column Encryption',
                   'paragraphs': ['Database TDE and column-level encryption protect data at rest '
                                  'within a bank estate. They do not authenticate membership of '
                                  'records in an inter-bank settlement batch after export, nor do '
                                  'they provide counterparty-verifiable Merkle commitments. '
                                  'ECC-HISE addresses the export and exchange path that TDE leaves '
                                  'unprotected once files leave the encrypted database boundary.',
                                  'Composition is natural: systems may keep TDE for storage, '
                                  'tokenize sensitive fields, and wrap exported batches in '
                                  'ECC-HISE envelopes for transmission and archival audit.']},
                  {'heading': '5.3.11 Authenticated Streaming and Secure Logging',
                   'paragraphs': ['Secure logging and forward-secure sequential authentication '
                                  '(e.g., hash chains, truncated MAC chains) address related '
                                  'integrity goals for event streams. ECC-HISE targets unordered '
                                  'or batch-oriented settlement files with random-access Merkle '
                                  'proofs, which hash chains do not efficiently provide for '
                                  'arbitrary record inclusion checks.',
                                  'Where banks require both streaming ingestion and batch '
                                  'settlement, a hash-chained ingest log can feed records into '
                                  'ECC-HISE batches at cut-off times, combining continuous '
                                  'monitoring with counterparty-verifiable envelopes.']},
                  {'heading': '5.3.12 Comparison With CMS/PKCS Envelope Formats',
                   'paragraphs': ['Cryptographic Message Syntax (CMS) and related PKCS envelope '
                                  'formats provide standardized hybrid encryption and signed-data '
                                  'structures widely supported by toolkits. ECC-HISE is not '
                                  'proposed as a competitor to CMS library ubiquity; it is a '
                                  'domain-specific packing that mandates hierarchical HKDF labels, '
                                  'per-record AEAD plus signatures, and Merkle audit as '
                                  'first-class fields.',
                                  'A production realization could encode ECC-HISE semantics inside '
                                  'CMS attributes or as a profiled CBOR structure, preserving the '
                                  'security design while improving interoperability with existing '
                                  'PKI toolchains.']}]},
 {'heading': '5.4 Synthesis: Vulnerabilities and Research Contributions',
  'paragraphs': ['This section synthesizes findings from Sections 5.1 through 5.3, lists security '
                 'vulnerabilities present in existing e-banking and e-finance systems, and '
                 'identifies the issues addressed by this dissertation.'],
  'subsections': [{'heading': '5.4.1 Vulnerabilities in Existing Systems',
                   'paragraphs': ['V1 — Decoupled authentication layers: TLS encrypts channels '
                                  'without binding user identity to session keys, enabling session '
                                  'hijacking after token theft.',
                                  'V2 — Absence of device binding: Standard ECDH and TLS do not '
                                  'incorporate device fingerprints in key derivation.',
                                  'V3 — Bearer token semantics: OAuth and JWT sessions are '
                                  'transferable to any client possessing the token.',
                                  'V4 — Flat key hierarchies: Long-lived DEKs increase blast '
                                  'radius of key compromise.',
                                  'V5 — Transport-only integrity: mTLS and TLS do not protect data '
                                  'after termination.',
                                  'V6 — Audit friction: Manual reconciliation required without '
                                  'cryptographic batch proofs.',
                                  'V7 — Static PSK rotation gaps: Infrequent key rotation in '
                                  'inter-bank file transfer.',
                                  'V8 — Legacy TLS configurations: TLS 1.2 without forward secrecy '
                                  'in some deployments.'],
                   'table': {'headers': ['Vulnerability', 'Affected systems', 'Addressed by'],
                             'rows': [['V1 Decoupled auth', 'TLS + app login', 'ECC-DTB-AKA'],
                                      ['V2 No device bind', 'TLS, ECDH', 'ECC-DTB-AKA'],
                                      ['V3 Bearer tokens', 'OAuth, JWT', 'ECC-DTB-AKA (TBK HMAC)'],
                                      ['V4 Flat keys', 'TDE, file PSK', 'ECC-HISE hierarchy'],
                                      ['V5 Transport-only', 'mTLS, TLS', 'ECC-HISE envelope'],
                                      ['V6 Audit friction', 'SIEM, manual', 'ECC-HISE Merkle'],
                                      ['V7 Static PSK', 'PGP inter-bank', 'ECC-HISE per-batch SK'],
                                      ['V8 Legacy TLS', 'Older gateways', 'ECC-DTB-AKA fixed alg']],
                             'caption': 'Table 5.4: Vulnerabilities in existing e-banking systems '
                                        'and dissertation responses.'}},
                  {'heading': '5.4.2 Research Contributions',
                   'paragraphs': ['This dissertation makes the following original contributions to '
                                  'information security in e-banking and e-finance systems:',
                                  'C1 — ECC-DTB-AKA: A novel three-round ECC-based authenticated '
                                  'key agreement protocol with device fingerprint and transaction '
                                  'nonce binding in HKDF derivation, formally analyzed and '
                                  'quantitatively evaluated.',
                                  'C2 — ECC-HISE: A novel hierarchical secure envelope scheme with '
                                  'Merkle audit chains for server-server batch data transfer, '
                                  'providing confidentiality, integrity, and efficient audit '
                                  'verification.',
                                  'C3 — Dual-layer methodology: An integrated architecture '
                                  'combining client-server and server-server ECC-based security in '
                                  'a coherent e-financial service design.',
                                  'C4 — Prototype implementation: Working software demonstrating '
                                  'both schemes with REST APIs, benchmarks, and end-to-end '
                                  'integration tests.',
                                  'C5 — Quantitative evaluation: Empirical comparison with TLS '
                                  '1.3, ECDH, static PSK, and TLS record-layer baselines using '
                                  'reproducible benchmark suites.']},
                  {'heading': '5.4.3 Limitations and Future Work',
                   'paragraphs': ['Limitations include: software-based key storage (no HSM in '
                                  'prototype); proof sketches rather than machine-verified proofs; '
                                  'simplified certificate handling; single-process settlement '
                                  'demo. Future work: post-quantum algorithm integration (ML-KEM, '
                                  'ML-DSA); HSM deployment; formal verification in ProVerif or '
                                  'Tamarin; large-scale field trial with partner institution; '
                                  'meta-Merkle trees for million-record national settlement.']},
                  {'heading': '5.4.4 Alignment with Regulatory Requirements',
                   'paragraphs': ['PCI DSS Requirement 4 mandates strong cryptography for '
                                  'transmission; Requirement 3 for storage. PSD2 Strong Customer '
                                  'Authentication aligns with ECC-DTB-AKA mutual authentication. '
                                  'SWIFT CSP controls for integrity and non-repudiation align with '
                                  'ECC-HISE signed Merkle batch headers. The proposed schemes '
                                  'support compliance objectives while exceeding minimum baselines '
                                  'through integrated device binding and cryptographic audit.']},
                  {'heading': '5.4.5 Contribution Claims Revisited with Evidence Pointers',
                   'paragraphs': ['Contribution C1 (ECC-DTB-AKA design) is evidenced by Chapter '
                                  "2's protocol specification, security property sketches, and "
                                  'attack-resistance table. C2 (ECC-HISE design) is evidenced by '
                                  "Chapter 3's hierarchy, envelope algorithms, and audit proofs. "
                                  'C3 (dual-layer methodology) is evidenced by the architectural '
                                  'integration in Chapter 4 and the combined coverage matrix in '
                                  'this chapter. C4 (prototype and evaluation) is evidenced by '
                                  'benchmarks and implementation modules.',
                                  'These claims are bounded: proofs are sketches rather than '
                                  'machine-checked derivations; benchmarks are prototype-scale; '
                                  'user studies of fingerprint UX are future work. Stating bounds '
                                  'is part of scholarly contribution discipline and guides the '
                                  'future-work agenda.']},
                  {'heading': '5.4.6 Implications for Electronic Finance Security Practice',
                   'paragraphs': ['Practitioners can adopt ECC-DTB-AKA ideas incrementally: begin '
                                  'with transaction-bound HMAC tags under keys derived from '
                                  'existing TLS-PSK or app keys, then move to full ephemeral ECDH '
                                  'with device binding. ECC-HISE ideas can begin as Merkle '
                                  'manifests alongside existing encrypted files, then migrate to '
                                  "hierarchical keys. The dissertation's value for practice is a "
                                  'coherent blueprint rather than an all-or-nothing '
                                  'rip-and-replace.']},
                  {'heading': '5.4.7 Regulatory Mapping Sketch',
                   'paragraphs': ['At a high level, ECC-DTB-AKA supports SCA-style possession '
                                  'factors and reduces reliance on SMS OTP; ECC-HISE supports '
                                  'integrity and audit evidence expected under SWIFT CSP and '
                                  'internal governance for settlement systems. Detailed '
                                  'control-by-control mapping is institution-specific and left as '
                                  'future applied work; the dissertation supplies the '
                                  'cryptographic substrate such mappings require.']},
                  {'heading': '5.4.8 What Would Falsify the Contributions',
                   'paragraphs': ['Scholarly claims should be falsifiable. C1 would be weakened by '
                                  'a practical attack that forges ECC-DTB-AKA sessions without '
                                  'client keys or breaks binding so that TBK authorizes '
                                  'transactions unbound to txn_nonce under the stated adversary '
                                  'model. C2 would be weakened by undetectable batch mutations '
                                  'that preserve header signatures and Merkle roots, or by '
                                  'hierarchy collapses that derive SK_batch without DK_i under '
                                  'HKDF assumptions.',
                                  'C3 would be weakened if the layers interacted unsafely (e.g., '
                                  'settlement accepting client bearer tokens in lieu of '
                                  'envelopes). No such interaction is required by the '
                                  'architecture: the layers compose through ordinary business '
                                  'records, not through shared session secrets. Stating '
                                  'falsification criteria clarifies the evaluation burden for '
                                  'future work and examiners.']}]},
 {'heading': '5.5 Chapter Summary',
  'paragraphs': ['This chapter evaluated ECC-DTB-AKA and ECC-HISE against Chapter 1 attack '
                 'mechanisms, reviewed prior work on authentication/key exchange (Section 5.2) and '
                 'data encryption/integrity (Section 5.3), and synthesized eight identified '
                 'vulnerabilities with five research contributions. Quantitative results confirm '
                 'ECC-DTB-AKA achieves 0.52 ms authentication with superior security properties '
                 'over TLS and ECDH, and ECC-HISE provides audit-capable batch protection at 23.32 '
                 'ms per 100 records. The concluding remarks summarize contributions and outline '
                 'future research directions.'],
  'subsections': [{'heading': '5.5.1 Transition to Conclusions',
                   'paragraphs': ['The conclusions chapter consolidates the problem statement, '
                                  'dual-layer solution, empirical findings, limitations, and '
                                  'research outlook into a compact closing argument for the '
                                  'dissertation.']}]}]
