# รายการคัดเลือกบทที่ 4.2 (จากบทที่ 4.1 ของ Proposal draft 12)

เกณฑ์: งานต้องรองรับบันไดวัดใน 4.1 (นาข้าวน้ำขัง → chamber–GC เป็นค่าอ้างอิง → ตัดทาง spectroscopy/ดาวเทียม → eNose/MOS+ML → ช่องว่างสามเสา)  
คลังแม่ที่ [`docs/paper/screened/`](../paper/screened/) **ไม่ถูกลบ** รายการ “ลบ” หมายถึงไม่คัดลอกเข้าโฟลเดอร์นี้

ตรวจชื่อ–DOI จาก Crossref / RIS ที่มีอยู่ ก่อนใส่คลัง  
เครื่องมือ `firecrawl_research_*` ไม่พร้อม (ต้อง OAuth) จึงใช้ Crossref + หน้าสำนักพิมพ์ OA + คลัง screened

รวม **40 เรื่อง** ในคลังนี้: RIS ครบ 40, PDF ได้ 32, ติดเพย์วอลล์หรือถูกบล็อกการดาวน์โหลด 8  
รอบ 2 เติม 13 เรื่อง OA จากผลค้นห้ามุม (ไม่ใส่งานเพย์วอลล์ที่ subagent แนะนำ เช่น Taguem 2021, Silberstein 2024, van den Bossche 2017)  
รอบ 3 (2026-08-20): เพิ่ม Othman et al. 2026 หลัง novelty check — คู่แข่งตรงแกน eNose+ML+นา (ดู [`othman-2026-positioning.md`](othman-2026-positioning.md))

---

## เพิ่มเข้ามา (ไม่ได้อยู่ในรายการอ้างอิงท้าย draft 12 หรืออยู่ใน screened แต่ 4.2 เดิมไม่ได้ใช้)

| Stem | งาน | DOI | เหตุผลที่เพิ่ม | PDF |
|------|-----|-----|----------------|-----|
| `2025_Saunois_Global_Methane_Budget_2000-2020` | Saunois et al., *Earth Syst. Sci. Data*, 2025 — Global Methane Budget 2000–2020 | 10.5194/essd-17-1873-2025 | แทนตัวเลขสัดส่วน CH₄ จากนาใน 4.1 ที่ยังไม่มีแหล่งงบประมาณโลก | มี |
| `2022_IPCC_AR6_WGIII_Chapter07_AFOLU` | IPCC AR6 WGIII บทที่ 7 AFOLU (ตำรา/รายงาน) | 10.1017/9781009157926.009 | แหล่ง AFOLU ที่ระบุว่า rice cultivation เป็นแหล่ง CH₄ เกษตรหลักร่วมกับ enteric fermentation; เอเชียเป็นภูมิภาคหลัก | มี |
| `2020_Conrad_methane_production_soil_environments` | Conrad, *Microorganisms*, 2020 | 10.3390/microorganisms8060881 | กลไก methanogenesis ในดินนาข้าวน้ำขัง (OA) แทนบทหนังสือ Conrad 2007 ที่ติดลิขสิทธิ์ | มี |
| `2021_Tokida_modified_closed_chamber_rice_methane` | Tokida, *J. Agric. Meteorol.*, 2021 | 10.2480/agrmet.d-20-00029 | closed chamber ในนาข้าว — วิธีอ้างอิงระดับแปลง | มี (คัดลอกจาก screened) |
| `2022_LowCost_GC-FID_methane_rice_cultivation` | Li et al., *Molecules*, 2022 | 10.3390/molecules27133968 | GC-FID สำหรับ CH₄ ในนาข้าว | มี (คัดลอกจาก screened) |
| `2020_Bastviken_lowcost_CH4_sensors_flux_chambers` | Bastviken et al., *Biogeosciences*, 2020 | 10.5194/bg-17-3659-2020 | เซ็นเซอร์ CH₄ ต้นทุนต่ำใน flux chamber และผลของความชื้น | มี (คัดลอกจาก screened) |
| `2024_Kiplimo_ML_calibration_lowcost_methane_TGS` | Kiplimo et al., *Atmosphere*, 2024 | 10.3390/atmos15111313 | ML สอบเทียบ TGS สำหรับ CH₄ | มี (คัดลอกจาก screened) |
| `2024_Lakhmi_linear_nonlinear_gas_sensor_array_CH4` | Lakhmi et al., *Sensors*, 2024 | 10.3390/s24113499 | เปรียบ linear กับ non-linear บนอาเรย์ที่มี CH₄ — ใกล้โมเดลวิทยานิพนธ์ | มี |
| `2023_Shah_TGS2611-E00_methane_environmental_response` | Shah et al., *Atmos. Meas. Tech.*, 2023 | 10.5194/amt-16-3391-2023 | การตอบสนองของ TGS2611 ต่อ CH₄ และสภาพแวดล้อม | มี (คัดลอกจาก screened) |
| `2022_Furuta_inexpensive_MOx_trace_methane` | Furuta et al., *Atmos. Meas. Tech.*, 2022 | 10.5194/amt-15-5117-2022 | MOS ต้นทุนต่ำวัด CH₄ ระดับต่ำ | มี (คัดลอกจาก screened) |
| `2025_Chen_Jacob_GRPI_rice_paddy_methane_inventory` | Chen et al., *Earth's Future*, 2025 | 10.1029/2024EF005479 | ตัดทาง remote sensing: สินค้าคงคลังจากดาวเทียม Landsat ไม่ใช่การวัด ppm รายแปลง | มี (สำเนาสถาบัน Aberystwyth) |

