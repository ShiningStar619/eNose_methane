# Cite map: Proposal draft 6 — §4.1 ถึง §4.2

**แหล่ง:** `docs/Proposal draft 6.pdf`  
**คลังอ้างอิง:** `docs/paper/` + `docs/paper/literature-review-4.2-draft.md`  
**หลักการ:** รวมเป็น **รายการ References ชุดเดียว** — §4.1 ใช้ `[1]`–`[12]` ตาม IEEE ท้าย draft 6; §4.2 ใช้เลขต่อจาก `[13]` ขึ้นไป (หรือ reuse `[4]`–`[12]` เมื่ออ้างงานเดิม)

---

## ปัญหาใน draft 6 ตอนนี้

| ปัญหา | รายละเอียด |
|--------|------------|
| **เลขชนกัน** | §4.1: `[1]` = Krungsri; §4.2.1: `[1]` = Nguyen — คนละงาน |
| **Refs ไม่ครบ** | ข้อความ §4.2 อ้างถึง `[14]`–`[25]` แต่ท้ายเอกสารมีแค่ IEEE `[1]`–`[12]` (และรายการชุดสองเริ่มใหม่ที่ 1–7) |
| **§4.1 ว่าง** | ท้ายประโยค “ห้องแล็บ…แปลงจริงได้” มี `[][][]` — ยังไม่มีเลข |
| **§4.1 ผิดความหมาย** | `[3]` น้ำขัง → Thairath (ข่าวส่งออก); `[5,6]` chamber–GC → Rajasekar ไม่ใช่ระเบียบวิธี GC |

---

## A. §4.1 — cite ที่แนะนำ (แก้เฉพาะเลข)

| จุดในข้อความ | เดิม (draft 6) | **ใหม่** | ไฟล์ใน `docs/paper` |
|--------------|----------------|----------|---------------------|
| ส่งออก / รายได้ | `[1, 2]` | คง `[1, 2]` | — (นอกคลัง) |
| ครัวเรือน / พื้นที่นา | `[1, 2]` | คง `[1, 2]` | — |
| น้ำขัง นาปี–นาปรัง | `[3]` | **`[4]`** | `methane/2023_Nguyen_...pdf` |
| methanogens / ปล่อย CH₄ | `[4]` | คง `[4]` | ไฟล์เดียวกัน |
| สัดส่วน 12–26% | `[4]` | คง `[4]` | ไฟล์เดียวกัน |
| chamber+GC วิธีอ้างอิง | `[5, 6]` | **`[6, 7]`** | Zaman + Mumu |
| แรงงาน / sampling | `[6, 7]` | คง `[6, 7]` | Zaman + Mumu |
| สเปกโทรสโกปี + ดาวเทียม | `[8]` | คง `[8]` *(หรือ `[8, 22]` ถ้าเพิ่ม Xu)* | Tyagi; Xu = `[22]` ด้านล่าง |
| ประโยค eNose/เซ็นเซอร์ราคาประหยัด | *(ว่าง)* | **`[5, 12]`** | Rajasekar + Ahmad |
| eNose+ML + T/H/P | `[10]` | คง `[10]` | Domènech-Gil |
| “ยังเน้นห้องแล็บ…” | `[][][]` | **`[11, 12]`** | Baruah + Ahmad (**อย่าใส่ `[10]`**) |
| Domènech-Gil ชื่อในข้อความ | `[10]` | คง `[10]` | Domènech-Gil |
| อ้างอิง chamber–GC ท้ายย่อหน้า | *(ว่าง)* | **`[6, 7]`** | Zaman + Mumu |

---

## B. §4.2 — แผนที่เลข lit-review → เลข Proposal รวม

ใน draft 6 ข้อความ §4.2 ยังใช้เลขจาก `literature-review-4.2-draft.md` (`[1]`–`[25]`) ซึ่ง **ชนกับ §4.1**  
ตารางด้านล่างคือเลขที่ควรใส่แทนใน Proposal:

### 4.2.1 การปล่อย CH₄ และปัจจัยควบคุม

