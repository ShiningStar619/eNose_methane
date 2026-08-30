# ช่องว่างของ 4.2 ไม่ได้อยู่ที่จำนวนเรื่อง แต่เป็นช่องว่างของหน่วยวัด: งานที่มีฉบับเต็มส่วนใหญ่ตอบฟลักซ์แปลงนา ขณะที่วิทยานิพนธ์วัด ppm ในห้องทดลอง

เอกสารทำงานสำหรับ systematic review ของบท 4.2 และคลังทฤษฎีบทที่ 5  
แหล่งต้นทาง: `docs/draft/Proposal draft 12.1.docx` (ดึงข้อความ 30 ส.ค. 2026) และคลัง `docs/paper/screened/`  
ภาษาของรายงานตามคำขอ: ไทย

## บทคัดย่อ

ร่างข้อเสนอ 12.1 จัดวรรณกรรม 4.2 เป็นห้าหัวตามสเกลการวัด ไม่ใช่สามหัวแบบร่าง 12 ก่อนหน้า คำถามของรอบนี้จึงไม่ใช่แค่ “มีงานพอหรือยัง” แต่เป็นว่า งานที่อ้างใน 4.1–4.2 มีฉบับเต็มให้เปิดตรวจได้หรือไม่ และแต่ละหัวมีหลักฐานสนับสนุนอย่างน้อยห้าชิ้นหรือยัง การคัดจากคลัง `screened` พบว่าหมายเลขอ้างอิงที่ถูกใช้จริงใน 4.1 และโครง 4.2 มีทั้งชุดที่มี PDF ในคลัง ชุดที่มีแต่ metadata และชุดที่ไฟล์ชื่อเรื่องไม่ตรงกับเนื้อใน งานที่ไม่มีฉบับเต็มถูกตัดออกจากชุดที่ใช้ยืนยันข้ออ้างในรายงานนี้ รอบ 30 ส.ค. 2026 ดึง PDF จาก EuropePMC และแหล่ง OA อื่นเข้าคลังแล้วสำหรับ Rajasekar, Zaman (บทที่ 2), Domènech-Gil *ES&T*, Ye, Yin, Fu, Andrews, Mitchell, Lakhmi, Minamikawa 2015 และ Conrad 2020 ข้ออ้างเชิงปริมาณจากงานเหล่านี้จึงใช้ได้ในระดับฉบับเต็มแล้ว งานที่ยังขาด PDF (Xuan, Rafy, Vo, Nguyen เล่มจริง, Zhou เต็ม) ยังอยู่นอกชุดยืนยัน บทที่ 5 ควรยึดตำราทฤษฎีที่ตรวจแล้วเป็นแกน แล้วใช้ paper เป็นตัวอย่าง ไม่กลับทาง ตำราใน `project-knowledge` ใช้ได้แน่นที่ 5.5 ส่วน 5.1–5.4 ต้องดึงจากงานนอกคลังตำราชุดนั้น Gardner & Bartlett กับ Pearce Handbook ยังไม่มี PDF ฟรี

## 1. บทนำ

ร่าง 12.1 ขยาย 4.2 จากสามย่อหน้าในร่าง 12 เป็นโครงห้าหัว:

1. การปล่อยก๊าซมีเทนจากนาข้าวน้ำขัง
2. การวัดก๊าซมีเทนในระดับแปลงนา
3. การประเมินการปล่อยก๊าซมีเทนระดับภูมิภาค
4. การตรวจวัดด้วยจมูกอิเล็กทรอนิกส์และเซ็นเซอร์โลหะออกไซด์
5. การสอบเทียบความเข้มข้นด้วยการเรียนรู้แบบมีผู้สอน

รายการอ้างอิงยาวถึง [56] แต่ตัวเนื้อ 4.2 ในไฟล์ 12.1 ยังเป็นโครงหัวข้อ ไม่ใช่ย่อหน้าปริทัศน์เต็มรูป รายงานนี้จึงตอบคำถามปฏิบัติสามข้อ

- **RQ1.** งานใน `docs/paper/screened` งานใดถูกใช้ใน 4.1 และโครง 4.2 และงานใดมีฉบับเต็มให้เปิดได้
- **RQ2.** แต่ละหัวของ 4.2 มีงานสนับสนุนครบห้าชิ้นหรือยัง งานเสริมที่แนะนำคืออะไร
- **RQ3.** บทที่ 5 ควรยึดทฤษฎีจากตำราหรือ paper ใด และตำราใน `project-knowledge` ใส่หัวใดได้

มุมของรายงาน: ช่องว่างหลักไม่ใช่การขาดวรรณกรรมนาข้าว แต่เป็นการไม่ตรงหน่วย งานฉบับเต็มในคลังส่วนใหญ่พูดฟลักซ์ (มวลต่อพื้นที่ต่อเวลา) ขณะที่ขอบเขตทดลองของข้อเสนอวัดความเข้มข้น ppm ในห้องปฏิบัติการ

## 2. วิธี

ขอบเขต: งานที่ปรากฏเป็นหมายเลขใน 4.1 หรือในโครง/รายการอ้างอิงของ 4.2 ในร่าง 12.1 รวมงานที่ถูกใช้เป็นรูป เกณฑ์คัดเข้าของชุด “ใช้ยืนยันข้ออ้างได้” คือมี PDF หรือ extract ที่เปิดเนื้อได้ในคลัง หรือมี DOI ที่ Crossref / Semantic Scholar / OpenAlex ยืนยัน และมีลิงก์ open access ที่ตรวจแล้ว เกณฑ์คัดออก: มีแค่ `.bib`/`.ris` ไม่มีฉบับเต็ม DOI ที่ Crossref คืนค่าว่าง ไฟล์ชื่อเรื่องไม่ตรงเนื้อ และงานปศุสัตว์ที่ไม่แตะนาข้าว

เครื่องมือค้น: Semantic Scholar, OpenAlex, Crossref, Unpaywall/EuropePMC (ผ่าน paper-search) และค้นเว็บสำหรับ guideline ที่ไม่ได้อยู่ในวารสาร Firecrawl CLI ติดตั้งแล้ว (`v1.23.3`) แต่เครื่องนี้ถูกบล็อกถ้าไม่มี API key จึงไม่ได้ใช้ Firecrawl เป็นแหล่งหลัก รอบ ingest PDF ใช้ `europepmc.org/api/getPdf` เป็นหลัก เพราะ MDPI และ PMC NCBI คืน 403/HTML จาก crawler ลิงก์ที่ลงคลังเป็น OA ที่ตรวจ `%PDF-` แล้ว ไม่ใช้ Sci-Hub

เกณฑ์หลักฐาน: PDF ในคลัง = เปิดแล้ว metadata + บทคัดย่อจากดัชนี = ใช้ได้ระดับข้อค้นพบในบทคัดย่อ วารสารปิดที่ไม่มี PDF = ใช้ได้แค่ชื่อเรื่อง/บทคัดย่อ ห้ามยกตัวเลขในเนื้อมาอ้างเป็นหลักฐานชั้นใน

