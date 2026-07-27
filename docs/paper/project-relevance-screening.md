# การคัดกรองความเกี่ยวข้องของเอกสารต่อโครงการ eNose–ML สำหรับมีเทนในนาข้าว

วันที่คัดกรอง: 23 กรกฎาคม 2026  
ขอบเขต: เอกสารภายใต้ `docs/paper/` เท่านั้น ไม่ค้นหรือเติมข้อมูลจากเว็บ

> **อัปเดตโครงสร้าง (23 ก.ค. 2026):** ไฟล์ถูกย้ายไป `docs/paper/screened/{direct,supporting,excluded}/` และ `cite/` ในแต่ละหมวดแล้ว เส้นทาง `methane/`, `enose/`, `algorithm/`, `methods-*` ในรายการด้านล่างเป็นตำแหน่งตอนคัดกรอง — ดูตำแหน่งปัจจุบันที่ [`screened/README.md`](screened/README.md)
>
> **อัปเดต batch find-paper (23 ก.ค. 2026):** เพิ่ม D25–D30 และ S21–S26 จาก `candidates_2026-07-23/` (ดู §10)
>
> **อัปเดต reorg taxonomy (23 ก.ค. 2026):** จัดหมวดใหม่ตาม thesis-focused taxonomy — ย้าย agronomy/AWD/model ไป supporting และเลื่อน chamber–GC rice ขึ้น direct (ดู §11) · คลังไฟล์จริง: direct **22** / supporting **31** / excluded **2** bib (+ E01 stub ไม่มี bib) · master: [`screened/references.bib`](screened/references.bib) / [`screened/references.ris`](screened/references.ris) · รายงาน: [`citation-reorg-report-2026-07-23.md`](citation-reorg-report-2026-07-23.md)
## 1. คำถามและวิธีคัดกรอง

คำถามคัดกรองคือ เอกสารแต่ละเรื่องให้หลักฐานที่ใช้พัฒนาหรืออธิบายระบบ eNose/MOS ร่วมกับ machine learning เพื่อวัดความเข้มข้น CH₄ หรือประเมินการปล่อย CH₄ ในนาข้าว โดยมี static chamber–GC/GC-FID เป็นวิธีอ้างอิง ได้โดยตรงหรือไม่

ตรวจ corpus ทุกหมวดที่มี paper (`methane`, `methods-chamber-gc`, `methods-spectroscopy`, `methods-field`, `methods-remote`, `enose`, `algorithm`) รวม PDF, Markdown/text extract และ BibTeX/RIS sidecar แล้วรวมไฟล์ที่อ้างถึง DOI หรือชื่อเรื่องเดียวกันเป็น paper เดียว ไม่ถือ `README.md`, literature review ของโครงการ, script และไฟล์ใน `graphify-out/` เป็น paper ทั้งนี้ไม่พบไฟล์ paper จริงใน `archive/` ณ วันที่คัดกรอง

ช่วงปีไม่ได้ใช้เป็นเกณฑ์ตัดออก เพราะเป้าหมายคือคัดกรอง corpus ทั้งหมด ปีที่รายงานยึด metadata ภายใน PDF/BibTeX/RIS มากกว่าปีที่ฝังในชื่อไฟล์

### เกณฑ์คัดเข้าโดยตรง

เข้าอย่างน้อยหนึ่งข้อโดยมีความจำเพาะต่อโจทย์ ไม่ใช่เพียงพบคำว่า sensor หรือ ML:

1. ศึกษา CH₄ จาก rice paddy/rice field โดยตรง รวมการเกิด flux ปัจจัยควบคุม mitigation การวัดภาคสนาม หรือแบบจำลองที่ใช้ข้อมูลนาข้าว
2. ใช้ low-cost MOS/eNose เพื่อตรวจ วัด หรือสอบเทียบ CH₄ เชิงปริมาณ
3. ใช้ ML/regression เพื่อ calibration หรือทำนาย CH₄/ความเข้มข้นก๊าซจากสัญญาณ sensor array โดยมี CH₄ เป็น analyte ในการศึกษา
4. ให้ระเบียบวิธี chamber–GC หรือการวัด GHG จากดินเกษตร/นาข้าวที่ถ่ายโอนเป็น ground truth ของโครงการได้โดยตรง

### เกณฑ์คัดเข้าเป็นหลักฐานสนับสนุน

ให้หลักการหรือวิธีที่ถ่ายโอนได้ แต่ขาดอย่างน้อยหนึ่งองค์ประกอบสำคัญ เช่น ไม่ใช่นาข้าว ไม่ใช่ CH₄ ไม่ใช่ regression/quantification หรือเป็นรีวิวกว้างด้าน sensor, ML, chamber, spectroscopy หรือ deployment

### เกณฑ์คัดออก

คัดออกเมื่อหัวข้อจริงไม่เกี่ยวกับ CH₄/นาข้าว/eNose gas quantification, เป็นงานจำแนกก๊าซทั่วไปที่ไม่มีหลักฐานการถ่ายโอนสู่การประมาณ CH₄ เชิงปริมาณ, หรือ metadata ขัดแย้งจนไม่สามารถยืนยันว่าเป็น paper ที่ชื่อไฟล์กล่าวอ้าง

### ระดับหลักฐานที่ใช้

- **PDF ใน corpus**: มี full text อยู่ใน repository แต่การคัดกรองนี้ใช้ชื่อเรื่อง บทคัดย่อ/metadata และส่วนที่จำเป็น ไม่ใช่ critical appraisal เต็มบทความทุกเรื่อง
- **Structured extract/abstract**: อ่าน extract หรือ abstract ที่เก็บใน repository
- **Stub + metadata**: มี Markdown stub และ BibTeX/RIS; ยังไม่มี full text
- **Metadata-only**: พบเฉพาะ BibTeX ใน working tree จึงตัดสินได้ในระดับ title/metadata และสาระที่บันทึกไว้ใน literature review ภายในโครงการเท่านั้น

## 2. ผลรวม

- paper ไม่ซ้ำทั้งหมด (ตอนคัดกรองแรก): **48 เรื่อง** (ก่อน batch find-paper 2026-07-23)
- คัดเข้าโดยตรง: **24 เรื่อง** → หลัง batch: **30** (D01–D30) → **หลัง reorg taxonomy: 22 bib ใน `direct/`** (ดู §11; ID ที่ใช้จริงหลังย้ายรวม D04–D05, D10–D11, D15–D32)
- คัดเข้าเป็นหลักฐานสนับสนุน: **20 เรื่อง** → หลัง batch: **26** (S01–S26) → **หลัง reorg: 31 bib ใน `supporting/`** (รวม S27–S36 จาก demotion และคง S ที่ยังมีไฟล์)
- คัดออก: **4 เรื่อง** ในตารางคัดกรอง (E01–E04) แต่คลังไฟล์มี bib **2** + stub E01 (orphan E02/S09/S16/S17 ถูกลบก่อนหน้า)
- รวม sidecar ใน `screened/` หลัง reorg: **55** entries (ทุกตัวมี `.bib`+`.ris`) + E01 stub
## 3. คัดเข้าโดยตรง (24 เรื่อง)

### D01 — Effects of Water and Fertilizer Management Practices on Methane Emissions from Paddy Soils: Synthesis and Perspective

