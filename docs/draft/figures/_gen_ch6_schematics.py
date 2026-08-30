"""Generate Ch.6 schematics in the example-proposal style (Cordia New)."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyArrowPatch,
    FancyBboxPatch,
    Polygon,
    Rectangle,
    Circle,
    FancyBboxPatch as FBP,
)
from matplotlib.patches import Ellipse, RegularPolygon
import matplotlib.patches as mpatches

OUT = Path(__file__).resolve().parent
plt.rcParams["font.family"] = "Cordia New"
plt.rcParams["font.size"] = 12
plt.rcParams["axes.unicode_minus"] = False

NAVY = "#1f4e79"
BLUE = "#5b9bd5"
ORANGE = "#ed7d31"
GREEN = "#70ad47"
GOLD = "#ffc000"
GRAY = "#7f7f7f"
INK = "#1a1a1a"


def rbox(ax, x, y, w, h, text, fc="white", ec=NAVY, lw=1.3, size=11, weight="normal"):
    p = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.06",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2,
    )
    ax.add_patch(p)
    ax.text(
        x + w / 2, y + h / 2, text, ha="center", va="center",
        color=INK, fontsize=size, fontweight=weight, zorder=3, linespacing=1.12,
    )
    return p


def oval(ax, x, y, w, h, text, fc="#fff2cc"):
    e = Ellipse((x + w / 2, y + h / 2), w, h, facecolor=fc, edgecolor=NAVY, lw=1.4, zorder=2)
    ax.add_patch(e)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=12, fontweight="bold", zorder=3)
    return e


def diamond(ax, cx, cy, w, h, text, fc="#f8cbad"):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    p = Polygon(pts, closed=True, facecolor=fc, edgecolor=NAVY, lw=1.4, zorder=2)
    ax.add_patch(p)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=11, zorder=3)
    return p


def para(ax, x, y, w, h, text, fc="#deebf7"):
    skew = 0.22
    pts = [(x + skew, y + h), (x + w, y + h), (x + w - skew, y), (x, y)]
    p = Polygon(pts, closed=True, facecolor=fc, edgecolor=NAVY, lw=1.3, zorder=2)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=11, zorder=3, linespacing=1.1)
    return p


def arrow(ax, x1, y1, x2, y2, color=NAVY, lw=1.5, style="-|>"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=11,
            linewidth=lw, color=color, zorder=1,
        )
    )


def make_machine():
    fig, ax = plt.subplots(figsize=(11.4, 6.6), dpi=180)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(5.7, 6.32, "การทำงานของเครื่อง eNose", ha="center", va="center",
            fontsize=18, fontweight="bold", color=NAVY)

    # Legend
    ax.plot([8.55, 9.25], [6.28, 6.28], color=BLUE, lw=2.4)
    ax.text(9.35, 6.28, "อากาศอ้างอิง (Baseline)", va="center", fontsize=10)
    ax.plot([8.55, 9.25], [5.98, 5.98], color=ORANGE, lw=2.4, ls="--")
    ax.text(9.35, 5.98, "ก๊าซตัวอย่าง (Measure)", va="center", fontsize=10)
    ax.plot([8.55, 9.25], [5.68, 5.68], color=GRAY, lw=2.0)
    ax.text(9.35, 5.68, "สัญญาณข้อมูล", va="center", fontsize=10)

    # Inputs
    rbox(ax, 0.25, 4.55, 2.05, 0.85, "อากาศอ้างอิง\n(Baseline)", "#deebf7", BLUE, size=12)
    rbox(ax, 0.25, 3.35, 2.05, 0.85, "ก๊าซตัวอย่าง CH4\n(Measure)", "#fce4d6", ORANGE, size=12)

    rbox(ax, 2.75, 3.55, 2.45, 1.55,
         "วาล์ว SV1–SV4\nปั๊ม / พัดลม", GOLD, NAVY, size=13, weight="bold")
    ax.text(3.97, 3.42, "Baseline: SV2 + SV3 + ปั๊ม\nMeasure:  SV1 + SV4 + ปั๊ม\nVacuum:   SV3 + ปั๊ม",
            ha="center", va="top", fontsize=9.5, color=GRAY, family="Cordia New")

    rbox(ax, 5.65, 3.45, 2.85, 1.85,
         "ห้องวัด\nTGS2612 × 4  (ss1–ss4)\nฮีตเตอร์ GPIO 13", "#e2efda", GREEN, size=12, weight="bold")
    rbox(ax, 8.95, 3.90, 1.85, 0.85, "ไอเสีย", "#f2f2f2", GRAY, size=12)

    arrow(ax, 2.30, 4.97, 2.75, 4.55, BLUE, 2.0)
    arrow(ax, 2.30, 3.77, 2.75, 4.15, ORANGE, 2.0)
    arrow(ax, 5.20, 4.32, 5.65, 4.32)
    arrow(ax, 8.50, 4.32, 8.95, 4.32)

    # Sensing
    rbox(ax, 3.05, 1.70, 2.65, 1.05, "ADS1263  ~100 Hz\nแรงดัน MOS 4 ช่อง", "#ddebf7", BLUE, size=11)
    rbox(ax, 6.05, 1.70, 2.65, 1.05, "BME280  ~10 Hz\nT / RH / P", "#f8cbad", ORANGE, size=11)
    arrow(ax, 7.07, 3.45, 4.37, 2.75, GRAY, 1.4)
    arrow(ax, 7.07, 3.45, 7.37, 2.75, GRAY, 1.4)

    rbox(ax, 3.35, 0.22, 5.35, 1.12,
         "Raspberry Pi\nลำดับอัตโนมัติ Op1–Op7  ·  บันทึก CSV  ·  ทำนาย ppm",
         "white", NAVY, lw=2.0, size=12, weight="bold")
    arrow(ax, 4.37, 1.70, 5.20, 1.34, GRAY)
    arrow(ax, 7.37, 1.70, 6.90, 1.34, GRAY)

    ax.annotate(
        "รีเลย์ GPIO (BCM)\nSV1=21  SV2=20  SV3=16  SV4=12\nปั๊ม=26  พัดลม=19  ฮีตเตอร์=13",
        xy=(4.0, 4.20), xytext=(0.30, 1.20),
        fontsize=10, color=NAVY,
        arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.05),
        bbox=dict(boxstyle="round,pad=0.28", fc="#fff2cc", ec=GOLD),
    )
    ax.text(9.55, 0.55, "GC ใช้ติดป้าย ppm\n(ไม่ใช่ส่วนของเครื่อง)",
            ha="center", va="center", fontsize=10, color=ORANGE)

    fig.tight_layout(pad=0.2)
    path = OUT / "fig_ch6_machine_operation.png"
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def make_model_flow():
    fig, ax = plt.subplots(figsize=(7.8, 11.2), dpi=180)
    ax.set_xlim(0, 7.8)
    ax.set_ylim(0, 11.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(3.9, 10.85, "ขั้นตอนการสร้างแบบจำลองถดถอย",
            ha="center", va="center", fontsize=16, fontweight="bold", color=NAVY)

    cx, w = 3.9, 4.7
    xs = cx - w / 2

    oval(ax, xs + 1.35, 10.05, 2.0, 0.55, "เริ่ม")
    para(ax, xs, 8.95, w, 0.85, "ไฟล์รายรอบ + หน้าต่างวิเคราะห์\nBaseline 250–300 s · Measure 305–365 s")
    rbox(ax, xs, 7.95, w, 0.72, "1. จับคู่ adc1263_*.csv กับ bme280_*.csv", "#deebf7")
    rbox(ax, xs, 6.85, w, 0.85, "2. สกัดลักษณะเด่น\ndV / dVmax / slope / ratio + T, RH, P", "#deebf7")

    diamond(ax, cx, 6.05, 3.6, 0.95, "QC: ตัวอย่าง >= 10 จุด\nในทั้งสองหน้าต่าง?")
    rbox(ax, 6.05, 5.75, 1.45, 0.55, "ตัดรอบ", "#fce4d6", ORANGE, size=10)

    rbox(ax, xs, 4.75, w, 0.72, "3. เลือก dVmax_ss4, dVmax_ss3,\nT_baseline, T_measure", "#e2efda")
    rbox(ax, xs, 3.78, w, 0.72, "4. GroupKFold (k = 5)", "#fff2cc")
    rbox(ax, xs, 2.88, w, 0.65, "5. StandardScaler -> Linear Regression", "#deebf7")
    rbox(ax, xs, 1.98, w, 0.65, "6. ประเมิน RMSE, MAE, R² เทียบ GC", "#deebf7")
    rbox(ax, xs, 1.05, w, 0.68, "7. บันทึก joblib แล้วโหลดขึ้น Raspberry Pi", "#e2efda")
    oval(ax, xs + 1.35, 0.28, 2.0, 0.52, "จบ")

    # arrows down the spine
    arrow(ax, cx, 10.05, cx, 9.80)
    arrow(ax, cx, 8.95, cx, 8.67)
    arrow(ax, cx, 7.95, cx, 7.70)
    arrow(ax, cx, 6.85, cx, 6.52)
    arrow(ax, cx, 5.57, cx, 5.47)
    arrow(ax, 5.70, 6.05, 6.05, 6.02)  # no branch
    ax.text(6.78, 6.40, "ไม่", fontsize=10, color=ORANGE, ha="center")
    ax.text(3.15, 5.52, "ใช่", fontsize=10, color=GREEN, ha="center")
    arrow(ax, cx, 4.75, cx, 4.50)
    arrow(ax, cx, 3.78, cx, 3.53)
    arrow(ax, cx, 2.88, cx, 2.63)
    arrow(ax, cx, 1.98, cx, 1.73)
    arrow(ax, cx, 1.05, cx, 0.80)

    ax.text(3.9, 0.08, "y = ความเข้มข้น CH4 จาก GC (ppm) ไม่ใช่ฟลักซ์",
            ha="center", va="center", fontsize=11, color=ORANGE)

    fig.tight_layout(pad=0.15)
    path = OUT / "fig_ch6_model_flowchart.png"
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def make_machine_flow():
    """Vertical Auto Mode flowchart for Fig. 6.1 (example-proposal style)."""
    fig, ax = plt.subplots(figsize=(7.6, 12.6), dpi=180)
    ax.set_xlim(0, 7.6)
    ax.set_ylim(0, 12.6)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    ax.text(
        3.8, 12.28, "ขั้นตอนการทำงานอัตโนมัติของเครื่อง eNose",
        ha="center", va="center", fontsize=15, fontweight="bold", color=NAVY,
    )

    cx, w = 3.8, 4.55
    xs = cx - w / 2

    oval(ax, xs + 1.28, 11.48, 2.0, 0.50, "เริ่ม")
    para(
        ax, xs, 10.42, w, 0.82,
        "อินพุต: อากาศอ้างอิง / ก๊าซตัวอย่าง CH4\nไฟล์กำหนดค่า  GPIO และระยะเวลา Op1–Op7",
    )
    rbox(ax, xs, 9.52, w, 0.68, "Op1  Heating  ·  ฮีตเตอร์ GPIO13\n~30 นาที ให้สภาวะคงที่", "#fff2cc")
    rbox(ax, xs, 8.68, w, 0.58, "เริ่มบันทึก  ADS1263 + BME280", "#deebf7")
    rbox(ax, xs, 7.82, w, 0.62, "Op2  Baseline  ·  SV2 + SV3 + ปั๊ม\nอากาศอ้างอิง  ~30 วินาที", "#deebf7")
    rbox(ax, xs, 7.02, w, 0.55, "Op3  Vacuum  ·  SV3 + ปั๊ม  ~10 วินาที", "white")
    rbox(ax, xs, 6.22, w, 0.55, "Op4  Mix Air  ·  พัดลม  ~10 วินาที", "white")
    rbox(ax, xs, 5.32, w, 0.62, "Op5  Measure  ·  SV1 + SV4 + ปั๊ม\nก๊าซตัวอย่าง  ~60 วินาที", "#fce4d6")
    rbox(ax, xs, 4.52, w, 0.55, "Op6  Vacuum Return  ·  ~10 วินาที", "white")
    rbox(ax, xs, 3.72, w, 0.55, "Op7  Recovery  ·  พักฟื้น  ~60 วินาที", "#e2efda")
    rbox(
        ax, xs, 2.72, w, 0.75,
        "หยุดบันทึก  กรอง LPF + MA\nสกัด dV  แล้วทำนาย ppm",
        "#e2efda",
    )
    diamond(ax, cx, 1.78, 3.55, 0.88, "เก็บรอบถัดไป?")
    oval(ax, xs + 1.28, 0.28, 2.0, 0.50, "จบ")

    ys = [
        (11.48, 11.24),
        (10.42, 10.20),
        (9.52, 9.26),
        (8.68, 8.44),
        (7.82, 7.57),
        (7.02, 6.77),
        (6.22, 5.94),
        (5.32, 5.07),
        (4.52, 4.27),
        (3.72, 3.47),
        (2.72, 2.22),
    ]
    for y1, y2 in ys:
        arrow(ax, cx, y1, cx, y2)

    ax.text(2.55, 1.28, "ไม่", fontsize=11, color=ORANGE, ha="center")
    arrow(ax, cx, 1.34, cx, 0.78)
    ax.text(5.55, 1.95, "ใช่", fontsize=11, color=GREEN, ha="center")
    arrow(ax, 5.55, 1.78, 6.55, 1.78)
    arrow(ax, 6.55, 1.78, 6.55, 8.13)
    arrow(ax, 6.55, 8.13, 6.12, 8.13)

    ax.text(
        3.8, 0.06,
        "ระยะเวลาเป็นค่าตั้งต้นในไฟล์กำหนดค่า  หน้าต่างวิเคราะห์คงที่ตอนฝึกและทำนาย",
        ha="center", va="center", fontsize=10, color=GRAY,
    )

    fig.tight_layout(pad=0.12)
    path = OUT / "fig_ch6_01_flowchart.png"
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


if __name__ == "__main__":
    print(make_machine())
    print(make_model_flow())
    print(make_machine_flow())
