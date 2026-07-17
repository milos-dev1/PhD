"""Generate Chapter 4 architecture figures."""

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


def fig_4_1_architecture() -> None:
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    tiers = [
        ("Client Tier\n(Mobile App)", 5, 7, "#E3F2FD"),
        ("Application Tier\n(Auth + Transaction API)", 5, 5.2, "#E8F5E9"),
        ("Settlement Tier\n(Batch + ECC-HISE)", 5, 3.4, "#FFF3E0"),
        ("Governance Tier\n(HSM + Audit Log)", 5, 1.6, "#F3E5F5"),
    ]
    for label, x, y, color in tiers:
        ax.add_patch(FancyBboxPatch((1, y - 0.5), 8, 1, boxstyle="round,pad=0.05", facecolor=color, edgecolor="#333"))
        ax.text(x, y, label, ha="center", va="center", fontsize=9)
    ax.annotate("ECC-DTB-AKA", xy=(9.2, 6.2), fontsize=7, color="#1565C0")
    ax.annotate("ECC-HISE", xy=(9.2, 3.4), fontsize=7, color="#E65100")
    ax.set_title("Figure 4.1: Integrated e-financial service system architecture", fontsize=10)
    save("fig_4_1_architecture.png")


def fig_4_2_flow() -> None:
    fig, ax = plt.subplots(figsize=(7, 2.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 2)
    ax.axis("off")
    steps = ["Login\nECC-DTB-AKA", "Transaction\nHMAC(TBK)", "Queue\nRecord", "Batch\nECC-HISE", "Verify\nMerkle"]
    for i, s in enumerate(steps):
        x = 1 + i * 2.2
        ax.add_patch(FancyBboxPatch((x - 0.7, 0.5), 1.4, 1, boxstyle="round,pad=0.05", facecolor="#E8F0FE", edgecolor="#1a73e8"))
        ax.text(x, 1, s, ha="center", va="center", fontsize=7)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 0.85, 1), xytext=(x + 0.7, 1), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 4.2: End-to-end transaction and settlement flow", fontsize=10)
    save("fig_4_2_flow.png")


def fig_4_3_dtb_modules() -> None:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    mods = [("crypto_utils", 2, 2.5), ("protocol.py", 5, 2.5), ("api/app.py", 8, 2.5), ("demo.py", 5, 0.8)]
    for m, x, y in mods:
        ax.add_patch(FancyBboxPatch((x - 1, y - 0.4), 2, 0.8, boxstyle="round,pad=0.05", facecolor="#E3F2FD", edgecolor="#1565C0"))
        ax.text(x, y, m, ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(4, 2.5), xytext=(3, 2.5), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(7, 2.5), xytext=(6, 2.5), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.annotate("", xy=(5, 1.2), xytext=(5, 2.1), arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 4.3: ECC-DTB-AKA software module diagram", fontsize=10)
    save("fig_4_3_dtb_modules.png")


def fig_4_4_hise_modules() -> None:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    mods = [("hierarchy.py", 1.8, 2.5), ("merkle.py", 4.5, 2.5), ("envelope.py", 7.2, 2.5), ("api/app.py", 4.5, 0.8)]
    for m, x, y in mods:
        ax.add_patch(FancyBboxPatch((x - 1, y - 0.4), 2, 0.8, boxstyle="round,pad=0.05", facecolor="#FFF3E0", edgecolor="#E65100"))
        ax.text(x, y, m, ha="center", va="center", fontsize=7)
    for x1, x2 in [(2.8, 3.5), (5.5, 6.2), (4.5, 2.2)]:
        ax.annotate("", xy=(x2, 2.5 if x2 != 4.5 else 1.2), xytext=(x1, 2.5 if x1 != 4.5 else 1.2),
                    arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 4.4: ECC-HISE software module diagram", fontsize=10)
    save("fig_4_4_hise_modules.png")


def fig_4_5_deployment() -> None:
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    nodes = {"Mobile": (1.5, 2), "API GW": (4, 3), "Auth": (6.5, 3), "Settlement": (6.5, 1), "Audit DB": (9, 2)}
    for n, (x, y) in nodes.items():
        ax.add_patch(FancyBboxPatch((x - 0.7, y - 0.35), 1.4, 0.7, boxstyle="round,pad=0.05", facecolor="#E8F5E9", edgecolor="#2E7D32"))
        ax.text(x, y, n, ha="center", va="center", fontsize=8)
    ax.set_title("Figure 4.5: Deployment topology for prototype services", fontsize=10)
    save("fig_4_5_deployment.png")


if __name__ == "__main__":
    fig_4_1_architecture()
    fig_4_2_flow()
    fig_4_3_dtb_modules()
    fig_4_4_hise_modules()
    fig_4_5_deployment()
    print(f"Saved Chapter 4 figures to {FIG_DIR}")