| เนื้อหา | เลขในข้อความปัจจุบัน | **เลขใหม่** | งาน / path |
|---------|----------------------|-------------|------------|
| methanogens / กลไก | `[1]` | **`[4]`** | Nguyen — `methane/2023_Nguyen_...pdf` |
| 10–12% Monsoon Asia | `[2]` | **`[13]`** | Zhou 2024 — `methane/2024_Zhou_...md` *(stub)* |
| ~11% ของ 308 Tg | `[3]` | **`[14]`** | งาน discovery / รีวิว mitigation *(ยังไม่มี PDF ในคลัง — ใส่ DOI เมื่อมี)* |
| AWD ↓64.5±12.3% | `[4]` | **`[15]`** | Rafy et al. 2025 *(Firecrawl; ยังไม่มีในคลัง)* |
| eddy covariance AWD | `[5]` | **`[16]`** | Anapalli — `methane/2023_Anapalli_...pdf` |
| rhizosphere / ราก | `[6]` | **`[17]`** | `methane/2024_rice_root_rhizosphere_...pdf` |
| carbon availability + pH | `[7]` | **`[18]`** | `methane/2025_methane_emissions_carbon_availability_...pdf` |
| Yang EENF / พันธุ์ข้าว | `[8]` | **`[19]`** | `methane/2025_product_type_rice_variety_...pdf` |
| CH4MOD | `[9]` | **`[20]`** | Hu et al. 2024 — `methane/2025_CH4MOD_...pdf` |
| ความผันผวนตามฤดูกาล | `[2]` | **`[13]`** | Zhou |

### 4.2.2 Chamber–GC มาตรฐาน

| เนื้อหา | เดิม | **ใหม่** | path |
|---------|------|----------|------|
| Zaman / วิธีอ้างอิง | `[10]` | **`[6]`** | `methods-chamber-gc/2021_Zaman_...pdf` |
| Mumu / ข้อจำกัด | `[11]` | **`[7]`** | `methods-chamber-gc/2024_Mumu_...pdf` |
| *(ถ้าเพิ่ม Vo เพื่อยืนยัน GC)* | — | **`[21]`** | Vo TGA vs GC — `methods-spectroscopy/2022_Vo_...pdf` |
| *(ถ้าเพิ่ม Borhan)* | — | **`[9]`** | `methods-chamber-gc/2022_Borhan_...pdf` |

### 4.2.3 วิธีวัดอื่น

| เนื้อหา | เดิม | **ใหม่** | path |
|---------|------|----------|------|
| Tyagi สเปกโทรสโกปี *(ข้อความยังไม่มี cite)* | — | **`[8]`** | `methods-spectroscopy/2025_Tyagi_...pdf` |
| Vo et al. TGA | `[14]` | **`[21]`** | `methods-spectroscopy/2022_Vo_...pdf` |
| Xu remote sensing | `[15]` | **`[22]`** | `methods-remote/2025_Xu_...pdf` *(ตรวจว่ามีไฟล์)* |
| Rajasekar MQ4/TGS | `[16]` | **`[5]`** | `methods-field/2022_Rajasekar_...pdf` |
| Zhang ML นาข้าว | `[17]` | **`[23]`** | `methane/2025_Zhang_ML_in-situ_...pdf` |

### 4.2.4 eNose + ML

| เนื้อหา | เดิม | **ใหม่** | path |
|---------|------|----------|------|
| Ye et al. eNose+ML | `[18]` | **`[24]`** | `enose/2021_Ye_...pdf` |
| Domènech-Gil | `[19]` | **`[10]`** | `enose/2024_Domenech-Gil_...pdf` |
| Ahmad MOS | `[20]` | **`[12]`** | `enose/2026_Ahmad_...pdf` |
| Yin CH₄/CO | `[21]` | **`[25]`** | `enose/2023_Yin_...pdf` |
| MOS chemiresistive review | `[22]` | **`[26]`** | `enose/2023_MOS_chemiresistive_...pdf` |
| Baruah | `[23]` | **`[11]`** | `algorithm/2025_Baruah_...pdf` |
| Andrews | `[24]` | **`[27]`** | `algorithm/2023_Andrews_...pdf` |
| Mitchell | `[25]` | **`[28]`** | `algorithm/2024_Mitchell_...pdf` |
| *(ถ้าเพิ่ม Lakhmi / Jiang / Wang)* | — | `[29]`–`[31]` | `algorithm/2024_Lakhmi_...`, `...Jiang_...`, `...Wang_...` |

---

## C. รายการ References รวมที่ควรมีท้าย Proposal (§4.1–4.2)

### คงจาก draft 6 (IEEE)