## 3. งานที่ถูกใช้ใน 4.1 และ 4.2 กับสถานะฉบับเต็ม

### 3.1 งานที่เปิดฉบับเต็มในคลังได้ และสมควรคงไว้

| หมายเลขใน 12.1 | งาน | ใช้ที่ | ไฟล์ในคลัง |
|---:|---|---|---|
| [16] | Anapalli et al., *Heliyon* 2023 | 4.2 หัว 1–2 (AWD, eddy covariance) | `supporting/2023_Anapalli_eddy_covariance_AWD_rice_methane.pdf` |
| [17] | Guan et al., *Plants* 2024 | 4.2 หัว 1 (ราก/ไรโซสเฟียร์) | `supporting/2024_rice_root_rhizosphere_methane_emission.pdf` |
| [18] | Dai et al., *Sci. Rep.* 2026 | 4.2 หัว 1 (คาร์บอน, pH) | `supporting/2025_methane_emissions_carbon_availability_soil_pH_gradient.pdf` |
| [19] | Yang et al., *Agronomy* 2022 | 4.2 หัว 1 (ปุ๋ย/พันธุ์) | `supporting/2025_product_type_rice_variety_agronomic_CH4_emissions.pdf` |
| [20] | Hu et al., *iScience* 2024 | PDF มีในคลัง; ในร่าง 12 **ไม่มีในเนื้อ 4.1/4.2** มีแค่รายการอ้างอิง ร่าง 12.1 มีหัวโมเดลกระบวนการแต่ยังไม่ใส่เลข | `supporting/2025_CH4MOD_global_methane_emissions_rice_paddies.pdf` |
| [32] | Saunois et al., *Earth Syst. Sci. Data* 2025 | 4.1/4.2 หัว 3 (งบมีเทนโลก) | `oa-fetch/essd-17-1873-2025.pdf` |
| [45] | Collier-Oxandale et al., *Atmos. Meas. Tech.* 2018 | 4.2 หัว 4–5 (สอบเทียบ MOS นอกนา) | `oa-fetch/2018_Collier-Oxandale_AMT_lowcost_methane.pdf` |
| [47] | Tokida, *J. Agric. Meteorol.* 2021 | 4.2 หัว 2 (chamber) | `direct/2021_Tokida_modified_closed_chamber_rice_methane.pdf` |
| [48] | Li et al., *Molecules* 2022 | 4.2 หัว 2 / ทฤษฎี 5.3 (GC-FID) | `direct/2022_LowCost_GC-FID_methane_rice_cultivation.pdf` |
| [49] | Bastviken et al., *Biogeosciences* 2020 | 4.2 หัว 2 และ 4 (เซ็นเซอร์ใน chamber) | `direct/2020_Bastviken_lowcost_CH4_sensors_flux_chambers.pdf` |
| [50] | Kiplimo et al., *Atmosphere* 2024 | 4.2 หัว 5 (ML calibrate TGS) | `direct/2024_Kiplimo_ML_calibration_lowcost_methane_TGS.pdf` |
| [52] | Shah et al., *Atmos. Meas. Tech.* 2023 | 4.2 หัว 4 (TGS2611 + T/H) | `direct/2023_Shah_TGS2611-E00_methane_environmental_response.pdf` |
| [53] | Furuta et al., *Atmos. Meas. Tech.* 2022 | 4.2 หัว 4 (MOS ระดับต่ำ) | `direct/2022_Furuta_inexpensive_MOx_trace_methane.pdf` |
| [5] | Rajasekar & Selvi, *Sensors* 2022 | 4.1; 4.2 หัว 4; รูปที่ 6 | `direct/2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf` (EuropePMC PMC9185635; เปิดหน้าแรกแล้ว) |
| [6] | Zaman et al. 2021 บทที่ 2 Springer OA | 4.1; 4.2 หัว 2 | `direct/2021_Zaman_GHG_measurement_agricultural_soils_methodology.pdf` (บทที่ 2, 98 หน้า) |
| [10] | Domènech-Gil et al., *Environ. Sci. Technol.* 2024 | 4.1; 4.2 หัว 4; รูปที่ 5 | `direct/2024_Domenech-Gil_eNose_environmental_methane_monitoring.pdf` (PMC10785752; เล่ม 58:352–361) |
| [24] | Ye, Liu & Li, *Sensors* 2021 | 4.2 หัว 4 | `supporting/2021_Ye_smart_eNose_machine_learning_review.pdf` |
| [25] | Yin et al., *Sensors* 2023 | 4.2 หัว 4 | `supporting/2023_Yin_eNose_CH4_CO_mixed_gas_identification.pdf` |
| [26] | Fu et al., *Molecules* 2023 | 4.2 หัว 4 | `supporting/2023_MOS_chemiresistive_methane_sensor_review.pdf` |
| [27] | Andrews et al., *Sensors* 2023 | 4.2 หัว 5 | `direct/2023_Andrews_ML_calibrating_gas_sensors_methane_emissions.pdf` |
| [28] | Mitchell, Cox & Lewis, *Sensors* 2024 | 4.2 หัว 5; รูปที่ 4 | `direct/2024_Mitchell_Figaro_lowcost_methane_ML_calibration.pdf` |
| [51] | Lakhmi et al., *Sensors* 2024 | 4.2 หัว 5 | `direct/2024_Lakhmi_linear_nonlinear_gas_sensor_array_CH4.pdf` (PMC11174819; **อย่าใช้ PMC11174900** ซึ่งเป็นงาน celiac คนละเรื่อง) |
| — | Minamikawa et al. 2015 GRA guidelines | 4.2 หัว 2; ทฤษฎี 5.2 | `direct/2015_Minamikawa_GRA_chamber_guidelines_rice.pdf` |
| — | Conrad 2020 *Microorganisms* | ทฤษฎี 5.1 | `supporting/2020_Conrad_methane_production_soil_flooding.pdf` |

งานฉบับเต็มในคลังที่ไม่ได้ใส่หมายเลขใน 4.1–4.2 แต่ใช้เติมหัวได้โดยไม่ invent citation: Gu et al. 2022 (น้ำ–ปุ๋ย, PDF), Furuta et al. 2024 (โหนด MOS, PDF), Shah et al. 2024 (TGS2611 หลุมฝังกลบ, PDF), Rivera-Martinez et al. 2024 (MOS+MLP รั่วไหล, PDF), Basheer et al. 2024 (รีวิวดินเกษตร, PDF)

### 3.2 งานที่ถูกอ้างแต่ต้องตัดออกจากชุดยืนยันข้ออ้าง จนกว่าจะมีฉบับเต็ม