- ผู้แต่ง/ปี/DOI: Xinyun Gu, Shimei Weng, Yu’e Li, Xiaoqi Zhou; 2022; `10.3390/ijerph19127324`
- แหล่ง: `methane/2022_water_fertilizer_management_methane_paddy_synthesis.pdf`; `methane/cite/2022_water_fertilizer_management_methane_paddy_synthesis.bib`
- หลักฐาน: PDF ใน corpus
- เหตุผล: ตรงแกน CH₄–paddy โดยสังเคราะห์ผลของน้ำและปุ๋ยต่อ emission เหมาะสำหรับกำหนดตัวแปรรบกวนและช่วงเก็บตัวอย่าง แต่ไม่ได้พัฒนา eNose หรือ ML

### D02 — Eddy covariance assessment of alternate wetting and drying floodwater management on rice methane emissions

- ผู้แต่ง/ปี/DOI: Saseendran S. Anapalli, Srinivasa R. Pinnamaneni, Krishna N. Reddy, Pradeep Wagle, Amanda J. Ashworth; 2023; `10.1016/j.heliyon.2023.e14696`
- แหล่ง: `methane/2023_Anapalli_eddy_covariance_AWD_rice_methane.pdf`; `methane/cite/2023_Anapalli_eddy_covariance_AWD_rice_methane.bib`
- หลักฐาน: PDF/abstract metadata ใน corpus
- เหตุผล: วัด CH₄ ในนาข้าวภาคสนามและแสดง temporal/management variability ภายใต้ AWD เทียบ continuous flooding จึงช่วยออกแบบ validation แม้วิธีอ้างอิงเป็น eddy covariance ไม่ใช่ chamber–GC

### D03 — Multiyear methane and nitrous oxide emissions in different irrigation management under long-term continuous rice rotation in Arkansas

- ผู้แต่ง/ปี/DOI: S. Karki, M. A. A. Adviento-Borbe, B. R. K. Runkle, B. Moreno-García, M. Anders, M. L. Reba; 2023; `10.1002/jeq2.20444`
- แหล่ง: `methane/2023_multiyear_methane_N2O_AWD_Arkansas_rice.md`; `methane/cite/2023_multiyear_methane_N2O_AWD_Arkansas_rice.bib`
- หลักฐาน: Stub + metadata
- เหตุผล: ตรงกับ CH₄ ในนาข้าวและผลของ irrigation ในข้อมูลหลายปี สนับสนุนว่าการสอบเทียบ/ทดสอบต้องครอบคลุมความแปรผันระยะยาว แต่ยังไม่มี full text ใน corpus

### D04 — Synchronous monitoring agricultural water qualities and greenhouse gas emissions based on low-cost Internet of Things and intelligent algorithms

- ผู้แต่ง/ปี/DOI: Huazhan Zhang, Rui Ren, Xiang Gao, Housheng Wang, Wei Jiang, Xiaosan Jiang, Zhaofu Li, Jianjun Pan, Jinyang Wang, Songhan Wang, Yanfeng Ding, Yue Mu, Xuelei Wang, Jizeng Du, Wen-Tao Li, Zhengqin Xiong, Jianwen Zou; 2025; `10.1016/j.watres.2024.122663`
- แหล่ง: `methane/2024_IoT_lowcost_GHG_monitoring_paddy_regions.md`; `methane/cite/2024_IoT_lowcost_GHG_monitoring_paddy_regions.bib`
- หลักฐาน: Stub + metadata
- เหตุผล: เชื่อม low-cost IoT, agricultural monitoring, GHG และ intelligent algorithms โดยตรง จึงใกล้แกน deployment ของโครงการมาก แม้ stub ไม่เพียงพอยืนยันชนิดเซ็นเซอร์และรายละเอียด validation

### D05 — Paddy rice methane emissions, controlling factors, and mitigation potentials across Monsoon Asia

- ผู้แต่ง/ปี/DOI: Hong Zhou, Fulu Tao, Yi Chen, Lichang Yin, Yibo Li, Yicheng Wang, Chenfang Su; 2024; `10.1016/j.scitotenv.2024.173441`
- แหล่ง: `methane/2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review.md`; `methane/cite/2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review.bib`; `methane/cite/S0048969724035885.bib`
- หลักฐาน: Stub + abstract metadata
- เหตุผล: ใช้ ML วิเคราะห์ spatiotemporal CH₄ และปัจจัยควบคุมในนาข้าว Monsoon Asia โดยตรง เหมาะกับบริบทภูมิภาคและการเลือก covariates แต่ความละเอียดประมาณ 10 km ไม่ใช่ sensor calibration ระดับแปลง

### D06 — Agro-technologies for greenhouse gases mitigation in flooded rice fields for promoting climate smart agriculture

- ผู้แต่ง/ปี/DOI: Manas Protim Rajbonshi, Sudip Mitra, Pratap Bhattacharyya; 2024; `10.1016/j.envpol.2024.123973`
- แหล่ง: `methane/2024_agro_technologies_GHG_mitigation_flooded_rice_India.md`; `methane/cite/2024_agro_technologies_GHG_mitigation_flooded_rice_India.bib`
- หลักฐาน: Stub + metadata
- เหตุผล: ตรงบริบท flooded rice และ GHG mitigation จึงใช้กำหนดสภาวะทดลองและแหล่งความแปรผัน CH₄ ได้ แต่ไม่มี full text เพื่อยืนยันวิธีวัดใน corpus

### D07 — Promoting rice-upland crops systems to mitigate direct greenhouse gas emissions from intensive rice-based agriculture globally

- ผู้แต่ง/ปี/DOI: Hanxiong Song, Tong Li, Qiuan Zhu, Xiaolu Zhou, Changhui Peng; 2025; `10.21203/rs.3.rs-7887418/v1`
- แหล่ง: `methane/2024_promoting_rice_upland_crops_mitigate_CH4.pdf`; `methane/cite/2024_promoting_rice_upland_crops_mitigate_CH4.bib`
- หลักฐาน: PDF ใน corpus
- เหตุผล: ศึกษา GHG จากระบบ rice-based agriculture และ mitigation โดยตรง จึงเกี่ยวกับ target context; เป็น preprint ตาม DOI และไม่ได้เน้น eNose/ML measurement

### D08 — Effects of Rice Root Development and Rhizosphere Soil on Methane Emission in Paddy Fields

- ผู้แต่ง/ปี/DOI: Sheng Guan, Zhijuan Qi, Sirui Li, Sicheng Du, Dan Xu; 2024; `10.3390/plants13223223`
- แหล่ง: `methane/2024_rice_root_rhizosphere_methane_emission.pdf`; `methane/cite/2024_rice_root_rhizosphere_methane_emission.bib`
- หลักฐาน: PDF ใน corpus
- เหตุผล: ตรงกับกลไกและความแปรผัน CH₄ ใน paddy field ช่วยอธิบายว่าระยะพัฒนารากและ rhizosphere เปลี่ยนสัญญาณที่ระบบต้องวัด แม้ไม่เกี่ยวกับ sensor/ML โดยตรง

### D09 — Global methane emissions from rice paddies: CH4MOD model development and application

