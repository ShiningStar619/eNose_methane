# Find-paper report — 23 กรกฎาคม 2026 (PHASE B)

**โครงการ:** eNose Methane (TGS2612 × 4 + BME280, ΔV, Linear Regression, static chamber–GC)  
**ขอบเขตค้นหา:** ปี 2020–2026 (เน้น 2022+), สูงสุด 12 เรื่องใหม่ที่ไม่ซ้ำคลัง `docs/paper/screened/`  
**หมวดเน้น:** (1) eNose/MOS + rice/field CH₄ (2) ML calibration MOS methane  

## สถานะเครื่องมือ

| เครื่องมือ | ผล |
|-----------|-----|
| `firecrawl_research_search_papers` / `related` / `inspect` / `read` | **ล้มเหลว** (OAuth `Unauthorized` / `Invalid redirect_uri`) แม้หลัง `mcp_auth` |
| `firecrawl_search` | ไม่เสถียร / ผลว่างบางครั้ง |
| Fallback ที่ใช้จริง | WebSearch + Crossref API (ยืนยัน DOI/metadata) + ดาวน์โหลด OA PDF |
| ตรวจซ้ำคลัง | เทียบ DOI กับ `docs/paper/screened/**/cite/*.bib` (42 DOI) |

**หมายเหตุ:** ไม่มีการแก้/ลบไฟล์ใน `docs/paper/screened/` — PDF ใหม่เก็บที่ `docs/paper/candidates_2026-07-23/` เท่านั้น และยังไม่แก้ `.bib` (รอ citation-manager)

---

## สรุปจำนวน

| กลุ่ม | จำนวน | PDF ได้ |
|------|------:|--------:|
| ตรงประเด็นสูง | 6 | 6/6 |
| เกี่ยวข้องรอง | 6 | 6/6 |
| **รวมเสนอใหม่** | **12** | **12/12** |
| ซ้ำกับคลังเดิม (พบระหว่างค้น) | 3 | — |
| ไม่แนะนำ | 3 | — |

โฟลเดอร์ candidates:

```
docs/paper/candidates_2026-07-23/
  mos-enose-field/     (4 PDF)
  ml-calibration/      (2 PDF)
  chamber-gc-rice/     (3 PDF)
  supporting-secondary/(3 PDF)
```

---

## A. ตรงประเด็นสูง (6)

### A1 — Addressing Low-Cost Methane Sensor Calibration Shortcomings with Machine Learning

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Elijah Kiplimo, Stuart N. Riddick, Mercy Mbua, Aashish Upreti, Abhinav Anand, et al. |
| Year | 2024 |
| Venue | Atmosphere |
| DOI | `10.3390/atmos15111313` |
| Link | https://doi.org/10.3390/atmos15111313 |
| หมวด | ML calibration MOS methane |
| สถานะยืนยัน | Crossref + OA PDF + abstract (WebSearch) — **ยืนยัน DOI/metadata แล้ว**; claim: RF ดีกว่า linear บน TGS2600/TGS2611 ที่ METEC |
| PDF | ได้ — `candidates_2026-07-23/ml-calibration/2024_Kiplimo_ML_calibration_lowcost_methane_TGS.pdf` |
| เกี่ยวอย่างไร | ตรงแกน ML calibration ของ Figaro TGS ที่โปรเจกต์ใช้ตระกูลเดียวกัน; แสดงว่า RH/T ทำให้ linear fail แต่ RF map Rs+T+RH → ppm ได้ |
| Proposed cite key | `Kiplimo2024_Atmos_ML_TGS_methane_cal` |
| ตำแหน่งเสนอ (citation-manager) | `docs/paper/screened/direct/cite/` (+ PDF ย้ายจาก candidates หลังคัด) |

