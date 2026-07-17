"""Generate Chapter 1 figures as PNG for Word embedding."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FIG_DIR = Path(__file__).resolve().parent.parent / "thesis" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "font.size": 9})


def save_fig(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIG_DIR / name, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()


def fig_1_1_attack_lifecycle() -> None:
    fig, ax = plt.subplots(figsize=(7, 2.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis("off")
    stages = [
        "Reconnaissance",
        "Initial Access",
        "Lateral Movement",
        "Privilege Escalation",
        "Exfiltration/Fraud",
        "Cover Tracks",
    ]
    for i, s in enumerate(stages):
        x = 0.3 + i * 1.55
        box = FancyBboxPatch((x, 0.6), 1.3, 0.8, boxstyle="round,pad=0.05",
                             facecolor="#E8F0FE", edgecolor="#1a73e8", linewidth=1)
        ax.add_patch(box)
        ax.text(x + 0.65, 1.0, s, ha="center", va="center", fontsize=7, wrap=True)
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + 1.35, 1.0), xytext=(x + 1.3, 1.0),
                        arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 1.1: Attack lifecycle in e-banking systems", fontsize=10, pad=10)
    save_fig("fig_1_1_attack_lifecycle.png")


def fig_1_2_client_auth_flow() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    boxes = [
        (1, 5, "Client\nTLS ClientHello"),
        (5, 5, "Bank Server\nTLS ServerHello + Cert"),
        (1, 3.5, "Client\nCredentials + MFA"),
        (5, 3.5, "Bank Server\nValidate + Issue Token"),
        (3, 1.5, "Encrypted Session\n(App Traffic)"),
    ]
    for x, y, t in boxes:
        box = FancyBboxPatch((x - 0.8, y - 0.5), 1.6, 1.0, boxstyle="round,pad=0.05",
                             facecolor="#FFF3E0", edgecolor="#E65100")
        ax.add_patch(box)
        ax.text(x, y, t, ha="center", va="center", fontsize=8)
    arrows = [(1.8, 5, 4.2, 5), (5, 4.5, 1, 4), (1.8, 3.5, 4.2, 3.5), (3, 3, 3, 2.5)]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_title("Figure 1.2: Current client-server authentication flow", fontsize=10)
    save_fig("fig_1_2_client_auth_flow.png")


def fig_1_3_server_mesh() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    nodes = {"API GW": (2, 4), "Auth Svc": (5, 5), "Acct Svc": (8, 4),
             "Settlement": (5, 2), "HSM": (2, 1.5)}
    for name, (x, y) in nodes.items():
        color = "#E8F5E9" if name != "HSM" else "#FCE4EC"
        box = FancyBboxPatch((x - 0.9, y - 0.4), 1.8, 0.8, boxstyle="round,pad=0.05",
                             facecolor=color, edgecolor="#2E7D32" if name != "HSM" else "#C62828")
        ax.add_patch(box)
        ax.text(x, y, name, ha="center", va="center", fontsize=8)
    pairs = [("API GW", "Auth Svc"), ("API GW", "Acct Svc"), ("Auth Svc", "Settlement"),
             ("Acct Svc", "Settlement"), ("Settlement", "HSM")]
    for a, b in pairs:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        ax.plot([x1, x2], [y1, y2], "b--", alpha=0.5, linewidth=1)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.15, "mTLS", fontsize=6, ha="center", color="#1565C0")
    ax.set_title("Figure 1.3: Server-server mTLS service mesh architecture", fontsize=10)
    save_fig("fig_1_3_server_mesh.png")


def fig_1_4_data_layers() -> None:
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    layers = [("In-Use (TEE/SGX)", "#F3E5F5"), ("In-Transit (TLS 1.3)", "#E3F2FD"),
              ("At-Rest (AES-256 TDE)", "#E8F5E9")]
    for i, (label, color) in enumerate(layers):
        y = 2.8 - i * 0.9
        box = FancyBboxPatch((1.5, y - 0.3), 7, 0.6, boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor="#333")
        ax.add_patch(box)
        ax.text(5, y, label, ha="center", va="center", fontsize=9)
    ax.set_title("Figure 1.4: Data protection layers in e-banking systems", fontsize=10)
    save_fig("fig_1_4_data_layers.png")


def fig_1_5_threat_model() -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    entities = {"Client": (1.5, 3), "Bank Server": (5, 4.5), "Settlement Server": (8.5, 3),
                "Adversary": (5, 1)}
    colors = {"Adversary": "#FFEBEE"}
    for name, (x, y) in entities.items():
        c = colors.get(name, "#E3F2FD")
        e = "#C62828" if name == "Adversary" else "#1565C0"
        box = FancyBboxPatch((x - 1, y - 0.4), 2, 0.8, boxstyle="round,pad=0.05",
                             facecolor=c, edgecolor=e)
        ax.add_patch(box)
        ax.text(x, y, name, ha="center", va="center", fontsize=8)
    for x1, y1, x2, y2 in [(2.5, 3.2, 4, 4.2), (6, 4.2, 7.5, 3.2), (2.5, 2.8, 7.5, 2.8)]:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<->", color="#333", lw=1))
    ax.annotate("", xy=(5, 2.5), xytext=(5, 3.5),
                arrowprops=dict(arrowstyle="->", color="#C62828", lw=1.5, linestyle="dashed"))
    ax.text(5, 0.3, "Dolev-Yao channel: eavesdrop, modify, replay", ha="center", fontsize=7, style="italic")
    ax.set_title("Figure 1.5: Threat model for e-banking system", fontsize=10)
    save_fig("fig_1_5_threat_model.png")


if __name__ == "__main__":
    fig_1_1_attack_lifecycle()
    fig_1_2_client_auth_flow()
    fig_1_3_server_mesh()
    fig_1_4_data_layers()
    fig_1_5_threat_model()
    print(f"Figures saved to {FIG_DIR}")
