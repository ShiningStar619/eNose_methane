"""Publication schematic: dual-line CH4 + air mixing into sample tank."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import (
    Circle, FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon, Arc,
)
import matplotlib.patches as mpatches

OUT = Path(__file__).resolve().parent

C = {
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "purple": "#CC79A7",
    "black": "#000000",
    "gray": "#BBBBBB",
    "tank": "#E8D5B7",
}


def _arrow(ax, a, b, color=C["black"], lw=1.5):
    ax.add_patch(
        FancyArrowPatch(
            a, b, arrowstyle="-|>", mutation_scale=12,
            color=color, linewidth=lw, shrinkA=0, shrinkB=0, zorder=1,
        )
    )


def _label(ax, x, y, text, color=C["black"], ha="left", fontsize=7.5, weight="normal"):
    ax.text(x, y, text, color=color, ha=ha, va="center", fontsize=fontsize,
            fontweight=weight, zorder=6)


def draw_cylinder(ax, x, y, label="99% CH$_4$"):
    w, h = 0.55, 1.15
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y), w, h * 0.78,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=C["sky"], edgecolor="black", lw=1.2, alpha=0.92, zorder=2,
    ))
    ax.add_patch(Rectangle(
        (x - w * 0.12, y + h * 0.78), w * 0.24, h * 0.12,
        facecolor="#555555", edgecolor="black", lw=1.0, zorder=3,
    ))
    ax.add_patch(Circle(
        (x, y + h * 0.95), w * 0.14,
        facecolor="#333333", edgecolor="black", lw=1.0, zorder=4,
    ))
    ax.text(x, y + h * 0.38, label, ha="center", va="center",
            fontsize=8, fontweight="bold", zorder=5)


def draw_regulator(ax, x, y):
    ax.add_patch(Circle((x, y), 0.18, facecolor=C["orange"],
                        edgecolor="black", lw=1.1, zorder=3))
    ax.plot([x - 0.08, x + 0.08], [y, y], color="black", lw=1.2, zorder=4)
    ax.plot([x, x], [y - 0.08, y + 0.08], color="black", lw=1.2, zorder=4)
    _label(ax, x + 0.28, y, "Regulator", C["blue"], fontsize=7)


def draw_gauge(ax, x, y, side="right"):
    ax.add_patch(Circle((x, y), 0.22, facecolor="white",
                        edgecolor="black", lw=1.2, zorder=3))
    ax.add_patch(Arc((x, y), 0.28, 0.28, theta1=200, theta2=340,
                     color="black", lw=1.0, zorder=4))
    ax.plot([x, x + 0.08], [y, y + 0.12], color=C["vermilion"], lw=1.4, zorder=5)
    ax.add_patch(Circle((x, y), 0.03, facecolor="black", zorder=5))
    lx = x + 0.32 if side == "right" else x - 0.32
    ha = "left" if side == "right" else "right"
    _label(ax, lx, y, "Pressure\ngauge", C["blue"] if side == "right" else C["purple"],
           ha=ha, fontsize=7)


def draw_valve(ax, x, y, side="right"):
    ax.add_patch(FancyBboxPatch(
        (x - 0.18, y - 0.18), 0.36, 0.36,
        boxstyle="round,pad=0.01,rounding_size=0.04",
        facecolor=C["yellow"], edgecolor="black", lw=1.1, zorder=3,
    ))
    ax.plot([x - 0.1, x + 0.1], [y - 0.1, y + 0.1], color="black", lw=1.5, zorder=4)
    ax.plot([x - 0.1, x + 0.1], [y + 0.1, y - 0.1], color="black", lw=1.5, zorder=4)
    lx = x + 0.28 if side == "right" else x - 0.28
    ha = "left" if side == "right" else "right"
    _label(ax, lx, y, "Valve", C["blue"] if side == "right" else C["purple"],
           ha=ha, fontsize=7)


def draw_rotameter(ax, x, y, side="right", q_label=r"$Q$"):
    ax.add_patch(FancyBboxPatch(
        (x - 0.2, y - 0.45), 0.4, 0.9,
        boxstyle="round,pad=0.01,rounding_size=0.04",
        facecolor="#D6EAF8", edgecolor="black", lw=1.2, zorder=3,
    ))
    for dy in (-0.25, -0.05, 0.15, 0.3):
        ax.plot([x - 0.12, x + 0.12], [y + dy, y + dy], color="#888888", lw=0.7, zorder=4)
    ax.add_patch(Polygon(
        [[x - 0.08, y - 0.05], [x + 0.08, y - 0.05], [x, y + 0.12]],
        closed=True, facecolor=C["orange"], edgecolor="black", lw=0.8, zorder=5,
    ))
    lx = x + 0.3 if side == "right" else x - 0.3
    ha = "left" if side == "right" else "right"
    color = C["blue"] if side == "right" else C["purple"]
    _label(ax, lx, y, f"Rotameter\n{q_label}", color, ha=ha, fontsize=7)


def draw_pump(ax, x, y):
    ax.add_patch(FancyBboxPatch(
        (x - 0.45, y - 0.28), 0.9, 0.56,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=C["purple"], edgecolor="black", lw=1.2, alpha=0.9, zorder=3,
    ))
    ax.text(x, y, "Air pump", ha="center", va="center",
            fontsize=8, fontweight="bold", color="white", zorder=4)


def draw_filter(ax, x, y):
    ax.add_patch(FancyBboxPatch(
        (x - 0.28, y - 0.22), 0.56, 0.44,
        boxstyle="round,pad=0.01,rounding_size=0.06",
        facecolor=C["green"], edgecolor="black", lw=1.1, alpha=0.85, zorder=3,
    ))
    ax.add_patch(Circle((x - 0.12, y), 0.07, facecolor="white",
                        edgecolor="black", lw=0.8, zorder=4))
    ax.add_patch(Circle((x + 0.12, y), 0.07, facecolor="white",
                        edgecolor="black", lw=0.8, zorder=4))
    _label(ax, x + 0.38, y, "Filter", C["purple"], fontsize=7)


def draw_tank(ax, x, y):
    ax.add_patch(FancyBboxPatch(
        (x - 1.1, y - 0.55), 2.2, 1.1,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=C["tank"], edgecolor="black", lw=1.4, zorder=3,
    ))
    ax.add_patch(Circle((x, y + 0.58), 0.08, facecolor="#555555",
                        edgecolor="black", lw=0.9, zorder=4))
    ax.text(x, y + 0.1, "Sample tank", ha="center", va="center",
            fontsize=10, fontweight="bold", zorder=5)
    ax.text(x, y - 0.28, r"($c_f$ ppm)", ha="center", va="center",
            fontsize=9, color=C["blue"], fontweight="bold", zorder=5)


def panel_schematic(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11.5)
    ax.axis("off")
    ax.set_title("A  Dual-line mixing into sample tank",
                 loc="left", fontsize=10, fontweight="bold", pad=2)

    # CH4 column x=2.6, Air column x=7.4
    x1, x2 = 2.6, 7.4

    # Sources
    draw_cylinder(ax, x1, 9.6)
    draw_pump(ax, x2, 10.2)

    # CH4 chain
    draw_regulator(ax, x1, 9.15)
    _arrow(ax, (x1, 9.55), (x1, 9.35))
    draw_gauge(ax, x1, 8.2, side="right")
    _arrow(ax, (x1, 8.95), (x1, 8.45))
    draw_valve(ax, x1, 7.15, side="right")
    _arrow(ax, (x1, 7.95), (x1, 7.35))
    draw_rotameter(ax, x1, 5.85, side="right", q_label=r"$Q_{\mathrm{CH_4}}$")
    _arrow(ax, (x1, 6.95), (x1, 6.35))

    # Air chain
    draw_filter(ax, x2, 9.2)
    _arrow(ax, (x2, 9.9), (x2, 9.45))
    draw_gauge(ax, x2, 8.2, side="left")
    _arrow(ax, (x2, 8.95), (x2, 8.45))
    draw_valve(ax, x2, 7.15, side="left")
    _arrow(ax, (x2, 7.95), (x2, 7.35))
    draw_rotameter(ax, x2, 5.85, side="left", q_label=r"$Q_{\mathrm{air}}$")
    _arrow(ax, (x2, 6.95), (x2, 6.35))

    # Merge to tank
    draw_tank(ax, 5.0, 2.4)
    _arrow(ax, (x1, 5.35), (x1, 3.5), color=C["blue"])
    _arrow(ax, (x2, 5.35), (x2, 3.5), color=C["purple"])
    _arrow(ax, (x1, 3.5), (4.0, 2.95), color=C["blue"])
    _arrow(ax, (x2, 3.5), (6.0, 2.95), color=C["purple"])

    ax.text(x1, 10.95, "CH$_4$ line", ha="center", fontsize=9,
            fontweight="bold", color=C["blue"])
    ax.text(x2, 10.95, "Air line", ha="center", fontsize=9,
            fontweight="bold", color=C["purple"])

    ax.text(
        5.0, 0.55,
        r"Flow tags: $Q_{\mathrm{CH_4}}$ (left rotameter),  $Q_{\mathrm{air}}$ (right rotameter)",
        ha="center", fontsize=7.5, style="italic", color="#444444",
    )


def panel_formula(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11.5)
    ax.axis("off")
    ax.set_title("B  Target concentration from two flows",
                 loc="left", fontsize=10, fontweight="bold", pad=2)

    ax.add_patch(FancyBboxPatch(
        (0.4, 1.0), 9.2, 9.8,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor="#FAFAFA", edgecolor="#888888", lw=1.0, zorder=1,
    ))

    ax.text(5.0, 10.2, "Ideal-gas mixing at same $T$, $P$",
            ha="center", fontsize=9, fontweight="bold", zorder=2)

    ax.text(0.8, 9.2, r"Mother: $c_m = 0.99 \times 10^{6} = 990{,}000$ ppm (99% CH$_4$)",
            ha="left", fontsize=8, zorder=2)
    ax.text(0.8, 8.5, r"Ambient air background: $c_a \approx 2$ ppm (optional)",
            ha="left", fontsize=8, zorder=2)

    ax.text(0.8, 7.5, "General balance (continuous fill / same fill time):",
            ha="left", fontsize=8, fontweight="bold", zorder=2)

    ax.text(
        5.0, 6.5,
        r"$c_f = \dfrac{Q_{\mathrm{CH_4}}\,c_m + Q_{\mathrm{air}}\,c_a}"
        r"{Q_{\mathrm{CH_4}} + Q_{\mathrm{air}}}\quad [\mathrm{ppm}]$",
        ha="center", fontsize=11, zorder=2,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#E8F4FC",
                  edgecolor=C["blue"], lw=1.0),
    )

    ax.text(0.8, 5.3, r"If $c_a \approx 0$ (ignore ambient CH$_4$):",
            ha="left", fontsize=8, zorder=2)
    ax.text(
        5.0, 4.5,
        r"$c_f \approx \dfrac{Q_{\mathrm{CH_4}}}{Q_{\mathrm{CH_4}}+Q_{\mathrm{air}}}"
        r"\times 990{,}000$",
        ha="center", fontsize=10, zorder=2,
    )

    ax.text(0.8, 3.5, "Worked example (ignore $c_a$):",
            ha="left", fontsize=8, fontweight="bold", zorder=2)
    ax.text(
        0.8, 2.7,
        r"$Q_{\mathrm{CH_4}}=0.05$ mL/min,  $Q_{\mathrm{air}}=99.95$ mL/min"
        "\n"
        r"$\Rightarrow\ c_f \approx 495$ ppm",
        ha="left", fontsize=8, zorder=2,
        family="monospace",
    )
    ax.text(
        0.8, 1.5,
        "Safety: 99% CH$_4$ is flammable (LEL ~5%). Use ventilated lab,\n"
        "no ignition sources; prefer certified dilute mother gas when possible.",
        ha="left", fontsize=7.5, color=C["vermilion"], zorder=2,
    )


def main():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "mathtext.fontset": "dejavusans",
        "figure.facecolor": "white",
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
    })

    fig = plt.figure(figsize=(10.5, 7.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.08)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    panel_schematic(ax_a)
    panel_formula(ax_b)

    fig.suptitle(
        "Gas mixing setup for target CH$_4$ concentration in a sample tank",
        fontsize=11, fontweight="bold", y=0.98,
    )
    fig.text(
        0.5, 0.02,
        "Hand sketch → publication schematic  |  Okabe–Ito colors  |  Dual rotameter volumetric mixing",
        ha="center", fontsize=7.5, color="#555555",
    )

    for ext in ("png", "pdf"):
        path = OUT / f"fig_ch4_air_mixing_sample_tank.{ext}"
        fig.savefig(path, bbox_inches="tight", dpi=300 if ext == "png" else None)
        print(f"wrote {path}")

    # also save a clean schematic-only version for slides
    fig2, ax = plt.subplots(figsize=(5.2, 7.0))
    panel_schematic(ax)
    ax.set_title("Gas mixing: 99% CH$_4$ + air → sample tank",
                 loc="left", fontsize=10, fontweight="bold")
    for ext in ("png", "pdf"):
        path = OUT / f"fig_ch4_air_mixing_sample_tank_schematic_only.{ext}"
        fig2.savefig(path, bbox_inches="tight", dpi=300 if ext == "png" else None)
        print(f"wrote {path}")
    plt.close(fig2)
    plt.close(fig)


if __name__ == "__main__":
    main()
