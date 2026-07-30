# ponytail: one-shot builder for index.html — delete if unused
from pathlib import Path
import re
import json

root = Path(__file__).resolve().parent.parent  # docs/paper
base = Path(__file__).resolve().parent  # screened
out = base / "index.html"


def field(text, name):
    pat = rf"{name}\s*=\s*\{{((?:[^{{}}]|\{{[^{{}}]*\}})*)\}}"
    mm = re.search(pat, text, re.I | re.S)
    if not mm:
        return ""
    v = mm.group(1)
    v = re.sub(r"<[^>]+>", "", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v


def parse_authors(a):
    if not a:
        return ""
    parts = [p.strip() for p in re.split(r"\s+and\s+", a)]
    names = []
    for p in parts:
        if "," in p:
            last, first = p.split(",", 1)
            names.append(f"{first.strip()} {last.strip()}")
        else:
            names.append(p)
    if len(names) <= 2:
        return ", ".join(names)
    return f"{names[0]} et al."


file_index = {}
for tier in ["direct", "supporting", "excluded"]:
    td = base / tier
    if not td.exists():
        continue
    for f in td.iterdir():
        if f.is_file() and f.suffix.lower() in {".pdf", ".md", ".txt"}:
            rel = f"{tier}/{f.name}"
            stems = {f.stem}
            if f.stem.endswith("_extract"):
                stems.add(f.stem[: -len("_extract")])
            for s in stems:
                file_index.setdefault(s, []).append(
                    {
                        "path": rel,
                        "name": f.name,
                        "ext": f.suffix.lower(),
                        "size": f.stat().st_size,
                    }
                )

papers = []
for tier in ["direct", "supporting", "excluded"]:
    cite = base / tier / "cite"
    if not cite.exists():
        continue
    for bib in sorted(cite.glob("*.bib")):
        text = bib.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"@\w+\{([^,]+)", text)
        key = m.group(1).strip() if m else bib.stem
        title = field(text, "title")
        authors_raw = field(text, "author")
        year = field(text, "year")
        doi = field(text, "doi") or field(text, "DOI")
        journal = field(text, "journal") or field(text, "booktitle")
        url = field(text, "url")
        stem = bib.stem
        matched = list(file_index.get(stem, []))
        if not matched:
            for fs, flist in file_index.items():
                if fs == stem or fs.startswith(stem) or stem.startswith(fs):
                    matched = list(flist)
                    break
        seen = set()
        uniq = []
        for x in matched:
            if x["path"] not in seen:
                seen.add(x["path"])
                uniq.append(x)
        papers.append(
            {
                "key": key,
                "stem": stem,
                "tier": tier,
                "title": title or stem.replace("_", " "),
                "authors": parse_authors(authors_raw),
                "authors_full": authors_raw,
                "year": year,
                "doi": doi,
                "journal": journal,
                "url": url,
                "files": uniq,
                "bib": f"{tier}/cite/{bib.name}",
                "screen_id": "",
                "reason": "",
                "evidence": "",
                "why_th": "",
            }
        )

e01 = base / "excluded" / "2024_diurnal_methane_emission_rice_paddy_ebullition.md"
if e01.exists() and not any(p["stem"].startswith("2024_diurnal") for p in papers):
    papers.append(
        {
            "key": "E01_stub",
            "stem": e01.stem,
            "tier": "excluded",
            "title": "Diurnal methane emission rice paddy ebullition (stub — DOI collision)",
            "authors": "",
            "authors_full": "",
            "year": "2024",
            "doi": "",
            "journal": "",
            "url": "",
            "files": [
                {
                    "path": f"excluded/{e01.name}",
                    "name": e01.name,
                    "ext": ".md",
                    "size": e01.stat().st_size,
                }
            ],
            "bib": "",
            "screen_id": "E01",
            "reason": "Stub ที่ DOI ชนงานคนละเรื่อง — ห้าม cite",
            "evidence": "Stub ไม่มี bib ที่เชื่อถือได้",
            "why_th": "คัดออกเพราะ metadata ไม่น่าเชื่อถือ (DOI ชี้ไปคนละเรื่อง)",
        }
    )

