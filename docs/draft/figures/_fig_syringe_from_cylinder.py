"""Schematic: how a gas-tight syringe samples from a calibration cylinder."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.patches as mpatches

OUT = Path(__file__).resolve().parent
OKABE = {
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "purple": "#CC79A7",
    "black": "#000000",
    "gray": "#BBBBBB",
}


def _cylinder(ax, x, y, w=0.55, h=1.35, color=OKABE["sky"], label="Mother\nCH4\n1000 ppm"):
    body = FancyBboxPatch(
        (x - w / 2, y), w, h * 0.78,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=color, edgecolor="black", linewidth=1.2, alpha=0.9, zorder=2,
    )
    ax.add_patch(body)
    neck = Rectangle((x - w * 0.12, y + h * 0.78), w * 0.24, h * 0.12,
                     facecolor="#666666", edgecolor="black", linewidth=1.0, zorder=3)
    ax.add_patch(neck)
    valve = Circle((x, y + h * 0.95), w * 0.14, facecolor="#444444",
                   edgecolor="black", linewidth=1.0, zorder=4)
    ax.add_patch(valve)
    ax.text(x, y + h * 0.38, label, ha="center", va="center", fontsize=8,
            fontweight="bold", color="black", zorder=5)


def _box(ax, x, y, w, h, text, facecolor, fontsize=8):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor=facecolor, edgecolor="black", linewidth=1.1, alpha=0.92, zorder=2,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            fontweight="bold", zorder=3, wrap=True)


def _arrow(ax, x1, y1, x2, y2, color=OKABE["black"], style="-|>"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style, mutation_scale=14,
            color=color, linewidth=1.6, zorder=1,
        )
    )


def _syringe(ax, x, y, scale=1.0, tip_right=True):
    """Simple side-view syringe icon."""
    L = 0.85 * scale
    H = 0.22 * scale
    if tip_right:
        body = FancyBboxPatch(
            (x - L, y - H / 2), L * 0.75, H,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            facecolor="white", edgecolor="black", linewidth=1.1, zorder=4,
        )
        tip = mpatches.Polygon(
            [[x - L * 0.25, y - H * 0.15], [x, y], [x - L * 0.25, y + H * 0.15]],
            closed=True, facecolor=OKABE["gray"], edgecolor="black", linewidth=1.0, zorder=5,
        )
        plunger = Rectangle((x - L - 0.12 * scale, y - H * 0.35), 0.12 * scale, H * 0.7,
                            facecolor=OKABE["blue"], edgecolor="black", linewidth=0.8, zorder=4)
    else:
        body = FancyBboxPatch(
            (x, y - H / 2), L * 0.75, H,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            facecolor="white", edgecolor="black", linewidth=1.1, zorder=4,
        )
        tip = mpatches.Polygon(
            [[x + L * 0.25, y - H * 0.15], [x, y], [x + L * 0.25, y + H * 0.15]],
            closed=True, facecolor=OKABE["gray"], edgecolor="black", linewidth=1.0, zorder=5,
        )
        plunger = Rectangle((x + L * 0.75, y - H * 0.35), 0.12 * scale, H * 0.7,
                            facecolor=OKABE["blue"], edgecolor="black", linewidth=0.8, zorder=4)
    ax.add_patch(body)
    ax.add_patch(tip)
    ax.add_patch(plunger)
    ax.text(x - (0.35 * scale if tip_right else -0.35 * scale), y + 0.28 * scale,
            "Gas-tight\nsyringe", ha="center", va="bottom", fontsize=7, zorder=5)


def _bag(ax, x, y, label="Target bag\n50 ppm", color=OKABE["green"]):
    bag = FancyBboxPatch(
        (x - 0.45, y - 0.35), 0.9, 0.7,
        boxstyle="round,pad=0.02,rounding_size=0.2",
        facecolor=color, edgecolor="black", linewidth=1.2, alpha=0.85, zorder=2,
    )
    ax.add_patch(bag)
    ax.add_patch(Circle((x, y + 0.38), 0.07, facecolor="#555555",
                        edgecolor="black", linewidth=0.9, zorder=3))
    ax.text(x, y - 0.02, label, ha="center", va="center", fontsize=7.5,
            fontweight="bold", zorder=4)


def panel_wrong(ax):
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("A  Wrong — do not do this", loc="left", fontsize=10, fontweight="bold",
                 color=OKABE["vermilion"], pad=4)

    _cylinder(ax, 1.5, 1.0, label="High-pressure\ncylinder\nvalve")
    _syringe(ax, 3.6, 2.55, scale=1.15, tip_right=False)
    _arrow(ax, 3.55, 2.55, 1.7, 2.35, color=OKABE["vermilion"])
    ax.text(3.7, 1.55,
            "Needle into raw\ncylinder valve\n= unsafe &\ninaccurate",
            ha="left", va="center", fontsize=8, color=OKABE["vermilion"])
    ax.text(3.0, 0.45, "X  Never sample unregulated high pressure",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=OKABE["vermilion"],
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#F8E0E0",
                      edgecolor=OKABE["vermilion"], linewidth=1.0))


def panel_method_a(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    ax.set_title("B  Method A — sample after regulator (septum / T-piece)",
                 loc="left", fontsize=10, fontweight="bold", color=OKABE["blue"], pad=4)

    _cylinder(ax, 1.1, 1.15, w=0.5, h=1.5, color=OKABE["sky"], label="Mother\n1000 ppm")
    _box(ax, 3.0, 2.55, 1.35, 0.7, "Regulator\n(low P out)", OKABE["orange"], 7.5)
    _box(ax, 5.1, 2.55, 1.45, 0.7, "Septum /\nT-piece", OKABE["yellow"], 7.5)
    _syringe(ax, 7.35, 2.55, scale=1.0, tip_right=False)
    _bag(ax, 9.0, 1.35, label="Target bag\n(e.g. 50 ppm)", color=OKABE["green"])

    _arrow(ax, 1.35, 2.55, 2.3, 2.55)
    _arrow(ax, 3.7, 2.55, 4.35, 2.55)
    _arrow(ax, 5.85, 2.55, 6.55, 2.55)
    _arrow(ax, 7.9, 2.25, 8.55, 1.7, color=OKABE["green"])

    ax.text(5.1, 1.85, "1) Open cylinder gently\n2) Draw volume (e.g. 50 mL)\n3) Inject into target bag\n4) Top up with zero air to 1 L",
            ha="center", va="top", fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F5F5F5",
                      edgecolor="#888888", linewidth=0.8))
    ax.text(9.0, 0.45, "Then mix / label bag", ha="center", fontsize=7.5, style="italic")


def panel_method_b(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    ax.set_title("C  Method B — easier: fill buffer bag, then syringe from bag",
                 loc="left", fontsize=10, fontweight="bold", color=OKABE["green"], pad=4)

    _cylinder(ax, 1.0, 1.3, w=0.48, h=1.35, color=OKABE["sky"], label="Mother\n1000 ppm")
    _box(ax, 2.7, 2.5, 1.2, 0.65, "Regulator", OKABE["orange"], 7.5)
    _bag(ax, 4.6, 2.5, label="Buffer bag\n= 1000 ppm", color=OKABE["purple"])
    _syringe(ax, 6.7, 2.5, scale=1.0, tip_right=False)
    _bag(ax, 8.85, 1.4, label="Target bag\n50 ppm", color=OKABE["green"])
    _box(ax, 8.85, 3.15, 1.5, 0.55, "Zero air\ntop-up", OKABE["sky"], 7)

    _arrow(ax, 1.25, 2.5, 2.05, 2.5)
    _arrow(ax, 3.35, 2.5, 3.95, 2.5)
    _arrow(ax, 5.15, 2.5, 5.85, 2.5)
    _arrow(ax, 7.35, 2.25, 8.3, 1.75, color=OKABE["green"])
    _arrow(ax, 8.85, 2.85, 8.85, 2.0, color=OKABE["blue"])

    ax.text(4.6, 1.35,
            "Syringe pulls from soft bag\n(low pressure, safer)",
            ha="center", va="top", fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#F5F5F5",
                      edgecolor="#888888", linewidth=0.8))
    ax.text(5.0, 0.35,
            "Recommended starting setup for this project (budget / beginner-friendly)",
            ha="center", fontsize=8, fontweight="bold", color=OKABE["green"])


def main():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "figure.facecolor": "white",
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
    })

    fig = plt.figure(figsize=(7.2, 8.6))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.25, 1.25], hspace=0.28)

    ax_a = fig.add_subplot(gs[0])
    ax_b = fig.add_subplot(gs[1])
    ax_c = fig.add_subplot(gs[2])

    panel_wrong(ax_a)
    panel_method_a(ax_b)
    panel_method_b(ax_c)

    fig.suptitle(
        "Sampling mother calibration gas with a gas-tight syringe",
        fontsize=11, fontweight="bold", y=0.98,
    )
    fig.text(
        0.5, 0.01,
        "Approach 1 for eNose CH4 training gas  |  Never syringe an unregulated cylinder valve",
        ha="center", fontsize=7.5, color="#444444",
    )

    for ext in ("png", "pdf"):
        path = OUT / f"fig_syringe_from_calibration_cylinder.{ext}"
        fig.savefig(path, bbox_inches="tight", dpi=300 if ext == "png" else None)
        print(f"wrote {path}")

    plt.close(fig)


if __name__ == "__main__":
    main()
