#!/usr/bin/env python3
"""Capture real GUI screenshots for docs/user-guide.

Run from repo root:
    py docs/user-guide/scripts/capture_gui_screenshots.py
"""
from __future__ import annotations

import os
import sys
import tkinter as tk
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "docs" / "user-guide" / "assets" / "screenshots"
DEMO_CSV = ROOT / "acquisition" / "processed_data" / "adc1263_demo_capture.csv"

# Native Pi touchscreen size (portrait) — matches HardwareControlGUI default geometry
WIN_SIZE = "480x800"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "program"))
os.chdir(ROOT)
os.environ.setdefault("PYTHONIOENCODING", "utf-8")


def _ensure_demo_csv() -> None:
    try:
        import numpy as np
        import pandas as pd
    except ImportError:
        return
    DEMO_CSV.parent.mkdir(parents=True, exist_ok=True)
    t = np.linspace(0, 60, 600)
    pd.DataFrame({
        "elapsed_time_sec": t,
        "ss1_lp_ma": 0.12 + 0.04 * np.sin(t / 8),
        "ss2_lp_ma": 0.15 + 0.03 * np.sin(t / 6 + 1),
        "ss3_lp_ma": 0.10 + 0.02 * np.cos(t / 10),
        "ss4_lp_ma": 0.11 + 0.025 * np.sin(t / 7 + 2),
    }).to_csv(DEMO_CSV, index=False)


def _grab_bbox(x1: int, y1: int, x2: int, y2: int):
    from PIL import ImageGrab
    return ImageGrab.grab(bbox=(x1, y1, x2, y2))


def _grab_window(root: tk.Tk):
    root.update_idletasks()
    root.update()
    pad = 10
    return _grab_bbox(
        root.winfo_rootx() - pad,
        root.winfo_rooty() - pad,
        root.winfo_rootx() + root.winfo_width() + pad,
        root.winfo_rooty() + root.winfo_height() + pad,
    )


def _grab_widget(widget: tk.Widget, pad: int = 12):
    widget.update_idletasks()
    return _grab_bbox(
        widget.winfo_rootx() - pad,
        widget.winfo_rooty() - pad,
        widget.winfo_rootx() + widget.winfo_width() + pad,
        widget.winfo_rooty() + widget.winfo_height() + pad,
    )


def _save(img, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    img.save(path, "PNG")
    print(f"  saved {path.relative_to(ROOT)}")


def _find_labelframe(parent: tk.Widget, keyword: str) -> tk.Widget | None:
    for w in parent.winfo_children():
        if isinstance(w, tk.LabelFrame) and keyword in str(w.cget("text")):
            return w
    return None


def main() -> None:
    _ensure_demo_csv()

    import tkinter.messagebox as mb
    mb.showinfo = mb.showwarning = mb.showerror = lambda *a, **k: None

    import gui as gui_module
    HardwareControlGUI = gui_module.HardwareControlGUI

    root = tk.Tk()
    root.title("eNose Hardware Control")
    root.geometry(WIN_SIZE)

    app = HardwareControlGUI(root)
    root.update_idletasks()
    root.lift()
    root.focus_force()

    def grab_mode_row():
        return _grab_widget(app.manual_btn.master, 24)

    def grab_op_times():
        frames = list(app.operation_frames.values())
        if not frames:
            return _grab_window(root)
        x1 = min(f.winfo_rootx() for f in frames) - 20
        y1 = min(f.winfo_rooty() for f in frames) - 12
        x2 = max(f.winfo_rootx() + f.winfo_width() for f in frames) + 20
        y2 = max(f.winfo_rooty() + f.winfo_height() for f in frames) + 12
        return _grab_bbox(x1, y1, x2, y2)

    def grab_save_btn():
        for w in app.pages["settings"].winfo_children():
            for c in w.winfo_children():
                if isinstance(c, tk.Button) and "Save" in str(c.cget("text")):
                    return _grab_widget(c, 48)
        return _grab_window(root)

    shots: list[tuple[str, Callable, Callable | None]] = [
        ("01-pi-desktop-gui.png", lambda: (app.show_page("control"), app.set_mode("auto")), None),
        ("02-control-overview.png", lambda: (app.show_page("control"), app.set_mode("auto")), None),
        ("03-select-auto.png", lambda: (app.show_page("control"), app.set_mode("auto")), grab_mode_row),
        ("04-settings-full.png", lambda: (root.geometry(WIN_SIZE), app.show_page("settings")), None),
        ("05-operation-times.png", lambda: app.show_page("settings"), grab_op_times),
        ("06-save-config.png", lambda: app.show_page("settings"), grab_save_btn),
        ("07-start-auto.png", lambda: (app.show_page("control"), app.set_mode("auto")), lambda: _grab_widget(app.start_btn, 36)),
        ("08-sequence-running.png", lambda: (
            app.show_page("control"),
            app.set_mode("auto"),
            app.progress_label.configure(text="Op2: Baseline [Recording]", fg="#3498db"),
            app.timer_label.configure(text="04:32"),
            app.status_label.configure(text="Status: Running...", fg="#3498db"),
        ), None),
        ("09-methane-result.png", lambda: (
            app.show_page("control"),
            app.set_mode("auto"),
            app._set_methane_ppm_readout("12.45"),
        ), None),
        ("10-display-graph.png", lambda: (
            root.geometry(WIN_SIZE),
            app.show_page("display"),
            app._plot_process_data() if hasattr(app, "_plot_process_data") else None,
        ), None),
        ("11-loop-settings.png", lambda: (
            root.geometry(WIN_SIZE),
            app.show_page("settings"),
            app.infinite_loop.set(False),
            app.loop_count.set("3"),
            app.cycle_label.configure(text="Current Cycle: 1"),
            app.toggle_loop_settings(),
        ), lambda: _grab_widget(_find_labelframe(app.pages["settings"], "Loop") or root, 16)),
        ("12-cloud-checkbox.png", lambda: app.show_page("settings"),
         lambda: _grab_widget(_find_labelframe(app.pages["settings"], "Cloud") or root, 16)),
        ("13-manual-mode.png", lambda: (
            app.show_page("control"),
            app.set_mode("manual"),
            app.set_device_state("s_valve1", True),
            app.set_device_state("pump", True),
            app.set_device_state("heater", True),
        ), None),
        ("14-stop-button.png", lambda: (app.show_page("control"), app.set_mode("auto")),
         lambda: _grab_widget(app.stop_btn, 44)),
    ]

    state = {"i": 0}

    def run_step():
        i = state["i"]
        if i >= len(shots):
            print("Done.")
            root.quit()
            return
        name, setup, crop_fn = shots[i]
        print(f"Capture {i + 1}/{len(shots)}: {name}")
        setup()
        root.update_idletasks()
        root.update()

        def snap():
            try:
                img = crop_fn() if crop_fn else _grab_window(root)
                _save(img, name)
            except Exception as exc:
                print(f"  WARN {name}: {exc}")
            state["i"] += 1
            root.after(150, run_step)

        root.after(450, snap)

    print("Capturing GUI screenshots...")
    root.after(600, run_step)
    root.mainloop()
    try:
        root.destroy()
    except tk.TclError:
        pass


if __name__ == "__main__":
    main()