screening = (root / "project-relevance-screening.md").read_text(
    encoding="utf-8", errors="replace"
)
blocks = re.split(r"\n(?=### (?:D|S|E)\d+)", screening)
screen_by_stem = {}
screen_by_doi = {}
screen_by_id = {}
for b in blocks:
    hm = re.match(r"### ((?:D|S|E)\d+)\s+[—\-]\s+(.+)", b)
    if not hm:
        continue
    sid, stitle = hm.group(1), hm.group(2).strip()
    reason_m = re.search(r"เหตุผล:\s*(.+)", b)
    evid_m = re.search(r"หลักฐาน:\s*(.+)", b)
    doi_m = re.search(r"`(10\.[^`]+)`", b)
    stems = re.findall(r"`[^`]*?/([A-Za-z0-9_\-\.]+)\.(?:pdf|md|bib|txt)`", b)
    stems = [s.replace("_extract", "") for s in stems]
    stems += re.findall(r"`([12]\d{3}_[A-Za-z0-9_\-]+)\.(?:pdf|md|bib)`", b)
    entry = {
        "id": sid,
        "title": stitle,
        "reason": reason_m.group(1).strip() if reason_m else "",
        "evidence": evid_m.group(1).strip() if evid_m else "",
        "doi": doi_m.group(1).strip() if doi_m else "",
        "stems": list(dict.fromkeys(stems)),
    }
    screen_by_id[sid] = entry
    if entry["doi"]:
        screen_by_doi[entry["doi"].lower()] = entry
    for s in entry["stems"]:
        screen_by_stem[s] = entry

# §10 batch tables: | ID | DOI | stem | reason |
for row in re.finditer(
    r"\|\s*((?:D|S|E)\d+)\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*([^|\n]+)\|",
    screening,
):
    sid, doi, stem, reason = (
        row.group(1),
        row.group(2).strip(),
        row.group(3).strip(),
        row.group(4).strip(),
    )
    entry = {
        "id": sid,
        "title": stem,
        "reason": reason,
        "evidence": "Batch find-paper 2026-07-23",
        "doi": doi,
        "stems": [stem],
    }
    screen_by_id.setdefault(sid, entry)
    screen_by_doi.setdefault(doi.lower(), entry)
    screen_by_stem.setdefault(stem, entry)

# §11 reorg ID remap (display current ID)
id_remap = {}
for row in re.finditer(
    r"\|\s*((?:D|S)\d+)\s*\|\s*((?:D|S)\d+)\s*\|\s*`([^`]+)`\s*\|",
    screening,
):
    old_id, new_id, stem = row.group(1), row.group(2), row.group(3).strip()
    id_remap[stem] = new_id
    if old_id in screen_by_id and stem not in screen_by_stem:
        screen_by_stem[stem] = screen_by_id[old_id]

for p in papers:
    hit = None
    if p["doi"] and p["doi"].lower() in screen_by_doi:
        hit = screen_by_doi[p["doi"].lower()]
    if not hit and p["stem"] in screen_by_stem:
        hit = screen_by_stem[p["stem"]]
    if not hit:
        for s, e in screen_by_stem.items():
            if s in p["stem"] or p["stem"] in s:
                hit = e
                break
    if hit:
        p["screen_id"] = id_remap.get(p["stem"], hit["id"])
        p["reason"] = hit["reason"]
        p["evidence"] = hit["evidence"]
        p["why_th"] = hit["reason"]
    elif p["stem"] in id_remap:
        p["screen_id"] = id_remap[p["stem"]]

draft = root.parent / "draft" / "4.2-สรุปสาระสำคัญจากงานวิจัยที่เกี่ยวข้อง.md"
if not draft.exists():
    draft = root / "literature-review-4.2.md"
lit_md = (
    draft.read_text(encoding="utf-8", errors="replace")
    if draft.exists()
    else "_ไม่พบไฟล์ lit review_"
)

extracts = {}
for p in papers:
    for f in p["files"]:
        if "extract" in f["name"].lower() or f["ext"] == ".txt":
            path = base / f["path"]
            if path.exists() and path.stat().st_size > 50:
                extracts[p["stem"]] = path.read_text(
                    encoding="utf-8", errors="replace"
                )[:12000]

for p in papers:
    for f in p["files"]:
        if f["ext"] == ".md" and f["size"] > 200:
            path = base / f["path"]
            txt = path.read_text(encoding="utf-8", errors="replace")
            if len(txt.strip()) > 100:
                extracts.setdefault(p["stem"], txt[:12000])

