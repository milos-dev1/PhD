"""Chapter 1: Threat Landscape and Security Gap Analysis."""

CHAPTER_TITLE = "Chapter 1"
CHAPTER_SUBTITLE = "Attack Mechanisms, Threat Landscape, and Security Gaps in E-Banking Systems"

SECTIONS = [{'heading': '1.1 Attack Mechanisms in E-Banking and E-Finance Services',
  'paragraphs': ['Electronic banking and electronic finance service systems operate in one of the '
                 'most adversarial computing environments in existence. The concentration of '
                 'monetary value, the interconnectivity of financial networks, and the diversity '
                 'of access channels create opportunities for attackers at every layer of the '
                 'technology stack. This section provides a systematic definition and taxonomy of '
                 'attack mechanisms currently employed against e-banking and e-finance services, '
                 'supported by representative case studies drawn from documented security '
                 'incidents.',
                 'An attack mechanism, in the context of this dissertation, is defined as a '
                 'systematic method or technique employed by an adversary to exploit a '
                 'vulnerability in an e-banking or e-finance system component—whether technical, '
                 'procedural, or human—in order to achieve an unauthorized objective such as theft '
                 'of funds, exfiltration of sensitive data, disruption of service, or compromise '
                 'of system integrity. Attack mechanisms differ from individual exploits in that '
                 'they describe reusable patterns that can be adapted to multiple targets and '
                 'environments.'],
  'subsections': [{'heading': '1.1.1 Taxonomy of Attacks',
                   'paragraphs': ['We classify attack mechanisms against e-banking systems into '
                                  "six primary categories based on the attacker's objective and "
                                  'the layer of the system stack targeted: (1) credential and '
                                  'authentication attacks, (2) communication channel attacks, (3) '
                                  'application-layer attacks, (4) infrastructure attacks, (5) '
                                  'insider and supply-chain attacks, and (6) social engineering '
                                  'attacks. Table 1.1 summarizes these categories with '
                                  'representative techniques.',
                                  'Credential and authentication attacks target the mechanisms by '
                                  'which users and systems prove their identity. Techniques '
                                  'include credential stuffing (automated injection of '
                                  'username-password pairs leaked from unrelated breaches), '
                                  'brute-force password guessing, pass-the-hash attacks against '
                                  'Windows authentication in bank internal networks, and '
                                  'exploitation of weak multi-factor authentication '
                                  'implementations that rely on SMS one-time passwords (OTPs) '
                                  'vulnerable to SIM-swapping.',
                                  'Communication channel attacks intercept, modify, or replay data '
                                  'in transit between clients and servers or between server nodes. '
                                  'The classic man-in-the-middle (MITM) attack positions the '
                                  'adversary between communicating parties, potentially '
                                  'decrypting, altering, and re-encrypting messages. SSL stripping '
                                  'downgrades HTTPS connections to HTTP, while BGP hijacking '
                                  'reroutes network traffic through attacker-controlled routers. '
                                  'Replay attacks capture valid authentication messages and '
                                  'retransmit them to gain unauthorized access.',
                                  'Application-layer attacks exploit vulnerabilities in banking '
                                  'software itself. SQL injection manipulates database queries '
                                  'through unsanitized user input. Cross-site scripting (XSS) '
                                  'injects malicious scripts into banking web pages viewed by '
                                  'other users. Cross-site request forgery (CSRF) tricks '
                                  'authenticated users into submitting unintended transactions. '
                                  'Business logic flaws may allow negative-amount transfers or '
                                  'bypass of transaction limits.',
                                  'Infrastructure attacks target the servers, networks, and cloud '
                                  'platforms hosting banking services. Distributed '
                                  'denial-of-service (DDoS) attacks overwhelm servers with '
                                  'traffic, rendering services unavailable. Ransomware encrypts '
                                  'critical banking data and demands payment for decryption keys. '
                                  'Container escape attacks in cloud-hosted banking microservices '
                                  'can compromise co-located workloads.',
                                  'Insider and supply-chain attacks leverage trusted positions or '
                                  'compromised third-party components. Malicious insiders with '
                                  'database access can exfiltrate customer records or manipulate '
                                  'account balances. Supply-chain compromises, such as the 2020 '
                                  'SolarWinds incident, insert backdoors into software updates '
                                  'distributed to thousands of organizations including financial '
                                  'institutions.',
                                  'Social engineering attacks manipulate human psychology rather '
                                  'than technical vulnerabilities. Phishing emails impersonate '
                                  'banks to harvest credentials. Vishing (voice phishing) uses '
                                  'phone calls to trick customers into revealing authentication '
                                  'codes. Pretexting creates fabricated scenarios to persuade bank '
                                  'employees to override security controls.'],
                   'table': {'headers': ['Category', 'Techniques', 'Primary Target', 'Impact'],
                             'rows': [['Credential/Auth',
                                       'Stuffing, brute force, SIM-swap',
                                       'Login systems',
                                       'Account takeover'],
                                      ['Channel',
                                       'MITM, SSL strip, replay, BGP hijack',
                                       'Network layer',
                                       'Data theft, fraud'],
                                      ['Application',
                                       'SQLi, XSS, CSRF, logic flaws',
                                       'Banking apps',
                                       'Data breach, fraud'],
                                      ['Infrastructure',
                                       'DDoS, ransomware, container escape',
                                       'Servers/cloud',
                                       'Outage, data loss'],
                                      ['Insider/Supply-chain',
                                       'Data exfiltration, backdoors',
                                       'Internal systems',
                                       'Mass breach'],
                                      ['Social engineering',
                                       'Phishing, vishing, pretexting',
                                       'Users/employees',
                                       'Credential theft']],
                             'caption': 'Table 1.1: Taxonomy of attack mechanisms against '
                                        'e-banking systems.'}},
                  {'heading': '1.1.2 Case Studies',
                   'paragraphs': ['Case Study 1 — Bangladesh Bank Heist (2016): Attackers gained '
                                  "access to the Bangladesh Bank's internal network, likely "
                                  'through a phishing email, and installed malware that monitored '
                                  'SWIFT Alliance Access software. Over several days, the '
                                  'attackers sent 35 fraudulent SWIFT transfer requests totaling '
                                  '$951 million. While most transfers were blocked, $81 million '
                                  'was successfully transferred to accounts in the Philippines. '
                                  'This case illustrates the catastrophic potential of '
                                  'server-server communication compromise when authentication and '
                                  'integrity controls on inter-bank messaging are insufficient.',
                                  'Case Study 2 — Capital One Data Breach (2019): A former cloud '
                                  'services employee exploited a misconfigured web application '
                                  'firewall to access an AWS S3 bucket containing personal data of '
                                  'over 100 million credit card applicants. The breach '
                                  'demonstrates that cloud-hosted e-finance systems introduce new '
                                  'attack vectors related to identity and access management '
                                  'misconfigurations, and that data-at-rest encryption alone is '
                                  'insufficient without proper access controls.',
                                  'Case Study 3 — Credential Stuffing Campaigns (2018–2024): '
                                  'Multiple major banks reported surges in account takeover fraud '
                                  'resulting from credential stuffing attacks using billions of '
                                  'leaked username-password pairs from non-financial breaches. '
                                  'Despite banks implementing account lockout and anomaly '
                                  'detection, the sheer volume of attempts (sometimes exceeding 50 '
                                  'million per day across the industry) results in a non-trivial '
                                  'success rate. These campaigns highlight the inadequacy of '
                                  'password-only authentication and the need for device-bound '
                                  'cryptographic authentication.',
                                  'Case Study 4 — EMV Relay Attacks (2020–2023): Researchers '
                                  'demonstrated relay attacks against contactless payment cards, '
                                  "where a proxy device near the victim's card relays NFC "
                                  "communication to a accomplice's device at a point-of-sale "
                                  'terminal hundreds of kilometers away. While EMV cryptography '
                                  'prevents card cloning, the relay attack bypasses proximity '
                                  'assumptions, showing that authentication protocols must bind '
                                  'cryptographic proofs to physical context.'],
                   'figure': 'Attack lifecycle flowchart: reconnaissance → initial access → '
                             'lateral movement → privilege escalation → data exfiltration/fraud → '
                             'cover tracks (Figure 1.1).'},
                  {'heading': '1.1.3 Attack Trends and Statistics',
                   'paragraphs': ['The financial services sector consistently ranks among the top '
                                  'three industries targeted by cyberattacks. The IBM Cost of a '
                                  'Data Breach Report (2024) reports that the average cost of a '
                                  'data breach in the financial sector is $5.9 million, compared '
                                  'to a cross-industry average of $4.45 million. Phishing remains '
                                  'the most common initial access vector, accounting for '
                                  'approximately 41% of breaches in financial services according '
                                  'to the Verizon Data Breach Investigations Report (2024).',
                                  'The adoption of mobile banking has shifted attack patterns: '
                                  'mobile malware targeting banking applications grew by 32% '
                                  'year-over-year, with trojans such as Anubis, Cerberus, and '
                                  'SharkBot employing overlay attacks to capture credentials and '
                                  'intercept SMS OTPs. Concurrently, API attacks against '
                                  'open-banking endpoints have emerged as a new threat category, '
                                  'with the OWASP API Security Top 10 identifying broken '
                                  'authentication and excessive data exposure as the most '
                                  'prevalent vulnerabilities.',
                                  'Ransomware groups have increasingly targeted financial '
                                  'institutions, with groups such as LockBit, ALPHV/BlackCat, and '
                                  'Cl0p claiming attacks on banks, insurance companies, and '
                                  'payment processors. The double-extortion model—encrypting data '
                                  'and threatening to publish stolen records—amplifies the '
                                  'pressure on victims to pay.',
                                  'From a defensive standpoint, understanding attack trends '
                                  'enables prioritization of security investments. The shift from '
                                  'perimeter-focused defenses to zero-trust architectures reflects '
                                  'the recognition that network boundaries have dissolved. In a '
                                  'zero-trust model, every access request—regardless of origin—is '
                                  'authenticated, authorized, and encrypted. The cryptographic '
                                  'schemes proposed in this dissertation align with zero-trust '
                                  'principles by providing device-bound, transaction-scoped '
                                  'authentication (ECC-DTB-AKA) and persistent integrity proofs '
                                  'that survive service-boundary crossings (ECC-HISE).']},
                  {'heading': '1.1.4 Regulatory and Standards Landscape',
                   'paragraphs': ['The regulatory environment surrounding e-banking security '
                                  'provides both constraints and guidance for cryptographic system '
                                  'design. The Payment Card Industry Data Security Standard (PCI '
                                  'DSS) v4.0 mandates strong cryptography for cardholder data '
                                  'protection, requiring TLS 1.2 or higher for transmission and '
                                  "AES-256 for storage. The European Union's Revised Payment "
                                  'Services Directive (PSD2) requires strong customer '
                                  'authentication (SCA) for electronic payments, implemented '
                                  'through two of three factors: knowledge (password), possession '
                                  '(device/token), and inherence (biometric).',
                                  'NIST Special Publication 800-52 Rev. 2 provides guidelines for '
                                  'TLS implementations in government and commercial systems, '
                                  'recommending TLS 1.3 with specific cipher suites. NIST SP '
                                  '800-57 Part 1 offers key-management guidance, recommending ECC '
                                  'P-256 for protection through 2030 and P-384 for longer-term '
                                  'requirements. ISO/IEC 27001:2022 specifies information security '
                                  'management system requirements applicable to financial '
                                  'institutions globally.',
                                  'The SWIFT Customer Security Programme (CSP) mandates 32 '
                                  'mandatory and advisory controls for institutions connected to '
                                  'the SWIFT network, including multi-factor authentication for '
                                  'operator sessions, network segmentation, and attestation of '
                                  'security compliance annually. Non-compliance can result in '
                                  'reporting to regulators and potential disconnection from the '
                                  'SWIFT network.',
                                  'These standards collectively establish minimum baselines but do '
                                  'not prescribe integrated methodologies for binding '
                                  'authentication to key exchange or for hierarchical '
                                  'data-protection envelopes. The gap between compliance and '
                                  'comprehensive security motivates the research contributions of '
                                  'this dissertation.']},
                  {'heading': '1.1.5 Detailed Analysis of Selected Attack Vectors',
                   'paragraphs': ['To provide depth beyond the taxonomy presented in Section '
                                  '1.1.1, this subsection examines three high-impact attack '
                                  'vectors in detail: man-in-the-middle attacks on banking '
                                  'sessions, session hijacking via token theft, and advanced '
                                  'persistent threats (APTs) targeting financial infrastructure.',
                                  'Man-in-the-middle (MITM) attacks on banking sessions exploit '
                                  'the fact that users often cannot distinguish legitimate bank '
                                  'servers from impersonating proxies. In a typical MITM scenario, '
                                  'the attacker positions a proxy between the client and the bank '
                                  "server. If the client does not validate the server's "
                                  'certificate chain correctly—or if the attacker has compromised '
                                  'a trusted CA or uses a corporate SSL-inspection proxy—the '
                                  'attacker can decrypt, inspect, and modify transaction data in '
                                  'real time. Tools such as mitmproxy and Burp Suite, while '
                                  'designed for legitimate security testing, demonstrate the '
                                  'feasibility of this attack class. Banking trojans such as Zeus '
                                  'and Emotet have historically automated MITM against banking '
                                  'websites by injecting fraudulent transaction fields into '
                                  'otherwise legitimate sessions, redirecting wire transfers to '
                                  'attacker-controlled accounts without altering the confirmation '
                                  'screen displayed to the user.',
                                  'Session hijacking via token theft represents a distinct but '
                                  'related threat. After successful authentication, the banking '
                                  'application issues a session token (cookie or bearer token) '
                                  'that the client presents with each subsequent request. If an '
                                  'attacker obtains this token—through XSS, malware memory '
                                  'scraping, or network sniffing on unencrypted channels—the '
                                  'attacker can impersonate the victim without knowing their '
                                  'password or MFA code. The OWASP Session Management Cheat Sheet '
                                  'recommends token rotation, binding tokens to client IP '
                                  'addresses, and using HttpOnly/Secure cookie flags, but these '
                                  'mitigations are not universally implemented and do not provide '
                                  'cryptographic binding between the token and the underlying '
                                  'key-exchange material.',
                                  'Advanced persistent threats (APTs) targeting financial '
                                  'infrastructure operate over extended time periods (weeks to '
                                  'months), maintaining covert access to bank networks while '
                                  'exfiltrating data or preparing fraudulent transactions. APT '
                                  'groups such as Carbanak (also known as FIN7) and Lazarus Group '
                                  'have demonstrated the ability to compromise bank internal '
                                  'networks, learn internal transaction workflows, and execute '
                                  'fraudulent transfers through the same channels used by '
                                  'legitimate operators. APT attacks often begin with '
                                  'spear-phishing emails containing weaponized documents, progress '
                                  'through lateral movement using stolen credentials, and '
                                  'culminate in access to SWIFT terminals or core banking systems. '
                                  'The Bangladesh Bank heist exemplifies an APT-style operation '
                                  'against financial infrastructure.']},
                  {'heading': '1.1.6 Impact Assessment Framework',
                   'paragraphs': ['Assessing the impact of attacks on e-banking systems requires a '
                                  'multidimensional framework that goes beyond simple financial '
                                  'loss figures. We adopt a framework with four impact dimensions: '
                                  'financial, operational, reputational, and regulatory.',
                                  'Financial impact encompasses direct losses (fraudulent '
                                  'transfers, ransom payments), indirect losses (customer '
                                  'compensation, legal fees), and recovery costs (forensic '
                                  'investigation, system restoration). The Ponemon Institute and '
                                  'IBM jointly publish annual cost-of-breach figures; for '
                                  'financial services in 2024, the average total cost was $5.9 '
                                  'million per breach, with an average of 258 days to identify and '
                                  'contain the breach.',
                                  'Operational impact includes service downtime, degraded '
                                  'performance during attacks, and diversion of IT resources from '
                                  'planned projects to incident response. A DDoS attack against a '
                                  "major bank's online banking portal can prevent millions of "
                                  'customers from accessing services for hours, generating '
                                  'call-center surges and transaction backlogs. The operational '
                                  'resilience requirements of the Bank of England and the European '
                                  'Central Bank mandate maximum tolerable downtime thresholds for '
                                  'critical payment systems.',
                                  'Reputational impact manifests as customer attrition, negative '
                                  'media coverage, and reduced stock valuation. Studies indicate '
                                  'that publicly traded banks experience an average stock price '
                                  'decline of 5–7% in the week following a major breach '
                                  'announcement, with partial recovery over subsequent months. '
                                  'Customer trust, once eroded, requires sustained investment in '
                                  'transparency and security improvements to rebuild.',
                                  'Regulatory impact includes fines, consent orders, and increased '
                                  'supervisory scrutiny. The GDPR permits fines up to 4% of global '
                                  'annual revenue for serious data protection violations. The U.S. '
                                  'Office of the Comptroller of the Currency (OCC) and the Federal '
                                  'Reserve have issued consent orders against banks with deficient '
                                  'cybersecurity programs, requiring multi-year remediation plans '
                                  'and independent third-party assessments.']},
                  {'heading': '1.1.5 Kill-Chain View of Remote Banking Fraud',
                   'paragraphs': ['A useful analytic lens is the intrusion kill chain adapted to '
                                  'remote banking fraud. Typical stages include: (1) '
                                  'reconnaissance of banking apps and open redirectors; (2) '
                                  'weaponization via phishing kits or trojanized APKs; (3) '
                                  'delivery through SMS, email, or malvertising; (4) exploitation '
                                  'of weak auth or session handling; (5) installation of overlay '
                                  'malware or theft of refresh tokens; (6) command-and-control via '
                                  'abused cloud channels; and (7) actions on objectives such as '
                                  'ATO wire transfers or mule-account cascades.',
                                  'Cryptographic channel improvements primarily disrupt stages 4–7 '
                                  'for remote adversaries who lack physical device control: '
                                  'device-bound session keys reduce the value of stolen cookies; '
                                  'transaction-bound keys reduce the value of ambient session '
                                  'tokens for payment injection; server-side envelopes reduce '
                                  'silent tampering of settlement outputs after compromise of a '
                                  'middleware hop. Understanding the kill chain clarifies why '
                                  'transport encryption alone—active mainly against passive '
                                  'wiretap at stage 5–6—is not a complete control set.']},
                  {'heading': '1.1.6 Economic Incentives and Attacker Business Models',
                   'paragraphs': ['Modern banking attacks are industrialized. Credential shops '
                                  'sell dumps; phishing-as-a-service lowers skill barriers; mule '
                                  'networks monetize stolen funds; ransomware crews target '
                                  'availability and extort. The economic asymmetry—attack '
                                  'automation versus institution-specific defenses—favors controls '
                                  'that invalidate entire classes of stolen material (bearer '
                                  'tokens, static file keys) rather than only detecting individual '
                                  'fraud cases after loss.',
                                  "This economic framing motivates the dissertation's design "
                                  'emphasis: make stolen session artifacts non-portable across '
                                  'devices and transactions, and make settlement batches '
                                  'non-silently mutable after TLS termination.']}]},
 {'heading': '1.2 Authentication and Key Exchange in E-Banking Systems',
  'paragraphs': ['Authentication and key exchange form the first line of cryptographic defense in '
                 'e-banking systems. Before any financial transaction can be authorized, the '
                 "participating parties must establish mutual confidence in each other's identity "
                 'and agree upon cryptographic keys for protecting subsequent communication. This '
                 'section reviews the authentication and key-exchange mechanisms currently '
                 'deployed in client-server and server-server environments of e-banking and '
                 'e-finance services, analyzes their operational characteristics, and identifies '
                 'limitations that motivate the scheme proposed in Chapter 2.'],
  'subsections': [{'heading': '1.2.1 Client-Server Authentication Mechanisms',
                   'paragraphs': ['The dominant client-server authentication model in retail '
                                  'e-banking comprises TLS 1.2/1.3 transport layer security '
                                  'combined with application-layer username-password '
                                  'authentication, often supplemented by a second factor (SMS OTP, '
                                  'hardware token, or mobile push notification). In this model, '
                                  'TLS provides server authentication via X.509 certificates and '
                                  'establishes encrypted channels, while the application layer '
                                  'authenticates the user independently.',
                                  'The TLS 1.3 handshake protocol operates as follows: the client '
                                  'sends a ClientHello message specifying supported cipher suites '
                                  'and a key share (typically ECDHE on curve X25519 or P-256). The '
                                  'server responds with ServerHello, its certificate chain, and a '
                                  'key share. Both parties derive handshake traffic keys and '
                                  'application traffic keys using HKDF. The full handshake '
                                  'requires one round trip (1-RTT); a subsequent resumption using '
                                  'pre-shared keys achieves 0-RTT, though 0-RTT data is vulnerable '
                                  'to replay attacks and is therefore restricted by banking '
                                  'applications.',
                                  'Application-layer authentication typically follows the TLS '
                                  'handshake. The client submits credentials (username, password '
                                  'hash, or token) over the encrypted channel. The server '
                                  'validates credentials against a stored database, often using '
                                  'bcrypt, scrypt, or Argon2 password hashing. Upon success, the '
                                  'server issues a session token (commonly a JSON Web Token or '
                                  'opaque server-side session identifier) that the client presents '
                                  'with subsequent requests.',
                                  'Multi-factor authentication (MFA) adds a second verification '
                                  'step. SMS-based OTP remains prevalent despite known '
                                  'vulnerabilities to SIM-swapping and SS7 protocol attacks. '
                                  'Time-based one-time passwords (TOTP) per RFC 6238, implemented '
                                  'by applications such as Google Authenticator, provide stronger '
                                  'security but are susceptible to real-time phishing proxies '
                                  '(e.g., Evilginx) that relay OTPs to the attacker. '
                                  'FIDO2/WebAuthn, based on public-key cryptography with hardware '
                                  'security keys or platform authenticators (biometrics), '
                                  'represents the current state of the art for phishing-resistant '
                                  'MFA.'],
                   'figure': 'Current client-server authentication flow: TLS handshake → '
                             'credential submission → MFA challenge → session token issuance '
                             '(Figure 1.2).'},
                  {'heading': '1.2.2 Server-Server Authentication and Key Exchange',
                   'paragraphs': ['Server-server authentication in e-finance encompasses '
                                  "communication between a bank's internal microservices, "
                                  'inter-bank payment networks (SWIFT, ACH, Fedwire, SEPA), card '
                                  'network processors (Visa, Mastercard), and third-party '
                                  'open-banking aggregators. These channels typically employ '
                                  'mutual TLS (mTLS) with client certificates, VPN tunnels, or '
                                  'dedicated leased lines with link-layer encryption.',
                                  'In the SWIFT network, authentication relies on the SWIFT '
                                  'Alliance Access software and bilateral key exchange (BKE) '
                                  'between institutions. Message authentication uses symmetric '
                                  "keys distributed through SWIFT's Secure Channel protocol. The "
                                  "2016 Bangladesh Bank heist exposed weaknesses in institutions' "
                                  'local security practices surrounding SWIFT terminal access '
                                  "rather than fundamental flaws in SWIFT's cryptographic "
                                  'protocols, but the incident nonetheless highlighted the '
                                  'importance of end-to-end authentication binding.',
                                  'Modern microservice architectures within banks increasingly use '
                                  'service mesh platforms (e.g., Istio, Linkerd) that automate '
                                  'mTLS between services. Certificate authorities internal to the '
                                  'bank issue short-lived certificates (typically 24-hour '
                                  'validity) to each service instance. While mTLS provides strong '
                                  'transport security, it does not address application-level '
                                  'authorization, message-level integrity for stored records, or '
                                  'auditability requirements for regulatory compliance.',
                                  'API-based open-banking connections (under PSD2, Open Banking '
                                  'UK, and similar frameworks) use OAuth 2.0 with PKCE (Proof Key '
                                  'for Code Exchange) for customer consent and access-token '
                                  'issuance. The authorization server authenticates the '
                                  'third-party provider, while the resource server (bank API) '
                                  'validates access tokens. Limitations include token theft via '
                                  'XSS, insufficient scope granularity, and the absence of '
                                  'transaction-level cryptographic binding.'],
                   'figure': 'Server-server authentication in a microservice e-finance '
                             'architecture with mTLS service mesh (Figure 1.3).'},
                  {'heading': '1.2.3 Identified Limitations and Drawbacks',
                   'paragraphs': ['Despite the breadth of deployed mechanisms, significant '
                                  'limitations persist in current client-server and server-server '
                                  'authentication and key-exchange practices. These limitations '
                                  'directly motivate the ECC-DTB-AKA scheme proposed in Chapter 2.',
                                  'Limitation 1 — Decoupled transport and application '
                                  'authentication: TLS authenticates the server (and optionally '
                                  'the client via mTLS) at the transport layer, while user '
                                  'authentication occurs separately at the application layer. This '
                                  'decoupling creates a gap: a valid TLS session does not '
                                  'cryptographically bind the authenticated user identity to the '
                                  'encryption keys. An attacker who compromises a session token '
                                  'can hijack the application session even though the TLS channel '
                                  'remains intact.',
                                  'Limitation 2 — Absence of device binding in key exchange: '
                                  'Standard TLS ECDHE derives session keys from ephemeral key '
                                  'pairs only, without incorporating device characteristics. If a '
                                  'session token is exfiltrated, it can be replayed from a '
                                  'different device. FIDO2 addresses this for the authentication '
                                  'step but does not integrate device binding into the '
                                  'key-exchange derivation itself.',
                                  'Limitation 3 — No transaction-level key derivation: Once a '
                                  'session is established, the same application traffic keys '
                                  'protect all transactions within the session. Compromise of '
                                  'session keys exposes all transactions, not merely the current '
                                  'one. Per-transaction key derivation without additional round '
                                  'trips is not supported by TLS or OAuth 2.0.',
                                  'Limitation 4 — Session token vulnerability: Opaque session '
                                  'tokens and JWTs are bearer credentials—whoever possesses the '
                                  'token is authenticated. Token theft via XSS, malware, or '
                                  'network interception remains a prevalent attack vector. Binding '
                                  'tokens to cryptographic key material established during '
                                  'authenticated key agreement would limit the impact of token '
                                  'compromise.',
                                  'Limitation 5 — Server-server channels lack message-level '
                                  'security: mTLS protects data in transit between services but '
                                  'does not provide persistent integrity proofs for stored or '
                                  'forwarded messages. If a message is intercepted after TLS '
                                  'termination and before re-encryption, it is vulnerable to '
                                  'tampering.',
                                  'Limitation 6 — Insufficient forward secrecy in legacy '
                                  'deployments: Although TLS 1.3 mandates forward secrecy, many '
                                  'e-banking systems still support TLS 1.2 with cipher suites that '
                                  'do not use ephemeral Diffie-Hellman (e.g., RSA key transport). '
                                  'Legacy load balancers and API gateways may terminate TLS and '
                                  're-encrypt with weaker configurations, creating forward-secrecy '
                                  'gaps.',
                                  'These six limitations collectively demonstrate that current '
                                  'authentication and key-exchange practices in e-banking systems, '
                                  'while adequate for baseline compliance, fail to provide the '
                                  'cryptographic binding of identity, device, and transaction '
                                  'context necessary to resist the attack mechanisms cataloged in '
                                  'Section 1.1. Chapter 2 addresses these limitations through the '
                                  'ECC-DTB-AKA protocol, which integrates mutual authentication, '
                                  'ECDH-based forward secrecy, device fingerprint binding, and '
                                  'on-demand transaction key derivation into a unified three-round '
                                  'handshake.'],
                   'table': {'headers': ['Limitation',
                                         'Affected Mechanism',
                                         'Attack Enabled',
                                         'Severity'],
                             'rows': [['Decoupled auth layers',
                                       'TLS + app login',
                                       'Session hijacking',
                                       'High'],
                                      ['No device binding',
                                       'TLS ECDHE',
                                       'Credential replay from new device',
                                       'High'],
                                      ['No per-txn key derivation',
                                       'TLS session keys',
                                       'Bulk transaction exposure',
                                       'Medium'],
                                      ['Bearer session tokens',
                                       'JWT / opaque tokens',
                                       'Token theft (XSS, malware)',
                                       'High'],
                                      ['No message-level integrity',
                                       'mTLS only',
                                       'Post-termination tampering',
                                       'Medium'],
                                      ['Legacy TLS configurations',
                                       'TLS 1.2 RSA suites',
                                       'Retroactive decryption',
                                       'Medium']],
                             'caption': 'Table 1.2: Limitations of current authentication and '
                                        'key-exchange mechanisms.'}},
                  {'heading': '1.2.4 Elliptic Curve Cryptography in Financial Authentication',
                   'paragraphs': ['Elliptic curve cryptography has become the preferred public-key '
                                  'primitive for new financial authentication deployments. '
                                  'Understanding its role in current systems is essential context '
                                  'for the novel schemes proposed in Chapters 2 and 3.',
                                  'An elliptic curve E over a finite field F_p is the set of '
                                  'points (x, y) satisfying the Weierstrass equation y² = x³ + ax '
                                  '+ b (mod p), together with a point at infinity forming an '
                                  'abelian group. Cryptographic security relies on the hardness of '
                                  'the elliptic curve discrete logarithm problem (ECDLP): given '
                                  'points P and Q = [k]P, find scalar k. For properly chosen '
                                  'curves with sufficiently large prime subgroups, the best known '
                                  'algorithms require exponential time, providing security '
                                  'proportional to half the bit length of the subgroup order.',
                                  'In TLS 1.3, the default key-exchange mechanism is ECDHE '
                                  '(Elliptic Curve Diffie-Hellman Ephemeral), using curves X25519 '
                                  'or P-256. The ephemeral nature of ECDHE provides forward '
                                  "secrecy: compromise of the server's long-term private key does "
                                  'not enable decryption of previously recorded sessions. EMV chip '
                                  'cards use ECDSA on curve secp256r1 for offline and online '
                                  'transaction authentication. FIDO2/WebAuthn employs ECDSA or '
                                  'Ed25519 for credential key pairs stored in hardware '
                                  'authenticators.',
                                  'Despite widespread ECC adoption, current deployments use ECC '
                                  'primarily for individual cryptographic operations (key '
                                  'agreement, signing) rather than as an integrated methodology '
                                  'binding authentication, key exchange, device context, and '
                                  'transaction scope. The ECC-DTB-AKA scheme proposed in Chapter 2 '
                                  'extends ECC key agreement with additional binding inputs '
                                  '(device fingerprint, transaction nonce) in the HKDF derivation, '
                                  'creating a cohesive protocol rather than a stack of independent '
                                  'cryptographic layers.']},
                  {'heading': '1.2.5 Comparative Overview of Authentication Protocols',
                   'paragraphs': ['Table 1.4 provides a comparative overview of authentication and '
                                  'key-exchange protocols commonly used in e-banking systems, '
                                  'highlighting properties relevant to the limitations identified '
                                  'in Section 1.2.3.',
                                  'TLS 1.3 full handshake provides server authentication and '
                                  'forward-secure key agreement in one round trip but does not '
                                  'authenticate the user at the cryptographic layer. OAuth 2.0 '
                                  'with PKCE adds authorization delegation for third-party API '
                                  'access but relies on bearer tokens vulnerable to theft. FIDO2 '
                                  'provides phishing-resistant user authentication but does not '
                                  'integrate with key-exchange derivation. Kerberos with PKINIT '
                                  '(public-key initialization) supports mutual authentication in '
                                  'enterprise environments but is rarely deployed in retail '
                                  'e-banking client-server channels.',
                                  'None of these protocols simultaneously achieves: (a) mutual '
                                  'authentication at the cryptographic layer, (b) device binding '
                                  'in key derivation, (c) per-transaction key derivation without '
                                  'additional round trips, and (d) three-round handshake '
                                  'efficiency. This gap is the design target for ECC-DTB-AKA.'],
                   'table': {'headers': ['Protocol',
                                         'Mutual Auth',
                                         'Forward Secrecy',
                                         'Device Bind',
                                         'Per-Txn Key',
                                         'Rounds'],
                             'rows': [['TLS 1.3', 'Server only', 'Yes', 'No', 'No', '1'],
                                      ['OAuth 2.0 PKCE', 'Delegated', 'Via TLS', 'No', 'No', '3+'],
                                      ['FIDO2/WebAuthn', 'User auth', 'N/A', 'Partial', 'No', '2'],
                                      ['ECDH + JWT', 'App layer', 'Yes', 'No', 'No', '2'],
                                      ['ECC-DTB-AKA (Ch.2)', 'Yes', 'Yes', 'Yes', 'Yes', '3']],
                             'caption': 'Table 1.4: Comparative overview of authentication '
                                        'protocols for e-banking.'}},
                  {'heading': '1.2.6 Password-Based Authentication Vulnerabilities',
                   'paragraphs': ['Despite decades of security guidance, password-based '
                                  'authentication remains the default for retail e-banking in most '
                                  'jurisdictions. Understanding its inherent vulnerabilities is '
                                  'essential for motivating cryptographic alternatives.',
                                  'Human-chosen passwords exhibit highly skewed distributions. '
                                  'Analysis of breached password databases consistently shows that '
                                  'the top 100 passwords account for approximately 17% of all '
                                  "passwords, with '123456', 'password', and 'qwerty' appearing in "
                                  'virtually every corpus. Password complexity rules (requiring '
                                  'uppercase, numbers, symbols) often result in predictable '
                                  'substitutions (P@ssw0rd) that provide minimal additional '
                                  'entropy.',
                                  'Password hashing algorithms mitigate offline attacks against '
                                  'stolen databases. Bcrypt, scrypt, and Argon2 are designed to be '
                                  'computationally expensive, limiting the rate at which attackers '
                                  'can test guessed passwords. However, weak passwords remain '
                                  'vulnerable even with strong hashing, and credential stuffing '
                                  'attacks bypass hashing entirely by testing leaked credentials '
                                  'from other breaches against banking login portals.',
                                  'Password reset mechanisms introduce additional attack surfaces. '
                                  "Knowledge-based authentication questions (mother's maiden name, "
                                  'first pet) are often guessable from social media. Email-based '
                                  'reset links can be intercepted if the email account is '
                                  'compromised. SMS-based reset codes inherit SIM-swapping '
                                  'vulnerabilities. These weaknesses reinforce the need for '
                                  'cryptographic authentication mechanisms that do not rely solely '
                                  'on shared secrets memorized by humans.']},
                  {'heading': '1.2.4 Session Token Lifecycles and Refresh-Token Risk',
                   'paragraphs': ['OAuth 2.0 and OIDC deployments in open banking and mobile '
                                  'banking commonly issue short-lived access tokens and '
                                  'longer-lived refresh tokens. Refresh tokens, if stolen from '
                                  'device storage or backup channels, allow prolonged API access '
                                  'without user presence. PKCE mitigates authorization-code '
                                  'interception on public clients but does not bind subsequent API '
                                  'calls to a device-bound key hierarchy.',
                                  'Banks mitigate with refresh-token rotation, device cookies, and '
                                  'step-up authentication. These are policy controls on top of '
                                  'bearer semantics. ECC-DTB-AKA instead makes the cryptographic '
                                  'session key depend on device fingerprint material and derives '
                                  'payment authorizers from transaction nonces—shifting from '
                                  'policy-enforced bearer tokens toward cryptographically bound '
                                  'authenticators.']},
                  {'heading': '1.2.5 Mutual TLS in Service Meshes: Strengths and Blind Spots',
                   'paragraphs': ['Service meshes (Istio, Linkerd, and vendor equivalents) '
                                  'democratized mTLS between microservices. Strengths include '
                                  'automated certificate rotation and workload identity. Blind '
                                  'spots remain: mesh identity often equals workload identity, not '
                                  'business-transaction identity; sidecar termination again '
                                  'creates plaintext; and east-west traffic after termination is '
                                  'trusted implicitly. For settlement and clearing adapters that '
                                  'export files to external institutions, mesh mTLS does not '
                                  'travel with the file.',
                                  'Hence Chapter 1 treats mTLS as necessary but incomplete for '
                                  'SR5–SR8, motivating ECC-HISE at the application data plane.']}]},
 {'heading': '1.3 Data Encryption, Security, and Integrity in E-Banking',
  'paragraphs': ['Beyond authentication and key establishment, e-banking systems must protect the '
                 'confidentiality, integrity, and availability of financial data throughout its '
                 'lifecycle. This section examines the data encryption, security, and integrity '
                 'mechanisms currently employed in e-banking and e-finance services, with emphasis '
                 'on server-server data transfer and storage, and identifies drawbacks that '
                 'motivate the ECC-HISE scheme proposed in Chapter 3.'],
  'subsections': [{'heading': '1.3.1 Data Encryption Mechanisms',
                   'paragraphs': ['Data-at-rest encryption in banking systems typically employs '
                                  'AES-256 in Galois/Counter Mode (GCM) or XTS mode. '
                                  'Database-level encryption (transparent data encryption, TDE) '
                                  'protects entire tablespaces, while column-level encryption '
                                  'targets sensitive fields (account numbers, social security '
                                  'numbers). Key management is performed by HSMs certified to FIPS '
                                  '140-2 Level 3 or higher, with key-encryption keys (KEKs) stored '
                                  'in hardware and data-encryption keys (DEKs) wrapped under KEKs.',
                                  'Data-in-transit encryption relies primarily on TLS as described '
                                  'in Section 1.2. For server-server bulk data transfer (e.g., '
                                  'end-of-day settlement files, regulatory reporting batches), '
                                  'institutions may additionally employ PGP/GPG encryption or '
                                  'proprietary file-encryption tools with pre-shared symmetric '
                                  'keys distributed via out-of-band channels.',
                                  'Elliptic curve cryptography appears in data-protection contexts '
                                  'primarily through ECIES (Elliptic Curve Integrated Encryption '
                                  'Scheme), which combines ECDH key agreement with a symmetric '
                                  'cipher and MAC. ECIES is standardized in IEEE 1363a and SEC 1, '
                                  'and provides semantic security under chosen-ciphertext attacks '
                                  'when implemented with appropriate KDF and MAC (or authenticated '
                                  'encryption). However, standard ECIES operates at the message '
                                  'level without hierarchical key management or batch audit '
                                  'capabilities required for inter-bank settlement.'],
                   'figure': 'Data protection layers in e-banking: at-rest (TDE), in-transit '
                             '(TLS), in-use (confidential computing) (Figure 1.4).'},
                  {'heading': '1.3.2 Data Integrity and Audit Mechanisms',
                   'paragraphs': ['Integrity protection for individual messages is commonly '
                                  'provided by HMAC-SHA256 or by the authenticated encryption '
                                  'inherent in AES-GCM. Digital signatures using RSA or ECDSA '
                                  'provide non-repudiation for high-value transactions and '
                                  'regulatory submissions. However, per-message signatures do not '
                                  'efficiently support batch verification of large settlement '
                                  'files containing millions of records.',
                                  'Audit trails in e-banking systems log transaction events, '
                                  'access attempts, and administrative actions to tamper-evident '
                                  'storage. Common implementations include append-only databases, '
                                  'write-once-read-many (WORM) storage, and centralized SIEM '
                                  'platforms. Blockchain and distributed-ledger technologies have '
                                  'been proposed and piloted for settlement audit (e.g., '
                                  "JPMorgan's Onyx, R3 Corda), offering Merkle-tree-based "
                                  'integrity guarantees but introducing latency and scalability '
                                  'trade-offs unsuitable for all use cases.',
                                  'Hash chains—where each log entry includes the hash of the '
                                  'previous entry—provide lightweight tamper evidence without the '
                                  'overhead of full blockchain consensus. Merkle trees enable '
                                  'efficient verification that a specific record is included in a '
                                  'batch without reprocessing the entire batch, a property '
                                  'essential for regulatory audit of large settlement files.']},
                  {'heading': '1.3.3 Identified Limitations and Drawbacks',
                   'paragraphs': ['The following limitations in current data encryption, security, '
                                  'and integrity mechanisms motivate the ECC-HISE scheme proposed '
                                  'in Chapter 3.',
                                  'Limitation 1 — Flat key management hierarchies: Many '
                                  'institutions use a small number of long-lived symmetric keys '
                                  'for bulk encryption, increasing the blast radius of key '
                                  'compromise. Hierarchical key derivation that scopes keys to '
                                  'business domains and individual batches limits exposure.',
                                  'Limitation 2 — Disconnected encryption and audit: Encryption '
                                  'and audit logging are typically implemented as independent '
                                  'systems. An encrypted batch file may be stored without a '
                                  'cryptographically linked integrity proof that enables '
                                  'third-party verification of completeness and ordering.',
                                  'Limitation 3 — Inefficient batch integrity verification: '
                                  'Per-record digital signatures do not scale to settlement '
                                  'batches containing millions of entries. A Merkle-tree-based '
                                  'approach enables O(log n) verification per record while '
                                  'maintaining O(1) batch-level integrity evidence.',
                                  'Limitation 4 — Static pre-shared keys in server-server '
                                  'channels: Inter-bank file transfer often relies on symmetric '
                                  'keys distributed manually and rotated infrequently (annually or '
                                  'biannually). ECC-based ephemeral key agreement per batch '
                                  'eliminates long-lived shared secrets.',
                                  'Limitation 5 — Lack of end-to-end integrity across service '
                                  'boundaries: In microservice architectures, a message may be '
                                  'decrypted at each service boundary (TLS termination), processed '
                                  'in plaintext, and re-encrypted. Envelope encryption that '
                                  'persists integrity proofs across service boundaries addresses '
                                  'this gap.',
                                  'Limitation 6 — Regulatory audit friction: Demonstrating to '
                                  'auditors that no records were added, removed, or reordered in a '
                                  'settlement batch currently requires manual reconciliation or '
                                  'expensive full-batch reprocessing. Cryptographic audit chains '
                                  'reduce audit cost and increase confidence.',
                                  'These six limitations in data-security mechanisms parallel the '
                                  'authentication gaps identified in Section 1.2, but operate at a '
                                  'different layer of the system stack. While Section 1.2 concerns '
                                  'who is communicating and how keys are established, this section '
                                  'concerns what data is protected, how integrity is maintained, '
                                  'and how compliance can be demonstrated. Chapter 3 addresses '
                                  'these limitations through ECC-HISE, which combines hierarchical '
                                  'ECC key derivation, authenticated envelope encryption, and '
                                  'Merkle-tree audit chains into a cohesive server-server '
                                  'data-protection methodology.'],
                   'table': {'headers': ['Limitation',
                                         'Current Practice',
                                         'Proposed Direction (Ch.3)',
                                         'Impact'],
                             'rows': [['Flat key hierarchy',
                                       'Few long-lived DEKs',
                                       'ECC hierarchical derivation',
                                       'Key compromise scope'],
                                      ['Disconnected audit',
                                       'Separate log systems',
                                       'Merkle-linked envelopes',
                                       'Tamper detection'],
                                      ['Batch verification cost',
                                       'Per-record signatures',
                                       'Merkle tree batch proofs',
                                       'Scalability'],
                                      ['Static PSKs',
                                       'Annual manual rotation',
                                       'Ephemeral ECDH per batch',
                                       'Long-term exposure'],
                                      ['Service-boundary gaps',
                                       'TLS terminate/decrypt',
                                       'Persistent envelope integrity',
                                       'Insider tampering'],
                                      ['Audit friction',
                                       'Manual reconciliation',
                                       'Cryptographic audit chain',
                                       'Compliance cost']],
                             'caption': 'Table 1.3: Limitations of current data security '
                                        'mechanisms and proposed directions.'}},
                  {'heading': '1.3.4 Key Management in Financial Institutions',
                   'paragraphs': ['Effective data encryption in e-banking depends critically on '
                                  'key management—the generation, distribution, storage, rotation, '
                                  'and destruction of cryptographic keys. Poor key management can '
                                  'render even the strongest encryption algorithms ineffective, as '
                                  'demonstrated by numerous breaches where encryption was deployed '
                                  'but keys were stored alongside encrypted data in accessible '
                                  'locations.',
                                  'Financial institutions typically employ a tiered key-management '
                                  'architecture. At the top level, master keys are generated '
                                  'within FIPS 140-2 Level 3 (or higher) hardware security modules '
                                  'and never leave the HSM in plaintext form. Key-encryption keys '
                                  '(KEKs) wrap data-encryption keys (DEKs) for distribution to '
                                  'application servers. DEKs encrypt actual customer data and are '
                                  'rotated frequently (daily to monthly) depending on data '
                                  'classification and regulatory requirements.',
                                  'The ANSI X9.24-3 standard specifies key-management requirements '
                                  'for symmetric keys in financial services, including '
                                  'dual-control procedures for key generation and split-knowledge '
                                  'requirements for critical keys. PCI DSS Requirement 3 mandates '
                                  'protection of stored cardholder data, including key-management '
                                  'procedures for encryption keys. However, these standards focus '
                                  'on symmetric key hierarchies and do not address ECC-based '
                                  'hierarchical derivation for batch envelope encryption with '
                                  'integrated audit chains—the design space targeted by '
                                  'ECC-HISE.']},
                  {'heading': '1.3.5 Merkle Trees and Cryptographic Audit Trails',
                   'paragraphs': ['Merkle trees (hash trees) provide an efficient data structure '
                                  'for verifying integrity of large datasets. A Merkle tree is a '
                                  'binary tree in which each leaf node contains the hash of a data '
                                  'block, and each internal node contains the hash of the '
                                  'concatenation of its children. The root hash commits to the '
                                  'entire dataset: any modification to any leaf changes the root '
                                  'hash. A verifier can confirm inclusion of a specific record '
                                  'with O(log n) hash computations given an authentication path '
                                  '(Merkle proof) from the leaf to the root.',
                                  'In e-banking settlement, Merkle trees enable regulators and '
                                  'counterparties to verify that a specific transaction was '
                                  'included in a batch settlement without reprocessing the entire '
                                  'batch. Combined with digital signatures on the Merkle root, the '
                                  'tree provides both integrity and non-repudiation at the batch '
                                  'level. Bitcoin and other blockchains use Merkle trees in block '
                                  'headers for similar reasons, though blockchain consensus '
                                  'introduces latency unsuitable for real-time settlement. '
                                  'ECC-HISE adopts Merkle trees for audit without requiring '
                                  'distributed consensus, making it applicable to traditional '
                                  'inter-bank settlement workflows.',
                                  'The integration of Merkle audit chains with ECC-based envelope '
                                  'encryption—rather than treating encryption and audit as '
                                  'separate subsystems—constitutes a key differentiator of the '
                                  'ECC-HISE approach developed in Chapter 3. By including the '
                                  'Merkle root in the signed batch header, any tampering with '
                                  'individual records is detectable through root mismatch, while '
                                  'the hierarchical key structure limits the scope of key '
                                  'compromise to individual batches within specific business '
                                  'domains.']},
                  {'heading': '1.3.6 Homomorphic Encryption and Emerging Approaches',
                   'paragraphs': ['While not part of the proposed schemes in this dissertation, '
                                  'emerging cryptographic technologies warrant brief discussion to '
                                  'situate the research within the broader landscape of financial '
                                  'data protection.',
                                  'Fully homomorphic encryption (FHE) enables computation on '
                                  'encrypted data without decryption, potentially allowing banks '
                                  'to perform fraud detection on encrypted transaction streams. '
                                  'However, FHE remains orders of magnitude slower than plaintext '
                                  'computation and is not yet practical for real-time e-banking '
                                  'workloads. Partial homomorphic schemes (Paillier, ElGamal) '
                                  'support specific operations (addition, multiplication) and have '
                                  'been piloted for privacy-preserving credit scoring.',
                                  'Confidential computing (Intel SGX, AMD SEV, ARM TrustZone) '
                                  'provides hardware-enforced memory isolation for applications '
                                  'processing sensitive data. Major cloud providers offer '
                                  'confidential virtual machines for financial workloads. These '
                                  "technologies address the 'data in use' protection gap "
                                  'identified in Section 1.3.1 but require trust in hardware '
                                  'manufacturers and are vulnerable to side-channel attacks.',
                                  'The schemes proposed in this dissertation (ECC-DTB-AKA and '
                                  'ECC-HISE) complement rather than replace these emerging '
                                  'approaches. ECC-DTB-AKA secures the client-server channel; '
                                  'ECC-HISE secures server-server batch data; confidential '
                                  'computing can protect in-memory processing; and post-quantum '
                                  'algorithms will eventually replace specific ECC primitives as '
                                  'standards mature.']},
                  {'heading': '1.3.4 Integrity Versus Confidentiality in Compliance Narratives',
                   'paragraphs': ['Regulatory narratives often emphasize encryption in transit and '
                                  'at rest. Integrity and non-repudiation receive comparatively '
                                  'less operational instrumentation, despite equal importance for '
                                  'settlement disputes and forensic readiness. Hash manifests '
                                  'without signatures are forgeable by anyone who can rewrite '
                                  'storage; signatures without binding to a batch structure allow '
                                  'selective dropping of records if receivers do not enforce '
                                  'cardinality checks.',
                                  'A sound integrity architecture needs: authenticated encryption '
                                  'or encrypt-then-MAC/sign discipline; binding to batch '
                                  'identifiers; protection of ordering; and efficient third-party '
                                  "verification. Chapter 3's ECC-HISE is evaluated explicitly "
                                  'against this checklist.']},
                  {'heading': '1.3.5 Cross-Border Settlement and Multi-Party Trust',
                   'paragraphs': ['Cross-border payments introduce additional custodians: '
                                  'correspondent banks, market infrastructures, and messaging '
                                  'networks. Each hop may terminate encryption and re-protect '
                                  'under local policy. Cryptographic commitments that survive '
                                  'hops—signed Merkle roots anchored to originator keys—reduce '
                                  'dispute ambiguity when a later hop alters content. While this '
                                  'dissertation focuses on bilateral envelopes suitable for '
                                  'bank-to-bank or bank-to-clearing interfaces, the same '
                                  'commitments can be shared with supervisory authorities as '
                                  'compact evidence.']}]},
 {'heading': '1.4 Threat Model, Assumptions, and Research Questions',
  'paragraphs': ['This section formalizes the threat model, system assumptions, and research '
                 'questions that guide the design and evaluation of the proposed schemes in '
                 'Chapters 2 through 5.'],
  'subsections': [{'heading': '1.4.1 Threat Model',
                   'paragraphs': ['We adopt a Dolev-Yao threat model extended with '
                                  'financial-domain adversary capabilities. The adversary A can: '
                                  '(a) eavesdrop on, insert, delete, modify, and replay messages '
                                  'on all network channels; (b) compromise up to N-1 of M server '
                                  'nodes in the settlement network (where M > 2N-1 for quorum '
                                  'systems, but we do not assume quorum); (c) extract session '
                                  'tokens and application data from a compromised client device; '
                                  '(d) perform offline dictionary attacks on captured password '
                                  'hashes (but not on ECDH ephemeral private keys due to '
                                  'computational hardness); (e) submit fraudulent transaction '
                                  'requests using stolen credentials.',
                                  'The adversary A cannot: (a) break the elliptic curve discrete '
                                  'logarithm problem (ECDLP) or compute discrete logarithms on the '
                                  'chosen curve; (b) break SHA-256, AES-256-GCM, or Ed25519 '
                                  'unforgeability; (c) extract private keys from an HSM (in the '
                                  'prototype, HSM is simulated and this assumption is noted as a '
                                  "limitation); (d) physically access the bank's data center "
                                  'without detection.',
                                  "Trust assumptions: the bank's certificate authority (CA) is "
                                  'trusted; registered client public keys are distributed securely '
                                  'during account enrollment; the clearing-house master key is '
                                  'generated and stored in an HSM at setup time.'],
                   'figure': 'Threat model diagram showing adversary position relative to client, '
                             'bank server, and inter-bank network (Figure 1.5).'},
                  {'heading': '1.4.2 System Assumptions',
                   'paragraphs': ['The e-banking system under consideration comprises: (1) a '
                                  'client application running on a smartphone or desktop with a '
                                  'secure element or trusted execution environment for key '
                                  'storage; (2) a bank application server providing RESTful APIs '
                                  'for account management and transaction authorization; (3) a '
                                  'settlement server participating in inter-bank batch transfer; '
                                  '(4) a clearing-house authority managing the master key '
                                  'hierarchy.',
                                  'Clients and servers have synchronized clocks within ±5 minutes '
                                  '(for timestamp validation and nonce freshness). Network '
                                  'connectivity is intermittent but eventually available. The '
                                  'elliptic curve used is SECP256R1 (NIST P-256) for ECDH/ECDSA '
                                  'operations and Ed25519 for batch signatures, unless otherwise '
                                  'noted.']},
                  {'heading': '1.4.3 Research Questions',
                   'paragraphs': ['RQ1: Can an ECC-based authenticated key agreement protocol that '
                                  'binds session keys to device fingerprints and transaction '
                                  'nonces overcome the authentication limitations identified in '
                                  'Section 1.2 while maintaining or improving communication '
                                  'efficiency?',
                                  'RQ2: Can a hierarchical ECC-based secure envelope scheme with '
                                  'Merkle audit chains address the data-security limitations '
                                  'identified in Section 1.3 for server-server batch transfer in '
                                  'e-finance systems?',
                                  'RQ3: How do the proposed schemes compare quantitatively to '
                                  'existing approaches (TLS 1.3, standard ECDH, ECIES, static PSK) '
                                  'in terms of authentication latency, ciphertext overhead, '
                                  'communication round trips, and resistance to attacks cataloged '
                                  'in Section 1.1?',
                                  'RQ4: Can both schemes be implemented in a unified e-financial '
                                  'service architecture and validated through programmatic testing '
                                  'and benchmark measurement?']},
                  {'heading': '1.4.4 Chapter Summary',
                   'paragraphs': ['This chapter has defined and categorized attack mechanisms '
                                  'against e-banking and e-finance systems, presented case studies '
                                  'demonstrating their real-world impact, reviewed current '
                                  'authentication and key-exchange mechanisms with six identified '
                                  'limitations (Section 1.2), reviewed current data encryption and '
                                  'integrity mechanisms with six identified limitations (Section '
                                  '1.3), and formalized the threat model and research questions '
                                  'guiding this dissertation. The identified limitations provide '
                                  'direct motivation for the two novel ECC-based schemes developed '
                                  'in Chapters 2 and 3, whose prior-work context is further '
                                  'elaborated in Chapter 5.']},
                  {'heading': '1.4.5 Security Requirements Derivation',
                   'paragraphs': ['From the threat model (Section 1.4.1) and the identified '
                                  'limitations (Sections 1.2.3 and 1.3.3), we derive the following '
                                  'security requirements that the proposed schemes must satisfy. '
                                  'These requirements serve as evaluation criteria in Chapter 5.',
                                  'SR1 (Mutual Authentication): Both communicating parties must '
                                  "cryptographically verify each other's identity before any "
                                  'financial data is exchanged. For client-server channels, this '
                                  "means the client verifies the bank server's identity via "
                                  "certificate chain, and the server verifies the client's "
                                  'identity via registered public key signature.',
                                  'SR2 (Forward Secrecy): Compromise of long-term private keys '
                                  'must not enable decryption of previously recorded sessions. '
                                  'Ephemeral ECDH key pairs must be used for session key '
                                  'establishment.',
                                  'SR3 (Device Binding): Session keys must be cryptographically '
                                  'bound to the client device, preventing session transfer to '
                                  'unauthorized devices even if session tokens are exfiltrated.',
                                  'SR4 (Transaction Binding): Individual transactions must be '
                                  'protected by keys derived specifically for that transaction, '
                                  'limiting the impact of single-transaction key compromise.',
                                  'SR5 (Data Confidentiality): Financial records in server-server '
                                  'batch transfer must be encrypted with semantically secure '
                                  'authenticated encryption.',
                                  'SR6 (Data Integrity): Any modification to batch records must be '
                                  'detectable through cryptographic verification, with batch-level '
                                  'integrity proofs enabling efficient audit.',
                                  'SR7 (Non-Repudiation): Batch senders must not be able to deny '
                                  'having sent a batch, achieved through digital signatures on '
                                  'batch headers.',
                                  'SR8 (Efficiency): Authentication must complete within '
                                  'acceptable latency bounds (target: under 200ms on commodity '
                                  'hardware) with minimal communication overhead.']},
                  {'heading': '1.4.6 Relationship to Subsequent Chapters',
                   'paragraphs': ['The security requirements SR1 through SR4 are addressed '
                                  'primarily by the ECC-DTB-AKA protocol developed in Chapter 2. '
                                  'Requirements SR5 through SR7 are addressed by the ECC-HISE '
                                  'scheme developed in Chapter 3. Requirement SR8 is evaluated '
                                  'quantitatively in Chapters 2, 3, and 5 through benchmark '
                                  'measurements of the prototype described in Chapter 4.',
                                  'Chapter 5 provides the comprehensive prior-work analysis '
                                  'specified in the dissertation requirements: Section 5.2 reviews '
                                  'authentication and key-exchange literature in depth (expanding '
                                  'on the overview in Section 1.2), Section 5.3 reviews data '
                                  'encryption and integrity literature (expanding on Section 1.3), '
                                  'and Section 5.4 synthesizes findings to demonstrate how the '
                                  'proposed schemes address the vulnerabilities cataloged in this '
                                  'chapter.',
                                  'Readers approaching this dissertation from a practitioner '
                                  'perspective may wish to read Section 1.1 and Sections '
                                  '1.2.3/1.3.3 first to understand the threat landscape and '
                                  'identified gaps, then proceed to Chapters 2 and 3 for protocol '
                                  'specifications, and Chapter 4 for implementation guidance. '
                                  'Readers with a research orientation may prefer to read Chapter '
                                  "5's prior-work analysis before the proposed schemes, to situate "
                                  'the contributions within the existing literature.']},
                  {'heading': '1.4.5 Security Requirements SR1–SR8 (Consolidated)',
                   'paragraphs': ['For reference in later chapters, the consolidated security '
                                  'requirements are: SR1 mutual authentication on client-server '
                                  'key establishment; SR2 forward secrecy for session keys; SR3 '
                                  'cryptographic device binding; SR4 per-transaction key '
                                  'separation; SR5 confidentiality of server-server batch records; '
                                  'SR6 authenticity of batch origin; SR7 integrity and ordering of '
                                  'batch membership; SR8 efficient third-party audit of inclusion. '
                                  'ECC-DTB-AKA targets SR1–SR4; ECC-HISE targets SR5–SR8; the '
                                  'dual-layer methodology targets their joint satisfaction in one '
                                  'e-finance architecture.']},
                  {'heading': '1.4.6 Scope Boundaries',
                   'paragraphs': ['Out of scope: physical ATM/card-present EMV protocol redesign; '
                                  'hardware side-channel evaluation of ECC implementations; '
                                  'large-scale user studies; full machine-checked proofs; and '
                                  'post-quantum drop-in replacements (discussed as future work). '
                                  'In scope: protocol design, analytical security argumentation, '
                                  'prototype implementation, and comparative evaluation against '
                                  'representative baselines.']}]}]