### A2 — Design and evaluation of a low-cost sensor node for near-background methane measurement

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Daniel Furuta, Bruce Wilson, Albert A. Presto, Jiayu Li |
| Year | 2024 |
| Venue | Atmospheric Measurement Techniques |
| DOI | `10.5194/amt-17-2103-2024` |
| Link | https://doi.org/10.5194/amt-17-2103-2024 |
| หมวด | MOS/eNose field CH₄ |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `mos-enose-field/2024_Furuta_lowcost_sensor_node_near_background_methane.pdf` |
| เกี่ยวอย่างไร | โหนด TGS2611-E00 + TGS2600 + T/RH สำหรับ near-background 2–10 ppm; อภิปราย baseline/cross-sensitivity — ใช้เปรียบเทียบกับ protocol baseline–measure ของโปรเจกต์ |
| Proposed cite key | `Furuta2024_AMT_lowcost_CH4_node` |
| ตำแหน่งเสนอ | `docs/paper/screened/direct/cite/` |

### A3 — Characterising the methane gas and environmental response of the Figaro Taguchi Gas Sensor (TGS) 2611-E00

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Adil Shah, Olivier Laurent, Luc Lienhardt, Grégoire Broquet, et al. |
| Year | 2023 |
| Venue | Atmospheric Measurement Techniques |
| DOI | `10.5194/amt-16-3391-2023` |
| Link | https://doi.org/10.5194/amt-16-3391-2023 |
| หมวด | MOS/eNose field CH₄ |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `mos-enose-field/2023_Shah_TGS2611-E00_methane_environmental_response.pdf` |
| เกี่ยวอย่างไร | ลักษณะการตอบสนอง TGS2611-E00 ต่อ CH₄, H₂O, T แบบละเอียด — ฐานสำคัญสำหรับชดเชยสภาพแวดล้อมก่อน/คู่กับ ML |
| Proposed cite key | `Shah2023_AMT_TGS2611E00_response` |
| ตำแหน่งเสนอ | `docs/paper/screened/direct/cite/` |

### A4 — Characterization of inexpensive metal oxide sensor performance for trace methane detection

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Daniel Furuta, Tofigh Sayahi, Jinsheng Li, Bruce Wilson, Albert A. Presto, Jiayu Li |
| Year | 2022 |
| Venue | Atmospheric Measurement Techniques |
| DOI | `10.5194/amt-15-5117-2022` |
| Link | https://doi.org/10.5194/amt-15-5117-2022 |
| หมวด | MOS/eNose field CH₄ |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `mos-enose-field/2022_Furuta_inexpensive_MOx_trace_methane.pdf` |
| เกี่ยวอย่างไร | เปรียบ TGS2600/2602/2611-C00/2611-E00/MQ4 ในช่วง 2–10 ppm; ชี้ TGS2611 และ MQ4 ว่ามีศักยภาพแต่ RH/T เป็นปัญหา — รองรับการเลือก sensor |
| Proposed cite key | `Furuta2022_AMT_MOx_trace_CH4` |
| ตำแหน่งเสนอ | `docs/paper/screened/direct/cite/` |

### A5 — Technical note: Facilitating the use of low-cost methane (CH₄) sensors in flux chambers

| ฟิลด์ | ค่า |
|------|-----|
| Authors | David Bastviken, Jonatan Nygren, Jonathan Schenk, Roser Parellada Massana, Nguyen Thanh Duc |
| Year | 2020 |
| Venue | Biogeosciences |
| DOI | `10.5194/bg-17-3659-2020` |
| Link | https://doi.org/10.5194/bg-17-3659-2020 |
| หมวด | MOS + chamber (field/flux) |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `chamber-gc-rice/2020_Bastviken_lowcost_CH4_sensors_flux_chambers.pdf` |
| เกี่ยวอย่างไร | NGM2611/TGS2611 ใน flux chamber + calibration + open-source logger; เชื่อม chamber กับ low-cost MOS โดยตรง (แม้บริบท aquatic ไม่ใช่นาข้าว) |
| Proposed cite key | `Bastviken2020_BG_CH4_sensors_flux_chambers` |
| ตำแหน่งเสนอ | `docs/paper/screened/direct/cite/` |

