# รายงานการซิงก์ citation sidecar

วันที่ตรวจ: 23 กรกฎาคม 2026  
ขอบเขต: `docs/paper/` เท่านั้น ไม่ค้นหรือเพิ่ม paper จากเว็บ

## สรุป

- paper ปัจจุบันที่มีไฟล์ต้นทางจริง (PDF, Markdown stub หรือ text extract) แบบไม่ซ้ำ: **18 เรื่อง**
- paper ที่จับคู่กับ citation sidecar ที่ถูกต้องแล้ว: **17 เรื่อง**
- paper ที่ยังไม่มี citation ที่เชื่อถือได้: **1 เรื่อง** (`2024_diurnal_methane_emission_rice_paddy_ebullition.md`)
- citation sidecar ก่อนซิงก์: **62 ไฟล์**, 47 งานไม่ซ้ำ
- citation sidecar หลังซิงก์: **43 ไฟล์**, 43 งานไม่ซ้ำ
- สร้างใหม่: **1 ไฟล์**
- ลบ: **20 ไฟล์** (duplicate 15, orphan ที่ไม่ถูกอ้าง 4, collision 1)
- DOI ซ้ำหลังซิงก์: **0**
- citation key ซ้ำหลังซิงก์: **0**

## Mapping: paper ปัจจุบัน → citation sidecar

- `methane/2022_water_fertilizer_management_methane_paddy_synthesis.pdf` → `methane/cite/2022_water_fertilizer_management_methane_paddy_synthesis.bib` (`10.3390/ijerph19127324`)
- `methane/2023_Anapalli_eddy_covariance_AWD_rice_methane.pdf` → `methane/cite/2023_Anapalli_eddy_covariance_AWD_rice_methane.bib` (`10.1016/j.heliyon.2023.e14696`)
- `methane/2023_multiyear_methane_N2O_AWD_Arkansas_rice.md` → `methane/cite/2023_multiyear_methane_N2O_AWD_Arkansas_rice.bib` (`10.1002/jeq2.20444`)
- `methane/2024_IoT_lowcost_GHG_monitoring_paddy_regions.md` → `methane/cite/2024_IoT_lowcost_GHG_monitoring_paddy_regions.bib` (`10.1016/j.watres.2024.122663`)
- `methane/2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review.md` → `methane/cite/2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review.bib` (`10.1016/j.scitotenv.2024.173441`)
- `methane/2024_agro_technologies_GHG_mitigation_flooded_rice_India.md` → `methane/cite/2024_agro_technologies_GHG_mitigation_flooded_rice_India.bib` (`10.1016/j.envpol.2024.123973`)
- `methane/2024_promoting_rice_upland_crops_mitigate_CH4.pdf` → `methane/cite/2024_promoting_rice_upland_crops_mitigate_CH4.bib` (`10.21203/rs.3.rs-7887418/v1`)
- `methane/2024_rice_root_rhizosphere_methane_emission.pdf` → `methane/cite/2024_rice_root_rhizosphere_methane_emission.bib` (`10.3390/plants13223223`)
- `methane/2025_CH4MOD_global_methane_emissions_rice_paddies.pdf` → `methane/cite/2025_CH4MOD_global_methane_emissions_rice_paddies.bib` (`10.1016/j.isci.2024.111237`)
- `methane/2025_ML_geochemical_drivers_Cd_methane_paddy_soils.md` → `methane/cite/2025_ML_geochemical_drivers_Cd_methane_paddy_soils.bib` (`10.1016/j.jhazmat.2026.141734`)
- `methane/_zhang2025_extract.txt` → `methane/cite/2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze.bib` (`10.1016/j.jenvman.2025.127132`)
- `methane/2025_methane_emissions_carbon_availability_soil_pH_gradient.pdf` → `methane/cite/2025_methane_emissions_carbon_availability_soil_pH_gradient.bib` (`10.1038/s41598-026-43940-8`)
- `methane/2025_product_type_rice_variety_agronomic_CH4_emissions.pdf` → `methane/cite/2025_product_type_rice_variety_agronomic_CH4_emissions.bib` (`10.3390/agronomy12102240`)
- `methane/2025_straw_mulching_AWD_reduces_methane_paddy.md` → `methane/cite/2025_straw_mulching_AWD_reduces_methane_paddy.bib` (`10.1016/j.jenvman.2026.130155`)
- `methane/2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.pdf` → `methane/cite/2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.bib` (`10.1007/978-3-031-37947-5_5`)
- `methane/2024_comprehensive_review_GHG_rice_paddies.pdf` → `methane/cite/2024_comprehensive_review_GHG_rice_paddies.bib` (`10.9734/ijecc/2024/v14i54206`)
- `methane/_MISFILED_Basheer2024_GHG_agricultural_soil.pdf` → `methane/cite/2024_Basheer_GHG_agricultural_soil_review.bib` (`10.3390/su16114789`) — สร้างจาก citation block ใน PDF
- `methane/2024_diurnal_methane_emission_rice_paddy_ebullition.md` → **ยังไม่มี sidecar ที่เชื่อถือได้**; stub อ้าง DOI `10.1111/gcb.17345` แต่ DOI นี้เป็นงาน pteropod คนละเรื่อง