- ผู้แต่ง/ปี/DOI: Qiwen Hu, Jingxian Li, Hanzhi Xie, Yao Huang, Josep G. Canadell, Wenping Yuan, Jinyang Wang, Wen Zhang, Lijun Yu, Shihua Li, Xinqing Lu, Tingting Li, Zhangcai Qin; 2024; `10.1016/j.isci.2024.111237`
- แหล่ง: `methane/2025_CH4MOD_global_methane_emissions_rice_paddies.pdf`; `methane/cite/2025_CH4MOD_global_methane_emissions_rice_paddies.bib`; `methane/cite/S2589004224024623.bib`
- หลักฐาน: PDF/abstract metadata ใน corpus
- เหตุผล: เป็น process-based model เฉพาะ CH₄ ในนาข้าวและ validate ด้วย 986 flux observations จึงเป็น benchmark เชิง emission modelling แต่ไม่ได้ทำนายจาก MOS/eNose และทำงานคนละสเกล

### D10 — Machine learning revealed geochemical drivers of cadmium availability and methane emissions in hydrologically fluctuating paddy soils

- ผู้แต่ง/ปี/DOI: Qiuyue Chen, Mengmeng Yin, Chengjie Hong, Bowen Fan, Jialin Chi, Zongqiang Zhu, Kai Liu, Xiaoxia Zhou, Liping Fang, Fangbai Li; 2026; `10.1016/j.jhazmat.2026.141734`
- แหล่ง: `methane/2025_ML_geochemical_drivers_Cd_methane_paddy_soils.md`; `methane/cite/2025_ML_geochemical_drivers_Cd_methane_paddy_soils.bib`
- หลักฐาน: Stub + metadata
- เหตุผล: ใช้ ML กับ methane emissions ใน paddy soils โดยตรง จึงสนับสนุนการเลือก geochemical/environmental covariates แต่ยังยืนยัน dataset, validation และ metric ไม่ได้จาก stub

### D11 — Machine learning-driven method for in-situ high-frequency CH4 measurement in paddy fields based on water-soil-air factors

- ผู้แต่ง/ปี/DOI: Qinjing Zhang, Weijia Wen, Yanhua Zhuang, Liang Zhang, Limei Zhai, Sisi Li, Hongbin Liu, Yun Du; 2025; `10.1016/j.jenvman.2025.127132`
- แหล่ง: `methane/_zhang2025_extract.txt`; `methane/cite/2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze.bib`; `methane/cite/S0301479725031081.bib`
- หลักฐาน: Structured extract/abstract
- เหตุผล: ตรง use case มากที่สุดด้าน ML + in-situ high-frequency CH₄ ในนาข้าว โดย DTR จากปัจจัยดินให้ R² = 0.84; อย่างไรก็ดี input เป็น water–soil–air factors ไม่ใช่ MOS/eNose และไฟล์เดิมเคยชี้ไป PDF ผิดเรื่อง

### D12 — Methane emissions from rice paddies are regulated by carbon availability and soil pH along a mean annual temperature gradient

- ผู้แต่ง/ปี/DOI: Dai Yusong, Cao Jiawei, Li Huabin, Hu Jinli, Liu Guangcheng, Su Ronglin, Wu Xian, Wang Yan, Hu Ronggui; 2026; `10.1038/s41598-026-43940-8`
- แหล่ง: `methane/2025_methane_emissions_carbon_availability_soil_pH_gradient.pdf`; `methane/cite/2025_methane_emissions_carbon_availability_soil_pH_gradient.bib`; `methane/cite/10.1038_s41598-026-43940-8-citation.ris`
- หลักฐาน: PDF + metadata
- เหตุผล: ระบุ carbon availability, soil pH และ temperature gradient ที่ควบคุม CH₄ ในนาข้าว จึงสำคัญต่อ confounder selection และ external validation แต่ไม่ใช่งาน sensor calibration

### D13 — Product Type, Rice Variety, and Agronomic Measures Determined the Efficacy of Enhanced-Efficiency Nitrogen Fertilizer on the CH4 Emission and Rice Yields in Paddy Fields: A Meta-Analysis

- ผู้แต่ง/ปี/DOI: Tong Yang, Mengjie Wang, Xiaodan Wang, Chunchun Xu, Fuping Fang, Fengbo Li; 2022; `10.3390/agronomy12102240`
- แหล่ง: `methane/2025_product_type_rice_variety_agronomic_CH4_emissions.pdf`; `methane/cite/2025_product_type_rice_variety_agronomic_CH4_emissions.bib`
- หลักฐาน: PDF ใน corpus
- เหตุผล: ตรง CH₄–paddy และแสดง heterogeneity จากพันธุ์ข้าว/มาตรการเกษตร เหมาะกำหนด sampling strata; เป็น meta-analysis ไม่ใช่ measurement-system study

### D14 — Straw mulching combined with alternate wetting and drying reduces methane emissions in paddy fields

- ผู้แต่ง/ปี/DOI: Chuanhai Shu, Zhonglin Wang, Binbin Liu, Yue Huang, Yuanqing Shi, Hongkun Xie, Mingming Hu, Qingyue Cheng, Qin Liao, Na Li, Zongkui Chen, Yongjian Sun, Zhiyuan Yang, Jun Ma; 2026; `10.1016/j.jenvman.2026.130155`
- แหล่ง: `methane/2025_straw_mulching_AWD_reduces_methane_paddy.md`; `methane/cite/2025_straw_mulching_AWD_reduces_methane_paddy.bib`
- หลักฐาน: Stub + metadata
- เหตุผล: ตรงกับ CH₄ ในนาข้าวและผลของ AWD/วัสดุอินทรีย์ จึงเกี่ยวกับช่วง dynamic range ที่เครื่องมือควรตรวจจับ แต่ไม่มี full text ใน corpus

### D15 — A Portable Device for Methane Measurement Using a Low-Cost Semiconductor Sensor: Development, Calibration and Environmental Applications

- ผู้แต่ง/ปี/DOI: Leonardo Furst, Manuel Feliciano, Laercio Frare, Getúlio Igrejas; 2021; `10.3390/s21227456`
- แหล่ง: `enose/cite/2022_portable_lowcost_semiconductor_methane_sensor.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ตรงกับ low-cost semiconductor CH₄ measurement, calibration และ portable deployment จึงให้หลักฐานด้านเครื่องมือโดยตรง แม้ไม่ใช่ sensor array/ML และไม่มี full text ใน working tree

### D16 — Electronic Nose for Improved Environmental Methane Monitoring

- ผู้แต่ง/ปี/DOI: Guillem Domènech-Gil, Nguyen Thanh Duc, J. Jacob Wikner, Jens Eriksson, Sören Nilsson Påledal, Donatella Puglisi, David Bastviken; metadata ระบุ 2023 (ฉบับวารสาร volume 58 ใช้อ้างเป็น 2024 ในเอกสารโครงการ); `10.1021/acs.est.3c06945`
- แหล่ง: `enose/cite/2024_Domenech-Gil_eNose_environmental_methane_monitoring.bib`
- หลักฐาน: Metadata-only; มีรายละเอียดวิธี/ผลใน literature review ภายในโครงการ
- เหตุผล: เป็นหลักฐานตรงที่สุดด้าน eNose + environmental CH₄ + regression/calibration และการชดเชยสภาพแวดล้อม แต่บริบทและช่วงความเข้มข้นไม่ใช่ chamber gas จากนาข้าว

### D17 — Machine learning techniques to increase the performance of indirect methane quantification from a single, stationary sensor

- ผู้แต่ง/ปี/DOI: Robert S. Heltzel, Derek R. Johnson, Mohammed T. Zaki, Aron K. Gebreslase, Omar I. Abdul-Aziz; 2022; `10.1016/j.heliyon.2022.e11962`
- แหล่ง: `algorithm/cite/2022_ML_indirect_methane_quantification_single_sensor.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ตรงกับ ML เพื่อ methane quantification จาก low-cost stationary sensing จึงช่วยวาง baseline ของ regression แม้ไม่ใช่ eNose array หรือนาข้าว

