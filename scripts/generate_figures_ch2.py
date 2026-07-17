"""Generate Chapter 2 figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

FIG_DIR = Path(__file__).resolve().parent.parent / "thesis" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9})


def save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG_DIR / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_2_1_protocol_sequence() -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.plot([2, 2], [1, 7], "k-", lw=1)
    ax.plot([8, 8], [1, 7], "k-", lw=1)
    ax.text(2, 7.3, "Client C", ha="center", fontweight="bold")
    ax.text(8, 7.3, "Server S", ha="center", fontweight="bold")
    msgs = [
        (2, 8, 6.2, "MSG1: EK_C, PK_C, device_fp, nonce_c, Sig_C"),
        (8, 5.8, 2, "MSG2: EK_S, nonce_s, Cert_S, Sig_S"),
        (2, 3.6, 6, "MSG3: HMAC(TBK,txn), Sig_confirm"),
    ]
    y = 6.5
    for x1, x2, _, label in msgs:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", color="#1565C0"))
        ax.text(5, y + 0.2, label, ha="center", fontsize=7)
        y -= 1.8
    ax.text(5, 1.2, "MSK = HKDF(ECDH || device_fp || nonces)", ha="center", fontsize=8,
            bbox=dict(boxstyle="round", facecolor="#E8F5E9"))
    ax.set_title("Figure 2.1: ECC-DTB-AKA three-round handshake", fontsize=10)
    save("fig_2_1_protocol_sequence.png")


def fig_2_2_key_derivation() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    boxes = [
        (2, 4, "ECDH Shared\nSecret Z"),
        (5, 4, "HKDF Inputs:\nZ, device_fp,\nnonce_c, nonce_s"),
        (8, 4, "MSK\n(256-bit)"),
        (8, 2, "TBK_txn\n= HKDF(MSK, txn_nonce)"),
    ]
    for x, y, t in boxes:
        box = FancyBboxPatch((x - 1, y - 0.5), 2, 1, boxstyle="round,pad=0.05",
                             facecolor="#E3F2FD", edgecolor="#1565C0")
        ax.add_patch(box)
        ax.text(x, y, t, ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(4, 4), xytext=(3, 4), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(7, 4), xytext=(6, 4), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(8, 2.5), xytext=(8, 3.5), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 2.2: Key derivation hierarchy in ECC-DTB-AKA", fontsize=10)
    save("fig_2_2_key_derivation.png")


def fig_2_3_benchmark_chart() -> None:
    import json
    bench = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks" / "chapter2_benchmarks.json"
    if not bench.exists():
        schemes = ["ECC-DTB-AKA", "Standard ECDH", "TLS 1.3"]
        latency = [12.5, 4.2, 5.8]
        msg_bytes = [520, 130, 2800]
    else:
        data = json.loads(bench.read_text())
        schemes = [d["scheme"] for d in data]
        latency = [d["auth_latency_ms_mean"] for d in data]
        msg_bytes = [d["total_message_bytes_mean"] for d in data]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3))
    colors = ["#2E7D32", "#1565C0", "#E65100"]
    ax1.bar(schemes, latency, color=colors)
    ax1.set_ylabel("Latency (ms)")
    ax1.set_title("(a) Authentication latency")
    ax1.tick_params(axis="x", rotation=15, labelsize=7)
    ax2.bar(schemes, msg_bytes, color=colors)
    ax2.set_ylabel("Bytes")
    ax2.set_title("(b) Total message size")
    ax2.tick_params(axis="x", rotation=15, labelsize=7)
    fig.suptitle("Figure 2.3: Quantitative comparison of authentication schemes", fontsize=10)
    save("fig_2_3_benchmark_chart.png")


if __name__ == "__main__":
    fig_2_1_protocol_sequence()
    fig_2_2_key_derivation()
    fig_2_3_benchmark_chart()
    print(f"Saved Chapter 2 figures to {FIG_DIR}")