ตัดในที่นี้หมายถึง **ห้ามใช้ตัวเลขหรือกลไกชั้นในจากงานนั้น** ในปริทัศน์ จนกว่าจะเปิด PDF ได้ ยังเก็บในรายการอ้างอิงของร่างได้ในฐานะตัวชี้ทิศ แต่ไม่นับเป็นหนึ่งในห้าชิ้นต่อหัว

| หมายเลข | งาน | เหตุที่ตัด |
|---:|---|---|
| [4] | Nguyen et al. 2023 บทในหนังสือ | ในคลังไฟล์ชื่อนี้เป็นงานคนละเรื่อง (Ji et al. 2024) มีหลักฐานจากรอบคัดกรองเดิม |
| [7] | Mumu et al. 2024 | metadata อย่างเดียว |
| [8] | Tyagi et al. 2025 | metadata อย่างเดียว |
| [9] | Borhan & Khanaum 2022 | ปศุสัตว์ นอกขอบ 4.2 นาข้าว |
| [11] | Baruah & Mazumder 2025 | IEEE ปิด metadata อย่างเดียว |
| [12] | Ahmad et al. 2026 | metadata อย่างเดียว |
| [13] | Zhou et al. 2024 | stub `.md` ประมาณ 10 บรรทัด (ลิงก์ DOI/PubMed) **ไม่ใช่ extract** |
| [14] | Xuan et al. 2025 | **หายจาก screened ทั้ง PDF, md, bib, ris** |
| [15] | Rafy et al. 2025 | **หายจาก screened ทั้ง PDF, md, bib, ris** |
| [21] / [40] | Vo et al. 2026 *Front. Agron.* | DOI มีใน Crossref ของคลัง แต่ไม่มี PDF |
| [22] | Xu et al. 2025 SSRN | preprint metadata |
| [23] | Zhang et al. 2025 | มีแค่ `…_extract.txt` ระดับบทคัดย่อ; ในร่าง 12 **ไม่มีในเนื้อ 4.1/4.2** |
| [56] | Othman et al. 2026 JARSET | DOI `10.37934/araset.60.5.3350` Crossref คืนค่าว่าง **ไม่ใช้** |

ย้ายออกจากตารางนี้แล้วเพราะมี PDF ในคลัง: [5] Rajasekar, [6] Zaman บทที่ 2, [10] Domènech-Gil *ES&T*, [24]–[28] Ye/Yin/Fu/Andrews/Mitchell, [51] Lakhmi

ข่าวและแนวโน้มอุตสาหกรรม [1]–[3] ใช้ใน 4.1 ได้ในฐานะบริบทเศรษฐกิจ ไม่ใช่งานวิจัย systematic review

### 3.3 สิ่งที่ทำให้ฉงนระหว่างร่าง 12 กับ 12.1

ร่าง 12 มีย่อหน้า 4.2.1–4.2.4 พร้อมเลขอ้างอิง ร่าง 12.1 ตัดเนื้อ 4.2 เหลือหัวข้อและขยายรายการถึง [56] การไล่ว่าเลขไหนถูกใช้ใน 4.2 จึงต้องยึดร่าง 12 จนกว่า 12.1 จะใส่เลขกลับ ตัวเลขหนักในร่าง 12 จาก Rafy และ Vo ยังผูกกับงานที่ไม่มีฉบับเต็ม อย่าย้ายลง 12.1 จนกว่าจะเปิด PDF ส่วน Domènech-Gil [10] เปิดฉบับ *ES&T* ได้แล้วในรอบนี้

Hu [20] และ Zhang [23] มีใน References ของร่าง 12 แต่ไม่มีในเนื้อ 4.1/4.2 ไฟล์ Hu เป็น PDF จริง ใช้เติมหัว 3 ของ 12.1 ได้ Zhang ยังเป็น extract

### 3.4 รูปในร่าง 12 กับไฟล์ในคลัง

| รูป | งาน | ไฟล์ | เกรด |
|-----|------|------|------|
| 1 | Ji et al. 2024 *Front. Sustain. Food Syst.* | `supporting/2023_Nguyen_….pdf` | PDF แต่ชื่อไฟล์/`.bib` เป็น Nguyen |
| 2 | Anapalli et al. 2023 = [16] | PDF ตาม [16] | PDF |
| 3 | Bastviken et al. 2020 | `direct/2020_Bastviken_….pdf` | PDF |
| 4 | Kiplimo et al. 2024; caption ใส่ [10], [28] | `direct/2024_Kiplimo_….pdf` | PDF ของสถาปัตยกรรม; [10] และ [28] ไม่มี PDF |
| 5 | Domènech-Gil [10] | `direct/2024_Domenech-Gil_….pdf` | PDF ของ *ES&T* |
| 6 | Rajasekar [5] Fig. 3 | `direct/2022_Rajasekar_….pdf` | PDF |

`supporting/2024_DomenechGil_…Eurosensors.pdf` เป็น proceedings คนละเอกสารกับ [10] *ES&T*

## 4. Taxonomy ของ 4.2 ตามร่าง 12.1

แกนจัดเป็น **สเกลการวัด × ชนิดปริมาณ**

| | ความเข้มข้น (ppm/ppb) | ฟลักซ์ต่อพื้นที่ | บัญชี/แผนที่ภูมิภาค |
|---|---|---|---|
| กลไกในดินนา | หัว 1 | หัว 1 | — |
| แปลงนา | หัว 2 (GC ของตัวอย่างอากาศ) | หัว 2 (chamber, eddy) | — |
| ภูมิภาค | — | — | หัว 3 |
| MOS / e-nose | หัว 4–5 | Bastviken: เซ็นเซอร์ใน chamber | — |

ช่องว่างที่มองเห็นได้ทันที: เซลล์ “e-nose ให้ค่า ppm ในนาข้าวโดยเทียบ GC” ยังว่างในคลังฉบับเต็ม นี่คือช่องว่างวิจัยของวิทยานิพนธ์ ไม่ใช่ช่องว่างการค้นที่พลาด

## 5. หัว 4.2 การปล่อยก๊าซมีเทนจากนาข้าวน้ำขัง

นาข้าวน้ำขังปล่อย CH₄ เพราะดินขาดออกซิเจน methanogen ย่อยสารอินทรีย์ แล้วแก๊สออกสู่บรรยากาศทางท่ออากาศในต้น ทางฟอง และทางผิวน้ำ งานสนามของ Guan et al. [17] แสดงว่าฟลักซ์ผูกกับราก ไรโซสเฟียร์ และสัดส่วน methanogen/methanotroph ส่วน Dai et al. [18] แสดงว่าคลังคาร์บอนที่ใช้ได้และ pH อธิบายความแปรปรวนของการผลิตในดินตามแนวอุณหภูมิ ปัจจัยจัดการน้ำให้ผลลดฟลักซ์ซ้ำในหลายระบบ: Anapalli et al. [16] วัดด้วย eddy covariance แล้วพบว่า AWD ลด CH₄ ประมาณครึ่งหนึ่งโดยผลผลิตต่างกันเล็กน้อย Gu et al. (2022, PDF ในคลัง) สังเคราะห์งานสนามแล้วพบว่าการจัดการน้ำประหยัดน้ำลด CH₄ ได้มากแต่ผลต่อผลผลิตไม่เท่ากันทุกวิธี Yang et al. [19] จำกัดผลของปุ๋ยไนโตรเจนประสิทธิภาพสูงไว้ที่ชนิดผลิตภัณฑ์ พันธุ์ และการขังน้ำ

