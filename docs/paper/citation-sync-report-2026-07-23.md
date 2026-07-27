# Citation sync report — 23 กรกฎาคม 2026

**งาน:** คัดเข้า batch find-paper (`candidates_2026-07-23/`) → BibTeX + RIS (EndNote) + จัดหมวด `screened/`  
**แหล่ง metadata:** doi.org (`Accept: application/x-bibtex` และ `application/x-research-info-systems`) — ไม่เดา author/DOI/year  
**รายงานต้นทาง:** [`find-paper-report-2026-07-23.md`](find-paper-report-2026-07-23.md)

## สรุปจำนวน

| หมวด | รายการใหม่ | PDF | .bib | .ris |
|------|----------:|----:|-----:|-----:|
| `screened/direct/` | 6 (D25–D30) | 6 | 6 | 6 |
| `screened/supporting/` | 6 (S21–S26) | 6 | 6 | 6 |
| `screened/excluded/` | 0 | — | — | — |
| **รวม** | **12** | **12** | **12** | **12** |

**Collision กับคลังเดิม:** DOI ซ้ำ **0** · citation key ซ้ำ **0**  
**ไม่ลบ** ไฟล์ screened เดิม · candidates ยังคงเป็น staging archive (คัดลอก PDF ไม่ย้ายทิ้ง)

## Workflow ที่เลือก

ตาม [`screened/README.md`](screened/README.md) และข้อเสนอใน find-paper §F:

1. ตรวจ DOI กับ `screened/**/cite/*.bib` — ไม่ชน
2. ดึง BibTeX + RIS จาก doi.org ตาม DOI ในรายงาน
3. ตั้ง citation key = ชื่อไฟล์ stem (รูปแบบเดียวกับ Mitchell / Domènech-Gil เดิม)
4. คัดลอก PDF + วาง `.bib`/`.ris` เข้า `screened/{direct|supporting}/` และ `cite/`
5. อัปเดต `project-relevance-screening.md` §10 และ `screened/README.md` แบบมินิมอล

## Mapping (ก่อน → หลัง)

| ID | DOI | tier | PDF (screened) | .bib | .ris | candidates (ต้นทาง) |
|----|-----|------|----------------|------|------|---------------------|
| D25 / A1 | `10.3390/atmos15111313` | direct | `screened/direct/2024_Kiplimo_ML_calibration_lowcost_methane_TGS.pdf` | `screened/direct/cite/2024_Kiplimo_ML_calibration_lowcost_methane_TGS.bib` | `…/2024_Kiplimo_ML_calibration_lowcost_methane_TGS.ris` | `candidates_2026-07-23/ml-calibration/…` |
| D26 / A2 | `10.5194/amt-17-2103-2024` | direct | `screened/direct/2024_Furuta_lowcost_sensor_node_near_background_methane.pdf` | `screened/direct/cite/2024_Furuta_lowcost_sensor_node_near_background_methane.bib` | `…/2024_Furuta_lowcost_sensor_node_near_background_methane.ris` | `…/mos-enose-field/…` |
| D27 / A3 | `10.5194/amt-16-3391-2023` | direct | `screened/direct/2023_Shah_TGS2611-E00_methane_environmental_response.pdf` | `screened/direct/cite/2023_Shah_TGS2611-E00_methane_environmental_response.bib` | `…/2023_Shah_TGS2611-E00_methane_environmental_response.ris` | `…/mos-enose-field/…` |
| D28 / A4 | `10.5194/amt-15-5117-2022` | direct | `screened/direct/2022_Furuta_inexpensive_MOx_trace_methane.pdf` | `screened/direct/cite/2022_Furuta_inexpensive_MOx_trace_methane.bib` | `…/2022_Furuta_inexpensive_MOx_trace_methane.ris` | `…/mos-enose-field/…` |
| D29 / A5 | `10.5194/bg-17-3659-2020` | direct | `screened/direct/2020_Bastviken_lowcost_CH4_sensors_flux_chambers.pdf` | `screened/direct/cite/2020_Bastviken_lowcost_CH4_sensors_flux_chambers.bib` | `…/2020_Bastviken_lowcost_CH4_sensors_flux_chambers.ris` | `…/chamber-gc-rice/…` |
| D30 / A6 | `10.1039/d3ea00138e` | direct | `screened/direct/2024_Shah_TGS2611-C00_landfill_methane.pdf` | `screened/direct/cite/2024_Shah_TGS2611-C00_landfill_methane.bib` | `…/2024_Shah_TGS2611-C00_landfill_methane.ris` | `…/mos-enose-field/…` |
| S21 / B1 | `10.5194/amt-17-4257-2024` | supporting | `screened/supporting/2024_RiveraMartinez_MOS_methane_leak_emission_MLP.pdf` | `screened/supporting/cite/2024_RiveraMartinez_MOS_methane_leak_emission_MLP.bib` | `…/2024_RiveraMartinez_MOS_methane_leak_emission_MLP.ris` | `…/ml-calibration/…` |
| S22 / B2 | `10.3390/proceedings2024097079` | supporting | `screened/supporting/2024_DomenechGil_efficient_methane_monitoring_Eurosensors.pdf` | `screened/supporting/cite/2024_DomenechGil_efficient_methane_monitoring_Eurosensors.bib` | `…/2024_DomenechGil_efficient_methane_monitoring_Eurosensors.ris` | `…/supporting-secondary/…` |
| S23 / B3 | `10.3390/molecules27133968` | supporting | `screened/supporting/2022_LowCost_GC-FID_methane_rice_cultivation.pdf` | `screened/supporting/cite/2022_LowCost_GC-FID_methane_rice_cultivation.bib` | `…/2022_LowCost_GC-FID_methane_rice_cultivation.ris` | `…/chamber-gc-rice/…` |
| S24 / B4 | `10.2480/agrmet.d-20-00029` | supporting | `screened/supporting/2021_Tokida_modified_closed_chamber_rice_methane.pdf` | `screened/supporting/cite/2021_Tokida_modified_closed_chamber_rice_methane.bib` | `…/2021_Tokida_modified_closed_chamber_rice_methane.ris` | `…/chamber-gc-rice/…` |
| S25 / B5 | `10.11591/ijai.v14.i1.pp231-239` | supporting | `screened/supporting/2025_Arif_NN_GHG_irrigated_paddy.pdf` | `screened/supporting/cite/2025_Arif_NN_GHG_irrigated_paddy.bib` | `…/2025_Arif_NN_GHG_irrigated_paddy.ris` | `…/supporting-secondary/…` |
| S26 / B6 | `10.18502/kls.v9i1.19350` | supporting | `screened/supporting/2025_Jaya_IoT_GHG_soil_paddy.pdf` | `screened/supporting/cite/2025_Jaya_IoT_GHG_soil_paddy.bib` | `…/2025_Jaya_IoT_GHG_soil_paddy.ris` | `…/supporting-secondary/…` |