### รอบ 2 — เติมช่องว่าง (OA ที่ตรวจ DOI/หน้าสำนักพิมพ์แล้ว)

| Stem | งาน | DOI / แหล่ง | เหตุผลที่เพิ่ม | PDF |
|------|-----|-------------|----------------|-----|
| `1990_Nouchi_rice_aerenchyma_CH4_transport` | Nouchi, Mariko & Aoki, *Plant Physiology*, 1990 | 10.1104/pp.94.1.59 | กลไกการขนส่ง CH₄ ผ่านต้นข้าว (ชื่อเรื่องจาก Crossref) | **ไม่มีไฟล์** — Crossref ระบุลิขสิทธิ์ ASPB หลังระยะรอ; PMC/OUP ดึงอัตโนมัติไม่ได้ |
| `2015_Oo_within_field_CH4_Myanmar` | Oo, Win & Bellingrath-Kimura, *SpringerPlus*, 2015 | 10.1186/s40064-015-0901-2 | ความแปรในแปลงนาข้าวที่เมียนมา — รองรับว่าต้องวัดระดับแปลง | มี (Europe PMC PMC4379311; ไฟล์ PMC คนละเรคคอร์ดถูกทิ้งแล้ว) |
| `2015_Minamikawa_MIRSA_closed_chamber_rice_guidelines` | Minamikawa et al., NIAES, 2015 | ไม่มี DOI; ISBN 978-4-931508-16-3 | คู่มือ closed chamber มือสำหรับนาข้าว (MIRSA / GRA) | มี (Global Research Alliance) |
| `2019_IPCC_refinement_vol4_ch5_cropland_rice` | IPCC 2019 Refinement เล่ม 4 บทที่ 5 Cropland | ไม่มี DOI บท | สมการ CH₄ จากนาข้าวในแนวทางสินค้าคงคลัง | มี (NGGIP) |
| `2018_Wassmann_nighttime_closed_chamber_rice` | Wassmann et al., *PLOS ONE*, 2018 | 10.1371/journal.pone.0191352 | chamber กลางคืนในนาข้าว และความสัมพันธ์กลางคืน–ทั้งวัน | มี |
| `2024_Mazengo_closed_chamber_crop_GHG` | Mazengo et al., *Front. Agron.*, 2024 | 10.3389/fagro.2024.1464495 | ขั้นตอน static chamber + GC ในระบบพืช | มี |
| `2026_Vo_rice_GHG_measurement_approaches_I` | Vo et al., *Front. Agron.*, 2026 | 10.3389/fagro.2026.1693619 | คู่เล่มกับ Vo [21]: MSC / FAC / EC ในนาข้าว | มี |
| `2020_Zhang_fingerprint_rice_XCH4_monsoon_Asia` | Zhang et al., *Nat. Commun.*, 2020 | 10.1038/s41467-019-14155-5 | ลายนิ้วมือนาข้าวใน XCH₄ ดาวเทียมที่มรสุมเอเชีย — ตัดทางสเกลดาวเทียม | มี (PMC6987195) |
| `2024_Liang_TROPOMI_China_rice_methane` | Liang et al., *Environ. Sci. Technol.*, 2024 | 10.1021/acs.est.4c09822 | TROPOMI ที่ Heilongjiang — สเกลจังหวัด ไม่ใช่ ppm รายแปลง | มี (PMC11698026) |
| `2012_Eugster_TGS2600_ambient_methane_humidity` | Eugster & Kling, *Atmos. Meas. Tech.*, 2012 | 10.5194/amt-5-1925-2012 | TGS2600 กับ T/H ที่ความเข้มข้นบรรยากาศ | มี |
| `2020_Jorgensen_TGS2611E00_humidity_field` | Jørgensen et al., *Atmos. Meas. Tech.*, 2020 | 10.5194/amt-13-3319-2020 | TGS2611 (MOS) ภาคสนาม เทียบ CRDS | มี |
| `2018_CollierOxandale_TGS2600_field_quantification` | Collier-Oxandale et al., *Atmos. Meas. Tech.*, 2018 | 10.5194/amt-11-3569-2018 | แปลงสัญญาณ TGS2600 เป็น ppm ในสนาม | มี |
| `2021_RiveraMartinez_TGS_H2O_CO_crosssensitivity_ML` | Rivera Martinez et al., *Atmosphere*, 2021 | 10.3390/atmos12010107 | TGS + ML ที่พื้นหลัง; ห้องปฏิบัติการข้ามความไว H₂O/CO | มี (MDPI CDN) |