## Citation ที่สร้างหรือเติมข้อมูล

- สร้าง `methane/cite/2024_Basheer_GHG_agricultural_soil_review.bib` จาก metadata หน้าแรกของ PDF: ผู้แต่ง ชื่อเรื่อง วารสาร ปี volume article number และ DOI
- เติม `pages={14129}` ใน `methane/cite/2025_methane_emissions_carbon_availability_soil_pH_gradient.bib` จาก RIS ที่ตรง DOI และชื่อเรื่อง ก่อนลบ RIS ซ้ำ

## Duplicate ที่ลบ

รายการเหล่านี้มี DOI และ normalized title ตรงกับไฟล์ canonical ที่คงไว้:

- `methane/cite/S0048969724035885.bib` → Zhou 2024
- `methane/cite/S2589004224024623.bib` → CH4MOD
- `methane/cite/S2405844023019035.bib` → Anapalli 2023
- `methane/cite/ijerph-v19-i12_20260707.bib` → Gu et al. 2022
- `methane/cite/plants-v13-i22_20260707.bib` → Guan et al. 2024
- `methane/cite/S0301479725031081.bib` → Zhang et al. 2025
- `methane/cite/ris (4).ris` → Singh et al. 2024
- `methane/cite/10.1038_s41598-026-43940-8-citation.ris` → Dai et al. 2026
- aggregate ซ้ำ `cite/references.bib` จำนวน 7 ไฟล์ใน `methane`, `enose`, `algorithm`, `methods-chamber-gc`, `methods-field`, `methods-remote` และ `methods-spectroscopy`; ทุก entry ยังมี canonical sidecar แยกไฟล์อยู่

ไม่พบการใช้ citation key แบบ `\cite{...}` หรือ `[@key]` ใน `docs` จึงไม่มี key ที่ขาดจากการลบ duplicate เหล่านี้

## Orphan ที่ลบ

ยืนยันจาก DOI/ชื่อเรื่องว่าไม่มี PDF, stub, extract หรือ paper file ที่ตรงกันใน `docs/paper` และไม่พบการอ้างใน manuscript/literature-review นอกผลคัดกรอง:

- `enose/cite/2023_Moshayedi_eNose_agriculture_sustainability.bib`
- `enose/cite/2024_Rusdianto_eNose_methane_gas_detection.bib`
- `algorithm/cite/2026_Ha_eNose_artificial_intelligence_review.bib`
- `methods-chamber-gc/cite/2020_Cardador_GHG_measurement_methodologies_livestock_pig.bib`

## Collision ที่แก้

