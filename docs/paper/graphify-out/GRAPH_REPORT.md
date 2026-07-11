# Graph Report - paper  (2026-07-07)

## Corpus Check
- 11 files · ~662,156 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 57 nodes · 54 edges · 15 communities (7 shown, 8 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `229bdec8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]

## God Nodes (most connected - your core abstractions)
1. `Literature Review: การประยุกต์ใช้จมูกอิเล็กทรอนิกส์ ร่วมกับการเรียนรู้ของเครื่องในการประเมินปริมาณก๊าซมีเทนในนาข้าว` - 13 edges
2. `?????????????????` - 7 edges
3. `main()` - 4 edges
4. `1. บริบท: การเกิดและการวัด CH₄ จากนาข้าว` - 4 edges
5. `2. จมูกอิเล็กทรอนิกส์และเซ็นเซอร์ MOS สำหรับมีเทน` - 4 edges
6. `3. Machine Learning สำหรับประเมินความเข้มข้น/ปริมาณ CH₄` - 4 edges
7. `curl_download()` - 3 edges
8. `write_stub()` - 3 edges
9. `candidate_urls()` - 3 edges
10. `file_hash()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `file_hash()` --references--> `Path`  [EXTRACTED]
  migrate_thesis_papers.py →   _Bridges community 2 → community 7_

## Import Cycles
- None detected.

## Communities (15 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.20
Nodes (9): 10. บรรณานุกรม (References), 5. งานวิจัยหลัก (Key Papers), 6. ประเด็นที่วรรณกรรมเห็นพ้อง (Themes & Consensus), 7. คำถามเปิดและข้อถกเถียง (Open Questions), 8. แนวโน้มล่าสุด (Emerging Trends, 2024–2026), 9. ข้อจำกัดของรีวิวนี้, Literature Review: การประยุกต์ใช้จมูกอิเล็กทรอนิกส์ ร่วมกับการเรียนรู้ของเครื่องในการประเมินปริมาณก๊าซมีเทนในนาข้าว, Rerun Inputs (+1 more)

### Community 1 - "Community 1"
Cohesion: 0.29
Nodes (8): ????????????????? � ?????????????????????????, ?????????????????, 1-chamber-GC-flux-methods, 2-spectroscopy-TDLAS-TGA-FTIR, 3-auto-chamber-field-sensors, 4-enose-MOS-ML, 5-remote-sensing-AI-modeling, _misc-related

### Community 2 - "Community 2"
Cohesion: 0.52
Nodes (6): candidate_urls(), curl_download(), main(), unpaywall_pdf(), write_stub(), Path

### Community 3 - "Community 3"
Cohesion: 0.50
Nodes (4): 1.1 นาข้าวเป็นแหล่ง CH₄ สำคัญ, 1.2 ความผันผวนและความท้าทายในการวัดภาคสนาม, 1.3 งานสำคัญจาก `docs/paper/methane/`, 1. บริบท: การเกิดและการวัด CH₄ จากนาข้าว

### Community 4 - "Community 4"
Cohesion: 0.50
Nodes (4): 2.1 หลักการ eNose, 2.2 งาน eNose เฉพาะทาง CH₄, 2.3 งานที่เชื่อม eNose กับนาข้าวโดยตรง, 2. จมูกอิเล็กทรอนิกส์และเซ็นเซอร์ MOS สำหรับมีเทน

### Community 5 - "Community 5"
Cohesion: 0.50
Nodes (4): 3.1 ML calibration เซ็นเซอร์ต้นทุนต่ำ, 3.2 Regression และ deep learning บน sensor array, 3.3 ML สำหรับ CH₄ ในนาข้าว (ไม่ใช่ eNose), 3. Machine Learning สำหรับประเมินความเข้มข้น/ปริมาณ CH₄

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (3): 4.1 สรุปช่องว่างทางวิจัย (research gap), 4.2 ความสอดคล้องกับโปรเจกต์ eNose Methane, 4. การบูรณาการ: eNose + ML + นาข้าว — ช่องว่างและแนวทาง

## Knowledge Gaps
- **32 isolated node(s):** `1-chamber-GC-flux-methods`, `2-spectroscopy-TDLAS-TGA-FTIR`, `3-auto-chamber-field-sensors`, `4-enose-MOS-ML`, `5-remote-sensing-AI-modeling` (+27 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Literature Review: การประยุกต์ใช้จมูกอิเล็กทรอนิกส์ ร่วมกับการเรียนรู้ของเครื่องในการประเมินปริมาณก๊าซมีเทนในนาข้าว` connect `Community 0` to `Community 3`, `Community 4`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Why does `1. บริบท: การเกิดและการวัด CH₄ จากนาข้าว` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `2. จมูกอิเล็กทรอนิกส์และเซ็นเซอร์ MOS สำหรับมีเทน` connect `Community 4` to `Community 0`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **What connects `1-chamber-GC-flux-methods`, `2-spectroscopy-TDLAS-TGA-FTIR`, `3-auto-chamber-field-sensors` to the rest of the system?**
  _32 weakly-connected nodes found - possible documentation gaps or missing edges._