"""Download all openly available thesis reference PDFs.

Commercial books and paywalled standards are recorded as skipped (not pirated).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "references" / "pdfs"
OUT.mkdir(parents=True, exist_ok=True)

# Each entry: ref, slug, note, urls (tried in order), or skip_reason if none
# Ref numbers are 1-based bibliography indices.
CATALOG: list[dict] = [
    {
        "ref": 1,
        "slug": "RFC8446_TLS_1.3",
        "note": "TLS 1.3",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc8446.pdf",
            "https://www.rfc.fr/rfc/en/rfc8446.pdf",
        ],
    },
    {
        "ref": 2,
        "slug": "NIST_SP800-38D_GCM",
        "note": "AES-GCM",
        "urls": [
            "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf",
        ],
    },
    {
        "ref": 3,
        "slug": "NIST_SP800-57pt1r5_Key_Management",
        "note": "NIST key management",
        "urls": [
            "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf",
        ],
    },
    {
        "ref": 4,
        "slug": "RFC5280_X509_PKI",
        "note": "X.509 PKI / CRL profile",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc5280.pdf",
            "https://www.rfc.fr/rfc/en/rfc5280.pdf",
        ],
    },
    {
        "ref": 5,
        "slug": "Krawczyk_HKDF_CRYPTO2010",
        "note": "HKDF CRYPTO paper",
        "urls": [
            "https://eprint.iacr.org/2010/264.pdf",
            "https://www.iacr.org/archive/crypto2010/62230145/62230145.pdf",
        ],
    },
    {
        "ref": 6,
        "slug": "RFC5869_HKDF",
        "note": "HKDF RFC",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc5869.pdf",
            "https://www.rfc.fr/rfc/en/rfc5869.pdf",
        ],
    },
    {
        "ref": 7,
        "slug": "Bellare_Rogaway_Entity_Auth",
        "note": "Entity authentication / key distribution",
        "urls": [
            "https://cseweb.ucsd.edu/~mihir/papers/eakd.pdf",
            "https://www.cs.ucdavis.edu/~rogaway/papers/eakd-extended.pdf",
        ],
    },
    {
        "ref": 8,
        "slug": "Canetti_Krawczyk_Key_Exchange",
        "note": "CK key-exchange model",
        "urls": [
            "https://eprint.iacr.org/2001/040.pdf",
            "https://iacr.org/archive/eurocrypt2001/20450383.pdf",
            "https://www.iacr.org/archive/eurocrypt2001/20450383.pdf",
        ],
    },
    {
        "ref": 9,
        "slug": "Johnson_Menezes_Vanstone_ECDSA",
        "note": "ECDSA survey",
        "urls": [
            "https://cacr.uwaterloo.ca/techreports/1999/corr99-34.pdf",
            "https://www.cacr.math.uwaterloo.ca/techreports/1999/corr99-34.pdf",
        ],
    },
    {
        "ref": 10,
        "slug": "RFC8032_Ed25519",
        "note": "Ed25519 / EdDSA",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc8032.pdf",
            "https://www.rfc.fr/rfc/en/rfc8032.pdf",
        ],
    },
    {
        "ref": 11,
        "slug": "SEC1_Elliptic_Curve_Cryptography",
        "note": "SEC 1 ECC",
        "urls": [
            "https://www.secg.org/sec1-v2.pdf",
            "https://web.archive.org/web/20240000000000/https://www.secg.org/sec1-v2.pdf",
            "https://web.archive.org/web/20190414183407/https://www.secg.org/sec1-v2.pdf",
        ],
    },
    {
        "ref": 12,
        "slug": "ANSI_X9.63",
        "note": "ANSI X9.63",
        "skip": "Paywalled ANSI standard (purchase required)",
    },
    {
        "ref": 13,
        "slug": "RFC6749_OAuth2",
        "note": "OAuth 2.0",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc6749.pdf",
            "https://www.rfc.fr/rfc/en/rfc6749.pdf",
        ],
    },
    {
        "ref": 14,
        "slug": "RFC8252_OAuth_Native_Apps",
        "note": "OAuth for native apps / PKCE guidance",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc8252.pdf",
            "https://www.rfc.fr/rfc/en/rfc8252.pdf",
        ],
    },
    {
        "ref": 15,
        "slug": "W3C_WebAuthn",
        "note": "WebAuthn Level 2",
        "urls": [
            "https://www.w3.org/TR/webauthn-2/",
        ],
        "accept_html": True,
        "ext": ".html",
    },
    {
        "ref": 16,
        "slug": "EMVCo_Book2",
        "note": "EMV Book 2",
        "skip": "EMVCo specs require free registration / not direct-linkable",
    },
    {
        "ref": 17,
        "slug": "PCI_DSS_v4",
        "note": "PCI DSS v4.0",
        "urls": [
            "https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0.pdf",
            "https://listings.pcisecuritystandards.org/documents/PCI-DSS-v4_0.pdf",
        ],
    },
    {
        "ref": 18,
        "slug": "EU_PSD2_2015_2366",
        "note": "PSD2 directive",
        "urls": [
            "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32015L2366",
            "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L:2015:337:FULL",
        ],
    },
    {
        "ref": 19,
        "slug": "ISO_IEC_27001_2022",
        "note": "ISO/IEC 27001:2022",
        "skip": "Paywalled ISO standard (purchase required)",
    },
    {
        "ref": 20,
        "slug": "SWIFT_CSP",
        "note": "SWIFT CSP",
        "skip": "SWIFT CSP handbook requires SWIFT portal access",
    },
    {
        "ref": 21,
        "slug": "IBM_Cost_of_Data_Breach_2024",
        "note": "IBM Cost of a Data Breach 2024",
        "urls": [
            "https://www.ibm.com/downloads/documents/us-en/107a02e94948aa8c",
            "https://www.ibm.com/reports/data-breach",
        ],
        "accept_html": True,
        "ext": ".html",
    },
    {
        "ref": 22,
        "slug": "Verizon_DBIR_2024",
        "note": "Verizon DBIR 2024",
        "urls": [
            "https://www.verizon.com/business/resources/TXlp/reports/2024-dbir-data-breach-investigations-report.pdf",
            "https://www.verizon.com/business/resources/reports/dbir/",
        ],
    },
    {
        "ref": 23,
        "slug": "OWASP_API_Security_Top10_2023",
        "note": "OWASP API Security Top 10",
        "urls": [
            "https://owasp.org/API-Security/editions/2023/en/0x00-header/",
            "https://raw.githubusercontent.com/OWASP/API-Security/master/2023/en/dist/owasp-api-security-top-10.pdf",
            "https://github.com/OWASP/API-Security/raw/master/2023/en/dist/owasp-api-security-top-10.pdf",
        ],
    },
    {
        "ref": 24,
        "slug": "Bangladesh_Bank_SWIFT_Heist",
        "note": "Bangladesh Bank SWIFT heist analysis",
        "skip": "No single canonical public investigation PDF; incident is cited from secondary sources",
    },
    {
        "ref": 25,
        "slug": "Kaspersky_Carbanak",
        "note": "Carbanak / Great Bank Robbery",
        "urls": [
            "https://media.kasperskycontenthub.com/wp-content/uploads/sites/43/2018/03/08064518/Carbanak_APT_eng.pdf",
            "https://securelist.com/the-great-bank-robbery-the-carbanak-apt/68732/",
        ],
    },
    {
        "ref": 26,
        "slug": "FIPS186-5_Digital_Signatures",
        "note": "FIPS 186-5",
        "urls": [
            "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf",
        ],
    },
    {
        "ref": 27,
        "slug": "FIPS180-4_Secure_Hash",
        "note": "FIPS 180-4 SHS",
        "urls": [
            "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf",
        ],
    },
    {
        "ref": 28,
        "slug": "NIST_SP800-52r2_TLS",
        "note": "NIST SP 800-52 Rev. 2 TLS",
        "urls": [
            "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf",
        ],
    },
    {
        "ref": 29,
        "slug": "NIST_SP800-56Ar3_Key_Establishment",
        "note": "NIST SP 800-56A Rev. 3",
        "urls": [
            "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Ar3.pdf",
        ],
    },
    {
        "ref": 30,
        "slug": "Merkle_Digital_Signature_CRYPTO1987",
        "note": "Merkle digital signatures / trees",
        "urls": [
            "https://link.springer.com/content/pdf/10.1007/3-540-48184-5_21.pdf",
            "https://www.ralphmerkle.com/papers/Thesis1982.pdf",
        ],
    },
    {
        "ref": 31,
        "slug": "Bitcoin_Whitepaper",
        "note": "Bitcoin whitepaper",
        "urls": [
            "https://bitcoin.org/bitcoin.pdf",
        ],
    },
    {
        "ref": 32,
        "slug": "Corda_Introduction",
        "note": "Corda introduction",
        "urls": [
            "https://www.r3.com/wp-content/uploads/2017/01/corda-platform-whitepaper.pdf",
            "https://docs.r3.com/_/downloads/en/platform/pdf/",
            "https://www.corda.net/wp-content/uploads/2016/11/corda-introductory-whitepaper.pdf",
            "https://web.archive.org/web/20170329200347/https://www.corda.net/wp-content/uploads/2016/11/corda-introductory-whitepaper.pdf",
        ],
    },
    {
        "ref": 33,
        "slug": "Diffie_Hellman_New_Directions",
        "note": "Diffie–Hellman 1976",
        "urls": [
            "https://ee.stanford.edu/~hellman/publications/24.pdf",
            "https://www-ee.stanford.edu/~hellman/publications/24.pdf",
        ],
    },
    {
        "ref": 34,
        "slug": "Miller_Elliptic_Curves_CRYPTO1985",
        "note": "Miller ECC CRYPTO 1985",
        "urls": [
            "https://link.springer.com/content/pdf/10.1007/3-540-39757-4_20.pdf",
            "https://web.northeastern.edu/seigen/CSG713Spr08/Papers/Miller85.pdf",
        ],
    },
    {
        "ref": 35,
        "slug": "Koblitz_Elliptic_Curve_Cryptosystems",
        "note": "Koblitz ECC 1987",
        "urls": [
            "https://www.ams.org/journals/mcom/1987-48-177/S0025-5718-1987-0866109-5/S0025-5718-1987-0866109-5.pdf",
        ],
    },
    {
        "ref": 36,
        "slug": "Boneh_Franklin_IBE",
        "note": "Boneh–Franklin IBE",
        "urls": [
            "https://eprint.iacr.org/2001/090.pdf",
            "https://crypto.stanford.edu/~dabo/papers/bfibe.pdf",
        ],
    },
    {
        "ref": 37,
        "slug": "Bellare_Namprempre_Authenticated_Encryption",
        "note": "Authenticated encryption notions",
        "urls": [
            "https://eprint.iacr.org/2000/025.pdf",
            "https://cseweb.ucsd.edu/~mihir/papers/oem.pdf",
        ],
    },
    {
        "ref": 38,
        "slug": "Dolev_Yao_Public_Key_Protocols",
        "note": "Dolev–Yao model",
        "urls": [
            "https://www.cs.huji.ac.il/~dolev/pubs/dolev-yao-ieee-1983.pdf",
            "https://web.cs.ucdavis.edu/~rogaway/classes/227/spring05/papers/dolevyao.pdf",
        ],
    },
    {
        "ref": 39,
        "slug": "Gennaro_SSL3_Analysis",
        "note": "SSL 3.0 analysis",
        "urls": [
            "https://www.usenix.org/legacy/publications/library/proceedings/ec96/full_papers/wagner/wagner.pdf",
            "https://crypto.stanford.edu/~dabo/pubs/papers/ssl-analysis.pdf",
        ],
    },
    {
        "ref": 40,
        "slug": "Rescorla_SSL_TLS_Book",
        "note": "SSL and TLS (Addison-Wesley)",
        "skip": "Commercial book (copyrighted)",
    },
    {
        "ref": 41,
        "slug": "Handbook_Applied_Cryptography",
        "note": "Handbook of Applied Cryptography",
        "urls": [
            "https://cacr.uwaterloo.ca/hac/about/chap1.pdf",
        ],
        "skip": "Full book is commercial; free chapter PDFs exist at cacr.uwaterloo.ca/hac/ (not auto-bundled)",
    },
    {
        "ref": 42,
        "slug": "Katz_Lindell_Modern_Cryptography",
        "note": "Introduction to Modern Cryptography",
        "skip": "Commercial book (copyrighted)",
    },
    {
        "ref": 43,
        "slug": "Stallings_Cryptography_Network_Security",
        "note": "Cryptography and Network Security",
        "skip": "Commercial book (copyrighted)",
    },
    {
        "ref": 44,
        "slug": "Anderson_Security_Engineering",
        "note": "Security Engineering (Anderson)",
        "urls": [
            "https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch1-7.pdf",
            "https://www.cl.cam.ac.uk/~rja14/book.html",
        ],
        # Author freely publishes chapters; grab overview page if PDF fails
        "accept_html": True,
        "ext": ".html",
    },
    {
        "ref": 45,
        "slug": "Schneier_Applied_Cryptography",
        "note": "Applied Cryptography",
        "skip": "Commercial book (copyrighted)",
    },
    {
        "ref": 46,
        "slug": "Ferguson_Schneier_Kohno_Cryptography_Engineering",
        "note": "Cryptography Engineering",
        "skip": "Commercial book (copyrighted)",
    },
    {
        "ref": 47,
        "slug": "Gordon_Security_Breaches_Stock_Market",
        "note": "Security breaches / stock market",
        "urls": [
            "https://www.sciencedirect.com/science/article/pii/S0167404811000453/pdfft",
        ],
        "skip": "Likely paywalled journal article; no stable open PDF confirmed",
    },
    {
        "ref": 48,
        "slug": "Ponemon_Cost_Cyber_Crime_Financial",
        "note": "Ponemon / Accenture cyber cost study",
        "urls": [
            "https://www.accenture.com/content/dam/accenture/final/accenture-com/document-2/Accenture-State-of-Cybersecurity-2023.pdf",
            "https://www.accenture.com/_acnmedia/PDF-165/Accenture-State-of-Cybersecurity-2023.pdf",
        ],
    },
    {
        "ref": 49,
        "slug": "BIS_PFMI",
        "note": "Principles for Financial Market Infrastructures",
        "urls": [
            "https://www.bis.org/cpmi/publ/d101a.pdf",
            "https://www.bis.org/cpmi/publ/d101.pdf",
        ],
    },
    {
        "ref": 50,
        "slug": "ECB_Internal_Models_Operational_Risk",
        "note": "ECB guide to internal models",
        "urls": [
            "https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.guidetointernalmodels_consolidated_202110~1d2e3e5b71.en.pdf",
            "https://www.bankingsupervision.europa.eu/ecb/pub/pdf/ssm.supervisory_guides202110_internalmodels.en.pdf",
        ],
    },
    {
        "ref": 51,
        "slug": "Basel_Operational_Risk_Sound_Practices",
        "note": "Basel operational risk sound practices",
        "urls": [
            "https://www.bis.org/publ/bcbs96.pdf",
            "https://www.bis.org/bcbs/publ/d424.pdf",
            "https://www.bis.org/bcbs/publ/d515.pdf",
        ],
    },
    {
        "ref": 52,
        "slug": "Open_Banking_UK_Security_Profile",
        "note": "Open Banking UK security profile",
        "urls": [
            "https://openbanking.atlassian.net/wiki/spaces/DZ/pages/1078036530/Read+Write+Data+API+Specification+-+v3.1.10",
            "https://standards.openbanking.org.uk/",
        ],
        "accept_html": True,
        "ext": ".html",
    },
    {
        "ref": 53,
        "slug": "CSA_Cloud_Security_Guidance_v4",
        "note": "CSA Security Guidance v4",
        "urls": [
            "https://cloudsecurityalliance.org/artifacts/security-guidance-v4",
            "https://downloads.cloudsecurityalliance.org/artifacts/security-guidance-v4.pdf",
        ],
    },
    {
        "ref": 54,
        "slug": "NIST_PQC_ML-KEM_ML-DSA",
        "note": "NIST PQC (FIPS 203/204)",
        "urls": [
            "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf",
            "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf",
        ],
        # download first URL as primary; second saved as companion if first ok
        "also": [
            (
                "54b_NIST_FIPS204_ML-DSA.pdf",
                "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf",
            )
        ],
    },
    {
        "ref": 55,
        "slug": "Bernstein_Curve25519",
        "note": "Curve25519",
        "urls": [
            "https://cr.yp.to/ecdh/curve25519-20060209.pdf",
            "https://www.iacr.org/archive/pkc2006/39580001/39580001.pdf",
        ],
    },
    {
        "ref": 56,
        "slug": "IEEE_1363a_ECIES",
        "note": "IEEE 1363a",
        "skip": "Paywalled IEEE standard (purchase required)",
    },
    {
        "ref": 57,
        "slug": "ANSI_X9.102_Key_Wrap",
        "note": "ANSI X9.102",
        "skip": "Paywalled ANSI standard (purchase required)",
    },
    {
        "ref": 58,
        "slug": "RFC5652_CMS",
        "note": "Cryptographic Message Syntax",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc5652.pdf",
            "https://www.rfc.fr/rfc/en/rfc5652.pdf",
        ],
    },
    {
        "ref": 59,
        "slug": "RFC8017_PKCS1",
        "note": "PKCS #1 RSA",
        "urls": [
            "http://www.rfc.fr/rfc/en/rfc8017.pdf",
            "https://www.rfc.fr/rfc/en/rfc8017.pdf",
        ],
    },
    {
        "ref": 60,
        "slug": "Goodrich_Tamassia_Algorithm_Design",
        "note": "Algorithm Design and Applications",
        "skip": "Commercial book (copyrighted)",
    },
    {
        "ref": 61,
        "slug": "Camenisch_Lysyanskaya_Anonymous_Credentials",
        "note": "Anonymous credentials",
        "urls": [
            "https://eprint.iacr.org/2001/019.pdf",
            "https://www.iacr.org/archive/eurocrypt2001/20450093.pdf",
        ],
    },
    {
        "ref": 62,
        "slug": "Bhargavan_Triple_Handshakes_TLS",
        "note": "Triple handshakes (TLS)",
        "urls": [
            "https://www.mitls.org/downloads/tls13-paper.pdf",
            "https://hal.inria.fr/hal-01102259/document",
            "https://www.ieee-security.org/TC/SP2014/papers/TripleHandshakesandCookieCutters_BreakingandFixingAuthenticationoverTLS.pdf",
        ],
    },
    {
        "ref": 63,
        "slug": "Dennis_EBanking_Security_Survey",
        "note": "E-banking security survey",
        "skip": "Paywalled Computers & Security article; no confirmed open PDF",
    },
    {
        "ref": 64,
        "slug": "Aloul_Online_Banking_Security",
        "note": "Online banking security measures",
        "urls": [
            "https://www.aus.edu/sites/default/files/pages/files/online_banking_security_measures_and_vulnerabilities.pdf",
            "https://www.researchgate.net/publication/224230291_Online_Banking_Security_Measures_and_Vulnerabilities",
        ],
    },
    {
        "ref": 65,
        "slug": "Ruiter_Poll_TLS_State_Fuzzing",
        "note": "Protocol state fuzzing of TLS",
        "urls": [
            "https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-de-ruiter.pdf",
            "https://www.cs.ru.nl/~erikpoll/papers/usenix2015.pdf",
        ],
    },
    {
        "ref": 66,
        "slug": "Cremers_TAMARIN_Prover",
        "note": "TAMARIN prover",
        "urls": [
            "https://tamarin-prover.github.io/manual/tex/tamarin-manual.pdf",
            "https://people.inf.ethz.ch/cremersc/publications/files/cav2013.pdf",
            "https://link.springer.com/content/pdf/10.1007/978-3-642-39799-8_43.pdf",
        ],
    },
    {
        "ref": 67,
        "slug": "Blanchet_ProVerif",
        "note": "ProVerif / applied pi calculus",
        "urls": [
            "https://bblanche.gitlabpages.inria.fr/publications/BlanchetFoundTrendsPrivacySecurity16.pdf",
            "https://prosecco.gforge.inria.fr/personal/bblanche/publications/BlanchetFoundTrendsPrivacySecurity16.pdf",
            "https://www.di.ens.fr/~blanchet/publications/BlanchetFoundTrendsPrivacySecurity16.pdf",
        ],
    },
]


def safe_filename(ref: int, slug: str, ext: str = ".pdf") -> str:
    return f"{ref:02d}_{slug}{ext}"


def curl_download(url: str, dest: Path, timeout: int = 90) -> tuple[bool, str, bytes]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = [
        "curl.exe",
        "-sL",
        "-A",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "-o",
        str(tmp),
        "--max-time",
        str(timeout),
        "-w",
        "%{http_code}",
        url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        code = (proc.stdout or "").strip() or "?"
        if not tmp.exists():
            return False, f"HTTP {code} no file", b""
        data = tmp.read_bytes()
        tmp.unlink(missing_ok=True)
        return True, f"HTTP {code}", data
    except Exception as e:
        tmp.unlink(missing_ok=True)
        return False, str(e), b""


def is_pdf(data: bytes) -> bool:
    return data[:4] == b"%PDF"


def is_html(data: bytes) -> bool:
    head = data[:400].lower()
    return b"<!doctype" in head or b"<html" in head


def try_save(entry: dict) -> dict:
    ref = entry["ref"]
    note = entry["note"]
    if entry.get("skip") and not entry.get("urls"):
        return {
            "ref": ref,
            "ok": False,
            "skipped": True,
            "note": note,
            "detail": entry["skip"],
            "file": None,
            "url": None,
        }

    urls = entry.get("urls") or []
    accept_html = bool(entry.get("accept_html"))
    ext = entry.get("ext", ".pdf")
    dest = OUT / safe_filename(ref, entry["slug"], ext)
    last_detail = "no urls"

    # Prefer keeping an already-valid PDF for this ref number
    for cand in sorted(OUT.glob(f"{ref:02d}_*.pdf")):
        if is_pdf(cand.read_bytes()[:8]):
            return {
                "ref": ref,
                "ok": True,
                "skipped": False,
                "note": note,
                "detail": f"already present ({cand.stat().st_size} bytes)",
                "file": cand.name,
                "url": "local",
            }

    for url in urls:
        ok, detail, data = curl_download(url, dest)
        if not ok or not data:
            last_detail = detail
            continue
        if is_pdf(data):
            pdf_dest = OUT / safe_filename(ref, entry["slug"], ".pdf")
            pdf_dest.write_bytes(data)
            result = {
                "ref": ref,
                "ok": True,
                "skipped": False,
                "note": note,
                "detail": f"{len(data)} bytes",
                "file": pdf_dest.name,
                "url": url,
            }
            # companions (e.g. FIPS 204)
            for fname, aurl in entry.get("also") or []:
                aok, _, adata = curl_download(aurl, OUT / fname)
                if aok and is_pdf(adata):
                    (OUT / fname).write_bytes(adata)
            return result
        if accept_html and is_html(data) and len(data) > 2000:
            dest.write_bytes(data)
            return {
                "ref": ref,
                "ok": True,
                "skipped": False,
                "note": note,
                "detail": f"HTML {len(data)} bytes (no PDF mirror)",
                "file": dest.name,
                "url": url,
            }
        # OWASP / github may return HTML redirect pages
        if b"%PDF" in data[:1024]:
            # sometimes BOM/prefix
            idx = data.find(b"%PDF")
            data = data[idx:]
            pdf_dest = OUT / safe_filename(ref, entry["slug"], ".pdf")
            pdf_dest.write_bytes(data)
            return {
                "ref": ref,
                "ok": True,
                "skipped": False,
                "note": note,
                "detail": f"{len(data)} bytes",
                "file": pdf_dest.name,
                "url": url,
            }
        last_detail = f"{detail}; not PDF (got {data[:20]!r}…, {len(data)} bytes)"

    if entry.get("skip"):
        return {
            "ref": ref,
            "ok": False,
            "skipped": True,
            "note": note,
            "detail": entry["skip"],
            "file": None,
            "url": None,
        }

    return {
        "ref": ref,
        "ok": False,
        "skipped": False,
        "note": note,
        "detail": last_detail,
        "file": None,
        "url": None,
    }


def write_index(results: list[dict]) -> None:
    ok = [r for r in results if r["ok"]]
    skipped = [r for r in results if r.get("skipped")]
    failed = [r for r in results if not r["ok"] and not r.get("skipped")]

    lines = [
        "# Thesis Reference Downloads",
        "",
        f"- **Downloaded:** {len(ok)} / {len(results)}",
        f"- **Skipped (paywall / commercial / no public file):** {len(skipped)}",
        f"- **Failed (URL tried, no usable file):** {len(failed)}",
        "",
        "## Downloaded",
        "",
        "| Ref | File | Note |",
        "|-----|------|------|",
    ]
    for r in ok:
        lines.append(f"| [{r['ref']}] | `{r['file']}` | {r['note']} |")

    lines += ["", "## Skipped", "", "| Ref | Reason |", "|-----|--------|"]
    for r in skipped:
        lines.append(f"| [{r['ref']}] {r['note']} | {r['detail']} |")

    if failed:
        lines += ["", "## Failed", "", "| Ref | Detail |", "|-----|--------|"]
        for r in failed:
            lines.append(f"| [{r['ref']}] {r['note']} | {r['detail']} |")

    lines += ["", "## Sources (successful)", ""]
    for r in ok:
        if r.get("url") and r["url"] != "local":
            lines.append(f"- **[{r['ref']}]** {r['url']}")
    lines.append("")

    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


def main() -> None:
    # Normalize older filenames that don't match slug pattern but are valid
    # (keep them; try_save detects any NN_*.pdf)

    results = []
    for entry in CATALOG:
        print(f"[{entry['ref']:02d}] {entry['slug']} ...", flush=True)
        r = try_save(entry)
        status = "OK" if r["ok"] else ("SKIP" if r.get("skipped") else "FAIL")
        print(f"     {status}: {r['detail']}", flush=True)
        results.append(r)

    write_index(results)
    ok_n = sum(1 for r in results if r["ok"])
    skip_n = sum(1 for r in results if r.get("skipped"))
    fail_n = len(results) - ok_n - skip_n
    print(f"\nDone: {ok_n} downloaded, {skip_n} skipped, {fail_n} failed -> {OUT}")


if __name__ == "__main__":
    main()