งานที่ subagent แนะนำแต่ **ไม่ใส่รอบนี้** (เพย์วอลล์ หรือไกลโจทย์): Taguem et al. 2021 (Elsevier VOR); Silberstein et al. 2024 (อาร์เรย์เคลื่อนที่น้ำมัน/ก๊าซ — ใกล้แต่ซ้ำแกนกับ Collier/Rivera ที่ได้ OA แล้ว); van den Bossche 2017; Sander 2014; Rajendran TDLAS; Song UAV

### รอบ 3 — เติมคู่แข่งช่องว่าง (OA จาก novelty search)

| Stem | งาน | DOI / แหล่ง | เหตุผลที่เพิ่ม | PDF |
|------|-----|-------------|----------------|-----|
| `2026_Othman_SVM_eNose_methane_paddy_ecosystems` | Othman et al., *J. Adv. Res. Appl. Sci. Eng. Technol.*, 2026 — E-Nose + SVM ในปaddy | 10.37934/araset.60.5.3350 | คู่แข่งตรง: นา + MOS E-Nose + ML; บังคับปรับช่องว่างสามเสา — ดู extract + positioning | มี |

---

## คงไว้จาก draft 12 (รองรับบันได 4.1)

| Draft 12 | Stem | งาน | PDF |
|---------|------|-----|-----|
| [4] | `2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation` | Nguyen et al. 2023 บทหนังสือ carbon footprint ข้าว | มี (คัดลอกจาก screened) |
| [5] | `2022_Rajasekar_GHG_sensing_rice_fields_near_field` | Rajasekar & Selvi, *Sensors*, 2022 | มี |
| [6] | `2021_Zaman_GHG_measurement_agricultural_soils_methodology` | Zaman et al. 2021 บท Springer (ตำราวิธี chamber–GC) | **ไม่มีไฟล์** — หนังสือเป็น Open Access แต่เซิร์ฟเวอร์ Springer ส่งหน้า HTML เมื่อดึงอัตโนมัติ |
| [7] | `2024_Mumu_methodological_progress_agricultural_GHG` | Mumu et al., *Carbon Management*, 2024 | **เพย์วอลล์** |
| [8] | `2025_Tyagi_methane_sensing_environmental_review` | Tyagi et al., *Environ. Technol. Rev.*, 2025 | **เพย์วอลล์** |
| [10] | `2024_Domenech-Gil_eNose_environmental_methane_monitoring` | Domènech-Gil et al., *Environ. Sci. Technol.*, 2024 (ปีปฏิทิน 2024; RIS มี 2023) | มี (Europe PMC PMC10785752) |
| [11] | `2025_Baruah_ML_eNose_healthcare_agriculture_review` | Baruah & Mazumder, IEEE TIM, 2025 | **เพย์วอลล์** |
| [12] | `2026_Ahmad_MOS_sensors_precision_agriculture` | Ahmad et al., *Adv. Sensor Res.*, 2026 | **เพย์วอลล์** |
| [13] | `2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review` | Zhou et al., *Sci. Total Environ.*, 2024 | **เพย์วอลล์** |
| [21] | `2025_Vo_TGA_vs_GC_methane_rice` | Vo et al., *Front. Agron.*, 2026 (DOI 10.3389/fagro.2025.1693620) | มี |
| [23] | `2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze` | Zhang et al., *J. Environ. Manage.*, 2025 | **เพย์วอลล์** |
| [24] | `2021_Ye_smart_eNose_machine_learning_review` | Ye et al., *Sensors*, 2021 | มี |
| [26] | `2023_Fu_MOS_chemiresistive_methane_sensor_review` | Fu et al., *Molecules*, 2023 | มี |
| [27] | `2023_Andrews_ML_calibrating_gas_sensors_methane_emissions` | Andrews et al., *Sensors*, 2023 | มี |
| [28] | `2024_Mitchell_Figaro_lowcost_methane_ML_calibration` | Mitchell et al., *Sensors*, 2024 | มี |

---

## เอออกจากชุด 4.2 (ยังอยู่ใน screened ถ้ามี)