เส้นทางเต็มภายใต้ `docs/paper/`

## EndNote

- นำเข้าได้ทั้ง **`.ris`** (แนะนำสำหรับ EndNote) และ **`.bib`**
- ไฟล์ RIS ของ batch ใหม่อยู่คู่กับ `.bib` ใน `screened/{tier}/cite/`
- รายการ screened เดิมส่วนใหญ่ยังมีแค่ `.bib` (ยังไม่มี RIS ย้อนหลัง) — นอกขอบเขตรอบนี้

## ข้อผิดพลาดที่ต้องแก้

- **ไม่มี** DOI collision / key collision ในรอบนี้

## ความไม่แน่นอนที่ต้องตรวจต้นฉบับ

1. **Arif 2025 (`S25`)** — Crossref ให้ `pages={231}` ขณะที่ DOI path มี `pp231-239`; ไม่แก้เป็น 231–239 จากเดา ถ้าต้องการ pages ครบควรยืนยันจาก PDF/publisher
2. **Jaya 2025 (`S26`)** — ชื่อผู้แต่งท้ายจาก Crossref มีอักขระพิเศษในฟิลด์ `Abdul Aziz`; คงตาม publisher metadata
3. **Bastviken 2020 (`D29`)** — จัด **direct** ตามเกณฑ์ MOS ใน flux chamber (find-paper A5) แต่บริบท aquatic ไม่ใช่นาข้าว; หากต้องการเข้มงวดเฉพาะ rice context อาจย้ายไป supporting ภายหลัง
4. **Domènech-Gil proceedings (`S22`)** — คนละ DOI กับ EST journal ในคลัง (`10.1021/acs.est.3c06945` / D16); ไม่ใช่ซ้ำ แต่เป็น companion — ห้ามรวม entry

## ไม่สร้าง cite (นอก batch ที่ผ่าน)

| DOI | เหตุผล |
|-----|--------|
| `10.1021/acs.est.3c06945` | มีใน screened direct แล้ว (D16) |
| `10.3390/s24041066` | มีใน screened direct แล้ว (D20) |
| `10.3390/s22114141` | มีใน screened direct แล้ว (D23) |
| Qian / food eNose / MIRSA | ไม่แนะนำใน find-paper; ไม่มี PDF ใน candidates |

## ไฟล์ที่แก้/สร้าง

| ไฟล์ | การกระทำ |
|------|----------|
| `docs/paper/screened/direct/*.pdf` (6) | สร้าง (คัดลอกจาก candidates) |
| `docs/paper/screened/direct/cite/*.{bib,ris}` (12) | สร้าง |
| `docs/paper/screened/supporting/*.pdf` (6) | สร้าง |
| `docs/paper/screened/supporting/cite/*.{bib,ris}` (12) | สร้าง |
| `docs/paper/screened/README.md` | อัปเดตจำนวน |
| `docs/paper/project-relevance-screening.md` | เพิ่ม §10 + ปรับผลรวม |
| `docs/paper/citation-sync-report-2026-07-23.md` | สร้าง (รายงานนี้) |

## ตรวจแล้วไม่พบปัญหา

- DOI ทั้ง 12 รายการ resolve ได้และได้ BibTeX+RIS
- ไม่ทับไฟล์ screened เดิม
- ไม่ renumber citation ของ manuscript
- ไม่เรียก thesis-writer
