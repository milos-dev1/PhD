"""Generate Chapter 5 evaluation figures."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

FIG_DIR = Path(__file__).resolve().parent.parent / "thesis" / "figures"
BENCH2 = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks" / "chapter2_benchmarks.json"
BENCH3 = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks" / "chapter3_benchmarks.json"
plt.rcParams.update({"font.family": "serif", "font.size": 9})


def save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG_DIR / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_5_1_attack_matrix() -> None:
    attacks = ["MITM", "Replay", "Session\nhijack", "Tampering", "Insider\naudit"]
    dtb = [5, 5, 5, 4, 3]
    hise = [5, 5, 0, 5, 5]
    x = np.arange(len(attacks))
    w = 0.35
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.bar(x - w / 2, dtb, w, label="ECC-DTB-AKA", color="#2E7D32")
    ax.bar(x + w / 2, hise, w, label="ECC-HISE", color="#1565C0")
    ax.set_ylabel("Resistance (1-5)")
    ax.set_xticks(x)
    ax.set_xticklabels(attacks, fontsize=8)
    ax.legend(fontsize=8)
    ax.set_title("Figure 5.1: Comparative attack resistance overview", fontsize=10)
    save("fig_5_1_attack_matrix.png")


def fig_5_2_combined_benchmark() -> None:
    if BENCH2.exists() and BENCH3.exists():
        b2 = json.loads(BENCH2.read_text())
        b3 = json.loads(BENCH3.read_text())
        auth_lat = next(d["auth_latency_ms_mean"] for d in b2 if d["scheme"] == "ECC-DTB-AKA")
        batch_lat = next(d["latency_ms_mean"] for d in b3 if d["scheme"] == "ECC-HISE" and d["records"] == 100)
    else:
        auth_lat, batch_lat = 0.52, 23.32
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(["ECC-DTB-AKA\n(auth ms)", "ECC-HISE\n(100 rec ms)"], [auth_lat, batch_lat], color=["#2E7D32", "#1565C0"])
    ax.set_ylabel("Milliseconds")
    ax.set_title("Figure 5.2: Combined quantitative performance of proposed schemes", fontsize=10)
    save("fig_5_2_combined_benchmark.png")


def fig_5_3_tls_handshake() -> None:
    fig, ax = plt.subplots(figsize=(7, 2.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")
    steps = ["ClientHello", "ServerHello\n+ Cert", "Finished", "App Data"]
    for i, s in enumerate(steps):
        x = 1 + i * 2.2
        ax.text(x, 1.5, s, ha="center", fontsize=8, bbox=dict(boxstyle="round", facecolor="#E3F2FD"))
        if i < 3:
            ax.annotate("", xy=(x + 1.5, 1.5), xytext=(x + 0.5, 1.5), arrowprops=dict(arrowstyle="<->", color="#333"))
    ax.set_title("Figure 5.3: TLS 1.3 full handshake flow", fontsize=10)
    save("fig_5_3_tls_handshake.png")


def fig_5_4_oauth_pkce() -> None:
    fig, ax = plt.subplots(figsize=(7, 2.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")
    for i, s in enumerate(["Auth Request", "User Login", "Auth Code", "Token Exchange", "API Call"]):
        x = 0.8 + i * 1.8
        ax.text(x, 1.5, s, ha="center", fontsize=7, bbox=dict(boxstyle="round", facecolor="#FFF3E0"))
        if i < 4:
            ax.annotate("", xy=(x + 1.2, 1.5), xytext=(x + 0.6, 1.5), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 5.4: OAuth 2.0 PKCE authorization flow", fontsize=10)
    save("fig_5_4_oauth_pkce.png")


def fig_5_5_mtls() -> None:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    for n, x, y in [("Service A", 2, 2), ("Service B", 5, 3), ("Service C", 8, 2)]:
        ax.text(x, y, n, ha="center", fontsize=8, bbox=dict(boxstyle="round", facecolor="#E8F5E9"))
    ax.plot([2, 5], [2.3, 2.7], "b--", alpha=0.6)
    ax.plot([5, 8], [2.7, 2.3], "b--", alpha=0.6)
    ax.text(3.5, 2.7, "mTLS", fontsize=7, color="#1565C0")
    ax.set_title("Figure 5.5: mTLS service mesh authentication", fontsize=10)
    save("fig_5_5_mtls.png")


def fig_5_6_tls_vs_envelope() -> None:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.text(2.5, 2.5, "TLS terminate\n→ plaintext\n→ re-encrypt", ha="center", fontsize=8, bbox=dict(boxstyle="round", facecolor="#FFEBEE"))
    ax.text(7.5, 2.5, "ECC-HISE\nenvelope persists\nintegrity", ha="center", fontsize=8, bbox=dict(boxstyle="round", facecolor="#E8F5E9"))
    ax.set_title("Figure 5.6: TLS record layer vs. persistent envelope integrity", fontsize=10)
    save("fig_5_6_tls_vs_envelope.png")


def fig_5_7_merkle_compare() -> None:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.text(2.5, 2, "Blockchain:\nMerkle + consensus\n(high latency)", ha="center", fontsize=8, bbox=dict(boxstyle="round", facecolor="#E3F2FD"))
    ax.text(7.5, 2, "ECC-HISE:\nMerkle + signatures\n(no consensus)", ha="center", fontsize=8, bbox=dict(boxstyle="round", facecolor="#FFF3E0"))
    ax.set_title("Figure 5.7: Merkle audit — blockchain vs. ECC-HISE", fontsize=10)
    save("fig_5_7_merkle_compare.png")


if __name__ == "__main__":
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig_5_1_attack_matrix()
    fig_5_2_combined_benchmark()
    fig_5_3_tls_handshake()
    fig_5_4_oauth_pkce()
    fig_5_5_mtls()
    fig_5_6_tls_vs_envelope()
    fig_5_7_merkle_compare()
    print(f"Saved Chapter 5 figures to {FIG_DIR}")