TAG_RULES = [
    (
        "methane-paddy",
        [
            "Zhou",
            "Zhang_ML_in-situ",
            "geochemical",
            "water_fertilizer",
            "Anapalli",
            "AWD",
            "rhizosphere",
            "CH4MOD",
            "carbon_availability",
            "product_type",
            "straw_mulching",
            "promoting_rice",
            "agro_technologies",
            "Nguyen",
            "Basheer",
            "comprehensive_review",
        ],
    ),
    (
        "chamber-gc-methods",
        ["Zaman", "Mumu", "Vo_", "LowCost_GC", "Tokida", "Bastviken"],
    ),
    (
        "enose-mos-ch4",
        [
            "Domenech",
            "Furuta",
            "Shah_TGS",
            "portable_lowcost",
            "chemiresistive",
            "Ahmad",
            "Yin_",
            "Dobrzyniewski",
            "RiveraMartinez",
        ],
    ),
    (
        "ml-calibration-regression",
        [
            "Mitchell",
            "Andrews",
            "Kiplimo",
            "Lakhmi",
            "ML_indirect",
            "Arif",
            "TFA",
            "graph",
        ],
    ),
    ("field-iot-portable", ["Rajasekar", "IoT_lowcost", "Jaya", "portable"]),
]


def tags_for(stem):
    t = []
    for tag, keys in TAG_RULES:
        if any(k.lower() in stem.lower() for k in keys):
            t.append(tag)
    return t


for p in papers:
    p["tags"] = tags_for(p["stem"])

tier_order = {"direct": 0, "supporting": 1, "excluded": 2}
papers.sort(key=lambda p: (tier_order.get(p["tier"], 9), p.get("year") or "9999", p["title"]))

data = {
    "papers": papers,
    "extracts": extracts,
    "lit_md": lit_md,
    "meta": {
        "n": len(papers),
        "n_direct": sum(1 for p in papers if p["tier"] == "direct"),
        "n_supporting": sum(1 for p in papers if p["tier"] == "supporting"),
        "n_excluded": sum(1 for p in papers if p["tier"] == "excluded"),
        "n_pdf": sum(1 for p in papers if any(f["ext"] == ".pdf" for f in p["files"])),
        "lit_source": str(draft.as_posix()) if draft.exists() else "",
    },
}
data_json_safe = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace(
    ">", "\\u003e"
)

