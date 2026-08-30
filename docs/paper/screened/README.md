# Paper ที่คัดแล้ว (`screened/`)

**อ่านในเบราว์เซอร์:** เปิด [`index.html`](index.html) (ค้น/กรอง tier · สรุป screening · Literature Review · ลิงก์ PDF)  
สร้างใหม่ได้ด้วย `py -3 _build_reader.py` ในโฟลเดอร์นี้

**Single source of truth** ของคลังอ้างอิงวิทยานิพนธ์ eNose–CH₄ นาข้าว  
อัปเดตรอบ reorg: 23 ก.ค. 2026 — รวมคลังเก่า + batch `candidates_2026-07-23` และจัดหมวดตาม taxonomy thesis-focused

| โฟลเดอร์ | ความหมาย (relevance tier) | paper ไฟล์ | `.bib` | `.ris` |
|----------|---------------------------|----------:|------:|------:|
| [`direct/`](direct/) | ใกล้โจทย์สูง: eNose/MOS+CH₄, ML calibration CH₄, chamber–GC ในนา/เกษตร, field low-cost CH₄ ที่ validate ได้ | 15 | 23 | 23 |
| [`supporting/`](supporting/) | รอง: mitigation/AWD เชิง agronomy, flux/model context, remote sensing, review ทั่วไป, companion proceedings | 18 | 32 | 32 |
| [`excluded/`](excluded/) | นอกประเด็นชัด / stub ชน DOI / classification ที่ไม่ใช้ใน lit review หลัก | 1 | 2 | 2 |

**Master bibliography (EndNote / LaTeX):**

- [`references.bib`](references.bib) — รวมทุก tier (57 entries)
- [`references.ris`](references.ris) — รวมทุก tier สำหรับ import EndNote ครั้งเดียว (57 records)

รายงาน: [`../citation-reorg-report-2026-07-23.md`](../citation-reorg-report-2026-07-23.md) · sync batch ก่อนหน้า: [`../citation-sync-report-2026-07-23.md`](../citation-sync-report-2026-07-23.md) · screening: [`../project-relevance-screening.md`](../project-relevance-screening.md)

---

## Taxonomy 2 ชั้น

### 1) Relevance tier (โฟลเดอร์)

ใช้ตัดสินว่าจะอ้างใน lit review หลักแค่ไหน — **ไม่** renumber หมายเลขอ้างอิงใน manuscript (`[n]`) ในรอบนี้

| Tier | เกณฑ์สั้น |
|------|-----------|
| `direct` | อย่างน้อยหนึ่ง: MOS/eNose+CH₄ · ML calibration/quantification ของ CH₄ · chamber–GC/reference ในนาหรือดินเกษตร · field low-cost CH₄ ที่ validate ได้ |
| `supporting` | ถ่ายโอนได้แต่ขาดองค์ประกอบหลัก: agronomy/mitigation/AWD, process model, review กว้าง, remote sensing, companion conference, industrial leak ที่ไม่ใช่ chamber นา |
| `excluded` | นอกประเด็น, classification-only โดยไม่มีหลักฐาน regression CH₄, หรือ metadata ชนกับงานคนละเรื่อง |

### 2) Thematic tags (index — ไม่แยกโฟลเดอร์ย่อย)

ใช้จัดกลุ่มตอนเขียนบท / EndNote groups

| Tag | ความหมาย | ตัวอย่าง stem (หลัง reorg) |
|-----|----------|---------------------------|
| `methane-paddy` | flux / drivers / ML จากปัจจัยนา (ไม่ใช่ MOS) | `2024_Zhou_…`, `2025_Zhang_ML_in-situ_…`, `2025_ML_geochemical_…` |
| `chamber-gc-methods` | chamber, GC/GC-FID, agricultural GHG methods | `2021_Zaman_…`, `2024_Mumu_…`, `2022_Vo_…`, `2022_LowCost_GC-FID_…`, `2021_Tokida_…` |
| `enose-mos-ch4` | MOS/eNose สำหรับ CH₄ | `2024_Domenech-Gil_…`, `2022_Furuta_…`, `2023_Shah_…`, `2024_Shah_…` |
| `ml-calibration-regression` | ML/regression calibration หรือ concentration estimation | `2024_Mitchell_…`, `2023_Andrews_…`, `2024_Kiplimo_…`, `2024_Lakhmi_…` |
| `field-iot-portable` | portable / IoT / near-field rice deployment | `2022_Rajasekar_…`, `2024_IoT_lowcost_…`, `2022_portable_…` |
| `review` | รีวิว/สังเคราะห์กว้าง | `2021_Ye_…`, `2025_Tyagi_…`, `2023_MOS_…` |
| `remote-sensing` | CH₄ นาข้าวจากรีโมทเซนซิง | `2025_Xu_…` |
| `gas-ml-general` | ML ก๊าซผสม/classification ที่ไม่ใช่ calibration CH₄ | `2022_SVM_…` + excluded |
| `livestock-ghg` | วิธีวัด GHG สัตว์ ไม่ใช่นา | `2022_Borhan_…` |

