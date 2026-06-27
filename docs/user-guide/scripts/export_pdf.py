#!/usr/bin/env python3
"""Export single-file eNose user guide to HTML and PDF.

Usage from repo root:
    py docs/user-guide/scripts/export_pdf.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

GUIDE = Path(__file__).resolve().parents[1]
SOURCE = GUIDE / "eNose-User-Guide.md"
HTML_OUT = GUIDE / "eNose-User-Guide.html"
PDF_OUT = GUIDE / "eNose-User-Guide.pdf"


def find_pandoc() -> str:
    p = shutil.which("pandoc")
    if not p:
        raise SystemExit("pandoc not found — winget install JohnMacFarlane.Pandoc")
    return p


def find_chromium() -> Path | None:
    roots = [
        os.environ.get("PROGRAMFILES", r"C:\Program Files"),
        os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
        os.environ.get("LOCALAPPDATA", ""),
    ]
    names = [
        "Google/Chrome/Application/chrome.exe",
        "Microsoft/Edge/Application/msedge.exe",
    ]
    for root in roots:
        if not root:
            continue
        for name in names:
            path = Path(root) / name
            if path.is_file():
                return path
    return None


def export_html(pandoc: str) -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing {SOURCE}")
    css = GUIDE / "assets" / "style.css"
    cmd = [
        pandoc,
        str(SOURCE),
        "-o",
        str(HTML_OUT),
        "--from",
        "markdown+link_attributes",
        "--resource-path",
        str(GUIDE),
        "--standalone",
        "--embed-resources",
        "--toc",
        "--toc-depth=2",
        "-V",
        "lang=th",
        "--metadata",
        "title=eNose Methane — คู่มือผู้ใช้",
        "--metadata",
        "subtitle=Electronic Nose · GUI บน Raspberry Pi",
    ]
    if css.exists():
        cmd.extend(["--css", str(css)])
    subprocess.run(cmd, check=True, cwd=GUIDE)
    print(f"HTML: {HTML_OUT}")


def export_pdf_chromium() -> bool:
    browser = find_chromium()
    if not browser or not HTML_OUT.is_file():
        return False
    pdf_tmp = PDF_OUT.with_suffix(".tmp.pdf")
    pdf_tmp.unlink(missing_ok=True)
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_tmp}",
        "--no-pdf-header-footer",
        HTML_OUT.resolve().as_uri(),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    if not pdf_tmp.is_file() or pdf_tmp.stat().st_size < 500:
        return False
    pdf_tmp.replace(PDF_OUT)
    print(f"PDF:  {PDF_OUT}  (via {browser.name})")
    return True


def main() -> None:
    export_html(find_pandoc())
    if export_pdf_chromium():
        return
    print(f"PDF failed — open {HTML_OUT} → Print → Save as PDF")
    sys.exit(1)


if __name__ == "__main__":
    main()