### D18 — Application of Machine Learning for Calibrating Gas Sensors for Methane Emissions Monitoring

- ผู้แต่ง/ปี/DOI: Ballard Andrews, Aditi Chakrabarti, Mathieu Dauphin, Andrew Speck; 2023; `10.3390/s23249898`
- แหล่ง: `algorithm/cite/2023_Andrews_ML_calibrating_gas_sensors_methane_emissions.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ตรงกับบทบาท ML calibration สำหรับ methane emissions monitoring โดยเฉพาะ จึงเป็นฐานสำคัญของการชดเชย cross-sensitivity/drift และ validation

### D19 — Linear and Non-Linear Modelling Methods for a Gas Sensor Array Developed for Process Control Applications

- ผู้แต่ง/ปี/DOI: Riadh Lakhmi, Marc Fischer, Quentin Darves-Blanc, Rouba Alrammouz, Mathilde Rieu, Jean-Paul Viricelle; 2024; `10.3390/s24113499`
- แหล่ง: `algorithm/cite/2024_Lakhmi_linear_nonlinear_gas_sensor_array_CH4.bib`
- หลักฐาน: Metadata-only; corpus review ระบุว่าชุดก๊าซมี CH₄
- เหตุผล: เปรียบเทียบ linear/non-linear regression บน gas sensor array ที่มี CH₄ จึงตรงกับการตัดสินใจระหว่าง linear regression กับโมเดลซับซ้อนกว่า แต่ process-control gas mixtures ไม่ถ่ายโอนสู่นาข้าวโดยอัตโนมัติ

### D20 — Calibration of a Low-Cost Methane Sensor Using Machine Learning

- ผู้แต่ง/ปี/DOI: Hazel Louise Mitchell, Simon J. Cox, Hugh G. Lewis; 2024; `10.3390/s24041066`
- แหล่ง: `algorithm/cite/2024_Mitchell_Figaro_lowcost_methane_ML_calibration.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ตรงกับ Figaro/low-cost methane sensor และ ML calibration ในงานภาคสนาม จึงเป็นหลักฐานหลักด้าน hardware–model transfer แม้ไม่ใช่นาข้าวหรือ sensor array แบบโครงการ

### D21 — Methodology for Measuring Greenhouse Gas Emissions from Agricultural Soils Using Non-isotopic Techniques

- ผู้แต่ง/ปี/DOI: M. Zaman et al.; 2021; `10.1007/978-3-030-55396-8_2`
- แหล่ง: `methods-chamber-gc/cite/2021_Zaman_GHG_measurement_agricultural_soils_methodology.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เป็นระเบียบวิธีวัด GHG จากดินเกษตรโดยตรงและครอบคลุมแนว chamber/analytical reference ที่ใช้สร้าง ground truth ได้ จึงตรงแกน validation แม้ไม่ได้พัฒนา eNose

### D22 — Methodological progress in the measurement of agricultural greenhouse gases

- ผู้แต่ง/ปี/DOI: Nusrat Jahan Mumu, Jannatul Ferdous, Christoph Müller, Weixin Ding, Mohammad Zaman, Mohammad Mofizur Rahman Jahangir; 2024; `10.1080/17583004.2024.2366527`
- แหล่ง: `methods-chamber-gc/cite/2024_Mumu_methodological_progress_agricultural_GHG.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ทบทวนความก้าวหน้าของวิธีวัด agricultural GHG โดยตรง จึงใช้กำหนดข้อจำกัดและบทบาท chamber–GC เทียบเครื่องมือความถี่สูงได้ แต่รายละเอียด protocol ต้องอ่าน full text เพิ่ม

### D23 — Sensing and Analysis of Greenhouse Gas Emissions from Rice Fields to the Near Field Atmosphere

- ผู้แต่ง/ปี/DOI: Panneerselvam Rajasekar, James Arputha Vijaya Selvi; 2022; `10.3390/s22114141`
- แหล่ง: `methods-field/cite/2022_Rajasekar_GHG_sensing_rice_fields_near_field.bib`
- หลักฐาน: Metadata-only; corpus review บันทึกการใช้ chamber, MQ4 และ TGS2611
- เหตุผล: เป็นงานที่ตรงที่สุดด้าน low-cost MOS + chamber + rice field deployment แต่ใช้ manufacturer response/สูตรแทน eNose array และ ML regression

### D24 — Measurement approaches for greenhouse gas emissions from rice II: advanced technology for accelerating throughput

- ผู้แต่ง/ปี/DOI: Thi Bach Thuong Vo, Reiner Wassmann, Ryan R. Romasanta, Caesar Arloo R. Centeno, Mary Louise C. Mendoza, Georg Willibald, Ralf Kiese, Ando Mariot Radanielson; 2026; `10.3389/fagro.2025.1693620`
- แหล่ง: `methods-spectroscopy/cite/2022_Vo_TGA_vs_GC_methane_agricultural_soils.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ชื่อเรื่องจริงตรงกับการเพิ่ม throughput ของการวัด GHG จากข้าว จึงเกี่ยวกับ reference workflow และข้อจำกัดของ GC โดยตรง; ชื่อไฟล์ “2022_TGA_vs_GC” และปีไม่ตรง metadata จึงไม่ควรอ้างรายละเอียด TGA โดยไม่มี full text

## 4. คัดเข้าเป็นหลักฐานสนับสนุน (20 เรื่อง)

### S01 — Carbon Footprint Reduction from Closing Rice Yield Gaps

- ผู้แต่ง/ปี/DOI: Nguyen-Van-Hung, Nguyen Thi Ha-An, Grant Robert Singleton, Melanie Connor; 2023; `10.1007/978-3-031-37947-5_5`
- แหล่ง: `methane/2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.pdf`; `methane/cite/2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.bib`
- หลักฐาน: PDF ใน corpus
- เหตุผล: ให้บริบท carbon footprint และ mitigation ในระบบข้าว แต่ไม่ได้มุ่งวัด CH₄, sensor calibration หรือ ML regression โดยตรง

### S02 — A Comprehensive Review on Greenhouse Gas Emissions in Agriculture and Evolving Agricultural Practices for Climate Resilience

- ผู้แต่ง/ปี/DOI: Ashutosh Singh, Amit Kumar Pandey, Santhosh D T, Ganavi N R, Anjan Sarma, Chinmoy Deori, Juman Das, Shiva Kumar D; 2024; `10.9734/ijecc/2024/v14i54206`
- แหล่ง: `methane/2024_comprehensive_review_GHG_rice_paddies.pdf`; `methane/cite/2024_comprehensive_review_GHG_rice_paddies.bib`; `methane/cite/ris (4).ris`
- หลักฐาน: PDF/abstract metadata ใน corpus
- เหตุผล: เป็นรีวิว GHG ภาคเกษตรกว้าง แม้กล่าวถึง CH₄ จาก rice cultivation แต่ไม่ได้เจาะระบบตรวจวัดนาข้าว จึงเป็นเพียงฐานบริบท

### S03 — A Review of Greenhouse Gas Emissions from Agricultural Soil

- ผู้แต่ง/ปี/DOI: Sana Basheer, Xiuquan Wang, Aitazaz A. Farooque, Rana Ali Nawaz, Tianze Pang, Emmanuel Okine Neokye; 2024; `10.3390/su16114789`
- แหล่ง: `methane/_MISFILED_Basheer2024_GHG_agricultural_soil.pdf`
- หลักฐาน: Full text ตรวจแล้ว
- เหตุผล: มีหลักการ closed/static chamber, GC/infrared, auxiliary RH/pressure/temperature sensors และข้อจำกัดเชิงพื้นที่ที่ถ่ายโอนได้ แต่เป็นรีวิว agricultural soil GHG กว้าง ไม่ใช่ eNose–ML ในนาข้าว

### S04 — Development of Gas Sensor Array for Methane Reforming Process Monitoring

- ผู้แต่ง/ปี/DOI: Dominik Dobrzyniewski, Bartosz Szulczyński, Tomasz Dymerski, Jacek Gębicki; 2021; `10.3390/s21154983`
- แหล่ง: `enose/cite/2021_Dobrzyniewski_TGS_sensor_array_methane_reforming.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ให้หลักฐาน sensor-array response ในระบบที่เกี่ยวกับ methane แต่ analyte mixture และ process-control context ต่างจาก CH₄ emission ในนาข้าว

