#!/usr/bin/env python3
"""Generate polished GUI mock screenshots for eNose user guide.

Run: py docs/user-guide/scripts/generate_placeholders.py
Replace with real Pi/VNC captures per assets/screenshots/SHOTLIST.md
"""
from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Install Pillow: pip install Pillow")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1280, 800

# Match gui.py palette
C = {
    "bg": "#f0f0f0",
    "header": "#2c3e50",
    "nav_bar": "#34495e",
    "green": "#27ae60",
    "green_dark": "#1e8449",
    "red": "#c0392b",
    "blue": "#3498db",
    "purple": "#9b59b6",
    "gray": "#bdc3c7",
    "gray_dark": "#7f8c8d",
    "white": "#ffffff",
    "text": "#2c3e50",
    "accent": "#e74c3c",
    "ops": {
        "heating": "#fff59d",
        "baseline": "#81d4fa",
        "vacuum": "#b39ddb",
        "mix_air": "#a5d6a7",
        "measure": "#ffcc80",
        "vacuum_return": "#f48fb1",
        "recovery": "#80cbc4",
        "break_time": "#ffcdd2",
    },
}


def _font(size: int, bold: bool = False):
    candidates = (
        ["arialbd.ttf", "Arial Bold.ttf"] if bold else ["arial.ttf", "Arial.ttf"]
    ) + ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _rounded_rect(draw, xy, fill, outline=None, radius=8, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def _window(active_page: str = "Control") -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
    img = Image.new("RGB", (W, H), C["bg"])
    draw = ImageDraw.Draw(img)
    _rounded_rect(draw, [16, 16, W - 16, H - 16], C["white"], C["header"], radius=12, width=2)
    draw.rectangle([16, 16, W - 16, 68], fill=C["header"])
    draw.text((36, 28), "eNose Hardware Control", fill=C["white"], font=_font(22, True))
    # nav tabs bottom-right
    y0 = H - 56
    draw.rectangle([W - 340, y0, W - 24, H - 24], fill=C["nav_bar"])
    for i, label in enumerate(["Control", "Display", "Settings"]):
        x = W - 320 + i * 102
        on = label == active_page
        _rounded_rect(
            draw,
            [x, y0 + 8, x + 92, H - 32],
            C["green"] if on else "#5d6d7e",
            radius=6,
        )
        draw.text((x + 10, y0 + 18), label, fill=C["white"], font=_font(13, True))
    content_top = 84
    return img, draw, content_top


def _badge(draw, x, y, num: str, label: str):
    r = 18
    draw.ellipse([x - r, y - r, x + r, y + r], fill=C["accent"], outline=C["white"], width=2)
    draw.text((x - 6, y - 12), num, fill=C["white"], font=_font(16, True))
    draw.text((x + 26, y - 10), label, fill=C["accent"], font=_font(15, True))


def _btn(draw, xy, text, bg, fg=C["white"], bold=True):
    _rounded_rect(draw, xy, bg, radius=8)
    x0, y0, x1, y1 = xy
    tw = draw.textlength(text, font=_font(16, bold))
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0) / 2 - 10), text, fill=fg, font=_font(16, bold))


def _device_box(draw, xy, label, on=False):
    x0, y0, x1, y1 = xy
    fill = C["green"] if on else C["gray"]
    _rounded_rect(draw, [x0, y0, x1, y1], fill, C["text"], radius=6, width=2)
    tw = draw.textlength(label, font=_font(14, True))
    draw.text((x0 + (x1 - x0 - tw) / 2, y0 + (y1 - y0) / 2 - 8), label, fill=C["white"] if on else C["text"], font=_font(14, True))


def save(name: str, img: Image.Image):
    img.save(OUT / name, "PNG")
    print(f"  {name}")


def shot_01():
    img = Image.new("RGB", (W, H), "#1e272e")
    draw = ImageDraw.Draw(img)
    draw.text((40, 30), "Raspberry Pi Desktop", fill="#95a5a6", font=_font(14))
    _rounded_rect(draw, [120, 100, W - 120, H - 80], C["white"], C["header"], radius=10, width=2)
    draw.rectangle([120, 100, W - 120, 152], fill=C["header"])
    draw.text((140, 112), "eNose Hardware Control", fill=C["white"], font=_font(20, True))
    _btn(draw, [200, 220, 340, 275], "Manual", C["gray"], C["text"])
    _btn(draw, [360, 220, 500, 275], "Auto", C["green"])
    draw.text((140, 300), "Operation Sequence", fill=C["purple"], font=_font(16, True))
    _rounded_rect(draw, [140, 330, W - 160, 420], "#fafafa", C["gray"], radius=8)
    draw.text((160, 350), "Heat → BL → Vac → Mix → Meas → VR → Rec", fill=C["text"], font=_font(15))
    _btn(draw, [200, 500, 480, 560], "Start Auto Sequence", C["green"])
    save("01-pi-desktop-gui.png", img)


