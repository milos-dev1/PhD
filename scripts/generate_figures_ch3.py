"""Generate Chapter 3 figures."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

FIG_DIR = Path(__file__).resolve().parent.parent / "thesis" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9})


def save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG_DIR / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_3_1_hierarchy() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    boxes = [("Master Key (HSM)", 5, 4.2), ("Domain: Retail", 2.5, 2.8),
             ("Domain: Settlement", 7.5, 2.8), ("SK Batch N", 6, 1.2), ("SK Batch N+1", 9, 1.2)]
    for t, x, y in boxes:
        box = FancyBboxPatch((x - 1.2, y - 0.35), 2.4, 0.7, boxstyle="round,pad=0.05",
                             facecolor="#E8F5E9", edgecolor="#2E7D32")
        ax.add_patch(box)
        ax.text(x, y, t, ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(2.5, 3.15), xytext=(4.5, 3.85), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(7.5, 3.15), xytext=(5.5, 3.85), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(6, 1.55), xytext=(7.5, 2.45), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(9, 1.55), xytext=(7.5, 2.45), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 3.1: ECC-HISE hierarchical key structure", fontsize=10)
    save("fig_3_1_hierarchy.png")


def fig_3_2_envelope() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.5, 3.5), 9, 1, boxstyle="round,pad=0.05", facecolor="#E3F2FD", edgecolor="#1565C0"))
    ax.text(5, 4, "Batch Header: batch_id, epoch, Merkle Root, Sig_header", ha="center", fontsize=9)
    for i, x in enumerate([1.5, 4, 6.5]):
        ax.add_patch(FancyBboxPatch((x - 0.9, 1.2), 1.8, 1.8, boxstyle="round,pad=0.05", facecolor="#FFF3E0", edgecolor="#E65100"))
        ax.text(x, 2.3, f"Record {i+1}", ha="center", fontsize=8, fontweight="bold")
        ax.text(x, 1.9, "AES-GCM", ha="center", fontsize=7)
        ax.text(x, 1.6, "Ed25519 sig", ha="center", fontsize=7)
        ax.text(x, 1.3, "leaf hash", ha="center", fontsize=7)
    ax.set_title("Figure 3.2: ECC-HISE secure envelope with Merkle audit chain", fontsize=10)
    save("fig_3_2_envelope.png")


def fig_3_3_verify_flow() -> None:
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    steps = ["Receive\nBatch", "Verify\nHeader Sig", "Check\nMerkle Root", "Decrypt\nRecords", "Audit\nLog"]
    for i, s in enumerate(steps):
        x = 1 + i * 1.8
        ax.add_patch(FancyBboxPatch((x - 0.6, 1.5), 1.2, 0.9, boxstyle="round,pad=0.05", facecolor="#F3E5F5", edgecolor="#6A1B9A"))
        ax.text(x, 1.95, s, ha="center", va="center", fontsize=7)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 0.75, 1.95), xytext=(x + 0.6, 1.95), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 3.3: Server-server batch verification and audit flow", fontsize=10)
    save("fig_3_3_verify_flow.png")


def fig_3_4_benchmark() -> None:
    bench = Path(__file__).resolve().parent.parent / "thesis" / "benchmarks" / "chapter3_benchmarks.json"
    data = json.loads(bench.read_text()) if bench.exists() else []
    n100 = [d for d in data if d["records"] == 100]
    schemes = [d["scheme"].replace(" record layer only", "") for d in n100]
    lat = [d["latency_ms_mean"] for d in n100]
    sizes = [d["batch_bytes_mean"] for d in n100]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7, 3))
    a1.bar(schemes, lat, color=["#2E7D32", "#1565C0", "#E65100"])
    a1.set_title("(a) Latency (n=100)")
    a1.tick_params(axis="x", rotation=12, labelsize=6)
    a2.bar(schemes, sizes, color=["#2E7D32", "#1565C0", "#E65100"])
    a2.set_title("(b) Batch size (n=100)")
    a2.tick_params(axis="x", rotation=12, labelsize=6)
    fig.suptitle("Figure 3.4: ECC-HISE quantitative comparison", fontsize=10)
    save("fig_3_4_benchmark.png")


if __name__ == "__main__":
    fig_3_1_hierarchy()
    fig_3_2_envelope()
    fig_3_3_verify_flow()
    fig_3_4_benchmark()
    print(f"Saved Chapter 3 figures to {FIG_DIR}")