### S05 — Recent Progress in Smart Electronic Nose Technologies Enabled with Machine Learning Methods

- ผู้แต่ง/ปี/DOI: Zhenyi Ye, Yuan Liu, Qiliang Li; 2021; `10.3390/s21227620`
- แหล่ง: `enose/cite/2021_Ye_smart_eNose_machine_learning_review.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เป็นฐานทั่วไปของ eNose + ML ทั้ง classification และ quantitative analysis แต่ไม่ได้จำเพาะ CH₄ หรือนาข้าว

### S06 — An Outlook of Recent Advances in Chemiresistive Sensor-Based Electronic Nose Systems for Food Quality and Environmental Monitoring

- ผู้แต่ง/ปี/DOI: Alishba T. John, Krishnan Murugappan, David R. Nisbet, Antonio Tricoli; 2021; `10.3390/s21072271`
- แหล่ง: `enose/cite/2021_chemiresistive_eNose_food_environment_review.bib`
- หลักฐาน: Metadata-only
- เหตุผล: สนับสนุนสถาปัตยกรรม chemiresistive eNose และข้อจำกัดทั่วไป แต่บริบทส่วนใหญ่เป็น food/environmental monitoring และไม่ยืนยัน methane regression

### S07 — Application of Semiconductor Metal Oxide in Chemiresistive Methane Gas Sensor: Recent Developments and Future Perspectives

- ผู้แต่ง/ปี/DOI: Li Fu, Shixi You, Guangjun Li, Xingxing Li, Zengchang Fan; 2023; `10.3390/molecules28186710`
- แหล่ง: `enose/cite/2023_MOS_chemiresistive_methane_sensor_review.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เป็นฐานวัสดุและกลไก MOS สำหรับ CH₄ โดยตรง แต่ไม่ใช่ระบบ eNose deployment, ML calibration หรือนาข้าว

### S08 — Rapid Identification Method for CH4/CO/CH4-CO Gas Mixtures Based on Electronic Nose

- ผู้แต่ง/ปี/DOI: Jianxin Yin, Yongli Zhao, Zhi Peng, Fushuai Ba, Peng Peng, Xiaolong Liu, Qian Rong, Youmin Guo, Yafei Zhang; 2023; `10.3390/s23062975`
- แหล่ง: `enose/cite/2023_Yin_eNose_CH4_CO_mixed_gas_identification.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ใช้ eNose กับ CH₄ ใน gas mixture จึงช่วยเรื่อง cross-gas fingerprint แต่เป้าหมายเป็น identification/classification ไม่ใช่ regression หาความเข้มข้น

### S09 — Design of an E-Nose Detector for Contaminated Gas in Cow Farming Waste

- ผู้แต่ง/ปี/DOI: Andrew Setiawan Rusdianto, Winda Amilia, Laila Adhani Putri Malik; 2023; `10.46676/ij-fanres.v4i4.213`
- แหล่ง: `enose/cite/2024_Rusdianto_eNose_methane_gas_detection.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ให้ตัวอย่าง eNose ใน agricultural-waste field context ที่อาจถ่ายโอนด้าน deployment ได้ แต่ชื่อเรื่อง/metadata ไม่ยืนยัน methane quantification หรือ regression

### S10 — The Promise of Low-Cost Metal-Oxide Semiconductor Gas Sensors for Precision Agriculture

- ผู้แต่ง/ปี/DOI: Ali Ahmad, Sandra Sendra, Jaime Lloret, Jinhe Bai, Erin Rosskopf, Francesco Di Gioia; 2026; `10.1002/adsr.202500112`
- แหล่ง: `enose/cite/2026_Ahmad_MOS_sensors_precision_agriculture.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เชื่อม low-cost MOS กับ precision agriculture และข้อจำกัด deployment แต่เป็นรีวิวกว้างและไม่ได้จำเพาะ CH₄ ในนาข้าว

### S11 — A New Mixed-Gas-Detection Method Based on a Support Vector Machine Optimized by a Sparrow Search Algorithm

- ผู้แต่ง/ปี/DOI: Haitao Zhang, Yaozhen Han; 2022; `10.3390/s22228977`
- แหล่ง: `algorithm/cite/2022_SVM_sparrow_search_mixed_gas_concentration_prediction.bib`
- หลักฐาน: Metadata-only
- เหตุผล: สนับสนุน modelling ของ mixed-gas sensor response และอาจใช้เปรียบเทียบกับ regression ได้ แต่ metadata ไม่ยืนยัน CH₄, field transfer หรือนาข้าว

### S12 — E-Nose: Time–Frequency Attention Convolutional Neural Network for Gas Classification and Concentration Prediction

- ผู้แต่ง/ปี/DOI: Minglv Jiang, Na Li, Mingyong Li, Zhou Wang, Yuan Tian, Kaiyan Peng, Haoran Sheng, Haoyu Li, Qiang Li; 2024; `10.3390/s24134126`
- แหล่ง: `algorithm/cite/2024_Jiang_TFA-CNN_gas_classification_concentration_prediction.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เกี่ยวโดยตรงกับ time-series eNose และ concentration prediction แต่ไม่จำเพาะ CH₄ และความซับซ้อนของ deep learning อาจไม่เหมาะกับ dataset ขนาดเล็กของโครงการ

### S13 — Graph-Driven Models for Gas Mixture Identification and Concentration Estimation on Heterogeneous Sensor Array Signals

