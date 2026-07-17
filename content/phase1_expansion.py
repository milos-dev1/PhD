"""Additional expansion paragraphs for Phase 1 to reach B5 page targets."""

PREFACE_EXPANSION = [
    {
        "heading": "Methodological Approach",
        "paragraphs": [
            "The research methodology employed in this dissertation follows a design-science research "
            "paradigm, which is well suited to information security investigations that aim to create "
            "and evaluate novel artifacts (in this case, cryptographic protocols and their software "
            "implementations) to solve identified organizational and technical problems. The methodology "
            "comprises five iterative phases: problem identification, solution design, prototype "
            "development, demonstration, and evaluation.",
            "In the problem identification phase (Chapter 1), we systematically catalog attack mechanisms "
            "and analyze limitations of existing authentication, key-exchange, and data-protection "
            "mechanisms in e-banking systems. The solution design phase (Chapters 2 and 3) produces "
            "formal protocol specifications for ECC-DTB-AKA and ECC-HISE, accompanied by security "
            "analysis and comparative evaluation against established baselines. The prototype development "
            "phase (Chapter 4) translates protocol specifications into working software modules using "
            "Python and the OpenSSL-backed cryptography library. The demonstration phase exercises the "
            "prototype through representative e-banking scenarios including customer login, fund transfer, "
            "and inter-bank settlement batch processing. The evaluation phase (Chapter 5) measures "
            "quantitative performance metrics and assesses qualitative security properties against the "
            "threat model defined in Section 1.4.",
            "Elliptic curve cryptography is selected as the foundational primitive for both proposed "
            "schemes based on three criteria: (1) security efficiency — ECC P-256 provides approximately "
            "128 bits of security with a 256-bit key, compared to 3072-bit RSA keys for equivalent "
            "strength; (2) industry adoption — ECC is mandated or recommended by NIST, EMV, FIDO2, "
            "and TLS 1.3 specifications; and (3) implementation maturity — production-grade open-source "
            "libraries (OpenSSL, libsodium, Python cryptography) provide audited implementations of "
            "ECDH, ECDSA, and Ed25519 on standard curves.",
        ],
    },
    {
        "heading": "Structure of the E-Financial Service System",
        "paragraphs": [
            "Throughout this dissertation, we reference a conceptual e-financial service system that "
            "serves as the deployment context for the proposed security schemes. This system comprises "
            "four logical tiers: the client tier, the application tier, the settlement tier, and the "
            "governance tier.",
            "The client tier includes mobile banking applications, web browsers, and ATM terminals "
            "that customers use to access financial services. Clients communicate with the application "
            "tier over public networks (the Internet) and must authenticate themselves and establish "
            "encrypted sessions before performing transactions. The ECC-DTB-AKA protocol operates "
            "primarily in this tier, securing the client-server channel.",
            "The application tier consists of API gateways, authentication services, account management "
            "services, and transaction processing engines. These components are deployed as "
            "containerized microservices behind load balancers, with mutual TLS providing transport "
            "security between services. Application-tier services validate customer requests, enforce "
            "business rules, and initiate settlement operations.",
            "The settlement tier handles inter-bank and intra-bank batch processing, including "
            "end-of-day reconciliation, regulatory reporting, and payment clearing. Data transferred "
            "between settlement servers at different institutions requires confidentiality, integrity, "
            "and auditability beyond what transport-layer security alone provides. The ECC-HISE scheme "
            "operates in this tier, protecting batch data with hierarchical keys and Merkle audit chains.",
            "The governance tier encompasses certificate authorities, hardware security modules, "
            "security operations centers, and regulatory reporting interfaces. The clearing-house "
            "authority manages the master key for ECC-HISE's hierarchical key derivation, while the "
            "bank's internal CA issues certificates used in ECC-DTB-AKA server authentication.",
        ],
    },
]