รายการ thematic เต็ม: [`thematic-index.md`](thematic-index.md) (รายงาน reorg มีเฉพาะตัวอย่าง)

---

## Mapping ID ที่เปลี่ยนในรอบนี้

| ก่อน | หลัง | stem | เหตุผล |
|------|------|------|--------|
| S23 | **D31** | `2022_LowCost_GC-FID_methane_rice_cultivation` | chamber–GC rice → direct |
| S24 | **D32** | `2021_Tokida_modified_closed_chamber_rice_methane` | closed chamber rice → direct |
| D01 | **S27** | `2022_water_fertilizer_management_methane_paddy_synthesis` | agronomy synthesis |
| D02 | **S28** | `2023_Anapalli_eddy_covariance_AWD_rice_methane` | AWD flux context |
| D03 | **S29** | `2023_multiyear_methane_N2O_AWD_Arkansas_rice` | AWD multiyear |
| D06 | **S30** | `2024_agro_technologies_GHG_mitigation_flooded_rice_India` | mitigation review-ish |
| D07 | **S31** | `2024_promoting_rice_upland_crops_mitigate_CH4` | mitigation preprint |
| D08 | **S32** | `2024_rice_root_rhizosphere_methane_emission` | rhizosphere mechanism |
| D09 | **S33** | `2025_CH4MOD_global_methane_emissions_rice_paddies` | process model |
| D12 | **S34** | `2025_methane_emissions_carbon_availability_soil_pH_gradient` | soil drivers |
| D13 | **S35** | `2025_product_type_rice_variety_agronomic_CH4_emissions` | agronomic meta-analysis |
| D14 | **S36** | `2025_straw_mulching_AWD_reduces_methane_paddy` | AWD+straw mitigation |

ID ที่ว่างหลังย้าย: **D01, D02, D03, D06–D09, D12–D14, S23, S24** — อย่าสร้าง entry ใหม่ใส่ช่องว่างเหล่านี้โดยไม่บันทึกในรายงาน

---

## หมายเหตุปฏิบัติ

- หลายเรื่องยังมีแค่ `.bib`/`.ris` ใน `cite/` (ยังไม่มี PDF ในคลัง) — ยังเป็น metadata-level evidence รอบ 30 ส.ค. 2026 เติม PDF + `file`/`pdf` ให้ Rajasekar, Zaman บทที่ 2, Domènech-Gil *ES&T*, Ye, Yin, Fu, Andrews, Mitchell, Lakhmi (PMC11174819), Minamikawa 2015, Conrad 2020
- `excluded/` มี stub ที่ DOI ชนงานคนละเรื่อง (`2024_diurnal_…`) และ classification papers ที่ไม่ผ่านเกณฑ์
- BibTeX ของ Moshayedi / Rusdianto / Ha / Cardador ถูกลบไปก่อนหน้า (orphan) — ไม่มีในคลังปัจจุบัน; ดู screening § orphan
- `candidates_2026-07-23/` ยังเป็น staging archive (คัดลอกแล้ว ไม่ลบ)
- โฟลเดอร์เก่า `docs/paper/{methane,enose,algorithm,methods-*}/` **ไม่มีแล้ว** — ย้ายเข้า `screened/` ครบ
- Preprint ที่รู้จาก DOI: `S31` (`10.21203/rs.3.rs-7887418/v1`); arXiv preprint: `2024_Wang_…` (`2412.13891`, ไม่มี Crossref DOI)
