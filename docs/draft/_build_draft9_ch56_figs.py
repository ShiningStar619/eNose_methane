# -*- coding: utf-8 -*-
"""Insert diagrams/figures into §5–§6 of Proposal draft 8 → draft 9."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "docs/draft/Proposal draft 8.docx"
DST = ROOT / "docs/draft/Proposal draft 9.docx"

FIG = ROOT / "docs/draft/_fig_extract/final"
UG = ROOT / "docs/user-guide/assets"

# Insert BEFORE these anchors (end of section → start of next heading)
ANCHORS = {
    "before_5_4": "/body/p[@paraId=7FECFAC3]",  # end of 5.3
    "before_5_5": "/body/p[@paraId=7FECFAD1]",  # end of 5.4
    "before_5_6": "/body/p[@paraId=7FECFADF]",  # end of 5.5
    "before_6_3": "/body/p[@paraId=7FECFB07]",  # end of 6.2
    "before_6_5": "/body/p[@paraId=7FECFB0F]",  # end of 6.4
    "before_6_8": "/body/p[@paraId=7FECFB33]",  # end of 6.7
}


def oc(*args: str) -> str:
    r = subprocess.run(["officecli", *args], capture_output=True)
    out = (r.stdout or b"").decode("utf-8", "replace")
    err = (r.stderr or b"").decode("utf-8", "replace")
    if r.returncode not in (0, 2):
        raise RuntimeError(f"fail {r.returncode}: {args[:8]}\n{out}\n{err}")
    return out


def oc_json(*args: str) -> dict:
    r = subprocess.run(["officecli", *args, "--json"], capture_output=True)
    out = (r.stdout or b"").decode("utf-8", "replace")
    err = (r.stderr or b"").decode("utf-8", "replace")
    if r.returncode not in (0, 2):
        raise RuntimeError(f"fail {r.returncode}: {args[:8]}\n{out}\n{err}")
    return json.loads(out)


def _added_path(d: dict) -> str:
    data = d.get("data", d)
    blob = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    m = re.search(r"(/body/(?:p|group)(?:\[[^\]]+\]|/@[^\]]+\]))", blob)
    if not m:
        m = re.search(r"(/body/p\[@paraId=[^\]]+\])", blob)
    if m:
        return m.group(1)
    raise RuntimeError(f"cannot find added path: {blob[:800]}")


def add_caption(before: str, caption_suffix: str, seq_cache: str) -> str:
    d = oc_json(
        "add",
        str(DST),
        "/body",
        "--type",
        "paragraph",
        "--before",
        before,
        "--prop",
        "style=Caption",
        "--prop",
        "align=center",
    )
    path = _added_path(d)
    oc(
        "add",
        str(DST),
        path,
        "--type",
        "run",
        "--prop",
        "size=10pt",
        "--prop",
        "italic=true",
        "--prop",
        "text=รูปที่ ",
    )
    oc(
        "add",
        str(DST),
        path,
        "--type",
        "field",
        "--prop",
        "fieldType=seq",
        "--prop",
        "id=Figure",
        "--prop",
        f"text={seq_cache}",
    )
    oc(
        "add",
        str(DST),
        path,
        "--type",
        "run",
        "--prop",
        "size=10pt",
        "--prop",
        "italic=true",
        "--prop",
        f"text={caption_suffix}",
    )
    return path


def add_picture_block(
    before: str, src: Path, width: str, alt: str, caption_suffix: str, seq_cache: str
) -> None:
    cap = add_caption(before, caption_suffix, seq_cache)
    d = oc_json(
        "add",
        str(DST),
        "/body",
        "--type",
        "paragraph",
        "--before",
        cap,
        "--prop",
        "align=center",
        "--prop",
        "spaceAfter=6pt",
    )
    pic_para = _added_path(d)
    oc(
        "add",
        str(DST),
        pic_para,
        "--type",
        "picture",
        "--prop",
        f"src={src}",
        "--prop",
        f"width={width}",
        "--prop",
        f"alt={alt}",
    )
    print("OK picture", src.name, "→", pic_para)


def add_diagram_block(before: str, mmd: Path, width: str, caption_suffix: str, seq_cache: str) -> None:
    cap = add_caption(before, caption_suffix, seq_cache)
    d = oc_json(
        "add",
        str(DST),
        "/body",
        "--type",
        "diagram",
        "--before",
        cap,
        "--prop",
        f"src={mmd}",
        "--prop",
        f"width={width}",
        "--prop",
        "render=image",
        "--prop",
        "background=white",
    )
    print("OK diagram", mmd.name, "→", _added_path(d))


def main() -> None:
    # ensure clean copy
    try:
        oc("close", str(DST))
    except Exception:
        pass
    shutil.copy2(SRC, DST)
    print("copied →", DST.name)
    oc("open", str(DST))

    # Bottom-up so earlier section anchors stay valid
    add_diagram_block(
        ANCHORS["before_6_8"],
        FIG / "d13_pipeline.mmd",
        "14cm",
        ": กรอบการสร้างแบบจำลองและการประเมินผล (eNose เทียบกับ GC-FID)",
        "13",
    )
    add_picture_block(
        ANCHORS["before_6_5"],
        UG / "diagrams/auto-sequence-flow.png",
        "15cm",
        "Auto mode Op1 to Op7 sequence for eNose methane system",
        ": ลำดับการทำงานโหมดอัตโนมัติ Op1–Op7 และการวนรอบ (จากคู่มือผู้ใช้ระบบ eNose)",
        "12",
    )
    # same --before: later insert sits closer to anchor → insert methods first, then hardware
    add_diagram_block(
        ANCHORS["before_6_3"],
        FIG / "d10_methods.mmd",
        "13cm",
        ": กรอบวิธีวิจัยโดยรวมตั้งแต่ออกแบบระบบจนถึงทดสอบภาคสนาม",
        "10",
    )
    add_picture_block(
        ANCHORS["before_6_3"],
        UG / "screenshots/front-view.png",
        "12cm",
        "eNose methane hardware unit with Raspberry Pi touchscreen GUI",
        ": ชุดอุปกรณ์ eNose Methane และหน้าจอควบคุมบน Raspberry Pi (ภาพจากระบบจริงของโครงการ)",
        "11",
    )
    add_diagram_block(
        ANCHORS["before_5_6"],
        FIG / "d09_features.mmd",
        "12cm",
        ": การสกัดลักษณะเด่นจากสัญญาณ Baseline–Measure สู่การประมาณ ppm",
        "9",
    )
    add_picture_block(
        ANCHORS["before_5_5"],
        FIG / "06alt_ye_fig1_enose_analogy.png",
        "14cm",
        "Electronic nose analogy comparing biological and artificial olfaction",
        ": แนวคิดจมูกอิเล็กทรอนิกส์เปรียบเทียบกับระบบรับกลิ่นชีวภาพ (ดัดแปลงจาก Ye et al.)",
        "8",
    )
    add_diagram_block(
        ANCHORS["before_5_4"],
        FIG / "d07_chamber_flux.mmd",
        "14cm",
        ": หลักการเชื่อมความเข้มข้นใน static chamber สู่ฟลักซ์ CH₄",
        "7",
    )

    oc("close", str(DST))
    print("validate:", oc("validate", str(DST)))
    print(oc("view", str(DST), "stats"))
    q = oc_json("query", str(DST), "paragraph[style=Caption]")
    print("captions:", q.get("data", {}).get("matches"))
    print(oc("view", str(DST), "outline")[:800])


if __name__ == "__main__":
    main()
