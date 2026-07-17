"""Preface content for the PhD thesis."""

TITLE = "Preface"

SECTIONS = [
    {
        "heading": "Background and Motivation",
        "paragraphs": [
            "Electronic banking and electronic finance service systems have undergone a profound transformation "
            "over the past three decades. What began in the 1980s as rudimentary home-banking terminals "
            "connected via dial-up modems has evolved into a globally interconnected ecosystem comprising "
            "mobile banking applications, real-time payment rails, open-banking APIs, cryptocurrency "
            "custody services, and algorithmic trading platforms. According to industry reports, more than "
            "three billion individuals worldwide now access financial services through digital channels, and "
            "the volume of electronic payment transactions exceeds one trillion events annually. This "
            "digitization has delivered unprecedented convenience, financial inclusion, and operational "
            "efficiency, yet it has simultaneously expanded the attack surface available to adversaries "
            "ranging from opportunistic cybercriminals to sophisticated nation-state actors.",
            "The security of e-banking and e-finance systems is not merely a technical concern; it is a "
            "foundational requirement for economic stability and public trust. A single successful breach "
            "can result in direct financial losses measured in hundreds of millions of dollars, regulatory "
            "penalties, reputational damage that persists for years, and erosion of confidence in the "
            "broader financial system. High-profile incidents—including the 2016 Bangladesh Bank heist "
            "involving fraudulent SWIFT messages, the 2017 Equifax data breach affecting 147 million "
            "consumers, and numerous credential-stuffing campaigns targeting retail banking portals—"
            "demonstrate that existing security architectures, despite decades of investment, remain "
            "vulnerable to both novel and well-known attack vectors.",
            "Cryptography serves as the bedrock upon which e-banking security is built. From the SSL/TLS "
            "protocols that protect data in transit, to the EMV chip-and-PIN standards governing card "
            "present transactions, to the hardware security modules (HSMs) safeguarding root keys in "
            "data centers, cryptographic mechanisms are deeply embedded in every layer of the financial "
            "technology stack. Among the cryptographic primitives available today, elliptic curve "
            "cryptography (ECC) has emerged as the dominant choice for new deployments due to its favorable "
            "security-to-key-size ratio: a 256-bit elliptic curve key provides security comparable to a "
            "3072-bit RSA key, resulting in lower computational overhead, reduced bandwidth consumption, "
            "and improved performance on resource-constrained devices such as smartphones and IoT terminals.",
            "This dissertation addresses a critical gap at the intersection of ECC-based authentication, "
            "key exchange, and data protection in e-banking environments. While substantial prior research "
            "has investigated individual aspects of financial system security—ranging from multi-factor "
            "authentication protocols to blockchain-based audit trails—few works have proposed integrated "
            "methodologies that simultaneously strengthen client-server authentication channels and "
            "server-server data-transfer channels using coherent ECC-based designs, accompanied by "
            "rigorous analysis, quantitative evaluation, and practical implementation. The research presented "
            "herein aims to fill this gap by proposing, analyzing, implementing, and evaluating two novel "
            "schemes: ECC-DTB-AKA (Device- and Transaction-Bound Authenticated Key Agreement) and "
            "ECC-HISE (Hierarchical Integrity-preserving Secure Envelope).",
        ],
    },
    {
        "heading": "Development and Future Prospects of E-Banking and E-Finance",
        "paragraphs": [
            "The historical trajectory of electronic banking can be divided into four distinct generations. "
            "The first generation (1980s–1990s) featured proprietary dial-up systems with limited "
            "functionality, primarily balance inquiry and fund transfers between accounts at the same "
            "institution. The second generation (late 1990s–2000s) coincided with the commercialization "
            "of the World Wide Web, giving rise to internet banking portals protected by SSL/TLS and "
            "username-password authentication. The third generation (2010s) was driven by smartphone "
            "adoption, introducing mobile banking applications, biometric authentication, push "
            "notifications for transaction verification, and near-field communication (NFC) payments. "
            "We are now entering the fourth generation, characterized by open banking regulations "
            "(such as the European PSD2 directive and similar frameworks in the United Kingdom, Australia, "
            "and Brazil), real-time gross settlement (RTGS) systems operating 24/7, central bank digital "
            "currencies (CBDCs), and decentralized finance (DeFi) protocols that challenge traditional "
            "intermediation models.",
            "Several technological trends will shape the future of e-finance services and, by extension, "
            "the security requirements that must be satisfied. First, the proliferation of application "
            "programming interfaces (APIs) under open-banking mandates creates new client-server and "
            "server-server communication patterns in which third-party providers access customer account "
            "data and initiate payments on behalf of users. Each API endpoint represents a potential "
            "entry point for attackers, necessitating robust authentication and fine-grained authorization "
            "mechanisms. Second, the migration of banking workloads to cloud infrastructure introduces "
            "shared-responsibility security models in which traditional network perimeters dissolve and "
            "identity becomes the primary security boundary. Third, the increasing use of artificial "
            "intelligence and machine learning in fraud detection, credit scoring, and customer service "
            "creates new categories of adversarial attacks, including model poisoning and inference attacks "
            "on sensitive training data.",
            "Quantum computing poses a longer-term but strategically significant threat to current "
            "cryptographic infrastructure. Although cryptographically relevant quantum computers have not "
            "yet materialized, financial institutions with multi-decade data confidentiality requirements "
            "must begin planning for post-quantum migration. The U.S. National Institute of Standards and "
            "Technology (NIST) has standardized post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA), and "
            "regulatory bodies are expected to issue timelines for transition. The ECC-based schemes "
            "proposed in this dissertation are designed with algorithm agility in mind, enabling future "
            "replacement of specific primitives without altering the overall protocol architecture.",
            "Looking ahead, e-finance service systems will likely converge toward a hybrid architecture "
            "combining centralized trust anchors (banks, clearing houses, regulators) with distributed "
            "ledger technologies for settlement and audit. Security systems must evolve to protect not "
            "only traditional account-based transactions but also tokenized assets, smart-contract "
            "interactions, and cross-border payment corridors operating across heterogeneous regulatory "
            "jurisdictions. The methodologies developed in this thesis provide a foundation that can be "
            "extended to these emerging paradigms.",
        ],
    },
    {
        "heading": "The Importance of Security Systems in E-Banking and E-Finance",
        "paragraphs": [
            "Information security in electronic finance is commonly analyzed through the CIA triad "
            "(Confidentiality, Integrity, Availability) supplemented by authenticity, non-repudiation, "
            "and accountability. Each property carries particular significance in the banking domain.",
            "Confidentiality ensures that sensitive financial data—including account balances, transaction "
            "histories, personal identification information, and cryptographic keys—remains accessible only "
            "to authorized parties. Breaches of confidentiality can facilitate identity theft, targeted "
            "phishing, and insider trading. In e-banking systems, confidentiality must be maintained "
            "across multiple states: data at rest (stored in databases and backup systems), data in transit "
            "(moving across networks between clients, servers, and partner institutions), and data in use "
            "(being processed in memory during transaction authorization).",
            "Integrity guarantees that financial records and transaction messages have not been altered "
            "without detection. The integrity requirement is especially stringent in inter-bank settlement, "
            "where a modification to a single field in a payment instruction can redirect millions of dollars "
            "to an attacker-controlled account. Cryptographic mechanisms such as message authentication "
            "codes (MACs), digital signatures, and hash chains provide integrity protection, but their "
            "effectiveness depends on correct key management and comprehensive coverage of all data paths.",
            "Availability ensures that banking services remain accessible to legitimate users when needed. "
            "Distributed denial-of-service (DDoS) attacks against banking infrastructure have become "
            "increasingly common, with some attacks exceeding one terabit per second in traffic volume. "
            "While availability is often treated separately from cryptographic security, the two concerns "
            "intersect when authentication protocols are designed to resist resource-exhaustion attacks "
            "and when rate-limiting mechanisms must not inadvertently lock out legitimate customers.",
            "Authenticity and non-repudiation are particularly critical in financial contexts where "
            "disputes over transaction authorization arise frequently. A customer may claim that a wire "
            "transfer was unauthorized, while the bank asserts that valid credentials were presented. "
            "Strong mutual authentication protocols and digital signatures with long-term verifiability "
            "provide evidentiary support in such disputes. Regulatory frameworks including the Payment "
            "Card Industry Data Security Standard (PCI DSS), the Sarbanes-Oxley Act, and the General Data "
            "Protection Regulation (GDPR) impose legal obligations that translate directly into technical "
            "security requirements.",
            "The defense-in-depth principle dictates that no single security control should constitute a "
            "single point of failure. E-banking systems typically deploy firewalls, intrusion detection "
            "systems, security information and event management (SIEM) platforms, multi-factor "
            "authentication, encryption, and physical security for data centers in layered combination. "
            "However, the cryptographic layer—the focus of this dissertation—remains the ultimate guarantor "
            "of confidentiality and integrity when all other layers have been bypassed.",
        ],
    },
    {
        "heading": "Research Objectives and Scope",
        "paragraphs": [
            "The primary objective of this research is to design, analyze, implement, and evaluate novel "
            "ECC-based security schemes that address documented vulnerabilities in contemporary e-banking "
            "and e-finance systems. Specifically, the research pursues the following goals:",
            "First, to systematically catalog and analyze attack mechanisms currently deployed against "
            "e-banking and e-finance services, establishing a threat landscape that motivates the proposed "
            "countermeasures (Chapter 1). Second, to propose ECC-DTB-AKA, a device- and transaction-bound "
            "authenticated key agreement protocol for client-server channels, and to demonstrate its "
            "superiority over existing approaches in terms of security properties, communication efficiency, "
            "and computational overhead (Chapter 2). Third, to propose ECC-HISE, a hierarchical "
            "integrity-preserving secure envelope scheme for server-server data transfer, addressing "
            "limitations in current encryption and audit mechanisms (Chapter 3). Fourth, to implement both "
            "schemes in a working software prototype and to describe the security system architecture of "
            "an e-financial service system that integrates them (Chapter 4). Fifth, to conduct a "
            "comprehensive evaluation including review of prior work, quantitative performance comparison, "
            "and analysis of resistance to the attacks identified in Chapter 1 (Chapter 5).",
            "The scope of this dissertation is deliberately focused on the cryptographic and protocol "
            "layers of e-banking security. Physical security, social engineering, organizational policy, "
            "and regulatory compliance are acknowledged as important but are not the primary subject of "
            "investigation. The implementation prototype uses software-based key storage rather than "
            "hardware security modules, and the formal security proofs are presented as structured proof "
            "sketches rather than machine-verified derivations. These limitations are discussed frankly "
            "in the conclusions.",
        ],
    },
    {
        "heading": "Summary of Chapters",
        "paragraphs": [
            "Chapter 1 establishes the foundation of this dissertation by defining and categorizing "
            "attack mechanisms currently used against e-banking and e-finance services, including phishing, "
            "man-in-the-middle attacks, replay attacks, session hijacking, credential stuffing, and "
            "insider threats. The chapter presents real-world case studies illustrating the impact of "
            "successful attacks, reviews the current state of authentication and key-exchange mechanisms "
            "(Section 1.2) and data encryption and integrity mechanisms (Section 1.3), and identifies "
            "their respective limitations. Section 1.4 formalizes the threat model, system assumptions, "
            "and research questions that guide the subsequent chapters.",
            "Chapter 2 presents the first proposed methodology: ECC-DTB-AKA. This chapter describes an "
            "alternative approach to strengthening client-server security in e-banking systems through "
            "a novel authenticated key agreement protocol that binds session keys to device fingerprints "
            "and transaction nonces. The chapter includes detailed algorithmic descriptions, protocol "
            "flowcharts, a formal security analysis, and quantitative evaluation comparing ECC-DTB-AKA "
            "against TLS 1.3, standard ECDH, and OAuth 2.0 PKCE in terms of authentication latency, "
            "message overhead, and communication round trips.",
            "Chapter 3 presents the second proposed methodology: ECC-HISE. Taking a fundamentally "
            "different approach from Chapter 2, this chapter addresses server-server data protection "
            "through a hierarchical key management scheme combined with authenticated encryption and "
            "Merkle-tree audit chains. The scheme overcomes drawbacks of prior data-security approaches "
            "identified in Section 1.3, and the chapter provides algorithmic specifications, architectural "
            "diagrams, and effectiveness analysis.",
            "Chapter 4 describes the practical application of both proposed schemes. Section 4.1 presents "
            "the security system architecture of an e-financial service system integrating ECC-DTB-AKA "
            "and ECC-HISE. Sections 4.2 and 4.3 detail the programmatic implementation of the Chapter 2 "
            "and Chapter 3 schemes, respectively, including module structure, API design, and deployment "
            "considerations. Block diagrams and flowcharts visually represent the integrated system.",
            "Chapter 5 provides comprehensive analysis and evaluation. Section 5.1 assesses the "
            "effectiveness of the proposed methods against the attacks cataloged in Chapter 1. "
            "Section 5.2 reviews prior work on authentication and key exchange in server-server and "
            "client-server environments. Section 5.3 reviews prior work on data encryption, data security, "
            "and integrity in e-banking. Section 5.4 synthesizes findings from Sections 5.1 through 5.3, "
            "lists security vulnerabilities present in existing systems, and identifies the issues "
            "addressed by this dissertation.",
            "The concluding remarks summarize the contributions of this research, acknowledge limitations, "
            "and suggest directions for future work. The appendix provides complete algorithm listings, "
            "test vectors, benchmark raw data, and API specifications to support reproducibility.",
        ],
    },
    {
        "heading": "Acknowledgments",
        "paragraphs": [
            "The completion of this dissertation would not have been possible without the support and "
            "guidance of numerous individuals and institutions. I express my sincere gratitude to my "
            "doctoral supervisor for invaluable advice throughout the research process. I thank the "
            "faculty and staff of the Department of Information Security for providing an environment "
            "conducive to rigorous scholarship. I am also grateful to the developers of open-source "
            "cryptographic libraries whose tools enabled the implementation work described in Chapter 4, "
            "and to the authors of the foundational papers reviewed in Chapter 5, whose contributions "
            "form the intellectual context within which this research is situated.",
        ],
    },
]