### A6 — Determining methane mole fraction at a landfill site using the Figaro Taguchi gas sensor 2611-C00 and wind direction measurements

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Adil Shah, Olivier Laurent, Grégoire Broquet, Carole Philippon, Pramod Kumar, Elisa Allegrini, Philippe Ciais |
| Year | 2024 |
| Venue | Environmental Science: Atmospheres |
| DOI | `10.1039/d3ea00138e` |
| Link | https://doi.org/10.1039/d3ea00138e |
| หมวด | MOS/eNose field CH₄ |
| สถานะยืนยัน | Crossref + OA PDF (Semantic Scholar mirror) |
| PDF | ได้ — `mos-enose-field/2024_Shah_TGS2611-C00_landfill_methane.pdf` |
| เกี่ยวอย่างไร | field reconstruction ของ ppm จาก TGS2611-C00 ด้วย baseline resistance (T/H₂O) + wind; RMSE < 1 ppm — แนวทาง field calibration ที่ถ่ายโอนได้ |
| Proposed cite key | `Shah2024_ESA_TGS2611C00_landfill` |
| ตำแหน่งเสนอ | `docs/paper/screened/direct/cite/` |

---

## B. เกี่ยวข้องรอง (6)

### B1 — Using metal oxide gas sensors to estimate the emission rates and locations of methane leaks in an industrial site

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Rodrigo Rivera-Martinez, Pramod Kumar, Olivier Laurent, Gregoire Broquet, et al. |
| Year | 2024 |
| Venue | Atmospheric Measurement Techniques |
| DOI | `10.5194/amt-17-4257-2024` |
| Link | https://doi.org/10.5194/amt-17-4257-2024 |
| หมวด | ML calibration MOS methane (industrial) |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `ml-calibration/2024_RiveraMartinez_MOS_methane_leak_emission_MLP.pdf` |
| เกี่ยวอย่างไร | TGS2611-C00/E00 + MLP/polynomial reconstruct mole fraction แล้ว inverse emission — หลัก ML ใช้ได้ แต่บริบท leak อุตสาหกรรม ไม่ใช่นาข้าว |
| Proposed cite key | `RiveraMartinez2024_AMT_MOS_CH4_leak_MLP` |
| ตำแหน่งเสนอ | `docs/paper/screened/supporting/cite/` |

### B2 — Efficient Methane Monitoring with Low-Cost Chemical Sensors and Machine Learning

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Guillem Domènech-Gil, Nguyen Thanh Duc, J. Jacob Wikner, Jens Eriksson, Donatella Puglisi, et al. |
| Year | 2024 |
| Venue | Proceedings (Eurosensors 2023) |
| DOI | `10.3390/proceedings2024097079` |
| Link | https://doi.org/10.3390/proceedings2024097079 |
| หมวด | eNose + ML CH₄ |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `supporting-secondary/2024_DomenechGil_efficient_methane_monitoring_Eurosensors.pdf` |
| เกี่ยวอย่างไร | conference สั้นของกลุ่มเดียวกับ Domènech-Gil EST (มีในคลังแล้ว); PLSR + eNose ambient CH₄ — ใช้เป็น companion ไม่แทน journal หลัก |
| Proposed cite key | `DomenechGil2024_Proc_efficient_CH4_eNose` |
| ตำแหน่งเสนอ | `docs/paper/screened/supporting/cite/` |

### B3 — Low-Cost Detection of Methane Gas in Rice Cultivation by GC-FID Based on Manual Injection and Split Pattern

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Chaofeng Li, Qingge Ji, Xianshu Fu, Xiaoping Yu, Zihong Ye, Mingzhou Zhang, Chuanxin Sun, Yulou Qiu |
| Year | 2022 |
| Venue | Molecules |
| DOI | `10.3390/molecules27133968` |
| Link | https://doi.org/10.3390/molecules27133968 |
| หมวด | chamber–GC / rice reference method |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `chamber-gc-rice/2022_LowCost_GC-FID_methane_rice_cultivation.pdf` |
| เกี่ยวอย่างไร | ลดต้นทุน GC-FID สำหรับ CH₄ จากข้าว (manual injection) — สนับสนุน ground truth lab ไม่ใช่ eNose |
| Proposed cite key | `Li2022_Molecules_GC_FID_rice_CH4` |
| ตำแหน่งเสนอ | `docs/paper/screened/supporting/cite/` |