งานทฤษฎีเส้นทางในต้นที่ควรเติมแม้ยังไม่มีในคลัง: Nouchi, Mariko และ Aoki (1990) *Plant Physiol.* DOI 10.1104/pp.94.1.59 มี PDF จาก Oxford Academic ตาม Semantic Scholar และ Oo, Win และ Bellingrath-Kimura (2015) *SpringerPlus* DOI 10.1186/s40064-015-0901-2 ซึ่งวัดความแปรผันภายในแปลงในเมียนมา ฟลักซ์ที่จุดออกน้ำสูงกว่าจุดอื่น 2–2.5 เท่า และคาร์บอนรวมในดินเป็นตัวแปรหลัก Conrad (2020) *Microorganisms* DOI 10.3390/microorganisms8060881 อธิบายลำดับตัวรับอิเล็กตรอนและการที่ methanogen ทนออกซิเจนได้เกินที่เคยเชื่อ เหมาะกับ 5.1.1 มากกว่าการเป็นหลักฐานฟลักซ์แปลง

**ห้าชิ้นที่นับเป็นฉบับเต็มหรือ OA ที่ตรวจแล้วสำหรับหัวนี้**

1. Guan et al. 2024 — PDF ในคลัง
2. Dai et al. 2026 — PDF ในคลัง
3. Anapalli et al. 2023 — PDF ในคลัง
4. Yang et al. 2022 — PDF ในคลัง
5. Gu et al. 2022 *Int. J. Environ. Res. Public Health* 19:7324 — PDF ในคลัง

เสริมถ้าเปิดได้: Nouchi 1990 (กลไกท่ออากาศ), Oo 2015 (ความแปรผันในแปลง), Hu et al. [20] (โมเดลกระบวนการ ย้ายไปหัว 3 ได้) Conrad 2020 เปิด PDF ในคลังแล้ว รอบค้น OA ยังชี้งานกลไก/เมตาที่ยังไม่ได้ดึง: Qian 2023, Win 2021, Jiang 2019, Prangbang 2020 (บริบทไทย)

ข้อจำกัด: Rafy et al. [15] ที่ร่าง 12 ใช้ตัวเลขลด CH₄ ร้อยละ 64.5 ยังไม่มีฉบับเต็ม อย่าคัดลอกตัวเลขนั้นลง 12.1 Zhou [13] เป็นงานแผนที่ภูมิภาค ใช้ในหัว 3 ไม่ใช่หลักฐานกลไกแปลง

## 6. หัว 4.2 การวัดก๊าซมีเทนในระดับแปลงนา

static chamber กับ GC ยังเป็นวิธีอ้างอิงของฟลักซ์ดินเกษตร เพราะครอบพื้นที่จำกัด เก็บตัวอย่างตามเวลา แล้วแปลงความชันความเข้มข้นเป็นฟลักซ์ แนวปฏิบัติที่ใช้กับนาข้าวโดยตรงคือ Minamikawa, Tokida, Sudo, Padre และ Yagi (2015) ดาวน์โหลดจาก Global Research Alliance แล้วอยู่ในคลัง (`direct/2015_Minamikawa_….pdf`, 80 หน้า) Zaman et al. [6] บทที่ 2 ของหนังสือ Springer OA อธิบาย SOP chamber/GC ของดินเกษตร รวมข้อควรระวังในนาท่วม Tokida [47] ลดเวลาต่อห้องเหลือ 4–5 นาทีเมื่อใช้เครื่องวิเคราะห์พกพาแทน GC แบบเดิม Li et al. [48] ปรับ GC-FID ฉีดมือสำหรับตัวอย่างจากนา LOD 0.0567 ppm Wassmann et al. (2018) *PLOS ONE* DOI 10.1371/journal.pone.0191352 แสดงว่าการครอบห้องกลางคืนเพิ่มความไวเมื่อฟลักซ์ต่ำ Anapalli et al. [16] เป็นตัวอย่าง eddy covariance ที่คนละสเกลกับ chamber: แปลงใหญ่ ความต่อเนื่องสูง แต่ไม่ใช่ ground truth รายจุดแบบ chamber–GC

Bastviken et al. [49] อยู่คนละชั้น: ใส่เซ็นเซอร์ต้นทุนต่ำ *ใน* chamber เพื่อติดตามความเข้มข้นระหว่างครอบ ไม่ได้แทนที่ GC ในฐานะวิธีสอบเทียบของวิทยานิพนธ์นี้ แต่ชี้ว่าความชื้นในหัวห้องรบกวน MOS

**ห้าชิ้นสำหรับหัวนี้**

1. Minamikawa et al. 2015 (guideline) — PDF ในคลัง, [36]
2. Zaman et al. 2021 บทที่ 2 — PDF ในคลัง, [6]
3. Tokida 2021 — PDF ในคลัง, [47]
4. Li et al. 2022 — PDF ในคลัง, [48]
5. Anapalli et al. 2023 — PDF ในคลัง, [16] สำหรับแขนง eddy covariance

Collier et al. (2014) *J. Vis. Exp.* DOI 10.3791/52110 และ Bertora et al. (2018) *J. Vis. Exp.* DOI 10.3791/56754 เป็นโพรโตคอลภาพ chamber (ทั่วไป / นา) ที่รอบค้น OA ระบุว่า Gold OA บน PMC แต่ยังไม่ได้ดึงเข้าคลังในรอบนี้ อย่าใช้ตัวเลขจาก Vo [21] จนกว่าจะเปิด *Frontiers in Agronomy*

จุดที่งานขัดกัน: Meijide et al. (2011) *Biogeosciences* พบว่า chamber ให้ค่าฤดูสูงกว่า eddy ประมาณ ร้อยละ 30 ในนาอิตาลี ความต่างนี้อธิบายด้วยสเกลและความถี่ ไม่ได้อธิบายว่าวิธีใด “ผิด”

## 7. หัว 4.2 การประเมินการปล่อยก๊าซมีเทนระดับภูมิภาค