- ผู้แต่ง/ปี/รหัส: Ding Wang, Lei Wang, Huilin Yin, Guoqing Gu, Zhiping Lin, Wenwen Zhang; 2024; arXiv `2412.13891`; DOI: **ไม่พบข้อมูล**
- แหล่ง: `algorithm/cite/2024_Wang_graph_models_gas_mixture_concentration_estimation.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ให้แนวทาง concentration estimation จาก heterogeneous sensor arrays แต่เป็น benchmark/generic gas mixture และยังไม่เชื่อมกับ CH₄ ในนาข้าว

### S14 — A Review on Application of Machine Learning Techniques Coupled With E-Nose in Healthcare, Agriculture, and Allied Domains

- ผู้แต่ง/ปี/DOI: Samujjal Baruah, Dilwar Hussain Mazumder; 2025; `10.1109/tim.2025.3547517`
- แหล่ง: `algorithm/cite/2025_Baruah_ML_eNose_healthcare_agriculture_review.bib`
- หลักฐาน: Metadata-only
- เหตุผล: สังเคราะห์ ML + eNose ใน agriculture และช่วยวาง taxonomy ของโมเดล/validation แต่ไม่ได้จำเพาะ methane quantification หรือ rice field

### S15 — Quantification of Volatile Compounds in Mixtures Using a Single Thermally Modulated MOS Gas Sensor with PCA–ANN Data Processing

- ผู้แต่ง/ปี/DOI: Jolanta Wawrzyniak; 2025; `10.3390/s25226913`
- แหล่ง: `algorithm/cite/2025_PCA-ANN_single_MOS_sensor_quantification.bib`
- หลักฐาน: Metadata-only
- เหตุผล: แสดง quantitative regression จาก dynamic MOS signal ที่ถ่ายโอนแนวคิด feature extraction ได้ แต่ analytes เป็น volatile compounds ไม่ใช่ CH₄ และใช้ single thermally modulated sensor

### S16 — Electronic nose in gas sensing: from sensors to artificial intelligence – a review

- ผู้แต่ง/ปี/DOI: Dang Thi Thu Ha, Nguyen Dinh Van, Nguyen Duc Hoa; 2026; `10.1108/sr-01-2026-0051`
- แหล่ง: `algorithm/cite/2026_Ha_eNose_artificial_intelligence_review.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ให้ภาพรวม sensor-to-AI pipeline ของ eNose แต่เป็นหลักการทั่วไปและไม่ยืนยัน CH₄ regression หรือ field validation

### S17 — Review of the Methodologies for Measurement of Greenhouse Gas Emissions in Livestock Farming: Pig Farms as a Case of Study

- ผู้แต่ง/ปี/DOI: María José Cardador, Carolina Reyes-Palomo, Cipriano Díaz-Gaona, Lourdes Arce, Vicente Rodríguez-Estévez; 2020; `10.1080/10408347.2020.1855410`
- แหล่ง: `methods-chamber-gc/cite/2020_Cardador_GHG_measurement_methodologies_livestock_pig.bib`
- หลักฐาน: Metadata-only
- เหตุผล: วิธีวัด GHG และการเปรียบเทียบเครื่องมือถ่ายโอนได้บางส่วน แต่ livestock/pig facility มี source dynamics และ matrix ต่างจาก flooded rice soil

### S18 — Sensors and Methods for Measuring Greenhouse Gas Emissions from Different Components of Livestock Production Facilities

- ผู้แต่ง/ปี/DOI: Md Saidul Borhan, Mosammat Mustari Khanaum; 2022; `10.4236/gep.2022.1012014`
- แหล่ง: `methods-chamber-gc/cite/2022_Borhan_sensors_methods_GHG_livestock.bib`
- หลักฐาน: Metadata-only
- เหตุผล: สนับสนุนหลักการ sensor/chamber และข้อจำกัด GHG field measurement แต่บริบทปศุสัตว์ไม่ใช่นาข้าวและไม่ได้ยืนยัน eNose regression

### S19 — From Detection to Decision: A Systematic Literature Review of AI and Machine Learning Evolution in Methane Modelling

- ผู้แต่ง/ปี/DOI: Yang Xu, Abbas Yazdinejad, Hao Wang, Jude Dzevela Kong; 2025; `10.2139/ssrn.5218753`
- แหล่ง: `methods-remote/cite/2025_Xu_AI_ML_methane_rice_remote_sensing.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เป็นรีวิว AI/ML สำหรับ methane modelling จึงช่วยจัดกรอบโมเดล แต่ชื่อเรื่องจริงไม่ระบุ rice remote sensing ตามชื่อไฟล์ และเป็น SSRN work จึงไม่ใช่หลักฐานตรงของระบบ

### S20 — Environmental impacts and recent advancements in the sensing of methane: a review

- ผู้แต่ง/ปี/DOI: Lavista Tyagi, Rajni Devi, Shrestha Tyagi, Vinay Kumar, Kavita Sharma, Yogendra K. Gautam, Anuj Kumar, Saurabh Kapoor, Aman Bhardwaj, Ashwani Kumar; 2025; `10.1080/21622515.2025.2470448`
- แหล่ง: `methods-spectroscopy/cite/2025_Tyagi_methane_sensing_environmental_review.bib`
- หลักฐาน: Metadata-only
- เหตุผล: ใช้เปรียบเทียบเทคโนโลยีตรวจ CH₄ และวางข้อดีข้อจำกัดของ MOS กับวิธีอ้างอิงได้ แต่เป็นรีวิวกว้าง ไม่ใช่ eNose–ML ในนาข้าว

## 5. คัดออก (4 เรื่อง)

### E01 — ระเบียน `2024_diurnal_methane_emission_rice_paddy_ebullition`

- Metadata ที่พบจริง: Urs Hofmann Elizondo, Meike Vogt, Nina Bednaršek, Matthias Münnich, Nicolas Gruber; 2024; `10.1111/gcb.17345`; ชื่อจริง **The impact of aragonite saturation variability on shelled pteropods: An attribution study in the California Current System**
- แหล่ง: `methane/2024_diurnal_methane_emission_rice_paddy_ebullition.md`; `methane/cite/2024_diurnal_methane_emission_rice_paddy_ebullition.bib`
- หลักฐาน: Stub + metadata ที่ขัดแย้งกัน
- เหตุผล: DOI/ผู้แต่ง/ชื่อจริงเป็นงาน ocean acidification/pteropods ไม่เกี่ยวกับ CH₄ หรือนาข้าว ชื่อใน stub ว่า diurnal methane จึงไม่เพียงพอและไม่ควรใช้อ้างอิงจนกว่าจะแก้ metadata

### E02 — E-Nose-Driven Advancements in Ammonia Gas Detection: A Comprehensive Review from Traditional to Cutting-Edge Systems in Indoor to Outdoor Agriculture

- ผู้แต่ง/ปี/DOI: Ata Jahangir Moshayedi, Amir Sohail Khan, Jiandong Hu, Abdullah Nawaz, Jianxiong Zhu; 2023; `10.3390/su151511601`
- แหล่ง: `enose/cite/2023_Moshayedi_eNose_agriculture_sustainability.bib`
- หลักฐาน: Metadata-only
- เหตุผล: analyte คือ NH₃ และเป็นรีวิว eNose กว้างในเกษตร ไม่มีหลักฐาน methane quantification, rice-field transfer หรือ chamber–GC ที่จำเพาะพอ

### E03 — Enhanced Gas Classification in Electronic Nose Systems Using an SMOTE-Augmented Machine Learning Framework

- ผู้แต่ง/ปี/DOI: Minqiang Li, Chenxi Wu, Zhiyang Wang, Zhijian Wu, Wei Huang, Junru Chen, Kaibo Yu, Ting Wen, Hongbo Yin, Zhuqing Wang; 2026; `10.3390/s26020714`
- แหล่ง: `algorithm/cite/2024_enhanced_gas_classification_SMOTE_ML_eNose.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เป็น classification/imbalance framework ทั่วไป ไม่ใช่ concentration regression และ metadata ไม่ระบุ CH₄, paddy field หรือ transferable calibration

