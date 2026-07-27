# Citation reorg report — 23 กรกฎาคม 2026

**งาน:** รวมคลังอ้างอิงเก่า + batch find-paper 2026-07-23 เป็น single source of truth ที่ `docs/paper/screened/` จัดหมวดใหม่ตาม taxonomy thesis eNose–CH₄ นาข้าว สร้าง master BibTeX/RIS สำหรับ EndNote และตรวจ duplicate/collision  
**กฎ:** ไม่ invent metadata · DOI normalize ก่อนตัดสินซ้ำ · ไม่แก้ manuscript 4.1/4.2/5 ในรอบนี้

## สรุปจำนวน

### ก่อน reorg (หลัง sync batch 2026-07-23)

| หมวด | bib (entries) | paper ไฟล์โดยประมาณ | RIS |
|------|-------------:|--------------------:|----:|
| direct | 30 | 20 | 6 (batch ใหม่เท่านั้น) |
| supporting | 23 | 9 | 6 |
| excluded | 2 | 1 | 0 |
| **รวมในคลังไฟล์** | **55** | **30** | **12** |

หมายเหตุ: screening เดิมรายงาน 60 เรื่อง (D30+S26+E04) แต่ orphan 4 รายการ (Moshayedi, Rusdianto, Ha, Cardador) + E01 ที่ไม่มี `.bib` ถูกตัดออกจากคลังไฟล์แล้ว → เหลือ **55** entries ที่มี sidecar

### หลัง reorg

| หมวด | bib | ris | paper ไฟล์ |
|------|----:|----:|----------:|
| `direct/` | **22** | **22** | **12** |
| `supporting/` | **31** | **31** | **17** |
| `excluded/` | **2** | **2** | **1** |
| **รวม** | **55** | **55** | **30** |

Master:

- `docs/paper/screened/references.bib` (55 entries)
- `docs/paper/screened/references.ris` (55 records)

## Mapping ก่อน → หลัง (ย้าย tier)

| ก่อน | หลัง | stem | ทิศทาง | เหตุผลสั้น |
|------|------|------|--------|------------|
| S23 | D31 | `2022_LowCost_GC-FID_methane_rice_cultivation` | supporting→direct | GC-FID / rice ground-truth |
| S24 | D32 | `2021_Tokida_modified_closed_chamber_rice_methane` | supporting→direct | modified closed chamber นาข้าว |
| D01 | S27 | `2022_water_fertilizer_management_methane_paddy_synthesis` | direct→supporting | agronomy synthesis |
| D02 | S28 | `2023_Anapalli_eddy_covariance_AWD_rice_methane` | direct→supporting | AWD flux (eddy) |
| D03 | S29 | `2023_multiyear_methane_N2O_AWD_Arkansas_rice` | direct→supporting | AWD multiyear |
| D06 | S30 | `2024_agro_technologies_GHG_mitigation_flooded_rice_India` | direct→supporting | mitigation agro-tech |
| D07 | S31 | `2024_promoting_rice_upland_crops_mitigate_CH4` | direct→supporting | mitigation preprint |
| D08 | S32 | `2024_rice_root_rhizosphere_methane_emission` | direct→supporting | rhizosphere mechanism |
| D09 | S33 | `2025_CH4MOD_global_methane_emissions_rice_paddies` | direct→supporting | process model |
| D12 | S34 | `2025_methane_emissions_carbon_availability_soil_pH_gradient` | direct→supporting | soil drivers |
| D13 | S35 | `2025_product_type_rice_variety_agronomic_CH4_emissions` | direct→supporting | agronomic meta-analysis |
| D14 | S36 | `2025_straw_mulching_AWD_reduces_methane_paddy` | direct→supporting | AWD+straw mitigation |

**ไม่ย้าย:** D04, D05, D10, D11, D15–D30, S01–S22, S25–S26, E01–E04 (สถานะไฟล์)

## Duplicates / collisions

| ตรวจ | ผล |
|------|-----|
| DOI ซ้ำ (normalized) | **0** |
| citation key ซ้ำ | **0** |
| stem ซ้ำข้าม tier | **0** |
| companion คนละ DOI | Domènech-Gil EST (`D16`) ≠ Eurosensors proceedings (`S22`) — คงแยก entry |

### Stub / metadata ที่ยังต้องระวัง

| รายการ | สถานะ |
|--------|--------|
| E01 `2024_diurnal_methane_emission_rice_paddy_ebullition.md` | stub ใน `excluded/`; **ไม่มี** `.bib` ที่เชื่อถือได้ (DOI ชี้ pteropod คนละเรื่อง) — ห้าม cite |
| `2022_Vo_TGA_vs_GC_…` (D24) | ชื่อไฟล์ปี/TGA ไม่ตรง metadata จริง (Vo et al. rice GHG throughput) — อ้างตาม DOI/title จาก bib |
| Wang 2024 graph models (S13) | **ไม่มี Crossref DOI**; RIS สร้างจากฟิลด์ BibTeX ที่มีอยู่ + arXiv `2412.13891` |
| S31 (เดิม D07) | preprint Research Square `10.21203/rs.3.rs-7887418/v1` |
| Arif S25 pages | Crossref ให้ `pages={231}` ขณะ path มี pp231-239 — ไม่แก้จากเดา |