ไม่คัดลอกเข้า `docs/literature-review-4.2/`

| Draft 12 | งาน | เหตุผล |
|---------|-----|--------|
| [1] [2] [3] | Krungsri / The Nation / Thairath | ข่าวเศรษฐกิจข้าว — ใช้ใน 4.1 ไม่ใช่ literature review |
| [9] | Borhan & Khanaum 2022 GHG ปศุสัตว์ | คนละระบบผลิต |
| [14] | Xuan et al. 2025 mitigating methane rice | รีวิว mitigation ไม่ใช่เครื่องมือวัด |
| [15] | Rafy et al. 2025 AWD meta-analysis | agronomy / มาตรการน้ำ |
| [16] | Anapalli et al. 2023 eddy covariance AWD | คนละวิธีวัด |
| [17] | Guan et al. 2024 rice root rhizosphere | กลไกราก — ใช้ Conrad แทนในแกน 4.2.1 |
| [18] | Yusong et al. 2026 carbon availability / pH | ตัวแปรดิน ไม่ใช่เครื่องมือ |
| [19] | Yang et al. 2022 EENF meta-analysis | ปุ๋ย ไม่ใช่การวัด |
| [20] | Hu et al. 2024 CH4MOD | แบบจำลองระดับโลก คนละสเกล |
| [22] | Xu et al. 2025 SSRN AI/ML methane modelling | รีวิวการสร้างแบบจำลองมีเทนกว้าง ไม่จำเพาะสเกลดาวเทียมของนา; ใช้ Chen GRPI แทน |
| [25] | Yin et al. 2023 eNose CH₄/CO identification | จำแนกชนิดก๊าซ ไม่ใช่ regression ppm ในนา |
| [29] [30] [31] | Creswell; Madsen; Deisenroth et al. | ตำราวิธีวิจัย/สถิติ/ML — อยู่บทวิธี ไม่ใช่ 4.2 |

งานใน screened ที่ thematic-index จัดว่าไกลโจทย์ (GNN, TFA-CNN, classification, livestock) ไม่ถูกดึงเข้าโฟลเดอร์นี้เช่นกัน

---

## เพย์วอลล์ / ดาวน์โหลดไม่สำเร็จ (มี RIS แล้ว)

| Stem | สถานะ |
|------|--------|
| Zaman 2021 บท Springer | หนังสือระบุ Open Access; การดึงอัตโนมัติได้เฉพาะ HTML — โหลดมือจาก [Springer chapter](https://link.springer.com/chapter/10.1007/978-3-030-55396-8_2) |
| Mumu 2024 | Taylor & Francis ตอบ 403 |
| Tyagi 2025 | ไม่พบ OA |
| Baruah 2025 | IEEE TIM ไม่พบ OA |
| Ahmad 2026 | Wiley ไม่พบ OA |
| Zhou 2024 | Elsevier ไม่พบ OA |
| Zhang 2025 | Elsevier ไม่พบ OA |
| Nouchi 1990 | Crossref มี DOI และลิขสิทธิ์ ASPB; PMC/OUP ดึงอัตโนมัติได้แต่ HTML หรือไฟล์เล็กที่ไม่ใช่ PDF |

ไม่ใช้ Sci-Hub

---

## จับคู่กับโครง 4.2 ใหม่

- **4.2.1** นาข้าวน้ำขัง: Conrad; Saunois; IPCC AR6 Ch7; Nguyen; Zhou; Nouchi (metadata); Oo
- **4.2.2** chamber–GC: Zaman; Mumu; Tokida; Li GC-FID; Bastviken; Minamikawa MIRSA; IPCC 2019 Ch5; Wassmann; Mazengo; Vo เล่ม I
- **4.2.3** ตัดทาง: Tyagi; Vo เล่ม II; Chen GRPI; Zhang 2020 XCH₄; Liang TROPOMI
- **4.2.4** eNose/MOS+ML: Rajasekar; Domènech-Gil; Othman; Ye; Fu; Ahmad; Baruah; Andrews; Mitchell; Kiplimo; Lakhmi; Shah; Furuta; Eugster; Jørgensen; Collier-Oxandale; Rivera Martinez
- **4.2.5** ช่องว่าง (ปรับแล้ว): Rajasekar (MOS+นา); Domènech-Gil (eNose+ML ไม่ใช่นา); Zhang 2025 (ML+นา ไม่ใช่ MOS); **Othman 2026 (E-Nose+ML+นา แต่เป้าฟลักซ์/emission จาก chamber ของเซ็นเซอร์ ไม่ใช่สอบเทียบ ppm กับ GC)** — ร่างประโยคใน [`othman-2026-positioning.md`](othman-2026-positioning.md)