| # | งาน |
|---|-----|
| [1] | Sowcharoensuk, Krungsri Research, 2026 |
| [2] | The Nation, 2026 |
| [3] | Thairath, 2026 *(เก็บไว้; §4.1 ไม่ใช้กับน้ำขังแล้ว)* |
| [4] | Nguyen et al., 2023 |
| [5] | Rajasekar & Selvi, 2022 |
| [6] | Zaman et al., 2021 |
| [7] | Mumu et al., 2024 |
| [8] | Tyagi et al., 2025 |
| [9] | Borhan & Khanaum, 2022 |
| [10] | Domènech-Gil et al., 2023/2024 |
| [11] | Baruah & Mazumder, 2025 |
| [12] | Ahmad et al., 2026 |

### เพิ่มใหม่สำหรับ §4.2 (`[13]`–`[28]`)

| # | งาน | path / หมายเหตุ |
|---|-----|-----------------|
| [13] | Zhou et al., 2024, Monsoon Asia CH₄ review | `methane/2024_Zhou_...md` (stub) |
| [14] | งานรองรับ ~11% ของ 308 Tg | ยังไม่มี PDF — ใส่ชื่อเต็ม+DOI ก่อนส่ง |
| [15] | Rafy et al., 2025, AWD meta-analysis | Firecrawl; ยังไม่มีในคลัง |
| [16] | Anapalli et al., 2023 | `methane/2023_Anapalli_...pdf` |
| [17] | Rice root / rhizosphere, 2024 | `methane/2024_rice_root_...pdf` |
| [18] | Carbon availability + soil pH, 2025/2026 | `methane/2025_methane_emissions_carbon_...pdf` |
| [19] | Yang et al., 2022, Agronomy 12:2240 | `methane/2025_product_type_...pdf` |
| [20] | Hu et al., 2024, CH4MOD, iScience | `methane/2025_CH4MOD_...pdf` |
| [21] | Vo et al., 2026, Front. Agron. 7:1693620 | `methods-spectroscopy/2022_Vo_...pdf` |
| [22] | Xu et al., AI/ML remote sensing rice CH₄ | `methods-remote/...` |
| [23] | Zhang et al., 2025, J. Environ. Manage. | `methane/2025_Zhang_ML_in-situ_...pdf` |
| [24] | Ye et al., 2021 | `enose/2021_Ye_...pdf` |
| [25] | Yin et al., 2023 | `enose/2023_Yin_...pdf` |
| [26] | MOS chemiresistive CH₄ review, 2023 | `enose/2023_MOS_chemiresistive_...pdf` |
| [27] | Andrews et al., 2023 | `algorithm/2023_Andrews_...pdf` |
| [28] | Mitchell et al., 2024 | `algorithm/2024_Mitchell_...pdf` |

---

## D. Cheat sheet — แทนที่ในข้อความ §4.2 ทีละจุด

```
4.2.1:  [1]→[4]   [2]→[13]  [3]→[14]  [4]→[15]  [5]→[16]
        [6]→[17]  [7]→[18]  [8]→[19]  [9]→[20]
4.2.2:  [10]→[6]  [11]→[7]
4.2.3:  (ใส่ [8] หลัง TDLAS/CRDS/FTIR)  [14]→[21]  [15]→[22]
        [16]→[5]  [17]→[23]
4.2.4:  [18]→[24] [19]→[10] [20]→[12] [21]→[25] [22]→[26]
        [23]→[11] [24]→[27] [25]→[28]
สรุป 4.2.4: [19],[20],[24] → [10],[12],[27]
```

---

## E. สิ่งที่ต้องทำก่อนส่ง Proposal

1. **ลบรายการอ้างอิงชุดที่สอง** (ที่เริ่ม `1. Sowcharoensuk` ซ้ำ) — ใช้ชุด IEEE เดียว  
2. **เติม `[13]`–`[28]`** ใน References ตามตาราง C  
3. **แก้ §4.1** ตามตาราง A (โดยเฉพาะ `[3]→[4]`, `[5,6]→[6,7]`, เติม `[11,12]` แทน `[][][]`)  
4. **แทนเลขทั้ง §4.2** ตาม cheat sheet D  
5. งานที่ยังไม่มี PDF (`[14]`, `[15]`, `[22]`) — ใส่ DOI/ชื่อเต็มให้ครบ หรือดาวน์โหลดเข้า `docs/paper` ก่อน

---

## Rerun inputs

```text
workflow: firecrawl-research-papers
topic: Proposal draft 6 cite remapping §4.1–4.2 against docs/paper
target_count: unified [1]–[28]
output: docs/proposal-4.1-4.2-cites-draft6.md
```