## Orphan ที่ไม่อยู่ในคลังแล้ว (จากรอบ sync ก่อน)

ไม่กู้คืนในรอบนี้ (ไม่มี PDF/fulltext ใน repo):

- Moshayedi 2023 (เดิม E02)
- Rusdianto 2023/2024 (เดิม S09)
- Ha 2026 (เดิม S16)
- Cardador 2020 (เดิม S17)

ถ้าต้องการอ้างใหม่ ต้องดึง metadata จาก DOI ใหม่แล้วคัด tier ใหม่ — ห้ามเดา

## Candidates batch

`docs/paper/candidates_2026-07-23/` — PDF 12 ไฟล์ยังเป็น staging archive; **คัดเข้า screened ครบแล้ว** ในรอบ sync ก่อนหน้า (ไม่ลบ candidates)

โฟลเดอร์เก่า `docs/paper/{methane,enose,algorithm,methods-*}/` — **ไม่มีแล้ว** (ย้ายเข้า screened ก่อนหน้า)

## EndNote

1. Import ครั้งเดียว: `docs/paper/screened/references.ris`
2. หรือ import แยกตาม tier จาก `screened/{direct,supporting,excluded}/cite/*.ris`
3. ทุก entry ที่มี `.bib` ใน screened มี `.ris` คู่แล้ว (55/55)

แนะนำสร้าง EndNote groups ตาม thematic tags ด้านล่าง

## Thematic index

| Tag | stems (หลัง reorg) |
|-----|-------------------|
| `methane-paddy` | `2024_Zhou_…`, `2025_Zhang_ML_in-situ_…`, `2025_ML_geochemical_…`, + supporting agronomy S27–S36 |
| `chamber-gc-methods` | `2021_Zaman_…`, `2024_Mumu_…`, `2022_Vo_…`, `2022_LowCost_GC-FID_…` (D31), `2021_Tokida_…` (D32), `2020_Bastviken_…` |
| `enose-mos-ch4` | `2024_Domenech-Gil_…`, `2022_Furuta_…`, `2024_Furuta_…`, `2023_Shah_…`, `2024_Shah_…`, `2022_portable_…` |
| `ml-calibration-regression` | `2024_Mitchell_…`, `2023_Andrews_…`, `2024_Kiplimo_…`, `2024_Lakhmi_…`, `2022_ML_indirect_…`, `2024_RiveraMartinez_…` (S21) |
| `field-iot-portable` | `2022_Rajasekar_…`, `2024_IoT_lowcost_…`, `2025_Jaya_…` (S26) |

## สิ่งที่ต้อง sync ทีหลัง (ไม่ทำในรอบนี้)

1. **Manuscript / lit review 4.1–4.2 / บท 5** — ถ้ามีการอ้างเลข D##/S## หรือ path โฟลเดอร์เก่า ต้องอัปเดตตาม mapping ด้านบน (หมายเลข `[n]` ในข้อความอาจไม่กระทบ)
2. `docs/proposal-4.1-4.2-cites-draft6.md` — ตรวจ path cite ถ้ายังชี้ `methane/cite/` ฯลฯ
3. Full text ที่ยังเป็น stub: D03→S29, D04, D05, D06→S30, D10, D14→S36 และ metadata-only ใน enose/algorithm เดิม
4. Paywall / ไม่มี PDF: ส่วนใหญ่ของ D15–D24 (ยกเว้นที่มี PDF จาก batch ใหม่)

## ไฟล์ที่แก้/สร้าง

| ไฟล์ | การกระทำ |
|------|----------|
| `screened/{direct,supporting}/*` + `cite/*` | ย้าย 12 stems ตาม mapping |
| `screened/*/cite/*.ris` | เติม RIS จาก doi.org สำหรับ 42 entries + 1 จาก BibTeX/arXiv |
| `screened/references.bib` | สร้าง master |
| `screened/references.ris` | สร้าง master |
| `screened/README.md` | taxonomy + จำนวน + mapping |
| `project-relevance-screening.md` | §11 reorg |
| `citation-reorg-report-2026-07-23.md` | รายงานนี้ |

## ตรวจแล้วไม่พบปัญหา

- DOI / citation key collision หลังย้าย = 0
- ไม่ลบ PDF ที่ยังใช้อยู่
- ไม่แก้ข้อความ manuscript
- candidates ยังอยู่ครบเป็น archive