### B4 — Increasing measurement throughput of methane emission from rice paddies with a modified closed-chamber method

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Takeshi Tokida |
| Year | 2021 |
| Venue | Journal of Agricultural Meteorology |
| DOI | `10.2480/agrmet.d-20-00029` |
| Link | https://doi.org/10.2480/agrmet.d-20-00029 |
| หมวด | chamber method rice |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `chamber-gc-rice/2021_Tokida_modified_closed_chamber_rice_methane.pdf` |
| เกี่ยวอย่างไร | เพิ่ม throughput ของ closed chamber ในนาข้าวด้วย portable laser analyzer แทน GC — เปรียบเทียบข้อจำกัด/บทบาทของ GC กับ sensor ความถี่สูง |
| Proposed cite key | `Tokida2021_JAM_chamber_throughput_rice` |
| ตำแหน่งเสนอ | `docs/paper/screened/supporting/cite/` |

### B5 — Neural networks based-simple estimated model for greenhouse gas emission from irrigated paddy fields

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Chusnul Arif, Yohanes Aris Purwanto, Rudiyanto Rudiyanto, Masaru Mizoguchi |
| Year | 2025 |
| Venue | IAES International Journal of Artificial Intelligence (IJ-AI) |
| DOI | `10.11591/ijai.v14.i1.pp231-239` |
| Link | https://doi.org/10.11591/ijai.v14.i1.pp231-239 |
| หมวด | ML + rice GHG (ไม่ใช่ MOS) |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `supporting-secondary/2025_Arif_NN_GHG_irrigated_paddy.pdf` |
| เกี่ยวอย่างไร | NN ประมาณ CH₄/N₂O จาก soil moisture/T/EC โดย validate ด้วย closed chamber–GC ในนาข้าว — ใกล้ use case แต่ input ไม่ใช่ eNose |
| Proposed cite key | `Arif2025_IJAI_NN_paddy_GHG` |
| ตำแหน่งเสนอ | `docs/paper/screened/supporting/cite/` |

### B6 — Development of an IoT-based Monitoring System for Greenhouse Gas Emissions and Soil Health in Paddy Fields

| ฟิลด์ | ค่า |
|------|-----|
| Authors | Galang Indra Jaya, Alan Handru, Yovi Avianto, Amir Noviyanto, Valensi Kautsar, et al. |
| Year | 2025 |
| Venue | KnE Life Sciences |
| DOI | `10.18502/kls.v9i1.19350` |
| Link | https://doi.org/10.18502/kls.v9i1.19350 |
| หมวด | field IoT paddy CH₄ |
| สถานะยืนยัน | Crossref + OA PDF |
| PDF | ได้ — `supporting-secondary/2025_Jaya_IoT_GHG_soil_paddy.pdf` |
| เกี่ยวอย่างไร | IoT monitor CH₄ + soil health ในนาข้าว (เซ็นเซอร์ RS-CH4 ฯลฯ) — ใกล้ deployment แต่ไม่ใช่ MOS array/eNose+ML |
| Proposed cite key | `Jaya2025_KnE_IoT_GHG_paddy` |
| ตำแหน่งเสนอ | `docs/paper/screened/supporting/cite/` |

---

## C. ซ้ำกับคลังเดิม (พบระหว่างค้น — ไม่เสนอใหม่)

| DOI | ชื่อสั้น | สถานะในคลัง |
|-----|----------|-------------|
| `10.1021/acs.est.3c06945` | Domènech-Gil eNose environmental CH₄ | screened direct (D16) |
| `10.3390/s24041066` | Mitchell Figaro ML calibration | screened direct (D20) |
| `10.3390/s22114141` | Rajasekar GHG sensing rice fields | screened direct (D23) |

---

## D. ไม่แนะนำ (พร้อมเหตุผล)

