"""Second expansion pass for Phase 1 page depth."""

EXTRA_PREFACE = [
    {
        "heading": "Notation and Conventions",
        "paragraphs": [
            "Throughout this dissertation, the following notation and typographic conventions are "
            "employed unless otherwise stated. Scalar values and binary strings are denoted in "
            "lowercase italic (e.g., k, nonce). Group elements on elliptic curves are denoted in "
            "uppercase italic (e.g., P, Q, G). Functions and algorithms are denoted in upright "
            "font (e.g., H, HKDF, ECDH). Sets are denoted in calligraphic or blackboard-bold font "
            "(e.g., Z_q for integers modulo q).",
            "The symbol || denotes concatenation of bit strings. The symbol ← denotes uniform "
            "random sampling from a set. The symbol → denotes deterministic output of a function. "
            "A →_P B indicates that entity A sends message to entity B over protocol P. "
            "Security parameters are expressed in bits (e.g., 128-bit security, 256-bit key).",
            "Chapter and section references use decimal notation (e.g., Section 1.2.3). Figure and "
            "table references use chapter-qualified numbering (e.g., Figure 1.2, Table 1.3). "
            "Algorithm pseudocode is presented in numbered blocks in the appendix and referenced "
            "from the main text. All cryptographic algorithms use well-established standards: "
            "SHA-256 per FIPS 180-4, HKDF per RFC 5869, AES-256-GCM per NIST SP 800-38D, "
            "ECDSA per FIPS 186-5, and Ed25519 per RFC 8032.",
        ],
    },
]

EXTRA_CHAPTER01 = [
    {
        "parent_section": "1.1 Attack Mechanisms in E-Banking and E-Finance Services",
        "subsections": [
            {
                "heading": "1.1.6 Impact Assessment Framework",
                "paragraphs": [
                    "Assessing the impact of attacks on e-banking systems requires a multidimensional "
                    "framework that goes beyond simple financial loss figures. We adopt a framework "
                    "with four impact dimensions: financial, operational, reputational, and regulatory.",
                    "Financial impact encompasses direct losses (fraudulent transfers, ransom payments), "
                    "indirect losses (customer compensation, legal fees), and recovery costs (forensic "
                    "investigation, system restoration). The Ponemon Institute and IBM jointly publish "
                    "annual cost-of-breach figures; for financial services in 2024, the average total "
                    "cost was $5.9 million per breach, with an average of 258 days to identify and "
                    "contain the breach.",
                    "Operational impact includes service downtime, degraded performance during attacks, "
                    "and diversion of IT resources from planned projects to incident response. A DDoS "
                    "attack against a major bank's online banking portal can prevent millions of "
                    "customers from accessing services for hours, generating call-center surges and "
                    "transaction backlogs. The operational resilience requirements of the Bank of "
                    "England and the European Central Bank mandate maximum tolerable downtime thresholds "
                    "for critical payment systems.",
                    "Reputational impact manifests as customer attrition, negative media coverage, and "
                    "reduced stock valuation. Studies indicate that publicly traded banks experience "
                    "an average stock price decline of 5–7% in the week following a major breach "
                    "announcement, with partial recovery over subsequent months. Customer trust, once "
                    "eroded, requires sustained investment in transparency and security improvements "
                    "to rebuild.",
                    "Regulatory impact includes fines, consent orders, and increased supervisory "
                    "scrutiny. The GDPR permits fines up to 4% of global annual revenue for serious "
                    "data protection violations. The U.S. Office of the Comptroller of the Currency (OCC) "
                    "and the Federal Reserve have issued consent orders against banks with deficient "
                    "cybersecurity programs, requiring multi-year remediation plans and independent "
                    "third-party assessments.",
                ],
            },
        ],
    },
    {
        "parent_section": "1.2 Authentication and Key Exchange in E-Banking Systems",
        "subsections": [
            {
                "heading": "1.2.6 Password-Based Authentication Vulnerabilities",
                "paragraphs": [
                    "Despite decades of security guidance, password-based authentication remains the "
                    "default for retail e-banking in most jurisdictions. Understanding its inherent "
                    "vulnerabilities is essential for motivating cryptographic alternatives.",
                    "Human-chosen passwords exhibit highly skewed distributions. Analysis of breached "
                    "password databases consistently shows that the top 100 passwords account for "
                    "approximately 17% of all passwords, with '123456', 'password', and 'qwerty' "
                    "appearing in virtually every corpus. Password complexity rules (requiring uppercase, "
                    "numbers, symbols) often result in predictable substitutions (P@ssw0rd) that "
                    "provide minimal additional entropy.",
                    "Password hashing algorithms mitigate offline attacks against stolen databases. "
                    "Bcrypt, scrypt, and Argon2 are designed to be computationally expensive, limiting "
                    "the rate at which attackers can test guessed passwords. However, weak passwords "
                    "remain vulnerable even with strong hashing, and credential stuffing attacks "
                    "bypass hashing entirely by testing leaked credentials from other breaches against "
                    "banking login portals.",
                    "Password reset mechanisms introduce additional attack surfaces. Knowledge-based "
                    "authentication questions (mother's maiden name, first pet) are often guessable from "
                    "social media. Email-based reset links can be intercepted if the email account "
                    "is compromised. SMS-based reset codes inherit SIM-swapping vulnerabilities. "
                    "These weaknesses reinforce the need for cryptographic authentication mechanisms "
                    "that do not rely solely on shared secrets memorized by humans.",
                ],
            },
        ],
    },
    {
        "parent_section": "1.3 Data Encryption, Security, and Integrity in E-Banking",
        "subsections": [
            {
                "heading": "1.3.6 Homomorphic Encryption and Emerging Approaches",
                "paragraphs": [
                    "While not part of the proposed schemes in this dissertation, emerging cryptographic "
                    "technologies warrant brief discussion to situate the research within the broader "
                    "landscape of financial data protection.",
                    "Fully homomorphic encryption (FHE) enables computation on encrypted data without "
                    "decryption, potentially allowing banks to perform fraud detection on encrypted "
                    "transaction streams. However, FHE remains orders of magnitude slower than plaintext "
                    "computation and is not yet practical for real-time e-banking workloads. Partial "
                    "homomorphic schemes (Paillier, ElGamal) support specific operations (addition, "
                    "multiplication) and have been piloted for privacy-preserving credit scoring.",
                    "Confidential computing (Intel SGX, AMD SEV, ARM TrustZone) provides hardware-enforced "
                    "memory isolation for applications processing sensitive data. Major cloud providers "
                    "offer confidential virtual machines for financial workloads. These technologies "
                    "address the 'data in use' protection gap identified in Section 1.3.1 but require "
                    "trust in hardware manufacturers and are vulnerable to side-channel attacks.",
                    "The schemes proposed in this dissertation (ECC-DTB-AKA and ECC-HISE) complement "
                    "rather than replace these emerging approaches. ECC-DTB-AKA secures the "
                    "client-server channel; ECC-HISE secures server-server batch data; confidential "
                    "computing can protect in-memory processing; and post-quantum algorithms will "
                    "eventually replace specific ECC primitives as standards mature.",
                ],
            },
        ],
    },
]