Saunois et al. [32] วางนาข้าวไว้ในงบมีเทนโลกในฐานะแหล่งมนุษย์ที่ยังมีความไม่แน่นอนสูง Zhang, Xiao et al. (2020) *Nat. Commun.* DOI 10.1038/s41467-019-14155-5 มี PDF จากผู้พิมพ์ แสดงความสอดคล้องเชิงพื้นที่–ฤดูระหว่างพื้นที่นาในเอเชียมรสุมกับ XCH₄ จากดาวเทียม แต่ไม่รองรับการติดตามรายแปลง Hu et al. [20] ให้ช่วงการปล่อยโลกจาก CH₄MOD 8–78 Tg ปี⁻¹ เฉลี่ย 45 และชี้ว่าระบบน้ำเป็นตัวขับหลัก IPCC AFOLU (2022) และ IPCC 2019 Refinement บท cropland เป็นกรอบบัญชี ไม่ใช่การวัดรายแปลง

งานดาวเทียมรายประเทศอย่าง Liang et al. [42] ยังเป็น ACS ปิด ใช้ได้แค่ระดับชื่อเรื่องจนกว่าจะมี OA

**ห้าชิ้นสำหรับหัวนี้**

1. Saunois et al. 2025 — PDF ในคลัง, [32]
2. Zhang et al. 2020 *Nat. Commun.* — OA, [41]
3. Hu et al. 2024 — PDF ในคลัง, [20]
4. IPCC 2019 Refinement vol. 4 ch. 5 Cropland — [37]
5. IPCC AR6 WGIII ch. 7 AFOLU 2022 — [33]

อย่าใช้หัวนี้ไปสนับสนุนความละเอียดรายแปลง งานชุดนี้รวมกันชี้ตรงกันข้าม: ดาวเทียมและโมเดลกระบวนการต้องการการวัดภาคพื้นเป็นจุดยึด

## 8. หัว 4.2 จมูกอิเล็กทรอนิกส์และเซ็นเซอร์โลหะออกไซด์

นิยามปฏิบัติของ e-nose คืออาเรย์เซ็นเซอร์ที่เลือกจำเพาะบางส่วน บวกการรู้จำรูปแบบ ไม่ใช่เซ็นเซอร์เดี่ยวที่แปลง ppm ด้วยสูตรผู้ผลิต Rajasekar [5] ซึ่งร่างเดิมใช้เป็นตัวอย่างนาข้าว ใช้ MQ4/TGS2611 ใน chamber นาแต่แปลงค่าด้วยสูตรผู้ผลิต จึงอยู่คนละชั้นกับ e-nose+ML งานนี้เปิด PDF ได้แล้ว (12 หน้า) และเป็นงานนาข้าวชิ้นเดียวในรายการที่วัดใกล้แปลง

งานฉบับเต็มที่ใกล้โจทย์ฮาร์ดแวร์ที่สุดอยู่นอกนา: Shah et al. [52] แสดงว่า TGS2611-E00 ตอบทั้ง CH₄ และสภาพแวดล้อม Furuta et al. [53] และ Furuta et al. 2024 วัด MOS ใกล้พื้นหลัง Kiplimo et al. [50] และ Collier-Oxandale et al. [45] แสดงว่าการสอบเทียบเชิงเส้นอย่างเดียวไม่พอเมื่อความชื้นและอุณหภูมิเลื่อน Bastviken et al. [49] เตือนผลของไอน้ำใน chamber Ye et al. [24] ทบทวน e-nose+ML Fu et al. [26] ทบทวน MOS chemiresistive สำหรับมีเทน Yin et al. [25] จำแนก CH₄/CO ไม่ใช่ประมาณความเข้มข้น

Domènech-Gil et al. [10] เปิดฉบับ *ES&T* ได้แล้ว (10 หน้า, CC-BY 4.0, PMC10785752) ฮาร์ดแวร์คือ TGS2611-C00 + TGS2611-E00 + BME680 โมเดล PLSR ช่วงสนาม 1–150 ppm สนามทดสอบเป็นสวน บ่อบำบัด และพรุในสวีเดน ไม่ใช่นาข้าว ในห้องปฏิบัติการ R² = 0.97 และ RMSE = 89 ppb (ชุดทดสอบ R² > 0.9, RMSE < 100 ppb) ในสนาม R² อยู่ระหว่าง 0.36–0.91 และ RMSE อยู่ระหว่าง 33 ppb ถึง 5.3 ppm ค่า 5.3 ppm ตรงกับห้องกดตะกอนที่ความเข้มข้นสูง (ค่าเฉลี่ยประมาณ 34 ppm) และคิดเป็นความคลาดเคลื่อนสัมพัทธ์ร้อยละ 4.5 ข้ออ้างตัวเลขในร่างเดิมจึงใช้ได้แล้ว แต่ยังไม่ปิดช่องว่าง “ppm ในนาเทียบ GC”

ตำรานิยามที่ตรวจบน Crossref: Gardner และ Bartlett (1999) *Electronic Noses: Principles and Applications*, Oxford, DOI 10.1093/oso/9780198559559.001.0001 และ Pearce, Schiffman, Nagle และ Gardner (eds.) (2003) *Handbook of Machine Olfaction*, Wiley, DOI 10.1002/3527601597 ทั้งสองยังไม่มี PDF ฟรี ใช้ Wilson และ Baietto (2009) *Sensors* 9:5099 เป็นรีวิว OA ทดแทนได้เมื่อดึงเข้าคลัง

**ห้าชิ้นสำหรับหัวนี้ (ฉบับเต็มในคลัง)**

1. Rajasekar & Selvi 2022 — PDF ในคลัง, [5] นาข้าว MOS ไม่ใช่ ML
2. Domènech-Gil et al. 2024 *ES&T* — PDF ในคลัง, [10] e-nose+PLSR นอกนา
3. Shah et al. 2023 — PDF ในคลัง, [52]
4. Ye et al. 2021 — PDF ในคลัง, [24]
5. Fu et al. 2023 — PDF ในคลัง, [26]

เสริม: Furuta 2022 [53], Bastviken 2020 [49], Collier-Oxandale 2018 [45], Yin 2023 [25]

## 9. หัว 4.2 การสอบเทียบความเข้มข้นด้วยการเรียนรู้แบบมีผู้สอน

งานฉบับเต็มในคลังชี้ไปทางเดียวกัน: MOS สำหรับ CH₄ ต้องการโมเดลที่รับอุณหภูมิและความชื้นเข้าไปด้วย ไม่ใช่เส้น calib ห้องแล็บอย่างเดียว Kiplimo et al. [50] แก้ข้อบกพร่องของการสอบเทียบเซ็นเซอร์ต้นทุนต่ำด้วย ML Shah et al. [52] ให้ลักษณะตอบสนองต่อ CH₄ และสิ่งแวดล้อมของ TGS2611 ซึ่งเป็นฮาร์ดแวร์เดียวกับโจทย์ Andrews et al. [27] สอบเทียบเซ็นเซอร์ก๊าซมีเทนภาคสนามด้วย ML Mitchell et al. [28] สอบเทียบ Figaro CH₄ ต้นทุนต่ำด้วย ML Lakhmi et al. [51] เปรียบ MLR-PLS กับ ANN บนอาเรย์ที่มี CH₄ พบว่า ANN ดีกว่าสำหรับมีเทนเพราะการตอบของ MOX เป็นลอการิทึม (เปิดหน้าแรกแล้วตรงงาน; PMC ที่ถูกคือ PMC11174819)

