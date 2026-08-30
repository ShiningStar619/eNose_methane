# Thematic index (`screened/`)

ไม่แยกโฟลเดอร์ย่อย — แท็กอยู่ที่นี่และใน `index.html`
กฎจับแท็กอยู่ใน `_build_reader.py` (`TAG_RULES`)
อันดับความเกี่ยวข้องอยู่ใน `RELEVANCE` ของไฟล์เดียวกัน

**คำถามจัดอันดับ:** จมูกอิเล็กทรอนิกส์ (MOS array) + ML regression ให้ค่าความเข้มข้น CH₄ (ppm) ในนาข้าว โดยใช้ static chamber–GC เป็นค่าอ้างอิง

เกณฑ์ (เรียงมาก→น้อย): (1) แตะหลายเสาของช่องว่างวิจัย นา + MOS/eNose + ML-quantify CH₄ + chamber–GC (2) แตะเสาเดียวอย่างจำเพาะ (3) บริบทนา/รีวิวที่ถ่ายโอนได้ (4) คนละสเกลหรือคนละ analyte (5) `excluded` = ไม่ใช้ในคลัง

อันดับไม่ใช่คะแนนคุณภาพวารสาร และไม่ได้เปิด full text ใหม่ทุกรายการ — ใช้ title/metadata + ผลการคัดกรอง 23 ก.ค. 2026 + ช่องว่างใน literature review 4.2.6

รวม 56 เรื่อง (direct 22 / supporting 31 / excluded 3)