| รายการ | เหตุผล |
|--------|--------|
| Qian et al. 2023 *Nature Reviews Earth & Environment* (`10.1038/s43017-023-00482-1`) | รีวิว mitigation GHG ข้าวกว้าง ไม่เจาะ sensor/eNose/ML calibration; คลังมีบริบท paddy หนาอยู่แล้ว; PDF Nature มัก paywall |
| Intelligent gas sensors food safety review (PMC12346065) | food VOC/eNose — off-topic ชัดต่อ CH₄ นาข้าว |
| MIRSA closed-chamber rice guidelines (2015) | นอกช่วงปีที่เน้น และเป็น guideline ไม่ใช่ peer-reviewed paper ใหม่ |

---

## E. คำค้น / framing ที่ลองแล้ว

| ID | Query / framing | ผล |
|----|-----------------|-----|
| Q1 | electronic nose OR MOS sensor array methane rice paddy quantification | ไม่พบงาน end-to-end eNose+ML+rice; ได้ IoT paddy / Rajasekar (ซ้ำ) / NN soil |
| Q2 | TGS2611 OR TGS2612 OR Figaro methane chamber rice | ได้ Bastviken chamber + TGS family; rice+TGS ยังบาง |
| Q3 | ML calibration metal oxide / Figaro TGS methane | ได้ Kiplimo, Furuta, Rivera-Martinez; Mitchell ซ้ำ |
| Q4 | static chamber GC methane rice protocol | ได้ Tokida, Li GC-FID rice; Zaman/Mumu มีในคลังแล้ว |
| Q5 | IoT methane monitoring paddy semiconductor | ได้ Jaya 2025; Zhang IoT มีในคลังแล้ว |
| Q6 | ΔV OR transient response MOS methane quantification | **บางมาก / ไม่ได้ผล** — ไม่พบ paper ที่ตรง feature ΔV ชัดเจน |
| Extra | Shah TGS2611 landfill / Furuta AMT series | ได้ A3–A6 สำเร็จ |
| Firecrawl research_* | (ทุก framing) | **OAuth fail — ไม่ได้ใช้ semantic paper index** |

---

## F. ข้อเสนอสำหรับ citation-manager (ขั้นถัดไป)

1. สร้าง BibTeX **และ** RIS สำหรับ A1–A6 + B1–B6 (12 รายการ) ตาม DOI ด้านบน  
2. วาง `.bib`/`.ris` ตามคอลัมน์ตำแหน่งเสนอ (direct vs supporting)  
3. คัดลอก PDF จาก `candidates_2026-07-23/` เข้า `screened/direct/` หรือ `screened/supporting/` หลังผู้ใช้ยืนยันคัดเข้า  
4. อัปเดต `project-relevance-screening.md` / `screened/README.md` เมื่อคัดเสร็จ  
5. **อย่าทับ** ไฟล์ที่มี DOI ซ้ำใน screened

### รูปแบบ cite ที่ผู้ใช้ขอ

- BibTeX + RIS (EndNote) — รอบนี้ยังไม่สร้างไฟล์ cite (ตามคำสั่ง PHASE B)

---

## G. ข้อค้นพบสำคัญต่อ literature gap

- ยัง**ไม่พบ** peer-reviewed 2020–2026 ที่รวม **eNose array + ML regression + CH₄ ในนาข้าว** ในงานเดียว → ช่องว่างที่ lit-review ของโปรเจกต์ระบุยังยืนยืน  
- กระแสที่เติมได้ดีที่สุดรอบนี้คือ **TGS2611/Figaro characterization + ML calibration + flux-chamber MOS** (A1–A6) ซึ่งถ่ายโอนสู่ระบบ TGS2612 ของโปรเจกต์ได้โดยตรง  
- งานนาข้าวที่หาได้ใหม่มักเป็น **IoT/soil covariates/chamber–GC** ไม่ใช่ MOS fingerprint

---

## H. พร้อมส่งต่อ

| รายการ | สถานะ |
|--------|--------|
| รายงานนี้ | `docs/paper/find-paper-report-2026-07-23.md` |
| PDF candidates | `docs/paper/candidates_2026-07-23/` (12 ไฟล์) |
| citation-manager | **พร้อมรับต่อ** (สร้าง BibTeX+RIS, คัดเข้า screened) |
| lit-reviewer / thesis-writer | ยังไม่เรียกในรอบนี้ |
