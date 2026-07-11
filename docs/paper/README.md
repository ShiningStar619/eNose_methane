# คลังงานวิจัย (2020–2026)

**Literature review (6 หัวข้อ — Proposal §4.2):** [`literature-review-4.2.md`](literature-review-4.2.md)  
**Literature review (ฉบับเต็ม + corpus):** [`literature-review-enose-ml-methane-rice.md`](literature-review-enose-ml-methane-rice.md)

งานวิจัยจัดเป็น **7 หมวดหลัก** (+ `archive/` สำหรับงาน eNose ที่ไม่เกี่ยวกับ CH₄ นาข้าวโดยตรง):

| หมวด | โฟลเดอร์ | เนื้อหา | จำนวน |
|------|----------|---------|-------|
| **นาข้าว / CH₄** | [`methane/`](methane/) | การปล่อย CH₄ จากนาข้าว ปัจจัยควบคุม มาตรการลด emission | 12 PDF + 7 stub |
| **Chamber–GC** | [`methods-chamber-gc/`](methods-chamber-gc/) | วิธีอ้างอิง static chamber + GC / flux methodology | 4 PDF |
| **สเปกโทรสโกปี** | [`methods-spectroscopy/`](methods-spectroscopy/) | TDLAS, FTIR, TGA และรีวิวเทคโนโลยีตรวจจับ CH₄ | 2 PDF |
| **เซ็นเซอร์ภาคสนาม** | [`methods-field/`](methods-field/) | ระบบต้นทุนต่ำ / auto chamber ในแปลง | 1 PDF |
| **Remote sensing** | [`methods-remote/`](methods-remote/) | ดาวเทียม / UAV + ML ประเมิน CH₄ นาข้าว | 1 PDF |
| **eNose** | [`enose/`](enose/) | ฮาร์ดแวร์ eNose, MOS/TGS, การตรวจ CH₄ | 13 PDF |
| **Algorithm** | [`algorithm/`](algorithm/) | ML regression, calibration, รีวิว eNose+ML | 13 PDF |
| *(เก็บแยก)* | [`archive/`](archive/) | eNose อาหาร/คุณภาพพืช — ไม่ใช่ core thesis | 10 PDF |

## ดาวน์โหลดซ้ำ (Open Access)

```bash
python docs/paper/download_papers.py
```

ดึง PDF จาก Europe PMC / arXiv / Unpaywall — งานที่ไม่มี OA จะได้ไฟล์ `.md` พร้อมลิงก์ DOI

## ไฟล์สำคัญต่อวิทยานิพนธ์ (Proposal)

| อ้างอิง | ไฟล์ | หมวด |
|---------|------|------|
| [4] Nguyen | `methane/2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.pdf` | methane |
| [5] Rajasekar | `methods-field/2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf` | methods-field |
| [6] Zaman | `methods-chamber-gc/2021_Zaman_GHG_measurement_agricultural_soils_methodology.pdf` | methods-chamber-gc |
| [7] Mumu | `methods-chamber-gc/2024_Mumu_methodological_progress_agricultural_GHG.pdf` | methods-chamber-gc |
| [8] Tyagi | `methods-spectroscopy/2025_Tyagi_methane_sensing_environmental_review.pdf` | methods-spectroscopy |
| [9] Borhan | `methods-chamber-gc/2022_Borhan_sensors_methods_GHG_livestock.pdf` | methods-chamber-gc |
| [10] Domènech-Gil | `enose/2024_Domenech-Gil_eNose_environmental_methane_monitoring.pdf` | enose |
| [11] Baruah | `algorithm/2025_Baruah_ML_eNose_healthcare_agriculture_review.pdf` | algorithm |
| [12] Ahmad | `enose/2026_Ahmad_MOS_sensors_precision_agriculture.pdf` | enose |
| [13] Zhang | `methane/2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze.pdf` | methane |

## methane/

| ไฟล์ | หัวข้อ |
|------|--------|
| `2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.pdf` | คาร์บอนฟุตพริ้นท์นาข้าว |
| `2024_comprehensive_review_GHG_rice_paddies.pdf` | รีวิว GHG นาข้าว |
| `2024_promoting_rice_upland_crops_mitigate_CH4.pdf` | มาตรการลด CH₄ (rice–upland) |
| `2025_product_type_rice_variety_agronomic_CH4_emissions.pdf` | พันธุ์ข้าว / ปัจจัยเกษตร → CH₄ |
| `2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze.pdf` | ML + in-situ CH₄ นาข้าว (Yangtze) |
| `2022_water_fertilizer_management_methane_paddy_synthesis.pdf` | สังเคราะห์น้ำ–ปุ๋ย vs CH₄ |
| `2023_Anapalli_eddy_covariance_AWD_rice_methane.pdf` | Eddy covariance AWD |
| `2024_rice_root_rhizosphere_methane_emission.pdf` | รากข้าว / rhizosphere |
| `2025_CH4MOD_global_methane_emissions_rice_paddies.pdf` | โมเดล CH4MOD |
| `2025_methane_emissions_carbon_availability_soil_pH_gradient.pdf` | carbon availability + pH |
| *stub `.md`* | Zhou 2024, IoT GHG, straw mulching, ฯลฯ |

## methods-chamber-gc/

| ไฟล์ | หัวข้อ |
|------|--------|
| `2021_Zaman_GHG_measurement_agricultural_soils_methodology.pdf` | ระเบียบวิธี chamber non-isotopic |
| `2024_Mumu_methodological_progress_agricultural_GHG.pdf` | ความก้าวหน้าวิธีวัด GHG เกษตร |
| `2022_Borhan_sensors_methods_GHG_livestock.pdf` | เซ็นเซอร์ + chamber (หลักการ flux) |
| `2020_Cardador_GHG_measurement_methodologies_livestock_pig.pdf` | รีวิววิธีวัด GHG ฟาร์มหมู |

## methods-spectroscopy/

| ไฟล์ | หัวข้อ |
|------|--------|
| `2025_Tyagi_methane_sensing_environmental_review.pdf` | รีวิวเทคโนโลยีตรวจจับมีเทน |
| `2022_Vo_TGA_vs_GC_methane_agricultural_soils.pdf` | TGA เทียบ GC |

## methods-field/ · methods-remote/

| ไฟล์ | หัวข้อ |
|------|--------|
| `methods-field/2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf` | MQ4/TGS2611 + chamber นาข้าว |
| `methods-remote/2025_Xu_AI_ML_methane_rice_remote_sensing.pdf` | AI/ML + remote sensing นาข้าว |

## enose/ · algorithm/

ดูรายการเต็มในโฟลเดอร์ — ไฮไลต์: Domènech-Gil 2024, Rusdianto 2024, Ahmad 2026, Baruah 2025, Ha 2026, Lakhmi 2024, Mitchell 2024

## การเชื่อมกับโปรเจกต์

| องค์ประกอบโปรเจกต์ | หมวดที่เกี่ยวข้อง |
|-------------------|-----------------|
| TGS2612 array + Auto sequence | `enose/`, `algorithm/` |
| ΔV + Linear Regression | `algorithm/` (Lakhmi, Andrews, Mitchell) |
| BME280 + ปัจจัยสิ่งแวดล้อม | `methane/` (Zhang 2025), `enose/` (Domènech-Gil) |
| Static chamber + GC validate | `methods-chamber-gc/`, `methods-field/` |