CHAPTER01_EXPANSION = [
    {
        "parent_section": "1.1 Attack Mechanisms in E-Banking and E-Finance Services",
        "subsections": [
            {
                "heading": "1.1.5 Detailed Analysis of Selected Attack Vectors",
                "paragraphs": [
                    "To provide depth beyond the taxonomy presented in Section 1.1.1, this subsection "
                    "examines three high-impact attack vectors in detail: man-in-the-middle attacks on "
                    "banking sessions, session hijacking via token theft, and advanced persistent threats "
                    "(APTs) targeting financial infrastructure.",
                    "Man-in-the-middle (MITM) attacks on banking sessions exploit the fact that users "
                    "often cannot distinguish legitimate bank servers from impersonating proxies. In a "
                    "typical MITM scenario, the attacker positions a proxy between the client and the "
                    "bank server. If the client does not validate the server's certificate chain "
                    "correctly—or if the attacker has compromised a trusted CA or uses a corporate "
                    "SSL-inspection proxy—the attacker can decrypt, inspect, and modify transaction "
                    "data in real time. Tools such as mitmproxy and Burp Suite, while designed for "
                    "legitimate security testing, demonstrate the feasibility of this attack class. "
                    "Banking trojans such as Zeus and Emotet have historically automated MITM against "
                    "banking websites by injecting fraudulent transaction fields into otherwise "
                    "legitimate sessions, redirecting wire transfers to attacker-controlled accounts "
                    "without altering the confirmation screen displayed to the user.",
                    "Session hijacking via token theft represents a distinct but related threat. After "
                    "successful authentication, the banking application issues a session token (cookie "
                    "or bearer token) that the client presents with each subsequent request. If an "
                    "attacker obtains this token—through XSS, malware memory scraping, or network "
                    "sniffing on unencrypted channels—the attacker can impersonate the victim without "
                    "knowing their password or MFA code. The OWASP Session Management Cheat Sheet "
                    "recommends token rotation, binding tokens to client IP addresses, and using "
                    "HttpOnly/Secure cookie flags, but these mitigations are not universally implemented "
                    "and do not provide cryptographic binding between the token and the underlying "
                    "key-exchange material.",
                    "Advanced persistent threats (APTs) targeting financial infrastructure operate "
                    "over extended time periods (weeks to months), maintaining covert access to bank "
                    "networks while exfiltrating data or preparing fraudulent transactions. APT groups "
                    "such as Carbanak (also known as FIN7) and Lazarus Group have demonstrated the "
                    "ability to compromise bank internal networks, learn internal transaction workflows, "
                    "and execute fraudulent transfers through the same channels used by legitimate "
                    "operators. APT attacks often begin with spear-phishing emails containing weaponized "
                    "documents, progress through lateral movement using stolen credentials, and culminate "
                    "in access to SWIFT terminals or core banking systems. The Bangladesh Bank heist "
                    "exemplifies an APT-style operation against financial infrastructure.",
                ],
            },
        ],
    },
    {
        "parent_section": "1.2 Authentication and Key Exchange in E-Banking Systems",
        "subsections": [
            {
                "heading": "1.2.4 Elliptic Curve Cryptography in Financial Authentication",
                "paragraphs": [
                    "Elliptic curve cryptography has become the preferred public-key primitive for "
                    "new financial authentication deployments. Understanding its role in current systems "
                    "is essential context for the novel schemes proposed in Chapters 2 and 3.",
                    "An elliptic curve E over a finite field F_p is the set of points (x, y) satisfying "
                    "the Weierstrass equation y² = x³ + ax + b (mod p), together with a point at "
                    "infinity forming an abelian group. Cryptographic security relies on the hardness "
                    "of the elliptic curve discrete logarithm problem (ECDLP): given points P and Q = [k]P, "
                    "find scalar k. For properly chosen curves with sufficiently large prime subgroups, "
                    "the best known algorithms require exponential time, providing security proportional "
                    "to half the bit length of the subgroup order.",
                    "In TLS 1.3, the default key-exchange mechanism is ECDHE (Elliptic Curve Diffie-Hellman "
                    "Ephemeral), using curves X25519 or P-256. The ephemeral nature of ECDHE provides "
                    "forward secrecy: compromise of the server's long-term private key does not enable "
                    "decryption of previously recorded sessions. EMV chip cards use ECDSA on curve "
                    "secp256r1 for offline and online transaction authentication. FIDO2/WebAuthn employs "
                    "ECDSA or Ed25519 for credential key pairs stored in hardware authenticators.",
                    "Despite widespread ECC adoption, current deployments use ECC primarily for "
                    "individual cryptographic operations (key agreement, signing) rather than as an "
                    "integrated methodology binding authentication, key exchange, device context, and "
                    "transaction scope. The ECC-DTB-AKA scheme proposed in Chapter 2 extends ECC key "
                    "agreement with additional binding inputs (device fingerprint, transaction nonce) "
                    "in the HKDF derivation, creating a cohesive protocol rather than a stack of "
                    "independent cryptographic layers.",
                ],
            },
            {
                "heading": "1.2.5 Comparative Overview of Authentication Protocols",
                "paragraphs": [
                    "Table 1.4 provides a comparative overview of authentication and key-exchange "
                    "protocols commonly used in e-banking systems, highlighting properties relevant to "
                    "the limitations identified in Section 1.2.3.",
                    "TLS 1.3 full handshake provides server authentication and forward-secure key "
                    "agreement in one round trip but does not authenticate the user at the cryptographic "
                    "layer. OAuth 2.0 with PKCE adds authorization delegation for third-party API access "
                    "but relies on bearer tokens vulnerable to theft. FIDO2 provides phishing-resistant "
                    "user authentication but does not integrate with key-exchange derivation. Kerberos "
                    "with PKINIT (public-key initialization) supports mutual authentication in enterprise "
                    "environments but is rarely deployed in retail e-banking client-server channels.",
                    "None of these protocols simultaneously achieves: (a) mutual authentication at "
                    "the cryptographic layer, (b) device binding in key derivation, (c) per-transaction "
                    "key derivation without additional round trips, and (d) three-round handshake "
                    "efficiency. This gap is the design target for ECC-DTB-AKA.",
                ],
                "table": {
                    "headers": ["Protocol", "Mutual Auth", "Forward Secrecy", "Device Bind", "Per-Txn Key", "Rounds"],
                    "rows": [
                        ["TLS 1.3", "Server only", "Yes", "No", "No", "1"],
                        ["OAuth 2.0 PKCE", "Delegated", "Via TLS", "No", "No", "3+"],
                        ["FIDO2/WebAuthn", "User auth", "N/A", "Partial", "No", "2"],
                        ["ECDH + JWT", "App layer", "Yes", "No", "No", "2"],
                        ["ECC-DTB-AKA (Ch.2)", "Yes", "Yes", "Yes", "Yes", "3"],
                    ],
                    "caption": "Table 1.4: Comparative overview of authentication protocols for e-banking.",
                },
            },
        ],
    },
    {
        "parent_section": "1.3 Data Encryption, Security, and Integrity in E-Banking",
        "subsections": [
            {
                "heading": "1.3.4 Key Management in Financial Institutions",
                "paragraphs": [
                    "Effective data encryption in e-banking depends critically on key management—the "
                    "generation, distribution, storage, rotation, and destruction of cryptographic keys. "
                    "Poor key management can render even the strongest encryption algorithms ineffective, "
                    "as demonstrated by numerous breaches where encryption was deployed but keys were "
                    "stored alongside encrypted data in accessible locations.",
                    "Financial institutions typically employ a tiered key-management architecture. At the "
                    "top level, master keys are generated within FIPS 140-2 Level 3 (or higher) hardware "
                    "security modules and never leave the HSM in plaintext form. Key-encryption keys (KEKs) "
                    "wrap data-encryption keys (DEKs) for distribution to application servers. DEKs "
                    "encrypt actual customer data and are rotated frequently (daily to monthly) depending "
                    "on data classification and regulatory requirements.",
                    "The ANSI X9.24-3 standard specifies key-management requirements for symmetric "
                    "keys in financial services, including dual-control procedures for key generation "
                    "and split-knowledge requirements for critical keys. PCI DSS Requirement 3 mandates "
                    "protection of stored cardholder data, including key-management procedures for "
                    "encryption keys. However, these standards focus on symmetric key hierarchies and "
                    "do not address ECC-based hierarchical derivation for batch envelope encryption "
                    "with integrated audit chains—the design space targeted by ECC-HISE.",
                ],
            },
            {
                "heading": "1.3.5 Merkle Trees and Cryptographic Audit Trails",
                "paragraphs": [
                    "Merkle trees (hash trees) provide an efficient data structure for verifying "
                    "integrity of large datasets. A Merkle tree is a binary tree in which each leaf "
                    "node contains the hash of a data block, and each internal node contains the hash "
                    "of the concatenation of its children. The root hash commits to the entire dataset: "
                    "any modification to any leaf changes the root hash. A verifier can confirm "
                    "inclusion of a specific record with O(log n) hash computations given an "
                    "authentication path (Merkle proof) from the leaf to the root.",
                    "In e-banking settlement, Merkle trees enable regulators and counterparties to "
                    "verify that a specific transaction was included in a batch settlement without "
                    "reprocessing the entire batch. Combined with digital signatures on the Merkle "
                    "root, the tree provides both integrity and non-repudiation at the batch level. "
                    "Bitcoin and other blockchains use Merkle trees in block headers for similar "
                    "reasons, though blockchain consensus introduces latency unsuitable for real-time "
                    "settlement. ECC-HISE adopts Merkle trees for audit without requiring distributed "
                    "consensus, making it applicable to traditional inter-bank settlement workflows.",
                    "The integration of Merkle audit chains with ECC-based envelope encryption—rather "
                    "than treating encryption and audit as separate subsystems—constitutes a key "
                    "differentiator of the ECC-HISE approach developed in Chapter 3. By including the "
                    "Merkle root in the signed batch header, any tampering with individual records is "
                    "detectable through root mismatch, while the hierarchical key structure limits "
                    "the scope of key compromise to individual batches within specific business domains.",
                ],
            },
        ],
    },
]