- ลบ `methane/cite/2024_diurnal_methane_emission_rice_paddy_ebullition.bib`
- เหตุผล: key/ชื่อไฟล์สื่อถึง methane ในนาข้าว แต่ metadata ภายในเป็น “The impact of aragonite saturation variability on shelled pteropods...” DOI `10.1111/gcb.17345`
- ไม่ใส่ DOI ใหม่ให้ stub เพราะ repository ไม่มีหลักฐานที่ตรวจสอบได้ว่าระเบียน methane นี้ควรเป็น paper ใด
- stub ต้นทางไม่ได้ถูกแก้ตามข้อจำกัดของงาน และต้องถือเป็น blocker ห้ามนำไป cite จนกว่าจะมี metadata ที่ยืนยันได้

## Orphan ที่ไม่กล้าลบ (blocker)

เหลือ **26 citation sidecar** ที่ไม่มี paper ต้นทางใน corpus แต่ผลงานยังถูกอ้างแบบหมายเลขหรือระบุในบรรณานุกรมของ `literature-review-4.2.md`, `literature-review-4.2-draft.md` หรือ `literature-review-enose-ml-methane-rice.md` การลบจะทำให้ reference mapping ขาด จึงคงไว้:

- `enose/cite/`: Dobrzyniewski 2021, Ye 2021, chemiresistive eNose review 2021, Furst 2021, MOS methane review 2023, Yin 2023, Domènech-Gil 2023/2024 และ Ahmad 2026 (8)
- `algorithm/cite/`: Heltzel 2022, Zhang & Han 2022, Andrews 2023, Jiang 2024, Lakhmi 2024, Mitchell 2024, Wang arXiv 2024, SMOTE classification, tree-based identification, Baruah 2025 และ Wawrzyniak 2025 (11)
- `methods-chamber-gc/cite/`: Zaman 2021, Borhan 2022 และ Mumu 2024 (3)
- `methods-field/cite/`: Rajasekar & Selvi 2022 (1)
- `methods-remote/cite/`: Xu et al. 2025 (1)
- `methods-spectroscopy/cite/`: Vo et al. 2026 และ Tyagi et al. 2025 (2)

การปลด blocker ต้องเลือกอย่างใดอย่างหนึ่งในงานรอบถัดไป: นำ paper ต้นทางที่ถูกต้องกลับเข้า corpus หรือแก้ manuscript/bibliography ที่อ้างงานเหล่านี้ก่อน แล้วจึงลบ sidecar

## Metadata ที่ยังไม่ครบ

ตรวจตามชนิด BibTeX โดยไม่แต่งข้อมูลที่หาไม่ได้จาก corpus:

- `2024_Wang_graph_models_gas_mixture_concentration_estimation.bib` ไม่มี DOI (มี arXiv `2412.13891`)
- `2024_promoting_rice_upland_crops_mitigate_CH4.bib` เป็น preprint DOI แต่ entry เดิมไม่มี journal/volume/issue/pages
- `2025_Xu_AI_ML_methane_rice_remote_sensing.bib` ไม่มี journal/volume/issue/pages
- article บางรายการไม่มี issue หรือ pages/article number ได้แก่ Baruah, tree-based identification, Ahmad, straw mulching, geochemical drivers, Zhang, IoT, Zhou, agro-technologies, Basheer, Vo และ Mumu

รายการข้างต้นไม่ถูกเติมจากการคาดเดา และไม่มีการค้น paper ใหม่จากเว็บ

## ผลตรวจหลังซิงก์

- BibTeX ที่เหลือ 43 ไฟล์มี entry envelope และวงเล็บปีกกาสมดุล
- citation key 43 key ไม่ซ้ำ
- DOI normalized 42 ค่าไม่ซ้ำ; 1 entry ไม่มี DOI (Wang arXiv)
- ไม่เหลือ RIS sidecar
- paper ปัจจุบัน 17/18 เรื่องมี citation ที่จับคู่ย้อนกลับได้
- ไม่พบ shared citation ที่ถูกลบโดยไม่มี canonical replacement