### E04 — Fast and robust mixed gas identification and recognition using tree-based machine learning and sensor array response

- ผู้แต่ง/ปี/DOI: Ghazala Ansari, Rupali Singh, Sachin Kumar, Naglaa F. Soliman; 2025; `10.1038/s41598-025-19063-x`
- แหล่ง: `algorithm/cite/2024_tree_ML_mixed_gas_identification_sensor_array.bib`
- หลักฐาน: Metadata-only
- เหตุผล: เน้น identification/recognition ของ mixed gas ไม่ใช่ regression และไม่มีหลักฐานจาก metadata ว่าศึกษา CH₄ หรือนาข้าว จึงไม่ผ่านเกณฑ์เพียงเพราะใช้ sensor array + ML

## 6. Paper สำคัญที่สุดต่อบททบทวนวรรณกรรม

1. **Zhang et al. (2025), D11** — หลักฐานใกล้ use case ที่สุดด้าน high-frequency ML estimation ใน paddy field; ใช้เป็นตัวเปรียบเทียบว่าโครงการเพิ่ม MOS/eNose signal เข้าไปจากงานที่ใช้ soil–water–air factors
2. **Rajasekar & Selvi (2022), D23** — สะพานเชื่อม low-cost TGS/MQ4, chamber และ rice-field deployment; ใช้ชี้ช่องว่างที่ยังไม่มี eNose array + ML regression
3. **Domènech-Gil et al., D16** — ฐานหลักของ environmental methane eNose, multivariate calibration และ environmental compensation; ใช้รองรับความเป็นไปได้ของ TGS + T/RH/P
4. **Andrews et al. (2023), D18** — ฐานตรงของ ML calibration สำหรับ methane emissions monitoring; ใช้อภิปราย cross-sensitivity, drift และ reference calibration
5. **Mitchell et al. (2024), D20** — หลักฐาน Figaro low-cost CH₄ sensor + ML calibration ในบริบทภาคสนาม; ใช้รองรับ hardware–model pipeline
6. **Zaman et al. (2021), D21** — ฐานระเบียบวิธี agricultural-soil GHG ground truth; ใช้กำหนด chamber sampling และการวิเคราะห์อ้างอิง
7. **Mumu et al. (2024), D22** — ใช้เปรียบเทียบ chamber/GC กับเทคโนโลยีวัดสมัยใหม่ และอธิบาย trade-off ความแม่นยำ–ต้นทุน–sampling frequency
8. **Lakhmi et al. (2024), D19** — ใช้รองรับการเปรียบเทียบ linear กับ non-linear regression บน sensor array ที่มี CH₄ โดยไม่สรุปว่าผลจะถ่ายโอนสู่นาข้าวทันที
9. **Zhang et al. (2025), D04** — หลักฐานด้าน low-cost IoT + intelligent algorithms + agricultural GHG monitoring; ต้องอ่าน full text เพิ่มก่อนอ้างรายละเอียด sensor และ validation
10. **Vo et al. (2026), D24** — หลักฐานด้านการเพิ่ม throughput ของวิธีวัด GHG จากข้าวและตำแหน่งของ reference analytics; ต้องแก้การเรียกชื่อ/ปีจากชื่อไฟล์ก่อนนำไป cite

## 7. สังเคราะห์และช่องว่างจาก corpus

หลักฐานใน corpus แบ่งเป็นสามสายที่เชื่อมกันได้แต่ยังไม่ปรากฏครบใน paper เดียว: (1) CH₄ flux และปัจจัยแวดล้อมในนาข้าว (2) low-cost MOS/eNose สำหรับ CH₄ พร้อม calibration และ (3) ML regression/concentration estimation จาก sensor signals งาน Zhang (D11) รวม ML + paddy CH₄ แต่ไม่ใช้ eNose; Rajasekar (D23) รวม MOS + chamber + rice field แต่ไม่ใช้ ML regression; Domènech-Gil, Andrews และ Mitchell (D16, D18, D20) รวม CH₄ sensor + ML/calibration แต่ไม่ใช่นาข้าวและไม่ได้ validate ด้วย chamber–GC-FID ในระบบเดียวกับโครงการ

ดังนั้น research gap ที่ corpus รองรับคือ **ยังไม่มีหลักฐานใน repository ของงาน end-to-end ที่ใช้ MOS eNose array + environmental covariates + ML regression เพื่อให้ค่า CH₄ concentration จาก static-chamber rice-field samples และ validate เทียบ GC/GC-FID ใน study เดียว** ข้อความนี้จำกัดเฉพาะ corpus ภายใน ไม่ใช่ข้อยืนยันว่าไม่มีงานดังกล่าวในวรรณกรรมโลก

ต้องแยก target ให้ชัด: paper sensor/ML หลายเรื่องทำนาย **concentration** ขณะที่ paper นาข้าวส่วนใหญ่รายงาน **flux** การเปลี่ยน concentration ใน chamber ไม่เท่ากับ flux จนกว่าจะมี chamber geometry, enclosure time, temperature/pressure correction และ slope calculation ที่เหมาะสม นอกจากนี้งาน classification (เช่น Yin) ไม่ใช่หลักฐานว่าระบบทำ regression เชิงปริมาณได้

corpus รองรับการใช้ baseline/response dynamics ในระดับหลักการของ eNose แต่จากไฟล์ paper ที่อ่านได้ครั้งนี้ **ยังไม่มีหลักฐานตรงเพียงพอให้ยืนยันว่า ΔV นิยามเดียวกับโครงการเป็น feature มาตรฐานหรือดีที่สุด** จึงควรอธิบาย ΔV เป็น operational feature ของโครงการและทดสอบเทียบกับ ratio, slope หรือ time-series features แทนการอ้างว่าเป็น consensus ของ literature

## 8. ข้อจำกัดและรายการที่ควรอ่านเพิ่ม

1. working tree มี PDF จริงเฉพาะกลุ่ม `methane/` บางเรื่อง; `enose/`, `algorithm/` และ `methods-*` ส่วนใหญ่พบเพียง `.bib` แม้ `README.md` จะระบุว่ามี PDF จำนวนมาก การตัดสินกลุ่มเหล่านี้จึงเป็น metadata-level screening
2. Stub ที่ควรหา full text ภายใน corpus ก่อนเขียน claim เชิงวิธีหรือผล ได้แก่ D03, D04, D05, D06, D10 และ D14 โดยเฉพาะ D04 ซึ่งชื่อบอกความใกล้เคียงสูงแต่ยังไม่ทราบ sensor/reference/validation
3. D11 มี structured extract ที่ดี แต่ไม่มี full text; ห้ามขยาย claim เกิน abstract/extract และต้องจำว่า PDF ที่เคยผูกกับชื่อ Zhang เป็น Basheer 2024
4. E01 เป็น citation collision ร้ายแรง: ชื่อไฟล์/ชื่อ stub กับ DOI และ paper จริงไม่ตรงกัน ต้องแก้หรือเอาออกจาก bibliography ก่อนใช้
5. ชื่อไฟล์กับ metadata ไม่ตรงปีหลายเรื่อง เช่น Furst (ไฟล์ 2022 แต่ metadata 2021), CH4MOD (ไฟล์ 2025 แต่ metadata 2024), product-type (ไฟล์ 2025 แต่ metadata 2022), Vo (ไฟล์ 2022 แต่ metadata 2026), และ algorithm สองเรื่องที่ชื่อไฟล์ 2024 แต่ metadata 2025/2026
6. ไม่มีการประเมินคุณภาพงานวิจัยหรือ risk of bias แบบเต็มรูปแบบ และไม่ได้ค้นแหล่งภายนอกตามขอบเขตที่กำหนด