# Additional narrative blocks appended to key sections for page depth
PREFACE_DEEP = {
    "heading": "E-Banking in the Global Context",
    "paragraphs": [
        "The global e-banking landscape exhibits significant regional variation in technology adoption, "
        "regulatory frameworks, and security postures. In Scandinavia, nearly 100% of banking customers "
        "use digital channels, with mobile payment systems such as Swish and MobilePay achieving "
        "near-universal adoption. Strong government digital identity infrastructure (BankID in Sweden "
        "and Norway, NemID/MitID in Denmark) provides a foundation for cryptographic authentication "
        "that exceeds the security of username-password systems common in other regions.",
        "In East Asia, super-app ecosystems integrate banking, payments, social media, and e-commerce "
        "into single platforms (WeChat Pay, Alipay, LINE Pay). These platforms process transaction "
        "volumes exceeding those of entire countries' GDP, creating unique scalability and security "
        "challenges. QR-code-based payment authentication, while convenient, has been targeted by "
        "attackers who replace legitimate merchant QR codes with fraudulent ones—a threat vector that "
        "requires binding payment authorization to verified merchant identity.",
        "In Africa, mobile money services (M-Pesa, MTN Mobile Money) have brought banking to "
        "underbanked populations through feature phones and SMS-based interfaces. The security models "
        "for these systems often rely on SIM-card identity and PIN codes, making them vulnerable to "
        "SIM-swapping attacks that have resulted in significant financial losses. The ECC-DTB-AKA "
        "scheme's device-binding property is particularly relevant in markets where SIM-based identity "
        "is the primary authentication factor.",
        "In North America and Western Europe, open-banking initiatives are reshaping the competitive "
        "landscape by requiring banks to expose APIs to licensed third-party providers. This "
        "architectural shift multiplies the number of authentication and authorization endpoints, "
        "each requiring robust protection. The server-server security requirements for inter-institutional "
        "data exchange—addressed by ECC-HISE—become increasingly critical as payment initiation flows "
        "traverse multiple service providers before reaching the customer's bank.",
    ],
}