html_out = (
    r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>eNose Methane — Screened Papers Reader</title>
<style>
:root {
  --bg: #f7f4ef;
  --panel: #fffdf9;
  --ink: #1c1917;
  --muted: #78716c;
  --line: #e7e0d5;
  --accent: #0f766e;
  --accent-soft: #ccfbf1;
  --direct: #0f766e;
  --supporting: #a16207;
  --excluded: #b91c1c;
  --side: 320px;
  --serif: "IBM Plex Serif", "Sarabun", Georgia, serif;
  --sans: "IBM Plex Sans Thai", "Sarabun", system-ui, sans-serif;
}
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; background: var(--bg); color: var(--ink); font-family: var(--sans); }
a { color: var(--accent); }
.app { display: grid; grid-template-columns: var(--side) 1fr; height: 100vh; }
.side {
  border-right: 1px solid var(--line); background: var(--panel);
  display: flex; flex-direction: column; min-height: 0;
}
.brand { padding: 1.1rem 1rem 0.6rem; border-bottom: 1px solid var(--line); }
.brand h1 { margin: 0; font-size: 1.05rem; font-family: var(--serif); letter-spacing: -0.02em; }
.brand p { margin: 0.35rem 0 0; color: var(--muted); font-size: 0.8rem; line-height: 1.35; }
.controls { padding: 0.75rem 1rem; border-bottom: 1px solid var(--line); display: grid; gap: 0.5rem; }
.controls input[type=search] {
  width: 100%; padding: 0.55rem 0.7rem; border: 1px solid var(--line);
  border-radius: 8px; background: #fff; font: inherit;
}
.filters { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.filters label {
  font-size: 0.75rem; padding: 0.25rem 0.55rem; border-radius: 999px;
  border: 1px solid var(--line); background: #fff; cursor: pointer; user-select: none;
}
.filters label.on-direct { background: #ecfdf5; border-color: #99f6e4; color: var(--direct); }
.filters label.on-supporting { background: #fffbeb; border-color: #fde68a; color: var(--supporting); }
.filters label.on-excluded { background: #fef2f2; border-color: #fecaca; color: var(--excluded); }
.list { overflow: auto; flex: 1; padding: 0.4rem; }
.card {
  width: 100%; text-align: left; border: 1px solid transparent; background: transparent;
  border-radius: 10px; padding: 0.7rem 0.75rem; cursor: pointer; font: inherit; color: inherit;
}
.card:hover { background: #f5f1ea; }
.card.active { background: var(--accent-soft); border-color: #99f6e4; }
.card .meta { display: flex; gap: 0.4rem; align-items: center; margin-bottom: 0.25rem; flex-wrap: wrap; }
.badge {
  font-size: 0.68rem; font-weight: 600; padding: 0.12rem 0.4rem; border-radius: 999px;
  text-transform: uppercase; letter-spacing: 0.03em;
}
.badge.direct { background: #ccfbf1; color: var(--direct); }
.badge.supporting { background: #fef3c7; color: var(--supporting); }
.badge.excluded { background: #fee2e2; color: var(--excluded); }
.badge.pdf { background: #e0e7ff; color: #3730a3; }
.badge.id { background: #f5f5f4; color: #44403c; }
.card .title { font-size: 0.86rem; line-height: 1.35; font-weight: 600; }
.card .sub { margin-top: 0.2rem; font-size: 0.75rem; color: var(--muted); }
.main { display: flex; flex-direction: column; min-width: 0; min-height: 0; }
.tabs { display: flex; gap: 0.25rem; padding: 0.65rem 1rem 0; border-bottom: 1px solid var(--line); background: var(--panel); }
.tab {
  border: 0; background: transparent; padding: 0.55rem 0.85rem; border-radius: 8px 8px 0 0;
  font: inherit; cursor: pointer; color: var(--muted); border-bottom: 2px solid transparent;
}
.tab.active { color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }
.view { overflow: auto; padding: 1.25rem 1.5rem 3rem; flex: 1; }
.empty { color: var(--muted); padding: 2rem 0; }
.paper-head h2 { margin: 0 0 0.4rem; font-family: var(--serif); font-size: 1.45rem; line-height: 1.3; }
.paper-head .byline { color: var(--muted); margin: 0 0 1rem; font-size: 0.92rem; }
.kv { display: grid; grid-template-columns: 7.5rem 1fr; gap: 0.35rem 0.75rem; margin: 1rem 0 1.25rem; font-size: 0.9rem; }
.kv dt { color: var(--muted); }
.kv dd { margin: 0; }
.box {
  background: var(--panel); border: 1px solid var(--line); border-radius: 12px;
  padding: 1rem 1.1rem; margin: 0.9rem 0;
}
.box h3 { margin: 0 0 0.5rem; font-size: 0.95rem; }
.box p, .box pre { margin: 0; white-space: pre-wrap; line-height: 1.55; font-size: 0.92rem; }
.actions { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0 0.25rem; }
.btn {
  display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.45rem 0.75rem;
  border-radius: 8px; border: 1px solid var(--line); background: #fff; color: var(--ink);
  text-decoration: none; font-size: 0.85rem;
}
.btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.tagrow { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
.tag { font-size: 0.72rem; padding: 0.15rem 0.45rem; border-radius: 6px; background: #f5f5f4; color: #57534e; }
.lit h1, .lit h2, .lit h3 { font-family: var(--serif); }
.lit h1 { font-size: 1.4rem; }
.lit h2 { font-size: 1.15rem; margin-top: 1.6rem; border-top: 1px solid var(--line); padding-top: 1rem; }
.lit h3 { font-size: 1rem; }
.lit p { line-height: 1.65; }
.lit blockquote { border-left: 3px solid var(--accent); margin: 0.8rem 0; padding: 0.2rem 0.8rem; color: var(--muted); }
.lit code { font-size: 0.85em; background: #f5f5f4; padding: 0.05rem 0.3rem; border-radius: 4px; }
.stats { font-size: 0.75rem; color: var(--muted); padding: 0.5rem 1rem; border-top: 1px solid var(--line); }
@media (max-width: 860px) {
  .app { grid-template-columns: 1fr; grid-template-rows: 45vh 55vh; }
  .side { border-right: 0; border-bottom: 1px solid var(--line); }
}
</style>
</head>
<body>
<div class="app">
  <aside class="side">
    <div class="brand">
      <h1>Screened Papers</h1>
      <p>คลังอ้างอิง eNose–CH₄ นาข้าว · อ่านสรุป + lit review</p>
    </div>
    <div class="controls">
      <input id="q" type="search" placeholder="ค้นชื่อ / ผู้แต่ง / ปี / DOI / stem…" autocomplete="off"/>
      <div class="filters" id="filters">
        <label class="on-direct"><input type="checkbox" data-tier="direct" checked/> direct</label>
        <label class="on-supporting"><input type="checkbox" data-tier="supporting" checked/> supporting</label>
        <label class="on-excluded"><input type="checkbox" data-tier="excluded" checked/> excluded</label>
      </div>
    </div>
    <div class="list" id="list"></div>
    <div class="stats" id="stats"></div>
  </aside>
  <main class="main">
    <div class="tabs">
      <button class="tab active" data-view="paper">รายเรื่อง</button>
      <button class="tab" data-view="lit">Literature Review</button>
      <button class="tab" data-view="about">เกี่ยวกับ</button>
    </div>
    <div class="view" id="view"></div>
  </main>
</div>
<script id="DATA" type="application/json">"""
    + data_json_safe
    + r"""</script>
<script>
const DATA = JSON.parse(document.getElementById('DATA').textContent);
let activeStem = null;
let viewMode = 'paper';

function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function hasPdf(p) { return (p.files || []).some(f => f.ext === '.pdf'); }
function doiUrl(p) {
  if (p.doi) return 'https://doi.org/' + p.doi;
  return p.url || '';
}

function filtered() {
  const q = document.getElementById('q').value.trim().toLowerCase();
  const tiers = new Set([...document.querySelectorAll('#filters input:checked')].map(i => i.dataset.tier));
  return DATA.papers.filter(p => {
    if (!tiers.has(p.tier)) return false;
    if (!q) return true;
    const blob = [p.title, p.authors, p.authors_full, p.year, p.doi, p.stem, p.journal, p.screen_id, p.reason, ...(p.tags||[])].join(' ').toLowerCase();
    return blob.includes(q);
  });
}

function renderList() {
  const items = filtered();
  const list = document.getElementById('list');
  list.innerHTML = items.map(p => `
    <button class="card ${p.stem === activeStem ? 'active' : ''}" data-stem="${esc(p.stem)}">
      <div class="meta">
        <span class="badge ${esc(p.tier)}">${esc(p.tier)}</span>
        ${p.screen_id ? `<span class="badge id">${esc(p.screen_id)}</span>` : ''}
        ${hasPdf(p) ? '<span class="badge pdf">PDF</span>' : ''}
        <span style="font-size:0.72rem;color:var(--muted)">${esc(p.year)}</span>
      </div>
      <div class="title">${esc(p.title)}</div>
      <div class="sub">${esc(p.authors || '—')}</div>
    </button>`).join('') || '<div class="empty" style="padding:1rem">ไม่พบรายการ</div>';
  document.getElementById('stats').textContent =
    `แสดง ${items.length} / ${DATA.papers.length} · PDF ${DATA.meta.n_pdf} เรื่อง · direct ${DATA.meta.n_direct} · supporting ${DATA.meta.n_supporting}`;
  list.querySelectorAll('.card').forEach(btn => {
    btn.addEventListener('click', () => {
      activeStem = btn.dataset.stem;
      viewMode = 'paper';
      syncTabs();
      renderList();
      renderView();
    });
  });
}

function mdLite(src) {
  let t = esc(src);
  t = t.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');
  t = t.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  t = t.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  t = t.replace(/^# (.+)$/gm, '<h1>$1</h1>');
  t = t.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  t = t.replace(/`([^`]+)`/g, '<code>$1</code>');
  t = t.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  t = t.replace(/^(?!<h\d|<blockquote|<ul|<li)(.+)$/gm, (m, p1) => {
    if (!p1.trim()) return '';
    if (p1.startsWith('<')) return p1;
    return '<p>' + p1 + '</p>';
  });
  return t;
}

function renderPaper(p) {
  if (!p) return '<div class="empty">เลือก paper จากรายการด้านซ้าย</div>';
  const files = p.files || [];
  const pdfs = files.filter(f => f.ext === '.pdf');
  const others = files.filter(f => f.ext !== '.pdf');
  const extract = DATA.extracts[p.stem];
  const link = doiUrl(p);
  return `
    <div class="paper-head">
      <div class="meta" style="margin-bottom:0.5rem">
        <span class="badge ${esc(p.tier)}">${esc(p.tier)}</span>
        ${p.screen_id ? `<span class="badge id">${esc(p.screen_id)}</span>` : ''}
        ${(p.tags||[]).map(t => `<span class="tag">${esc(t)}</span>`).join('')}
      </div>
      <h2>${esc(p.title)}</h2>
      <p class="byline">${esc(p.authors_full || p.authors || '—')}${p.year ? ' · ' + esc(p.year) : ''}${p.journal ? ' · ' + esc(p.journal) : ''}</p>
    </div>
    <div class="actions">
      ${pdfs.map(f => `<a class="btn primary" href="${esc(f.path)}" target="_blank">เปิด PDF · ${esc(f.name)}</a>`).join('')}
      ${link ? `<a class="btn" href="${esc(link)}" target="_blank" rel="noopener">DOI / แหล่งต้นฉบับ</a>` : ''}
      ${p.bib ? `<a class="btn" href="${esc(p.bib)}" target="_blank">BibTeX</a>` : ''}
      ${others.map(f => `<a class="btn" href="${esc(f.path)}" target="_blank">${esc(f.name)}</a>`).join('')}
    </div>
    <dl class="kv">
      <dt>Stem</dt><dd><code>${esc(p.stem)}</code></dd>
      <dt>DOI</dt><dd>${p.doi ? esc(p.doi) : '—'}</dd>
      <dt>หลักฐาน</dt><dd>${esc(p.evidence || (hasPdf(p) ? 'มี PDF ในคลัง' : (files.length ? 'มีไฟล์ในคลัง' : 'metadata (bib) เท่านั้น')))}</dd>
    </dl>
    <div class="box">
      <h3>ทำไมเกี่ยวข้องกับโปรเจกต์ (จาก screening)</h3>
      <p>${esc(p.why_th || p.reason || 'ยังไม่มีบันทึก screening ที่จับคู่ได้ — ดู Literature Review หรือเปิด PDF/DOI')}</p>
    </div>
    <div class="box">
      <h3>สรุป / extract ในคลัง</h3>
      ${extract ? `<pre>${esc(extract)}</pre>` : '<p>ยังไม่มี extract ใน repo สำหรับเรื่องนี้ — อ่าน PDF (ถ้ามี) หรือดูแท็บ Literature Review สำหรับบริบทสังเคราะห์</p>'}
    </div>`;
}

function renderAbout() {
  const m = DATA.meta;
  return `
    <h2 style="font-family:var(--serif);margin-top:0">เกี่ยวกับหน้านี้</h2>
    <p>หน้า HTML เดียวสำหรับอ่านคลัง <code>docs/paper/screened/</code> ของวิทยานิพนธ์ eNose–ML วัด CH₄ ในนาข้าว</p>
    <ul>
      <li>รายการ ${m.n} เรื่อง จาก BibTeX (direct ${m.n_direct} · supporting ${m.n_supporting} · excluded ${m.n_excluded})</li>
      <li>มี PDF ในคลัง ${m.n_pdf} เรื่อง</li>
      <li>เหตุผลคัดกรองดึงจาก <code>project-relevance-screening.md</code></li>
      <li>แท็บ Literature Review ดึงจาก <code>${esc(m.lit_source)}</code></li>
    </ul>
    <p style="color:var(--muted);font-size:0.9rem">เปิดไฟล์นี้ด้วยเบราว์เซอร์ (file://) จากโฟลเดอร์ screened เพื่อให้ลิงก์ PDF/bib ทำงาน — ไม่ต้องรันเซิร์ฟเวอร์</p>`;
}

function syncTabs() {
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.view === viewMode));
}

function renderView() {
  const view = document.getElementById('view');
  if (viewMode === 'lit') {
    view.className = 'view lit';
    view.innerHTML = mdLite(DATA.lit_md);
    return;
  }
  if (viewMode === 'about') {
    view.className = 'view';
    view.innerHTML = renderAbout();
    return;
  }
  view.className = 'view';
  const p = DATA.papers.find(x => x.stem === activeStem) || filtered()[0];
  if (p && !activeStem) activeStem = p.stem;
  view.innerHTML = renderPaper(p);
}

document.getElementById('q').addEventListener('input', () => { renderList(); if (viewMode==='paper') renderView(); });
document.querySelectorAll('#filters input').forEach(i => i.addEventListener('change', () => {
  i.parentElement.classList.toggle('on-' + i.dataset.tier, i.checked);
  renderList();
}));
document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => {
  viewMode = t.dataset.view;
  syncTabs();
  renderView();
}));

renderList();
renderView();
</script>
</body>
</html>
"""
)

out.write_text(html_out, encoding="utf-8")
print("Wrote", out)
print("papers", data["meta"]["n"], "pdf", data["meta"]["n_pdf"], "extracts", len(extracts))
un = [p["stem"] for p in papers if not p["reason"]]
print("unmatched reasons", len(un))
for u in un[:20]:
    print(" ", u)