ตำราแกนของหัวนี้มีในโครงการแล้ว: Deisenroth, Faisal และ Ong (2020) *Mathematics for Machine Learning* DOI 10.1017/9781108679930 อธิบาย empirical risk minimization การถดถอยเชิงเส้น ชุดฝึก/ชุดทดสอบ และ overfitting Madsen (2011) *Statistics for Non-Statisticians* DOI 10.1007/978-3-642-17656-2 อธิบายการรายงานค่าประมาณพร้อมความไม่แน่นอน ซึ่งรองรับ RMSE/MAE/R² ใน 5.5.4

**ห้าชิ้นสำหรับหัวนี้**

1. Deisenroth et al. 2020 — ตำราใน `project-knowledge` และ [31]
2. Kiplimo et al. 2024 — PDF ในคลัง, [50]
3. Andrews et al. 2023 — PDF ในคลัง, [27]
4. Mitchell et al. 2024 — PDF ในคลัง, [28]
5. Lakhmi et al. 2024 — PDF ในคลัง, [51]

เสริม: Shah 2023 [52], Collier-Oxandale 2018 [45], Chai และ Draxler (2014) *Geosci. Model Dev.* DOI 10.5194/gmd-7-1247-2014 สำหรับ RMSE กับ MAE

ไม่มีงานฉบับเต็มในคลังที่ฝึก regression ให้ค่า ppm จากอาเรย์ MOS ในนาข้าวแล้วเทียบ GC นี่สอดคล้องช่องว่างที่ 4.1 ตั้งไว้ ไม่ใช่ช่องว่างจากการค้นไม่ครบ Rajasekar ใกล้แปลงนาที่สุดแต่ไม่ใช่ ML Domènech-Gil ใกล้ที่สุดด้าน e-nose+PLSR แต่สนามไม่ใช่นา

## 10. ทฤษฎีสำหรับบทที่ 5

โครง 5 ใน 12.1 กว้างกว่าไฟล์ `proposal-ch5-โครงหัวข้อ.md` เพราะดึงวิธีวัดเข้ามาไว้ใน 5.1.3 ทฤษฎีที่แนะนำด้านล่างจับกับหัวใน 12.1 โดยตรง ใช้ตำราหรือรีวิวกลไกเป็นแกน paper สนามเป็นตัวอย่าง

### 5.1 ก๊าซมีเทนในนาข้าวน้ำขัง

| หัวย่อย | แหล่งทฤษฎีที่ตรวจแล้ว | บทบาท |
|---|---|---|
| 5.1.1 สภาวะไร้ออกซิเจน / methanogen | Conrad (2020) *Microorganisms* 8:881 — PDF ในคลัง | ลำดับตัวรับอิเล็กตรอน การทน O₂ ของ methanogen |
| 5.1.1 เส้นทางในต้น | Nouchi et al. (1990) *Plant Physiol.* 94:59 | ท่ออากาศจากไรโซสเฟียร์สู่บรรยากาศ |
| 5.1.2 ตัวแปรเหนือผิวนา | Guan 2024, Dai 2026, Gu 2022, Anapalli 2023 | ราก คาร์บอน น้ำ อุณหภูมิ |
| 5.1.3 วิธีวัดแปลงเล็ก | Minamikawa et al. 2015; Tokida 2021; Li 2022 | chamber และ GC-FID |
| 5.1.3 แปลงใหญ่ | Anapalli 2023; แนว eddy vs chamber ของ Meijide 2011 | คนละสเกลกับห้องทดลองของวิทยานิพนธ์ |
| 5.1.3 ภูมิภาค | Saunois 2025; IPCC 2019/2022; Zhang 2020 *Nat. Commun.* | บัญชี ไม่ใช่ ppm รายจุด |

### 5.2 ความเข้มข้นกับฟลักซ์

ยังไม่มีตำราใน `project-knowledge` ที่นิยาม ppm กับฟลักซ์โดยตรง ใช้ Minamikawa et al. (2015) บทคำนวณฟลักซ์จากความชันความเข้มข้นในหัวห้อง (PDF ในคลัง) และ IPCC 2019 บท cropland สำหรับหน่วยบัญชี เน้นประโยคแกน: วิทยานิพนธ์นี้วัดความเข้มข้น ไม่รายงานฟลักซ์ฤดูปลูก Venterea et al. (2020) *J. Environ. Qual.* DOI 10.1002/jeq2.20124 มีสำเนา USDA ที่รอบค้น OA ตรวจ `%PDF-` แล้ว แต่ยังไม่ได้ดึงเข้าคลัง

### 5.3 GC และการสอบเทียบก๊าซ

Li et al. (2022) เป็น paper วิธีที่ใกล้ที่สุดในคลัง (GC-FID, LOD, กราฟมาตรฐาน) Zaman et al. (2021) บทที่ 2 เปิด PDF ได้แล้วในคลัง Skoog หรือตำราวิเคราะห์เครื่องมือทั่วไป **ไม่ได้ถูกค้นจนยืนยันฉบับที่ใช้ในโครงการ** จึงไม่ใส่ชื่อฉบับในรายงานนี้

### 5.4 จมูกอิเล็กทรอนิกส์และเซ็นเซอร์ก๊าซ

Gardner & Bartlett (1999) สำหรับนิยามอาเรย์ + pattern recognition Pearce et al. (2003) สำหรับ MOS, การส่งกลิ่น, และการประมวลสัญญาณ ทั้งสองยังไม่มีเล่ม OA เต็ม ใช้ Ye 2021 และ Fu 2023 ในคลังเป็นรีวิวร่วมสมัย บทที่ 8 ของ Gardner อธิบาย headspace, ห้องเซ็นเซอร์ และ ADC ซึ่งตรง 5.4.4 เมื่อเปิดเล่มได้ Shah 2023 และ Furuta 2022 สำหรับผล T/H ต่อ TGS/MOS

### 5.5 การเรียนรู้แบบมีผู้สอน

Deisenroth et al. (2020) เป็นแกน: ความหมาย supervised learning, การถดถอยเชิงเส้น, ERM, overfitting, ชุดฝึก/ทดสอบ Madsen (2011) สำหรับการกระจายของความคลาดเคลื่อนและความไม่แน่นอนของค่าประมาณ Kiplimo 2024 เป็นตัวอย่าง applied calibration ไม่ใช่ทฤษฎี

Creswell (2009) [29] ไม่ใช่ทฤษฎีของ 5.1–5.5 ใช้ได้ที่โครงข้อเสนอและการเขียนจุดประสงค์ ไม่ใช่บททฤษฎีแก๊สหรือเซ็นเซอร์

