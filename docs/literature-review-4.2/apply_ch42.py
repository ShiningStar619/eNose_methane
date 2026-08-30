#!/usr/bin/env python3
"""Patch Proposal draft 12.docx: replace 4.2, fix 4.1 share, append refs [32+]."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / "docs" / "draft" / "Proposal draft 12.docx"
FIG = ROOT / "docs" / "draft" / "figures" / "ch42"
HEAD = "/body/p[@paraId=45556683]"
PCT = "/body/p[@paraId=6D89206C]"
LAST_REF = "/body/p[@paraId=481B4E2E]"

REMOVE = [
    "784A8F32", "5F6468AC", "2A1083E6", "56A0DA3B", "73E0F4CE", "181C67D8",
    "14C87741", "6993AB6A", "6123E131", "3882ECEB", "11C7BE3A", "36D97C28",
    "507CD024", "5F49C51A", "2C1B4FFC", "2ED852B6", "3BE9D3A1", "14689438",
    "0B0ADBD3", "3A9FD8F6", "21532EC2", "0F3596B4", "15E34325", "4A93AE6B",
    "1E971FC1", "26AA03A2",
]

BODY = [
    "ส่วนนี้ทบทวนงานวิจัยตามลำดับเดียวกับที่มาของปัญหา เริ่มจากสาเหตุที่นาข้าวน้ำขังปล่อยก๊าซมีเทน และเหตุที่ต้องวัดในแปลง จากนั้นเป็นวิธีวัดมาตรฐานด้วยกล่องเก็บตัวอย่างร่วมกับ GC วิธีวัดด้วยแสงและดาวเทียม และงานจมูกอิเล็กทรอนิกส์หรือเซ็นเซอร์โลหะออกไซด์ร่วมกับการเรียนรู้ของเครื่อง ท้ายส่วนนี้สรุปว่าวิทยานิพนธ์นี้ต่างจากงานก่อนหน้าตรงจุดใด",
    "H|4.2.1 การปล่อยก๊าซมีเทนจากนาข้าวน้ำขังและการวัดระดับแปลง",
    "Conrad อธิบายว่าการย่อยสลายอินทรียวัตถุในดินที่ขาดออกซิเจนนำไปสู่การสร้าง CH₄ และดินนาข้าวตามฤดูกาลเป็นระบบที่สลับน้ำขังกับช่วงระบายน้ำ [34] Nouchi และคณะศึกษาการขนส่ง CH₄ จากไรโซสเฟียร์ผ่านต้นข้าว [55] ตามงบประมาณมีเทนโลก การปล่อยจากนาข้าวในช่วงทศวรรษ 2010–2019 ประมาณ 32 [25–37] Tg CH₄ yr⁻¹ หรือราวร้อยละ 9 ของการปล่อย CH₄ มานุษย์ทั้งโลก [32] IPCC AR6 ระบุว่าเอเชียรับผิดชอบราวร้อยละ 89 ของการปล่อยจากการปลูกข้าว และในเอเชียตะวันออกเฉียงใต้การปลูกข้าวเป็นแหล่ง CH₄ เกษตรหลักร่วมกับการหมักในกระเพาะสัตว์ (enteric fermentation) [33] Nguyen และคณะให้บริบทการจัดการนา [4] Zhou และคณะทบทวนการปล่อย CH₄ จากนาข้าวในมรสุมเอเชีย [13] ในช่วงน้ำขัง CH₄ ออกสู่บรรยากาศผ่านต้นข้าวเป็นหลัก ขณะที่ช่วงระบายน้ำก๊าซแลกเปลี่ยนจากผิวดินโดยตรง การวัดระดับแปลงจึงต้องครอบทั้งต้นข้าวและสภาพน้ำตามจริง ไม่ใช่ค่าเฉลี่ยภูมิภาคอย่างเดียว [36]",
    "IMG|fig01_minamikawa_CH4_pathways.png|เส้นทางปล่อย CH4 ในนาช่วงน้ำขังและช่วงระบายน้ำ จาก Minamikawa et al. 2015 Figure 6.4|12.0cm|5.5cm",
    "C|รูปที่ 1: เส้นทางปล่อย CH₄ และ N₂O ในช่วงน้ำขังและช่วงระบายน้ำ (ดัดแปลงจาก Minamikawa et al., 2015, Figure 6.4)",
    "Oo และคณะวัด CH₄ หลายจุดในนาข้าวที่เมียนมา พบค่าเฉลี่ยตามตำแหน่ง 8.7–26.6 mg m⁻² h⁻¹ และจุดปล่อยสูงกว่าจุดอื่นประมาณ 2–2.5 เท่า [35] เส้นโค้งฟลักซ์ของจุดทางน้ำเข้า กลางแปลง และทางน้ำออกไม่ซ้อนกันตลอดฤดูปลูก ค่าจากจุดเดียวจึงไม่แทนทั้งแปลง ซึ่งสอดคล้องกับข้อที่ 4.1 ว่าต้องมีข้อมูลระดับแปลง [35]",
    "IMG|fig02_oo_within_field_flux.png|ฟลักซ์ CH4 ตามตำแหน่งในแปลงนา จาก Oo et al. 2015 Figure 5|12.0cm|8.2cm",
    "C|รูปที่ 2: อัตราการปล่อยก๊าซมีเทนตามตำแหน่งทางน้ำเข้า กลางแปลง และทางน้ำออก ในนาข้าวสองแปลงที่เมียนมา (ดัดแปลงจาก Oo et al., SpringerPlus, 2015, Figure 5; doi: 10.1186/s40064-015-0901-2)",
    "H|4.2.2 วิธีการวัดแบบมาตรฐาน: static chamber ร่วมกับ GC",
    "Zaman และคณะรวบรวมวิธีวัดก๊าซเรือนกระจกจากดินเกษตร โดยระบุว่า closed chamber ใช้กันอย่างกว้างขวางและการวิเคราะห์เดิมใช้ GC [6] Mumu และคณะทบทวนความก้าวหน้าของวิธีวัดก๊าซเรือนกระจกจากระบบเกษตร [7] Minamikawa และคณะจัดคู่มือ closed chamber แบบใช้มือสำหรับนาข้าวภายใต้โครงการ MIRSA [36] IPCC 2019 Refinement เล่ม 4 บทที่ 5 มีสมการ CH₄ จาก rice cultivation สำหรับสินค้าคงคลังประเทศ ไม่ใช่โปรโตคอลความเข้มข้นรายแปลง [37] Tokida ปรับ closed chamber ในนาเพื่อเพิ่มจำนวนจุดวัด [47] Li และคณะรายงาน GC-FID สำหรับ CH₄ ในนาข้าว [48] Mazengo และคณะสรุปขั้นตอนครอบห้อง เก็บ vial แล้ววิเคราะห์ด้วย GC [39] เมื่อครอบห้อง ความเข้มข้น CH₄ และความชื้นเพิ่มขึ้นพร้อมกัน และสัญญาณเซ็นเซอร์ตามวงจรเดียวกัน การใช้เซ็นเซอร์ต้นทุนต่ำในห้องเก็บตัวอย่างจึงต้องวัดความชื้นและอุณหภูมิพร้อมกัน [49]",
    "IMG|fig03_bastviken_chamber_humidity.png|ความเข้มข้น CH4 สัญญาณเซ็นเซอร์ และความชื้นใน flux chamber จาก Bastviken et al. 2020 Figure 3|10.5cm|8.8cm",
    "C|รูปที่ 3: วัฏจักรเปิด–ปิด chamber ความเข้มข้น CH₄ สัญญาณเซ็นเซอร์ และความชื้น (ดัดแปลงจาก Bastviken et al., Biogeosciences, 2020, Figure 3; doi: 10.5194/bg-17-3659-2020)",
    "Wassmann และคณะรายงานจากนาข้าวว่าค่ากลางคืน 12 ชั่วโมงสัมพันธ์กับคาบ 24 ชั่วโมงที่ R² = 0.8419 [38] Vo และคณะประเมินว่าฉันทามติเรื่องฟลักซ์นาข้าวยังอาศัยการเก็บตัวอย่างด้วยห้องแบบมือ แม้มีข้อจำกัดเรื่องสภาพอากาศจุลภาคในหัวห้องและความถี่ต่อวัน [40]",
    "H|4.2.3 วิธีอื่นเพื่อตัดทาง: spectroscopy และ remote sensing",
    "Tyagi และคณะทบทวนเทคโนโลยีตรวจ CH₄ รวมสเปกโทรสโกปี [8] Vo และคณะเทียบ manual chamber–GC กับเครื่องวิเคราะห์ก๊าซแบบเลเซอร์ (trace gas analyzer) ทั้งแบบพกพาและแบบหลายวาล์วในนาที่สถาบันวิจัยข้าวนานาชาติ (IRRI) [21] GC ต้องเก็บ vial ส่งห้องปฏิบัติการ ขณะที่เครื่องวิเคราะห์แบบเลเซอร์วัดที่แปลงได้แต่ยังเป็นเครื่องมือราคาสูง ผลการทดลองพบว่าปัจจัยวิธีวัดไม่มีนัยสำคัญ (p = 0.47) ความต่างสูงสุด 12.62 mg m⁻² d⁻¹ ระบบหลายวาล์วครอบได้มากกว่า 110 แปลงต่อวัน เทียบกับราว 48 แปลงต่อวันของ GC แบบมือที่ครอบ 30 นาที ขณะที่เครื่องวิเคราะห์แบบเลเซอร์ใช้หน้าต่าง 4 นาที [21] งานนี้แสดงว่า GC ไม่ใช่เครื่องมือเดียวที่วัดในนาได้ แต่ยังไม่ตัดประเด็นต้นทุนต่อจุดวัดเมื่อเทียบกับอาเรย์ MOS",
    "IMG|fig04_vo_TGA_vs_GC_schematic.png|แผนผังเปรียบเทียบ GC แบบเก็บ vial กับ TGA พกพาและระบบ multi-valve จาก Vo et al. 2026 Figure 1|12.0cm|16.0cm",
    "C|รูปที่ 4: การถ่ายตัวอย่างจาก chamber ไป GC เทียบกับ TGA พกพาและระบบ multi-valve (ดัดแปลงจาก Vo et al., Front. Agron., 2026, Figure 1; doi: 10.3389/fagro.2025.1693620)",
    "Zhang และคณะเชื่อมพื้นที่นากับความเข้มข้น CH₄ ในบรรยากาศ (XCH₄) ในมรสุมเอเชีย ซึ่งคิดเป็นราวร้อยละ 87 ของพื้นที่นาโลกตามบทคัดย่อ และสรุปว่าแนวโน้มพื้นที่นาตั้งแต่ปี 2007 ไม่ใช่ตัวขับหลักของการเพิ่มขึ้นของ XCH₄ [41] Chen และคณะสร้างสินค้าคงคลังจากข้อมูลน้ำท่วม Landsat ในระดับกริด ไม่ใช่ความเข้มข้นรายแปลง [54] Liang และคณะผกผันข้อมูล TROPOMI ที่มณฑลเฮยหลงเจียงได้ 0.85 (0.69–1.03) Tg a⁻¹ สำหรับปี 2021 [42] สเกลดาวเทียมจึงตอบคำถามระดับภูมิภาค ไม่ใช่การติดตามในแปลงเดียวตามที่ 4.1 กำหนด",
    "H|4.2.4 eNose และ MOS ร่วมกับการเรียนรู้ของเครื่อง สำหรับประเมินความเข้มข้น CH₄",
    "Rajasekar และ Selvi ติดตั้งห้องเก็บตัวอย่างอัตโนมัติพร้อมเซ็นเซอร์ MQ4 และ TGS2611 ในนาข้าวที่อินเดีย และแปลงค่าเป็น ppm ด้วยสูตรผู้ผลิต Gas in PPM = pow(RS/R0, −2.95) × 1000 ไม่ใช่แบบจำลองการเรียนรู้จากอาเรย์หลายตัว [5] ระบบมีเซ็นเซอร์ MOS และห้องเก็บตัวอย่างในนาจริง แต่ประมาณค่าทีละหน่วยเซ็นเซอร์ตามสูตรผู้ผลิต ไม่ใช่ eNose ที่รวมเวกเตอร์หลายช่องแล้วถดถอยเป็น ppm [5]",
    "IMG|fig05_rajasekar_GAQU_rice.png|ระบบ chamber อัตโนมัติและหน่วยประมาณค่าก๊าซในนาข้าว จาก Rajasekar และ Selvi 2022 Figure 3|12.0cm|7.4cm",
    "C|รูปที่ 5: ระบบ chamber อัตโนมัติพร้อมหน่วยเซ็นเซอร์ CH₄ CO₂ และ N₂O ในนาข้าว (ดัดแปลงจาก Rajasekar และ Selvi, Sensors, 2022, Figure 3; doi: 10.3390/s22114141)",
    "Domènech-Gil และคณะใช้ TGS2611 ร่วมกับเซ็นเซอร์อุณหภูมิ ความชื้น และความดันในแบบจำลองการถดถอยกำลังสองน้อยที่สุดบางส่วน (PLSR) เพื่อชดเชยผลของสิ่งแวดล้อม และรายงานข้อผิดพลาดต่ำสุด 33 ppb กับค่า R² สูงสุด 0.91 สำหรับการวัด ณ จุดติดตั้งที่ความเข้มข้นบรรยากาศ [10] โมเดลที่รวมสัญญาณ MOS กับอุณหภูมิและความชื้นติดตาม CH₄ ได้ในภาคสนาม แต่บริบทเป็นสวนและระบบบำบัด ไม่ใช่แปลงนา และช่วงความเข้มข้นส่วนใหญ่ต่ำกว่าขอบเขตข้อเสนอนี้ที่ 5–100 ppm [10]",
    "IMG|fig06_domenech_PLSR_field.png|ผล PLSR เทียบค่าอ้างอิงในภาคสนาม จาก Domenech-Gil et al. 2024 Figure 5|12.0cm|12.4cm",
    "C|รูปที่ 6: ผลสอบเทียบ eNose กับ PLSR ต่อค่าอ้างอิงในพื้นที่ชุ่มน้ำ ห้องสลัดจ์ กองสลัดจ์ และสวน (ดัดแปลงจาก Domènech-Gil et al., Environ. Sci. Technol., 2024, Figure 5; doi: 10.1021/acs.est.3c06945)",
    "Eugster และ Kling แสดงว่า TGS2600 ไวต่ออุณหภูมิและความชื้นสัมพัทธ์ตามข้อกำหนดของผู้ผลิต จึงต้องชดเชยก่อนเทียบกับเครื่องวิเคราะห์อ้างอิง [43] อัตราส่วนความต้านทาน Rs/R0 ลดเมื่ออุณหภูมิหรือความชื้นสูงขึ้นแม้ความเข้มข้น CH₄ คงที่ การสอบเทียบด้วย CH₄ อย่างเดียวในห้องปฏิบัติการจึงไม่เพียงพอสำหรับแปลงนาที่ร้อนชื้น [43]",
    "IMG|fig07_eugster_TGS2600_TH.png|ความไวของ TGS2600 ต่อก๊าซและต่ออุณหภูมิความชื้น จาก Eugster และ Kling 2012 Figure 1|12.0cm|6.8cm",
    "C|รูปที่ 7: การตอบสนองของ Figaro TGS2600 ต่อความเข้มข้นก๊าซ (ก) และต่ออุณหภูมิกับความชื้นสัมพัทธ์ (ข) (ดัดแปลงจาก Eugster และ Kling, Atmos. Meas. Tech., 2012, Figure 1; doi: 10.5194/amt-5-1925-2012)",
    "Jørgensen และคณะใช้ TGS2611-E00 เทียบกับสเปกโทรสโกปีแบบโพรงสะท้อน (CRDS) ในช่วงประมาณ 2–100 ppm และรายงาน RMSE ทั้งช่วงสอบเทียบภาคสนาม 1.69 ppm [44] Collier-Oxandale และคณะแปลงสัญญาณ TGS2600 เป็น ppm ในสภาพแวดล้อมชนบทและเมือง [45] Rivera Martinez และคณะฝึกแบบจำลองจากความต้านทาน TGS เพื่อประมาณ CH₄ ใกล้พื้นหลัง โดยเป้าความแม่นยำ 0.1–0.2 ppm และพบว่าความไวต่อไอน้ำจากโมเดลใหญ่กว่าที่วัดในห้องควบคุม [46] Shah และคณะระบุลักษณะการตอบสนองของ TGS2611-E00 ต่อมีเทนและสิ่งแวดล้อม [52] Furuta และคณะประเมินเซ็นเซอร์ MOS ราคาถูกสำหรับ CH₄ ระดับต่ำ [53] Andrews, Mitchell และ Kiplimo เป็นสายงานสอบเทียบเซ็นเซอร์มีเทนต้นทุนต่ำด้วยการเรียนรู้ของเครื่องนอกบริบทนา [27], [28], [50] Lakhmi และคณะเปรียบแบบจำลองเชิงเส้นกับไม่เชิงเส้นบนอาเรย์ที่มี CH₄ เป็นก๊าซเป้าหมาย [51] Ye และ Fu ทบทวน eNose และเซ็นเซอร์ MOS ชนิดต้านทานเคมี [24], [26] Ahmad และ Baruah อภิปรายศักยภาพของ MOS และ eNose ในเกษตร [12], [11]",
    "Othman และคณะติดตั้งจมูกอิเล็กทรอนิกส์ที่ใช้เซ็นเซอร์ TGS-2611 และ MG-811 บนบอร์ดควบคุม ESP32 แล้วต่อเข้ากับกล่องเก็บตัวอย่างในแปลงนาเขตร้อน [56] แบบจำลองเครื่องเวกเตอร์สนับสนุน (SVM) ใช้สัญญาณก๊าซและสภาพแวดล้อมจากระบบนี้ เพื่อประมาณระดับการปล่อย งานนั้นแสดงว่าใช้จมูกอิเล็กทรอนิกส์ร่วมกับการเรียนรู้ของเครื่องในนาได้ แต่สิ่งที่แบบจำลองประมาณเป็นระดับการปล่อยที่คำนวณจากสัญญาณของระบบเซ็นเซอร์เอง งานนั้นไม่ได้รายงานการเทียบค่าความเข้มข้นเป็น ppm กับผลจากเครื่อง GC ซึ่งเป็นสิ่งที่วิทยานิพนธ์นี้จะทำ",
    "H|4.2.5 ช่องว่างการวิจัยและการจัดตำแหน่ง",
    "เมื่อเทียบงานใกล้เคียง แต่ละงานยังขาดอย่างน้อยหนึ่งอย่างที่วิทยานิพนธ์นี้ต้องการ Rajasekar และ Selvi วัดในนาด้วยเซ็นเซอร์โลหะออกไซด์ แต่คิดค่าจากสูตรผู้ผลิตทีละตัว ไม่ได้รวมสัญญาณหลายตัวแล้วเทียบเป็น ppm กับ GC [5] Domènech-Gil และคณะใช้จมูกอิเล็กทรอนิกส์ร่วมกับการเรียนรู้ของเครื่อง แต่ทดลองที่ความเข้มข้นระดับบรรยากาศในสวนและระบบบำบัด ไม่ใช่แปลงนา [10] Zhang และคณะใช้การเรียนรู้ของเครื่องในนาจากปัจจัยน้ำ ดิน และอากาศ โดยไม่มีสัญญาณเซ็นเซอร์โลหะออกไซด์ [23] Othman และคณะใช้จมูกอิเล็กทรอนิกส์ร่วมกับ SVM ในนาเขตร้อนแล้ว แต่ประมาณระดับการปล่อยจากสัญญาณเซ็นเซอร์เอง ไม่ได้เทียบ ppm กับ GC [56] วิทยานิพนธ์นี้จึงไม่ได้เสนอว่าเป็นงานแรกที่ใช้จมูกอิเล็กทรอนิกส์ร่วมกับการเรียนรู้ของเครื่องในนา แต่ตั้งคำถามต่างออกไป คือประมาณความเข้มข้นก๊าซมีเทนเป็น ppm จากผลต่างสัญญาณเซ็นเซอร์ระหว่างช่วงอากาศอ้างอิงกับช่วงวัด (ΔV) และจากอุณหภูมิความชื้น แล้วเทียบกับค่าจากวิธีครอบกล่องร่วมกับ GC รวมถึงออกแบบลำดับการวัดบนอุปกรณ์ที่นำไปแปลงนาได้ ไม่ใช่การเสนอวิธีวิเคราะห์ใหม่แทน GC",
]

REFS = [
    '[32] M. Saunois et al., "Global Methane Budget 2000–2020," Earth Syst. Sci. Data, vol. 17, no. 5, pp. 1873–1958, 2025, doi: 10.5194/essd-17-1873-2025.',
    '[33] IPCC, "Agriculture, Forestry and Other Land Uses (AFOLU)," in Climate Change 2022: Mitigation of Climate Change. Cambridge, U.K.: Cambridge Univ. Press, 2023, pp. 747–860, doi: 10.1017/9781009157926.009.',
    '[34] R. Conrad, "Methane production in soil environments—Anaerobic biogeochemistry and microbial life between flooding and desiccation," Microorganisms, vol. 8, no. 6, p. 881, 2020, doi: 10.3390/microorganisms8060881.',
    '[35] A. Z. Oo, K. T. Win, and S. D. Bellingrath-Kimura, "Within field spatial variation in methane emissions from lowland rice in Myanmar," SpringerPlus, vol. 4, p. 145, 2015, doi: 10.1186/s40064-015-0901-2.',
    '[36] K. Minamikawa, T. Tokida, S. Sudo, A. Padre, and K. Yagi, Guidelines for Measuring CH4 and N2O Emissions from Rice Paddies by a Manually Operated Closed Chamber Method. Tsukuba, Japan: NIAES, 2015.',
    '[37] IPCC, "Cropland," in 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories, vol. 4. IPCC, 2019, ch. 5.',
    '[38] R. Wassmann et al., "Increasing sensitivity of methane emission measurements in rice through deployment of closed chambers at nighttime," PLOS ONE, vol. 13, no. 2, p. e0191352, 2018, doi: 10.1371/journal.pone.0191352.',
    '[39] T. E. R. Mazengo, X. Zhong, X. Liu, M. F. Mwema, and R. Gill, "Non-flow-through static (closed chamber) method for sampling of greenhouse gases in crop production systems," Front. Agron., vol. 6, p. 1464495, 2024, doi: 10.3389/fagro.2024.1464495.',
    '[40] T. B. T. Vo, R. Wassmann, B. O. Sander, and A. M. Radanielson, "Measurement approaches for greenhouse gas emissions from rice I: technical evolution and scientific results obtained with different methods," Front. Agron., vol. 8, p. 1693619, 2026, doi: 10.3389/fagro.2026.1693619.',
    '[41] G. Zhang et al., "Fingerprint of rice paddies in spatial–temporal dynamics of atmospheric methane concentration in monsoon Asia," Nat. Commun., vol. 11, p. 554, 2020, doi: 10.1038/s41467-019-14155-5.',
    '[42] R. Liang et al., "Satellite-based monitoring of methane emissions from China’s rice hub," Environ. Sci. Technol., vol. 58, no. 52, pp. 23127–23137, 2024, doi: 10.1021/acs.est.4c09822.',
    '[43] W. Eugster and G. W. Kling, "Performance of a low-cost methane sensor for ambient concentration measurements in preliminary studies," Atmos. Meas. Tech., vol. 5, no. 8, pp. 1925–1934, 2012, doi: 10.5194/amt-5-1925-2012.',
    '[44] C. J. Jørgensen, J. Mønster, K. Fuglsang, and J. R. Christiansen, "Continuous methane concentration measurements at the Greenland ice sheet–atmosphere interface using a low-cost, low-power metal oxide sensor system," Atmos. Meas. Tech., vol. 13, no. 6, pp. 3319–3328, 2020, doi: 10.5194/amt-13-3319-2020.',
    '[45] A. Collier-Oxandale et al., "Assessing a low-cost methane sensor quantification system for use in complex rural and urban environments," Atmos. Meas. Tech., vol. 11, no. 6, pp. 3569–3594, 2018, doi: 10.5194/amt-11-3569-2018.',
    '[46] R. Rivera Martinez et al., "The potential of low-cost tin-oxide sensors combined with machine learning for estimating atmospheric CH4 variations around background concentration," Atmosphere, vol. 12, no. 1, p. 107, 2021, doi: 10.3390/atmos12010107.',
    '[47] T. Tokida, "Increasing measurement throughput of methane emission from rice paddies with a modified closed-chamber method," J. Agric. Meteorol., vol. 77, no. 2, pp. 160–165, 2021, doi: 10.2480/agrmet.d-20-00029.',
    '[48] C. Li et al., "Low-cost detection of methane gas in rice cultivation by gas chromatography-flame ionization detector based on manual injection and split pattern," Molecules, vol. 27, no. 13, p. 3968, 2022, doi: 10.3390/molecules27133968.',
    '[49] D. Bastviken, J. Nygren, J. Schenk, R. Parellada Massana, and N. T. Duc, "Technical note: Facilitating the use of low-cost methane (CH4) sensors in flux chambers," Biogeosciences, vol. 17, no. 13, pp. 3659–3667, 2020, doi: 10.5194/bg-17-3659-2020.',
    '[50] E. Kiplimo et al., "Addressing low-cost methane sensor calibration shortcomings with machine learning," Atmosphere, vol. 15, no. 11, p. 1313, 2024, doi: 10.3390/atmos15111313.',
    '[51] R. Lakhmi et al., "Linear and non-linear modelling methods for a gas sensor array developed for process control applications," Sensors, vol. 24, no. 11, p. 3499, 2024, doi: 10.3390/s24113499.',
    '[52] A. Shah et al., "Characterising the methane gas and environmental response of the Figaro Taguchi Gas Sensor (TGS) 2611-E00," Atmos. Meas. Tech., vol. 16, no. 13, pp. 3391–3419, 2023, doi: 10.5194/amt-16-3391-2023.',
    '[53] D. Furuta, T. Sayahi, J. Li, B. Wilson, A. A. Presto, and J. Li, "Characterization of inexpensive metal oxide sensor performance for trace methane detection," Atmos. Meas. Tech., vol. 15, no. 17, pp. 5117–5128, 2022, doi: 10.5194/amt-15-5117-2022.',
    '[54] Z. Chen et al., "Global Rice Paddy Inventory (GRPI): A high-resolution inventory of methane emissions from rice agriculture based on Landsat satellite inundation data," Earth’s Future, vol. 13, no. 4, 2025, doi: 10.1029/2024EF005479.',
    '[55] I. Nouchi, S. Mariko, and K. Aoki, "Mechanism of methane transport from the rhizosphere to the atmosphere through rice plants," Plant Physiol., vol. 94, no. 1, pp. 59–66, 1990, doi: 10.1104/pp.94.1.59.',
    '[56] M. M. Othman et al., "A Robust Support Vector Machine Model for Monitoring Methane Emission Levels in Paddy Ecosystems using Electronic Nose Technology," J. Adv. Res. Appl. Sci. Eng. Technol., vol. 60, no. 5, pp. 33–50, 2026, doi: 10.37934/araset.60.5.3350.',
]

OLD = "โดยมีรายงานว่าสัดส่วนการปล่อยจากนาข้าวอยู่ในช่วงร้อยละ 12–26 ของก๊าซเรือนกระจกจากพื้นที่เกษตร [4]"
NEW = "งบประมาณมีเทนโลกประมาณการปล่อยจากนาข้าวในช่วงทศวรรษ 2010–2019 เท่ากับ 32 [25–37] Tg CH₄ yr⁻¹ หรือราวร้อยละ 9 ของการปล่อย CH₄ มานุษย์ทั้งโลก [32] เอเชียรับผิดชอบราวร้อยละ 89 ของการปล่อยจากการปลูกข้าว [33]"


def oc(*args) -> dict:
    cmd = ["officecli", *args, "--json"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("FAIL", cmd, file=sys.stderr)
        print(r.stdout[-2000:], file=sys.stderr)
        print(r.stderr[-2000:], file=sys.stderr)
        raise SystemExit(r.returncode)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"raw": r.stdout}


def para_id_from_add(resp: dict) -> str:
    data = resp.get("data") or resp
    # common shapes
    for key in ("path", "Path"):
        if key in data and "paraId=" in str(data[key]):
            s = str(data[key])
            return s.split("paraId=")[1].split("]")[0]
    text = json.dumps(resp)
    if "paraId=" in text:
        return text.split("paraId=")[1].split("]")[0]
    raise RuntimeError("no paraId in " + text[:500])


def main() -> None:
    oc("open", str(FILE))
    ops = [{"command": "remove", "path": f"/body/p[@paraId={pid}]"} for pid in REMOVE]
    batch = ROOT / "docs" / "literature-review-4.2" / "_rm42.json"
    batch.write_text(json.dumps(ops, ensure_ascii=False), encoding="utf-8")
    oc("batch", str(FILE), "--input", str(batch))

    after = HEAD
    for item in BODY:
        if item.startswith("H|"):
            text = item[2:]
            resp = oc(
                "add", str(FILE), "/body", "--type", "paragraph", "--after", after,
                "--prop", f"text={text}",
                "--prop", "font=Cordia New", "--prop", "size=15pt",
                "--prop", "bold=true", "--prop", "spaceBefore=10pt",
                "--prop", "firstLineIndent=0pt",
            )
            after = f"/body/p[@paraId={para_id_from_add(resp)}]"
        elif item.startswith("C|"):
            text = item[2:]
            resp = oc(
                "add", str(FILE), "/body", "--type", "paragraph", "--after", after,
                "--prop", f"text={text}",
                "--prop", "font=Cordia New", "--prop", "size=14pt",
                "--prop", "italic=true", "--prop", "spaceAfter=6pt",
                "--prop", "firstLineIndent=0pt",
            )
            after = f"/body/p[@paraId={para_id_from_add(resp)}]"
        elif item.startswith("IMG|"):
            _, name, alt, w, h = item.split("|")
            src = FIG / name
            resp = oc(
                "add", str(FILE), "/body", "--type", "paragraph", "--after", after,
                "--prop", "text=",
                "--prop", "firstLineIndent=0pt",
            )
            ppath = f"/body/p[@paraId={para_id_from_add(resp)}]"
            oc(
                "add", str(FILE), ppath, "--type", "picture",
                "--prop", f"src={src}",
                "--prop", f"width={w}", "--prop", f"height={h}",
                "--prop", f"alt={alt}",
            )
            after = ppath
        else:
            resp = oc(
                "add", str(FILE), "/body", "--type", "paragraph", "--after", after,
                "--prop", f"text={item}",
                "--prop", "font=Cordia New", "--prop", "size=15pt",
                "--prop", "firstLineIndent=18pt", "--prop", "spaceBefore=5pt",
                "--prop", "spaceAfter=5pt",
            )
            after = f"/body/p[@paraId={para_id_from_add(resp)}]"
        print("ok", after)

    oc("set", str(FILE), PCT, "--find", OLD, "--replace", NEW)

    after = LAST_REF
    for ref in REFS:
        resp = oc(
            "add", str(FILE), "/body", "--type", "paragraph", "--after", after,
            "--prop", f"text={ref}",
            "--prop", "font=Cordia New", "--prop", "size=15pt",
            "--prop", "firstLineIndent=0pt", "--prop", "hangingIndent=18pt",
            "--prop", "indent=18pt",
        )
        after = f"/body/p[@paraId={para_id_from_add(resp)}]"
        print("ref", after)

    oc("save", str(FILE))
    print("saved")


if __name__ == "__main__":
    main()