def shot_02():
    img, draw, top = _window("Control")
    draw.text((36, top), "Control Mode", fill=C["text"], font=_font(18, True))
    _btn(draw, [36, top + 36, 160, top + 86], "Manual", C["gray"], C["text"])
    _btn(draw, [176, top + 36, 300, top + 86], "Auto", C["green"])
    _badge(draw, 80, top + 130, "1", "Manual / Auto")
    draw.text((36, top + 170), "Hardware Controls", fill=C["text"], font=_font(16, True))
    for i, n in enumerate(["Value 1", "Value 2", "Value 3", "Value 4"]):
        _device_box(draw, [36 + i * 130, top + 200, 150 + i * 130, top + 250], n)
    _badge(draw, 80, top + 290, "2", "Hardware Controls")
    _rounded_rect(draw, [36, top + 320, W - 60, top + 420], "#fafafa", C["purple"], radius=8, width=2)
    draw.text((50, top + 335), "Operation Sequence", fill=C["purple"], font=_font(15, True))
    draw.text((50, top + 365), "Heat → BL → Vac → Mix → Meas → VR → Rec", fill=C["text"], font=_font(14))
    _badge(draw, 80, top + 450, "3", "Operation Sequence")
    _btn(draw, [36, top + 480, 220, top + 535], "Start Auto Sequence", C["green"])
    _btn(draw, [240, top + 480, 360, top + 535], "Stop", C["red"])
    _badge(draw, 80, top + 570, "4", "Start / Stop")
    _rounded_rect(draw, [W - 280, top + 170, W - 60, top + 320], "#fafafa", C["green"], radius=8, width=2)
    draw.text((W - 260, top + 185), "Methane", fill=C["text"], font=_font(14))
    draw.text((W - 250, top + 220), "----", fill=C["gray_dark"], font=_font(42, True))
    draw.text((W - 120, top + 270), "ppm", fill=C["text"], font=_font(16))
    _badge(draw, W - 240, top + 350, "5", "Methane ppm")
    save("02-control-overview.png", img)


def shot_03():
    img, draw, top = _window("Control")
    draw.text((36, top), "Control Mode", fill=C["text"], font=_font(18, True))
    _btn(draw, [36, top + 40, 180, top + 100], "Manual", C["gray"], C["text"])
    _btn(draw, [200, top + 40, 344, top + 100], "Auto", C["green"])
    draw.text((36, top + 120), "ตั้งค่าเวลาแล้วกด Start เพื่อรันอัตโนมัติ", fill=C["gray_dark"], font=_font(14))
    # arrow
    draw.polygon([(190, top + 55), (175, top + 45), (175, top + 65)], fill=C["accent"])
    save("03-select-auto.png", img)


def shot_04():
    img, draw, top = _window("Settings")
    draw.text((36, top), "Auto Mode Parameters", fill=C["purple"], font=_font(20, True))
    _rounded_rect(draw, [36, top + 40, W - 60, top + 110], "#e8e8e8", radius=8)
    _btn(draw, [50, top + 55, 280, top + 95], "Input from UI", C["blue"])
    _btn(draw, [300, top + 55, 580, top + 95], "Load from config.json", C["gray"], C["text"])
    draw.text((36, top + 125), "Operation Duration (seconds)", fill=C["text"], font=_font(15, True))
    ops = [
        ("Heating (30m)", "heating", "1800"),
        ("Baseline (30s)", "baseline", "300"),
        ("Vacuum (10s)", "vacuum", "5"),
        ("Measure (60s)", "measure", "60"),
        ("Recovery (60s)", "recovery", "180"),
    ]
    for i, (label, key, val) in enumerate(ops):
        y = top + 160 + i * 52
        _rounded_rect(draw, [36, y, W - 60, y + 44], C["ops"][key], radius=6)
        draw.text((50, y + 12), label, fill=C["text"], font=_font(13, True))
        draw.text((W - 150, y + 12), f"{val} sec", fill=C["text"], font=_font(13))
    _btn(draw, [36, H - 130, 260, H - 75], "Save Config", C["green"])
    save("04-settings-full.png", img)


def shot_05():
    img, draw, top = _window("Settings")
    draw.text((36, top), "Operation Duration + Break Time", fill=C["text"], font=_font(18, True))
    rows = [
        ("Heating", "heating", "1800"),
        ("Baseline", "baseline", "300"),
        ("Vacuum", "vacuum", "5"),
        ("Mix Air", "mix_air", "0"),
        ("Measure", "measure", "60"),
        ("Vac Return", "vacuum_return", "0"),
        ("Recovery", "recovery", "180"),
        ("Break", "break_time", "10"),
    ]
    for i, (label, key, val) in enumerate(rows):
        y = top + 50 + i * 58
        col = C["ops"][key]
        _rounded_rect(draw, [36, y, W - 60, y + 48], col, radius=6)
        draw.text((50, y + 14), label, fill=C["text"], font=_font(14, True))
        draw.text((W - 160, y + 14), f"{val} sec", fill=C["text"], font=_font(14, True))
    save("05-operation-times.png", img)