## 11. ตำราใน project-knowledge กับบทที่ 5

คลังตำราของโครงการมีห้าเล่ม ใช้กับบทที่ 5 ได้ไม่เท่ากัน

| ตำรา (ไฟล์ใน knowledge base) | บท skill | ใส่ในบทที่ 5 ได้หรือไม่ |
|---|---|---|
| Bonanno, *Game Theory* | ch01, ch02 | ไม่ใส่ เนื้อหาไม่แตะแก๊ส เซ็นเซอร์ หรือการเรียนรู้จากคู่ข้อมูล |
| METU Academic Writing | ch03 | ไม่ใส่ในบททฤษฎี ใช้ตอนเขียนย่อหน้าให้มี claim + evidence |
| Madsen, *Statistics for Non-Statisticians* | ch04, ch05 | **ใส่ 5.5.3–5.5.4** การแบ่งข้อมูล การรายงานค่าประมาณ+ความไม่แน่นอน การกระจายของ error การไม่ใช้ p-value เปล่า ch04 เรื่องการวางแผนเก็บข้อมูลไปบท 6 ได้มากกว่า |
| Creswell, *Research Design* 3rd ed. | ch06, ch07 | ไม่ใส่ทฤษฎี 5.1–5.4 ใช้ deficiency model กับ 4.1 และ validity ของการทดลองในบท 6 |
| Deisenroth, Faisal & Ong, *Mathematics for Machine Learning* | ch08–ch10 | **ใส่ 5.5 ทั้งหัว** และบางส่วนของ 5.4 ถ้าพูดเวกเตอร์สัญญาณเซ็นเซอร์ |

รายละเอียด Deisenroth ที่จับหัว 5.5 ของ 12.1 ได้โดยตรง:

- **5.5.1** supervised = เรียนรู้จากคู่เข้า–ออก ผ่านกรอบ ERM (ch10)
- **5.5.2** งานนี้เป็นการถดถอย ไม่ใช่จำแนก ประโยคนี้ต้องเขียนชัด เพราะ SVM ในตำราเป็นตัวจำแนก ไม่ใช่โมเดลหลักของวิทยานิพนธ์
- **5.5.3** แบบจำลองเชิงเส้น: least squares, ridge, มุมมองภาพฉายตั้งฉาก (ch08, ch10)
- **5.5.3** overfitting และชุดฝึก/ทดสอบ (ch10) ความเป็นอิสระเชิงเส้นของช่องเซ็นเซอร์ (ch08) ถ้าอาเรย์มีช่องซ้ำ
- **5.5.4** RMSE/MAE/R² เป็นตัวชี้วัดความใกล้เคียงกับ GC ในขอบเขตที่ฝึก ไม่ใช่บทพิสูจน์ฟลักซ์นา Madsen เติมเรื่องความไม่แน่นอนของค่าประมาณ

เกาส์และ Bayes ใน ch09 ใช้ได้ถ้าอธิบายสมมติฐานสัญญาณรบกวนของการถดถอย อย่าขยายไป GMM/SVM ถ้าบท 6 ยังใช้แต่โมเดลเชิงเส้น

## 12. สังเคราะห์ข้ามหัว

งานฉบับเต็มรวมกันได้สามประเด็น ไม่ใช่สิบประเด็นย่อย

ประการแรก กลไกนาข้าวและการจัดการน้ำมีหลักฐานสนามและเมตา-วิเคราะห์ซ้ำกัน การขังน้ำต่อเนื่องเพิ่ม CH₄ การระบายหรือ AWD ลดได้ ผลผลิตไม่จำเป็นต้องลดตาม เงื่อนไขที่ทำให้ผลต่างกันคือดิน ฟาง และพันธุ์

ประการที่สอง วิธีวัดไม่แทนกัน chamber–GC เป็น ground truth รายจุด eddy covariance เป็นความต่อเนื่องแปลงใหญ่ ดาวเทียมเป็นภูมิภาค MOS เป็นความเข้มข้นต่อเนื่องที่มี cross-sensitivity การเอา RMSE ของ e-nose ในอากาศพื้นหลังไปเทียบฟลักซ์นาเป็นการเทียบคนละปริมาณ

ประการที่สาม ช่องว่างที่ 4.1 ตั้งไว้ยังว่างอยู่หลังเปิด PDF ชุดเซ็นเซอร์แล้ว ไม่มีงานในคลังที่แสดงอาเรย์ MOS + regression เป็น ppm + เทียบ GC ในบริบทนาข้าว Rajasekar ใกล้ที่สุดด้านสถานที่แต่ใช้สูตรผู้ผลิต ไม่ใช่ ML Domènech-Gil ใกล้ที่สุดด้าน e-nose+PLSR แต่สนามไม่ใช่นา และอ้างอิงเป็นเครื่องวิเคราะห์ก๊าซ (GGA) ไม่ใช่ chamber–GC

## 13. ปัญหาเปิดที่วรรณกรรมชี้ไว้เอง

เซลล์ taxonomy “e-nose ให้ ppm ในนา เทียบ chamber–GC” ว่างหลังค้นคลังและดัชนี OA นี่คือที่มาของวิทยานิพนธ์ ไม่ใช่ประโยค “ควรมีงานเพิ่ม”

งานที่ร่าง 12 ใช้ตัวเลขหนักจาก Rafy และ Vo ยังไม่มีฉบับเต็มในคลัง อย่าคัดลอกตัวเลขนั้นลง 12.1 ส่วน Domènech-Gil *ES&T* ใช้ตัวเลขจาก PDF ในคลังได้แล้ว

รอบค้น OA เติมรายการที่ยังไม่ได้ดึงเข้าคลัง ได้แก่ Qian et al. 2023 *Nat. Rev. Earth Environ.* (author PDF IRTA), Win et al. 2021 และ Wang et al. 2017 (PLOS), Linquist 2012 และ Jiang 2019 (author PDF UC Davis), Prangbang et al. 2020 (บริบทไทย), Neue & Roger 1993 (IRD), Collier/Bertora JoVE, Venterea 2020 (USDA), Wilson & Baietto 2009 งานเหล่านี้ตรวจ DOI แล้วแต่ไฟล์ยังไม่อยู่ใน `screened/` จนกว่าจะดึง

MDPI HTML เปิดในเบราว์เซอร์ได้ เครื่องนี้ดึง `/pdf` ไม่ได้เพราะ 403 ใช้ EuropePMC `getPdf` แทนได้ตามรอบนี้ Gardner & Bartlett 1994/1999 และ Pearce Handbook 2003 ยังไม่มีเล่ม OA

## 14. คำตอบต่อคำถามวิจัย