| อันดับ | ความเกี่ยวข้อง | tier | stem | tags | เหตุผลสั้น |
|------:|:---------------|------|------|------|----------|
| 1 | สูงมาก | direct | `2022_Rajasekar_GHG_sensing_rice_fields_near_field` | `field-iot-portable` | MOS (MQ4/TGS2611) + chamber ในนา — ขาด eNose array+ML→ppm |
| 2 | สูงมาก | direct | `2024_Domenech-Gil_eNose_environmental_methane_monitoring` | `enose-mos-ch4` | eNose+ML quantify CH4 ภาคสนาม — ไม่ใช่นาข้าว |
| 3 | สูงมาก | direct | `2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze` | `methane-paddy` | ML in-situ CH4 ในนา — ไม่ใช้สัญญาณ MOS |
| 4 | สูงมาก | direct | `2024_Mitchell_Figaro_lowcost_methane_ML_calibration` | `ml-calibration-regression` | ML calibrate Figaro CH4 ภาคสนาม |
| 5 | สูงมาก | direct | `2024_Kiplimo_ML_calibration_lowcost_methane_TGS` | `ml-calibration-regression` | ML calibrate TGS CH4 |
| 6 | สูงมาก | direct | `2023_Andrews_ML_calibrating_gas_sensors_methane_emissions` | `ml-calibration-regression` | ML calibrate เซ็นเซอร์ก๊าซสำหรับ methane emissions |
| 7 | สูงมาก | direct | `2022_portable_lowcost_semiconductor_methane_sensor` | `enose-mos-ch4`, `field-iot-portable` | เซ็นเซอร์สารกึ่งตัวนำพกพา วัด/สอบเทียบ CH4 |
| 8 | สูงมาก | direct | `2022_Furuta_inexpensive_MOx_trace_methane` | `enose-mos-ch4` | MOS ต้นทุนต่ำ วัด CH4 ระดับต่ำ |
| 9 | สูงมาก | direct | `2024_Furuta_lowcost_sensor_node_near_background_methane` | `enose-mos-ch4` | โหนด MOS วัด CH4 ใกล้พื้นหลัง |
| 10 | สูงมาก | direct | `2024_Lakhmi_linear_nonlinear_gas_sensor_array_CH4` | `ml-calibration-regression` | linear vs nonlinear บน array มี CH4 — ใกล้โมเดลวิทยานิพนธ์ |
| 11 | สูงมาก | direct | `2022_ML_indirect_methane_quantification_single_sensor` | `ml-calibration-regression` | ML quantify CH4 จากเซ็นเซอร์เดี่ยว |
| 12 | สูงมาก | direct | `2021_Tokida_modified_closed_chamber_rice_methane` | `chamber-gc-methods` | closed chamber วัด CH4 นาข้าว (GT) |
| 13 | สูงมาก | direct | `2022_LowCost_GC-FID_methane_rice_cultivation` | `chamber-gc-methods` | GC-FID ต้นทุนต่ำในนาข้าว (GT) |
| 14 | สูง | direct | `2023_Shah_TGS2611-E00_methane_environmental_response` | `enose-mos-ch4` | TGS2611 ตอบสนอง CH4+สภาพแวดล้อม — เซ็นเซอร์เดียวกับโจทย์ |
| 15 | สูง | direct | `2020_Bastviken_lowcost_CH4_sensors_flux_chambers` | `chamber-gc-methods` | เซ็นเซอร์ CH4 ต้นทุนต่ำใน flux chamber |
| 16 | สูง | direct | `2021_Zaman_GHG_measurement_agricultural_soils_methodology` | `chamber-gc-methods` | ระเบียบ chamber–GC ดินเกษตร |
| 17 | สูง | direct | `2024_Mumu_methodological_progress_agricultural_GHG` | `chamber-gc-methods` | วิธีวัด GHG เกษตร รวมข้อจำกัด chamber–GC |
| 18 | สูง | direct | `2024_IoT_lowcost_GHG_monitoring_paddy_regions` | `field-iot-portable` | IoT+อัลกอริทึม เฝ้า GHG ในพื้นที่นา |
| 19 | สูง | direct | `2024_Shah_TGS2611-C00_landfill_methane` | `enose-mos-ch4` | TGS2611 วัด CH4 ภาคสนาม — หลุมฝังกลบ ไม่ใช่นา |
| 20 | สูง | direct | `2022_Vo_TGA_vs_GC_methane_agricultural_soils` | `chamber-gc-methods` | เปรียบเทียบวิธีวิเคราะห์ CH4 ดินเกษตร/นา กับ GC |
| 21 | สูง | direct | `2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review` | `methane-paddy`, `review` | ปัจจัยควบคุม CH4 นา Monsoon Asia (บริบทภูมิภาค) |
| 22 | สูง | supporting | `2023_MOS_chemiresistive_methane_sensor_review` | `enose-mos-ch4`, `review` | รีวิว MOS สำหรับ CH4 |
| 23 | ปานกลาง | supporting | `2024_DomenechGil_efficient_methane_monitoring_Eurosensors` | `enose-mos-ch4` | companion ของ eNose CH4 (proceedings) |
| 24 | ปานกลาง | supporting | `2024_RiveraMartinez_MOS_methane_leak_emission_MLP` | `enose-mos-ch4` | MOS+MLP ประมาณ CH4 — บริบทรั่วไหลอุตสาหกรรม |
| 25 | ปานกลาง | supporting | `2025_PCA-ANN_single_MOS_sensor_quantification` | `ml-calibration-regression` | quantify ด้วย MOS เดี่ยว+PCA-ANN — ไม่จำเพาะนา/CH4 นา |
| 26 | ปานกลาง | supporting | `2026_Ahmad_MOS_sensors_precision_agriculture` | `enose-mos-ch4` | MOS ในเกษตรแม่นยำ — ไม่ใช่ CH4 นาโดยตรง |
| 27 | ปานกลาง | supporting | `2023_Yin_eNose_CH4_CO_mixed_gas_identification` | `enose-mos-ch4` | eNose จำแนก CH4/CO ไม่ใช่ regression ppm ในนา |
| 28 | ปานกลาง | supporting | `2025_Jaya_IoT_GHG_soil_paddy` | `field-iot-portable` | IoT GHG ดินนา — รายละเอียดเซ็นเซอร์/validation บาง |
| 29 | ปานกลาง | direct | `2025_ML_geochemical_drivers_Cd_methane_paddy_soils` | `methane-paddy` | ML กับ CH4 ดินนา จากตัวแปรธรณีเคมี ไม่ใช่ MOS |
| 30 | ปานกลาง | supporting | `2021_Dobrzyniewski_TGS_sensor_array_methane_reforming` | `enose-mos-ch4` | TGS array กับมีเทน — กระบวนการ reforming อุตสาหกรรม |
| 31 | ปานกลาง | supporting | `2022_water_fertilizer_management_methane_paddy_synthesis` | `methane-paddy` | ปัจจัยน้ำ-ปุ๋ยต่อ CH4 นา (บริบท ไม่ใช่เครื่องมือ) |
| 32 | ปานกลาง | supporting | `2023_Anapalli_eddy_covariance_AWD_rice_methane` | `methane-paddy` | CH4 นา+AWD แต่ eddy covariance คนละวิธีกับโจทย์ |
| 33 | ปานกลาง | supporting | `2023_multiyear_methane_N2O_AWD_Arkansas_rice` | `methane-paddy` | CH4 นาหลายปี+AWD — บริบทความแปรผัน |
| 34 | ปานกลาง | supporting | `2024_rice_root_rhizosphere_methane_emission` | `methane-paddy` | กลไกราก/rhizosphere ต่อ CH4 |
| 35 | ปานกลาง | supporting | `2025_CH4MOD_global_methane_emissions_rice_paddies` | `methane-paddy` | โมเดลกระบวนการระดับโลก คนละสเกล |
| 36 | ปานกลาง | supporting | `2025_straw_mulching_AWD_reduces_methane_paddy` | `methane-paddy` | mitigation นา ไม่ใช่การวัดด้วย eNose |
| 37 | ปานกลาง | supporting | `2024_agro_technologies_GHG_mitigation_flooded_rice_India` | `methane-paddy` | mitigation นาท่วม |
| 38 | ปานกลาง | supporting | `2025_product_type_rice_variety_agronomic_CH4_emissions` | `methane-paddy` | พันธุ์ข้าว/เกษตรต่อ CH4 |
| 39 | ปานกลาง | supporting | `2025_methane_emissions_carbon_availability_soil_pH_gradient` | `methane-paddy` | ตัวแปรดินต่อ CH4 |
| 40 | น้อย | supporting | `2024_promoting_rice_upland_crops_mitigate_CH4` | `methane-paddy` | mitigation ระบบข้าว-ไร่ preprint |
| 41 | น้อย | supporting | `2024_comprehensive_review_GHG_rice_paddies` | `methane-paddy`, `review` | รีวิว GHG นากว้าง |
| 42 | น้อย | supporting | `2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation` | `methane-paddy`, `review` | คาร์บอนฟุตพริ้นท์ข้าว ไม่ใช่เซ็นเซอร์ |
| 43 | น้อย | supporting | `2021_Ye_smart_eNose_machine_learning_review` | `review` | รีวิว eNose+ML ทั่วไป |
| 44 | น้อย | supporting | `2025_Tyagi_methane_sensing_environmental_review` | `review` | รีวิวการตรวจ CH4 รวม spectroscopy ต้นทุนสูง |
| 45 | น้อย | supporting | `2025_Arif_NN_GHG_irrigated_paddy` | `ml-calibration-regression` | NN ประมาณ GHG นาชลประทาน — ไม่ใช่สัญญาณ MOS |
| 46 | น้อย | supporting | `2024_Basheer_GHG_agricultural_soil_review` | `methane-paddy`, `review` | รีวิว GHG ดินเกษตรกว้าง |
| 47 | น้อย | supporting | `2025_Baruah_ML_eNose_healthcare_agriculture_review` | `review` | รีวิว eNose+ML สุขภาพ/เกษตร ไม่จำเพาะ CH4 นา |
| 48 | น้อย | supporting | `2021_chemiresistive_eNose_food_environment_review` | `enose-mos-ch4`, `review` | รีวิว eNose อาหาร/สิ่งแวดล้อม |
| 49 | น้อย | supporting | `2025_Xu_AI_ML_methane_rice_remote_sensing` | `remote-sensing` | remote sensing+ML ระดับภูมิภาค ไม่ถึงรายแปลง |
| 50 | น้อย | supporting | `2024_Wang_graph_models_gas_mixture_concentration_estimation` | `ml-calibration-regression` | GNN ก๊าซผสม — ถ่ายโอนวิธี ไม่ใช่ CH4 นา |
| 51 | น้อย | supporting | `2024_Jiang_TFA-CNN_gas_classification_concentration_prediction` | `ml-calibration-regression` | deep learning จำแนก/ความเข้มข้นก๊าซทั่วไป |
| 52 | น้อย | supporting | `2022_SVM_sparrow_search_mixed_gas_concentration_prediction` | `gas-ml-general` | SVM ก๊าซผสม ไม่จำเพาะ CH4 นา |
| 53 | น้อย | supporting | `2022_Borhan_sensors_methods_GHG_livestock` | `livestock-ghg` | วิธีวัด GHG ปศุสัตว์ คนละระบบผลิต |
| 54 | ไม่เกี่ยวข้อง | excluded | `2024_diurnal_methane_emission_rice_paddy_ebullition` | `methane-paddy` | excluded: stub ชน DOI / metadata ใช้ไม่ได้ |
| 55 | ไม่เกี่ยวข้อง | excluded | `2024_tree_ML_mixed_gas_identification_sensor_array` | `gas-ml-general` | excluded: จำแนกก๊าซผสม ไม่มี regression CH4 |
| 56 | ไม่เกี่ยวข้อง | excluded | `2024_enhanced_gas_classification_SMOTE_ML_eNose` | `gas-ml-general` | excluded: classification eNose ไม่ใช่ quantify CH4 นา |