CHAPTER01_DEEP = [
    {
        "parent_section": "1.4 Threat Model, Assumptions, and Research Questions",
        "subsections": [
            {
                "heading": "1.4.5 Security Requirements Derivation",
                "paragraphs": [
                    "From the threat model (Section 1.4.1) and the identified limitations (Sections "
                    "1.2.3 and 1.3.3), we derive the following security requirements that the proposed "
                    "schemes must satisfy. These requirements serve as evaluation criteria in Chapter 5.",
                    "SR1 (Mutual Authentication): Both communicating parties must cryptographically "
                    "verify each other's identity before any financial data is exchanged. For "
                    "client-server channels, this means the client verifies the bank server's identity "
                    "via certificate chain, and the server verifies the client's identity via registered "
                    "public key signature.",
                    "SR2 (Forward Secrecy): Compromise of long-term private keys must not enable "
                    "decryption of previously recorded sessions. Ephemeral ECDH key pairs must be used "
                    "for session key establishment.",
                    "SR3 (Device Binding): Session keys must be cryptographically bound to the "
                    "client device, preventing session transfer to unauthorized devices even if "
                    "session tokens are exfiltrated.",
                    "SR4 (Transaction Binding): Individual transactions must be protected by keys "
                    "derived specifically for that transaction, limiting the impact of single-transaction "
                    "key compromise.",
                    "SR5 (Data Confidentiality): Financial records in server-server batch transfer "
                    "must be encrypted with semantically secure authenticated encryption.",
                    "SR6 (Data Integrity): Any modification to batch records must be detectable "
                    "through cryptographic verification, with batch-level integrity proofs enabling "
                    "efficient audit.",
                    "SR7 (Non-Repudiation): Batch senders must not be able to deny having sent a "
                    "batch, achieved through digital signatures on batch headers.",
                    "SR8 (Efficiency): Authentication must complete within acceptable latency bounds "
                    "(target: under 200ms on commodity hardware) with minimal communication overhead.",
                ],
            },
            {
                "heading": "1.4.6 Relationship to Subsequent Chapters",
                "paragraphs": [
                    "The security requirements SR1 through SR4 are addressed primarily by the "
                    "ECC-DTB-AKA protocol developed in Chapter 2. Requirements SR5 through SR7 are "
                    "addressed by the ECC-HISE scheme developed in Chapter 3. Requirement SR8 is "
                    "evaluated quantitatively in Chapters 2, 3, and 5 through benchmark measurements "
                    "of the prototype described in Chapter 4.",
                    "Chapter 5 provides the comprehensive prior-work analysis specified in the "
                    "dissertation requirements: Section 5.2 reviews authentication and key-exchange "
                    "literature in depth (expanding on the overview in Section 1.2), Section 5.3 "
                    "reviews data encryption and integrity literature (expanding on Section 1.3), "
                    "and Section 5.4 synthesizes findings to demonstrate how the proposed schemes "
                    "address the vulnerabilities cataloged in this chapter.",
                    "Readers approaching this dissertation from a practitioner perspective may wish "
                    "to read Section 1.1 and Sections 1.2.3/1.3.3 first to understand the threat "
                    "landscape and identified gaps, then proceed to Chapters 2 and 3 for protocol "
                    "specifications, and Chapter 4 for implementation guidance. Readers with a "
                    "research orientation may prefer to read Chapter 5's prior-work analysis before "
                    "the proposed schemes, to situate the contributions within the existing literature.",
                ],
            },
        ],
    },
]