## 9. ไฟล์ metadata รวมที่ใช้ตรวจสอบ

- `methane/cite/references.bib`
- `enose/cite/references.bib`
- `algorithm/cite/references.bib`
- `methods-chamber-gc/cite/references.bib`
- `methods-field/cite/references.bib`
- `methods-remote/cite/references.bib`
- `methods-spectroscopy/cite/references.bib`

ไฟล์รวมเหล่านี้ใช้ตรวจ title, authors, year และ DOI เท่าที่มี ส่วนเหตุผลการคัดกรองจำกัดตามระดับหลักฐานที่ระบุในแต่ละรายการ

## 10. Batch เพิ่มจาก find-paper (23 ก.ค. 2026)

แหล่ง: [`find-paper-report-2026-07-23.md`](find-paper-report-2026-07-23.md)  
metadata: doi.org / Crossref → BibTeX + RIS  
ตำแหน่งไฟล์: `screened/{direct,supporting}/` และ `cite/` — รายละเอียด path ใน [`citation-sync-report-2026-07-23.md`](citation-sync-report-2026-07-23.md)

### คัดเข้าโดยตรงเพิ่ม (D25–D30)

| ID | DOI | stem | เกณฑ์หลัก |
|----|-----|------|-----------|
| D25 | `10.3390/atmos15111313` | `2024_Kiplimo_ML_calibration_lowcost_methane_TGS` | MOS/TGS + ML calibration CH₄ |
| D26 | `10.5194/amt-17-2103-2024` | `2024_Furuta_lowcost_sensor_node_near_background_methane` | low-cost MOS node near-background CH₄ |
| D27 | `10.5194/amt-16-3391-2023` | `2023_Shah_TGS2611-E00_methane_environmental_response` | TGS2611-E00 response ต่อ CH₄/T/H₂O |
| D28 | `10.5194/amt-15-5117-2022` | `2022_Furuta_inexpensive_MOx_trace_methane` | เปรียบ TGS/MQ สำหรับ trace CH₄ |
| D29 | `10.5194/bg-17-3659-2020` | `2020_Bastviken_lowcost_CH4_sensors_flux_chambers` | low-cost MOS ใน flux chamber (ไม่ใช่นาข้าว) |
| D30 | `10.1039/d3ea00138e` | `2024_Shah_TGS2611-C00_landfill_methane` | TGS2611-C00 field mole fraction |

### หลักฐานสนับสนุนเพิ่ม (S21–S26)

| ID | DOI | stem | เหตุผลสนับสนุน |
|----|-----|------|----------------|
| S21 | `10.5194/amt-17-4257-2024` | `2024_RiveraMartinez_MOS_methane_leak_emission_MLP` | MOS+MLP แต่บริบท industrial leak |
| S22 | `10.3390/proceedings2024097079` | `2024_DomenechGil_efficient_methane_monitoring_Eurosensors` | companion conference ของ D16 |
| S23 | `10.3390/molecules27133968` | `2022_LowCost_GC-FID_methane_rice_cultivation` | GC-FID rice ground-truth lab |
| S24 | `10.2480/agrmet.d-20-00029` | `2021_Tokida_modified_closed_chamber_rice_methane` | chamber throughput นาข้าว |
| S25 | `10.11591/ijai.v14.i1.pp231-239` | `2025_Arif_NN_GHG_irrigated_paddy` | NN+paddy GHG; input ไม่ใช่ eNose |
| S26 | `10.18502/kls.v9i1.19350` | `2025_Jaya_IoT_GHG_soil_paddy` | IoT paddy CH₄; ไม่ใช่ MOS array+ML |

### ไม่คัดเข้าจาก batch นี้

- ซ้ำคลังเดิม (ไม่สร้าง cite ใหม่): Domènech-Gil EST `10.1021/acs.est.3c06945`, Mitchell `10.3390/s24041066`, Rajasekar `10.3390/s22114141`
- ไม่แนะนำ (ไม่มีไฟล์ใน candidates): Qian 2023 review; food-safety eNose review; MIRSA 2015 guideline

> **หมายเหตุ reorg:** S23→D31 และ S24→D32 (ดู §11) — ตารางด้านบนเป็นสถานะตอนคัดเข้า batch

## 11. Reorg taxonomy (23 ก.ค. 2026)

แหล่งรายละเอียด: [`citation-reorg-report-2026-07-23.md`](citation-reorg-report-2026-07-23.md) · ตำแหน่งไฟล์: [`screened/README.md`](screened/README.md)

### เกณฑ์ tier ใหม่ (thesis-focused)

| Tier | เกณฑ์ |
|------|--------|
| direct | eNose/MOS+CH₄, ML calibration CH₄, chamber–GC ในนา/เกษตร, field low-cost CH₄ ที่ validate ได้ |
| supporting | mitigation/AWD agronomy, process model, remote sensing, review ทั่วไป, companion proceedings |
| excluded | นอกประเด็น / stub ชน DOI / classification ที่ไม่ใช้ใน lit review หลัก |

### Mapping ID ที่เปลี่ยน

| ก่อน | หลัง | stem |
|------|------|------|
| S23 | D31 | `2022_LowCost_GC-FID_methane_rice_cultivation` |
| S24 | D32 | `2021_Tokida_modified_closed_chamber_rice_methane` |
| D01 | S27 | `2022_water_fertilizer_management_methane_paddy_synthesis` |
| D02 | S28 | `2023_Anapalli_eddy_covariance_AWD_rice_methane` |
| D03 | S29 | `2023_multiyear_methane_N2O_AWD_Arkansas_rice` |
| D06 | S30 | `2024_agro_technologies_GHG_mitigation_flooded_rice_India` |
| D07 | S31 | `2024_promoting_rice_upland_crops_mitigate_CH4` |
| D08 | S32 | `2024_rice_root_rhizosphere_methane_emission` |
| D09 | S33 | `2025_CH4MOD_global_methane_emissions_rice_paddies` |
| D12 | S34 | `2025_methane_emissions_carbon_availability_soil_pH_gradient` |
| D13 | S35 | `2025_product_type_rice_variety_agronomic_CH4_emissions` |
| D14 | S36 | `2025_straw_mulching_AWD_reduces_methane_paddy` |

ข้อความ §3–§5 ด้านบนยังใช้ ID เดิมตอนคัดกรอง — เมื่ออ้าง ID หลังวันที่นี้ให้ใช้ตาราง mapping นี้หรือ README

### ผลรวมคลังไฟล์หลัง reorg

- `screened/direct/`: 22 bib + 22 ris + 12 paper files
- `screened/supporting/`: 31 bib + 31 ris + 17 paper files
- `screened/excluded/`: 2 bib + 2 ris + 1 stub/paper
- Master: `screened/references.bib` / `screened/references.ris`
- DOI collision / key collision: **0**