def shot_06():
    img, draw, top = _window("Settings")
    _btn(draw, [W // 2 - 120, H // 2 - 40, W // 2 + 120, H // 2 + 30], "Save Config", C["green"])
    draw.polygon([(W // 2 - 140, H // 2 - 5), (W // 2 - 160, H // 2 - 20), (W // 2 - 160, H // 2 + 10)], fill=C["accent"])
    save("06-save-config.png", img)


def shot_07():
    img, draw, top = _window("Control")
    _btn(draw, [W // 2 - 160, H // 2 - 35, W // 2 + 160, H // 2 + 35], "Start Auto Sequence", C["green"])
    draw.polygon([(W // 2 - 180, H // 2), (W // 2 - 200, H // 2 - 15), (W // 2 - 200, H // 2 + 15)], fill=C["accent"])
    save("07-start-auto.png", img)


def shot_08():
    img, draw, top = _window("Control")
    _rounded_rect(draw, [36, top + 20, W - 60, top + 200], "#fafafa", C["purple"], radius=10, width=2)
    draw.text((50, top + 35), "Operation Sequence", fill=C["purple"], font=_font(16, True))
    draw.text((50, top + 65), "Heat → BL → Vac → Mix → Meas → VR → Rec", fill=C["text"], font=_font(14))
    draw.text((50, top + 100), "Op2: Baseline [Recording]", fill=C["blue"], font=_font(20, True))
    draw.text((50, top + 140), "04:32", fill=C["accent"], font=_font(40, True))
    draw.text((50, top + 175), "Running...", fill=C["gray_dark"], font=_font(14))
    save("08-sequence-running.png", img)


def shot_09():
    img, draw, top = _window("Control")
    _rounded_rect(draw, [W - 300, top + 40, W - 60, top + 220], "#fafafa", C["green"], radius=10, width=2)
    draw.text((W - 280, top + 55), "Methane", fill=C["text"], font=_font(16))
    draw.text((W - 270, top + 95), "12.45", fill=C["green"], font=_font(48, True))
    draw.text((W - 130, top + 165), "ppm", fill=C["text"], font=_font(18))
    save("09-methane-result.png", img)


def shot_10():
    img, draw, top = _window("Display")
    draw.text((36, top), "Display (Process Data)", fill=C["text"], font=_font(18, True))
    _rounded_rect(draw, [36, top + 40, W - 60, top + 380], C["white"], C["gray"], radius=8, width=1)
    pts = [(60, top + 340), (200, top + 200), (400, top + 260), (600, top + 150), (900, top + 220), (1100, top + 180)]
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=C["blue"], width=3)
    _btn(draw, [W - 240, top + 400, W - 60, top + 450], "Refresh Graph", C["blue"])
    save("10-display-graph.png", img)


def shot_11():
    img, draw, top = _window("Settings")
    draw.text((36, top), "Loop Settings", fill=C["text"], font=_font(18, True))
    draw.text((50, top + 50), "[x] Infinite Loop", fill=C["text"], font=_font(16))
    draw.text((50, top + 100), "Cycles:  3", fill=C["text"], font=_font(16))
    draw.text((50, top + 140), "(0 = infinite)", fill=C["gray_dark"], font=_font(13))
    draw.text((50, top + 180), "Current Cycle: 1", fill=C["blue"], font=_font(16, True))
    save("11-loop-settings.png", img)


def shot_12():
    img, draw, top = _window("Settings")
    draw.text((36, top), "Cloud Upload", fill=C["text"], font=_font(18, True))
    draw.text((50, top + 55), "[ ] Auto-upload to Cloud", fill=C["text"], font=_font(16))
    draw.text((50, top + 100), "Cloud: —", fill=C["gray_dark"], font=_font(15))
    save("12-cloud-checkbox.png", img)


def shot_13():
    img, draw, top = _window("Control")
    _btn(draw, [36, top, 160, top + 50], "Manual", C["green"])
    _btn(draw, [180, top, 304, top + 50], "Auto", C["gray"], C["text"])
    draw.text((36, top + 70), "Hardware Controls", fill=C["text"], font=_font(16, True))
    devices = [("Value 1", True), ("Value 2", False), ("Pump", True), ("Heater", True),
                 ("Value 3", False), ("Value 4", False), ("Fan", False)]
    for i, (name, on) in enumerate(devices):
        col, row = i % 4, i // 4
        _device_box(draw, [36 + col * 150, top + 100 + row * 70, 170 + col * 150, top + 155 + row * 70], name, on)
    save("13-manual-mode.png", img)


def shot_14():
    img, draw, top = _window("Control")
    _btn(draw, [W // 2 - 80, H // 2 - 30, W // 2 + 80, H // 2 + 30], "Stop", C["red"])
    save("14-stop-button.png", img)


def main():
    print("Generating screenshots...")
    for fn in (shot_01, shot_02, shot_03, shot_04, shot_05, shot_06, shot_07,
               shot_08, shot_09, shot_10, shot_11, shot_12, shot_13, shot_14):
        fn()
    print("Done.")


if __name__ == "__main__":
    main()