**RQ1.** ในเนื้อ 4.1/4.2 ของร่าง 12 งานที่มี PDF จริงเดิมคือ [16] [17] [18] [19] บวกรูป Bastviken และ Kiplimo ([47]–[53] อยู่ในรายการของ 12.1) รอบ ingest นี้เติม PDF ของ [5] [6] [10] [24]–[28] [51] Minamikawa และ Conrad 2020 Hu [20] มี PDF แต่ไม่ถูกอ้างในเนื้อร่าง 12 Xuan [14] และ Rafy [15] ยังหายจากคลังทั้งไฟล์และ metadata

**RQ2.** ทั้งห้าหัวของ 4.2 มีชุดสนับสนุนห้าชิ้นที่เปิด PDF ในคลังได้ตามหมวด 5–9 หัว 4 ไม่บางเพราะขาดไฟล์แล้ว แต่บางเพราะงานนาข้าวด้วย MOS ที่เปิดได้ (Rajasekar) ไม่ใช่ e-nose+ML และงาน e-nose+PLSR ที่เปิดได้ (Domènech-Gil) ไม่ใช่นา

**RQ3.** บทที่ 5 ควรยึด Conrad 2020 (PDF ในคลัง) และ Nouchi 1990 สำหรับ 5.1 Ye 2021 / Fu 2023 เป็นรีวิว OA ของ 5.4 จนกว่าจะเปิด Gardner & Bartlett 1999 และ Pearce 2003 Minamikawa 2015, Zaman 2021 และ Li 2022 สำหรับ 5.2–5.3 Deisenroth 2020 และ Madsen 2011 สำหรับ 5.5 จาก `project-knowledge` ใช้ได้จริงแค่ Madsen กับ Deisenroth Creswell ไปบทโครงและบท 6 Bonanno ไม่ใช้ METU ใช้ตอนเขียนไม่ใช่ตอนตั้งทฤษฎี

## References

[1] Guan, S., et al., "Effects of Rice Root Development and Rhizosphere Soil on Methane Emission in Paddy Fields," *Plants*, 2024.
[2] Dai, Y., et al., "Methane emissions from rice paddies are regulated by carbon availability and soil pH along a mean annual temperature gradient," *Sci. Rep.*, 2026.
[3] Anapalli, S. S., et al., "Eddy covariance assessment of alternate wetting and drying floodwater management on rice methane emissions," *Heliyon*, 2023.
[4] Yang, T., et al., "Product type, rice variety, and agronomic measures determined the efficacy of enhanced-efficiency nitrogen fertilizer on the CH4 emission and rice yields in paddy fields," *Agronomy*, 2022.
[5] Gu, X., et al., "Effects of Water and Fertilizer Management Practices on Methane Emissions from Paddy Soils: Synthesis and Perspective," *Int. J. Environ. Res. Public Health*, 2022.
[6] Conrad, R., "Methane Production in Soil Environments—Anaerobic Biogeochemistry and Microbial Life between Flooding and Desiccation," *Microorganisms*, 2020.
[7] Nouchi, I., Mariko, S., and Aoki, K., "Mechanism of Methane Transport from the Rhizosphere to the Atmosphere through Rice Plants," *Plant Physiol.*, 1990.
[8] Oo, A. Z., Win, K. T., and Bellingrath-Kimura, S. D., "Within field spatial variation in methane emissions from lowland rice in Myanmar," *SpringerPlus*, 2015.
[9] Minamikawa, K., Tokida, T., Sudo, S., Padre, A., and Yagi, K., *Guidelines for Measuring CH4 and N2O Emissions from Rice Paddies by a Manually Operated Closed Chamber Method*, NIAES, 2015.
[10] Tokida, T., "Increasing measurement throughput of methane emission from rice paddies with a modified closed-chamber method," *J. Agric. Meteorol.*, 2021.
[11] Li, C., et al., "Low-Cost Detection of Methane Gas in Rice Cultivation by Gas Chromatography-Flame Ionization Detector," *Molecules*, 2022.
[12] Wassmann, R., et al., "Increasing sensitivity of methane emission measurements in rice through deployment of closed chambers at nighttime," *PLOS ONE*, 2018.
[13] Saunois, M., et al., "Global Methane Budget 2000–2020," *Earth Syst. Sci. Data*, 2025.
[14] Zhang, G., et al., "Fingerprint of rice paddies in spatial–temporal dynamics of atmospheric methane concentration in monsoon Asia," *Nat. Commun.*, 2020.
[15] Hu, Q., et al., "Global methane emissions from rice paddies: CH4MOD model development and application," *iScience*, 2024.
[16] IPCC, "Cropland," in *2019 Refinement to the 2006 IPCC Guidelines*, vol. 4, 2019.
[17] IPCC, "Agriculture, Forestry and Other Land Uses (AFOLU)," in *Climate Change 2022: Mitigation of Climate Change*, 2022.
[18] Gardner, J. W., and Bartlett, P. N., *Electronic Noses: Principles and Applications*, Oxford University Press, 1999.
[19] Pearce, T. C., Schiffman, S. S., Nagle, H. T., and Gardner, J. W., eds., *Handbook of Machine Olfaction*, Wiley, 2003.
[20] Shah, A., et al., "Characterising the methane gas and environmental response of the Figaro Taguchi Gas Sensor (TGS) 2611-E00," *Atmos. Meas. Tech.*, 2023.
[21] Furuta, D., et al., "Characterization of inexpensive metal oxide sensor performance for trace methane detection," *Atmos. Meas. Tech.*, 2022.
[22] Collier-Oxandale, A., et al., "Assessing a low-cost methane sensor quantification system for use in complex rural and urban environments," *Atmos. Meas. Tech.*, 2018.
[23] Bastviken, D., et al., "Technical note: Facilitating the use of low-cost methane (CH4) sensors in flux chambers," *Biogeosciences*, 2020.
[24] Kiplimo, E., et al., "Addressing Low-Cost Methane Sensor Calibration Shortcomings with Machine Learning," *Atmosphere*, 2024.
[25] Lakhmi, R., et al., "Linear and Non-Linear Modelling Methods for a Gas Sensor Array Developed for Process Control Applications," *Sensors*, 2024.
[26] Deisenroth, M. P., Faisal, A. A., and Ong, C. S., *Mathematics for Machine Learning*, Cambridge University Press, 2020.
[27] Madsen, B., *Statistics for Non-Statisticians*, Springer, 2011.
[28] Domènech-Gil, G., et al., "Electronic Nose for Improved Environmental Methane Monitoring," *Environ. Sci. Technol.*, 2024. (PDF ในคลัง: `direct/2024_Domenech-Gil_eNose_environmental_methane_monitoring.pdf`)
[29] Meijide, A., et al., "Seasonal trends and environmental controls of methane emissions in a rice paddy field in Northern Italy," *Biogeosciences*, 2011.

งานที่ Crossref ไม่ยืนยัน (Othman et al. DOI 10.37934/araset.60.5.3350) ไม่ปรากฏในรายการนี้
