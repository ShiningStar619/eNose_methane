# 4.2 สรุปสาระสำคัญจากงานวิจัยที่เกี่ยวข้อง (Literature Review)

**หัวข้อวิจัย:** การประยุกต์ใช้จมูกอิเล็กทรอนิกส์ ตรวจวัดแก๊สมีเทนในนาข้าว  
**แหล่งอ้างอิง:** [`docs/paper/`](.) (คลังงานวิจัย 2020–2026) เสริมด้วยการสืบค้นผ่าน Firecrawl Research  
**รูปแบบ cite:** ชุดรวมกับ Proposal §4.1 — `[1]`–`[12]` ตาม IEEE ท้าย Proposal; `[13]`–`[31]` สำหรับงาน §4.2 เพิ่มเติม (reuse `[4]`–`[12]` เมื่ออ้างงานเดิม)  
**แผนที่ cite:** [`../proposal-4.1-4.2-cites-draft6.md`](../proposal-4.1-4.2-cites-draft6.md)

งานวิจัยที่เกี่ยวข้องกับการตรวจวัดก๊าซมีเทนจากนาข้าวสามารถจัดกลุ่มได้เป็นสี่ประเด็นหลัก ได้แก่ (1) กลไกและปัจจัยที่ควบคุมการปล่อยก๊าซมีเทนจากนาข้าว (2) วิธีการวัดมาตรฐานที่ใช้เป็นวิธีอ้างอิง (3) วิธีการวัดทางเลือกอื่น และ (4) เทคโนโลยีจมูกอิเล็กทรอนิกส์ร่วมกับการเรียนรู้ของเครื่อง โดยแต่ละประเด็นนำเสนอทั้งข้อค้นพบเชิงปริมาณและช่องว่างที่นำไปสู่งานวิจัยนี้

---

## 4.2.1 การปล่อยก๊าซมีเทนจากนาข้าวและปัจจัยควบคุม

การปลูกข้าวแบบน้ำขังทำให้ดินอยู่ในสภาวะขาดออกซิเจน (anaerobic) ซึ่งเป็นเงื่อนไขที่เอื้อต่อจุลินทรีย์กลุ่มสร้างมีเทน (methanogens) ในการย่อยสลายอินทรียวัตถุและปล่อยก๊าซมีเทน (CH₄) ออกสู่บรรยากาศ ทั้งผ่านผิวน้ำ ฟองอากาศ (ebullition) และผ่านท่อลำเลียงอากาศในต้นข้าว [4] ด้วยเหตุนี้นาข้าวจึงกลายเป็นหนึ่งในแหล่งปล่อย CH₄ จากกิจกรรมมนุษย์ที่สำคัญ โดยงานทบทวนล่าสุดประเมินว่าการปลูกข้าวปล่อย CH₄ คิดเป็นประมาณ **ร้อยละ 10–12 ของการปล่อยมีเทนจากกิจกรรมมนุษย์ทั่วโลก** [13] หรือราวร้อยละ 11 ของการปล่อยมีเทนเชิงมนุษย์ทั้งหมดที่ระดับ 308 Tg ต่อปี [14] เมื่อพิจารณาว่าประมาณร้อยละ 90 ของข้าวถูกผลิตและบริโภคในทวีปเอเชีย Monsoon Asia จึงเป็นภูมิภาคที่มีความสำคัญเชิงยุทธศาสตร์ต่อการลดการปล่อยก๊าซ [13]

อย่างไรก็ตาม ปริมาณการปล่อย CH₄ จากนาข้าวไม่ใช่ค่าคงที่ แต่ผันแปรสูงตามการจัดการน้ำ พันธุ์ข้าว คุณสมบัติดิน และฤดูกาล Nguyen et al. [4] สรุปว่าการปล่อย CH₄ และไนตรัสออกไซด์ (N₂O) จากพื้นที่นาขึ้นอยู่กับรูปแบบการจัดการเป็นหลัก ในบรรดาปัจจัยเหล่านี้ **การจัดการน้ำ** ให้ผลชัดเจนที่สุด งานวิเคราะห์อภิมานจาก 47 งานภาคสนามพบว่าการจัดการน้ำแบบเปียกสลับแห้ง (alternate wetting and drying, AWD) ลดการปล่อย CH₄ ได้เฉลี่ย **ร้อยละ 64.5 ± 12.3** เมื่อเทียบกับการขังน้ำต่อเนื่อง โดยลดได้มากกว่าในเขตร้อน (ร้อยละ 68.2) และในดินเหนียว (ร้อยละ 71.3) แต่ทำให้ N₂O เพิ่มขึ้นราวร้อยละ 18.7 ส่งผลให้ศักยภาพภาวะโลกร้อนโดยรวม (GWP) ลดลงประมาณร้อยละ 42.1 [15] ผลในทิศทางเดียวกันนี้ได้รับการยืนยันจากการวัดด้วยเทคนิค eddy covariance ที่รายงานว่า AWD ลด CH₄ ได้อย่างมีนัยสำคัญเมื่อเทียบกับการขังน้ำ [16]

นอกจากการจัดการน้ำแล้ว ปัจจัยทางดินและชีวภาพก็มีบทบาทเช่นกัน งานวิจัยระดับ rhizosphere ชี้ว่าการพัฒนารากข้าวและสภาพดินรอบรากส่งผลต่ออัตราการปล่อย CH₄ [17] ขณะที่ปริมาณคาร์บอนที่ใช้ได้ (carbon availability) และค่า pH ของดินเป็นตัวควบคุมสำคัญของการปล่อยตาม gradient อุณหภูมิเฉลี่ยรายปี [18] ในอีกมิติหนึ่ง Yang et al. [19] ซึ่งวิเคราะห์อภิมานจาก 46 งานภาคสนาม พบว่าประสิทธิผลของปุ๋ยไนโตรเจนแบบ enhanced-efficiency (EENF) ต่อการลด CH₄ ขึ้นกับพันธุ์ข้าวและมาตรการเกษตรอย่างชัดเจน เช่น การใช้ inhibitor ลด CH₄ ได้ **ร้อยละ 23.6 ในพันธุ์ไฮบริด** เทียบกับเพียง **ร้อยละ 8.2 ในพันธุ์อินเบรด** และลดได้สูงสุดถึงร้อยละ 40.6 ในฤดูข้าวหลังของระบบปลูกสองฤดู นอกจากนี้ภายใต้การขังน้ำเป็นช่วง (intermittent flooding) inhibitor ลด CH₄ ได้ร้อยละ 24.9 ในขณะที่ภายใต้การขังน้ำต่อเนื่องผลลดลงจนไม่มีนัยสำคัญทางสถิติ [19] ตัวเลขเหล่านี้ยืนยันว่าพันธุ์ข้าวและมาตรการเกษตรไม่เพียงมีผลต่อการปล่อยโดยตรง แต่ยังกำหนดว่ามาตรการลดก๊าซจะ “ได้ผล” มากน้อยเพียงใดภายใต้เงื่อนไขจริง

เพื่อประมาณการปล่อยในระดับภูมิภาคและระดับโลก จึงมีการพัฒนาแบบจำลองเชิงกระบวนการ เช่น CH4MOD [20] แต่การประมาณระดับมหภาคยังมีความละเอียดไม่เพียงพอต่อการติดตามการเปลี่ยนแปลงในระดับแปลงนา เมื่อประกอบกับความผันผวนสูงทั้งตามฤดูกาล ระยะการเจริญเติบโตของข้าว และช่วงเวลาในแต่ละวัน [13] จึงสรุปได้ว่าการติดตามการปล่อย CH₄ เพื่อประเมินมาตรการลดก๊าซหรือเพื่อตรวจสอบความถูกต้องของเครื่องมือวัดใหม่ จำเป็นต้องอาศัย **การวัดซ้ำที่ความถี่เพียงพอในระดับแปลงนา** ไม่ใช่การสรุปจากค่าเฉลี่ยระดับภูมิภาคเพียงครั้งเดียว ซึ่งเป็นเหตุผลหลักที่ผลักดันความต้องการเครื่องมือวัดต้นทุนต่ำที่ติดตั้งภาคสนามได้

---

## 4.2.2 วิธีการวัดปริมาณก๊าซมีเทนแบบมาตรฐาน (Static Chamber ร่วมกับ GC)

ท่ามกลางความต้องการข้อมูลระดับแปลงนาข้างต้น การใช้ **ห้องเก็บตัวอย่างแบบปิด (static chamber)** ร่วมกับ **ก๊าซโครมาโทกราฟีชนิด flame ionization detector (GC-FID)** ยังคงเป็น **วิธีอ้างอิง (reference method / ground truth)** ที่ได้รับการยอมรับกว้างขวางที่สุดสำหรับการวัดฟลักซ์ (flux) ของก๊าซเรือนกระจกจากดินเกษตรกรรม [6] หลักการคือครอบ chamber ลงบนผิวดินหรือผิวน้ำเป็นระยะเวลาหนึ่ง แล้วเก็บตัวอย่างอากาศภายในตามช่วงเวลา เพื่อคำนวณอัตราการสะสมความเข้มข้นของ CH₄ ต่อหน่วยพื้นที่ต่อเวลา (เช่น mg m⁻² h⁻¹) ก่อนนำไปวิเคราะห์ด้วย GC ในห้องปฏิบัติการ Zaman et al. [6] ได้วางระเบียบวิธีมาตรฐานสำหรับการวัดก๊าซเรือนกระจกจากดินเกษตรด้วยเทคนิค non-isotopic ครอบคลุมตั้งแต่การออกแบบ chamber การเก็บตัวอย่าง จนถึงการวิเคราะห์ด้วย GC-FID โดยทั่วไป chamber แบบเก็บ vial ด้วยมือจะครอบประมาณ 20–30 นาที และเก็บตัวอย่างหลายจุดเวลาเพื่อหาความชันของความเข้มข้น

แม้วิธีนี้จะให้ความแม่นยำและความน่าเชื่อถือสูง แต่ Mumu et al. [7] ทบทวนความก้าวหน้าเชิงระเบียบวิธีของการวัดก๊าซเรือนกระจกในภาคเกษตร และชี้ว่าข้อจำกัดหลักของ chamber–GC อยู่ที่ **ต้นทุนสูง การใช้แรงงานมาก และความถี่ในการเก็บตัวอย่างที่ต่ำ** โดยทั่วไปการเก็บตัวอย่างทำได้เพียงไม่กี่ครั้งต่อสัปดาห์ ทำให้เสี่ยงต่อการพลาดจับพลวัตการปล่อยแบบรายวัน (diurnal) หรือเหตุการณ์ ebullition ที่เกิดขึ้นเป็นช่วง ๆ และติดตามการเปลี่ยนแปลงตลอดฤดูปลูกได้ยาก [7] ในทำนองเดียวกัน Borhan และ Khanaum [9] เปรียบเทียบเซ็นเซอร์และวิธีการวัดก๊าซเรือนกระจกจากฟาร์มปศุสัตว์ และยืนยันว่าแม้บริบทจะต่างจากนาข้าว แต่หลักการของ chamber ร่วมกับ GC สำหรับการวัดฟลักซ์สามารถถ่ายทอดมาประยุกต์กับพื้นที่นาได้

นอกจากหลักฐานเชิงระเบียบวิธีแล้ว งานภาคสนามยังยืนยันบทบาทของ chamber–GC ในฐานะวิธีอ้างอิง Vo et al. [21] เปรียบเทียบ manual chamber–GC กับ laser-based Trace Gas Analyzer (TGA) ในข้าวนาภายใต้ AWD และการขังน้ำต่อเนื่องที่ IRRI พบว่าทั้งสองวิธีให้ค่าฟลักซ์ CH₄ ใกล้เคียงกัน โดยปัจจัยวิธีวัดไม่มีนัยสำคัญทางสถิติ (p = 0.47) และความต่างสูงสุดระหว่าง GC กับ multi-valve TGA อยู่ที่เพียง 12.62 mg CH₄ m⁻² d⁻¹ ซึ่งเล็กเมื่อเทียบกับระดับการปล่อยโดยรวม อย่างไรก็ตาม การวัดแบบ manual chamber–GC ยังต้องครอบ chamber ประมาณ 30 นาที ขณะที่ TGA ใช้ได้ราว 4 นาที และในหนึ่งวันผู้ปฏิบัติงานหนึ่งคนครอบคลุมได้ราว 48 แปลง เทียบกับมากกว่า 110 แปลงของระบบ multi-valve TGA [21] ตัวเลขเหล่านี้จึงทั้ง **ยืนยันความน่าเชื่อถือของ GC** และ **ชี้ข้อจำกัดด้านแรงงานกับความถี่การเก็บตัวอย่าง** ซึ่งสอดคล้องกับข้อสรุปของ Mumu et al. [7]

ด้วยเหตุนี้ งานวิจัยนี้จึงกำหนดให้ **chamber ร่วมกับ GC-FID เป็นวิธีอ้างอิง** สำหรับสร้างค่าความเข้มข้น CH₄ ที่ใช้เป็น ground truth ในการฝึกและตรวจสอบความถูกต้องของแบบจำลองจมูกอิเล็กทรอนิกส์ แทนที่จะใช้เป็นเครื่องมือติดตามต่อเนื่องในภาคสนามโดยตรง [6], [7], [21]

---

## 4.2.3 วิธีการวัดปริมาณก๊าซมีเทนแบบอื่น ๆ

นอกเหนือจาก chamber–GC ยังมีวิธีการวัดและประเมิน CH₄ จากนาข้าวอีกหลายแนวทาง ซึ่งแต่ละแบบมีจุดเด่นและข้อจำกัดที่แตกต่างกันในมิติของความแม่นยำ ความละเอียดเชิงพื้นที่ ต้นทุน และความเหมาะสมกับการติดตามต่อเนื่อง

**เทคนิคสเปกโทรสโกปีความแม่นยำสูง** เช่น TDLAS, CRDS และ FTIR สามารถวัดความเข้มข้น CH₄ ได้ในระดับ ppm ถึง ppb พร้อมการตอบสนองที่รวดเร็ว Tyagi et al. [8] ทบทวนความก้าวหน้าของเทคโนโลยีเหล่านี้และสรุปว่าแม้จะให้ความแม่นยำสูงและเหมาะกับงานในห้องปฏิบัติการหรือสถานีตรวจวัดคงที่ แต่มี **ต้นทุนสูง ต้องการการตั้งค่าที่ซับซ้อน** และไม่คุ้มค่าต่อการติดตั้งหลายจุดในแปลงนาขนาดเล็ก หรือการติดตามอย่างต่อเนื่องตลอดฤดูปลูก ในทางปฏิบัติ การเชื่อมเครื่องมือวิเคราะห์ความแม่นยำสูงเข้ากับ chamber จึงกลายเป็นทางเลือกที่พยายามลดข้อจำกัดของ GC แบบเก็บ vial ดังที่แสดงใน §4.2.2 ว่า TGA ของ Vo et al. [21] ให้ผลเทียบเคียง GC ได้ดีและเพิ่ม throughput อย่างชัดเจน แต่ยังมีต้นทุนลงทุนสูง จึงยังไม่ใช่ทางเลือกต้นทุนต่ำสำหรับแปลงนาทั่วไป

**การสังเกตจากระยะไกล (remote sensing)** ทั้งจากดาวเทียมและอากาศยานไร้คนขับ (UAV) ครอบคลุมพื้นที่กว้างได้ แต่ความละเอียดเชิงพื้นที่มัก **ไม่ลงลึกถึงระดับรายแปลงนา** Xu et al. [22] นำเสนอการผสาน AI/ML เข้ากับข้อมูล remote sensing เพื่อประเมิน CH₄ จากนาข้าว ซึ่งเหมาะกับการประเมินระดับภูมิภาคมากกว่าการติดตามแบบเรียลไทม์ในแปลงเดียว นอกจากนี้ Vo et al. [21] ยังชี้ว่าเกณฑ์ตรวจจับของดาวเทียมปัจจุบัน (ราว 100–10,000 kg CH₄ h⁻¹) ยังห่างจากอัตราปล่อยพื้นหลังของนาข้าวในเอเชียตะวันออกเฉียงใต้ (ประมาณ 0.05 kg CH₄ ha⁻¹ h⁻¹) หลายระดับ ทำให้การประมาณจากระยะไกลยังต้องพึ่งการวัดภาคพื้นดินเป็น ground truth

**เซ็นเซอร์ก๊าซต้นทุนต่ำในภาคสนาม** เป็นทางเลือกที่ใกล้เคียงกับงานวิจัยนี้มากที่สุด Rajasekar และ Selvi [5] พัฒนาระบบ chamber อัตโนมัติร่วมกับเซ็นเซอร์ราคาประหยัด **MQ4 และ TGS2611** เพื่อวัด CH₄ จากนาข้าวสู่บรรยากาศใกล้ผิว ผลการทดลองแสดงให้เห็นว่าเซ็นเซอร์ต้นทุนต่ำสามารถติดตามแนวโน้มการปล่อยในภาคสนามได้จริง และพบว่าการจัดการน้ำแบบ controlled intermittent flooding ลด CH₄ ได้เมื่อเทียบกับการขังน้ำต่อเนื่อง อย่างไรก็ตาม ค่าที่ได้ยังต้อง **สอบเทียบกับวิธีอ้างอิงอย่างสม่ำเสมอ** และงานดังกล่าวใช้การแปลงค่าจากสูตรผู้ผลิต (Rs/R0) มากกว่าการใช้แบบจำลองการเรียนรู้ของเครื่องแบบหลายเซ็นเซอร์ จึงยังไม่ได้ให้ค่าความเข้มข้นแบบ ppm ผ่านสถาปัตยกรรม eNose ที่แท้จริง

**การประมาณ CH₄ จากปัจจัยดิน–น้ำ–อากาศ (proxy-based ML)** เป็นแนวทางล่าสุดในบริบทนาข้าว Zhang et al. [23] เสนอวิธี**ประมาณฟลักซ์ CH₄ ในสภาพแวดล้อมจริงแบบความถี่สูง** โดยไม่วัดก๊าซโดยตรงตลอดเวลา หลักการคือ (1) วัดฟลักซ์ CH₄ จริงด้วย chamber ในช่วงฝึกแบบจำลอง (2) อ่านปัจจัยที่เซ็นเซอร์ติดตามได้ต่อเนื่อง เช่น ความลึกน้ำในทุ่ง (Hpw) การนำไฟฟ้าของดิน (EC) อุณหภูมิดิน (Ts) และศักยภาพการปรองศ (Eh) (3) ใช้การเรียนรู้ของเครื่องแปลงค่าปัจจัยเหล่านี้เป็นฟลักซ์ CH₄ โดยอ้อม งานวิจัยดำเนินในทุ่งนาลุ่มแม่น้ำแยงซี (จังหวัดหูเป่ย) ช่วงมิถุนายน–กันยายน 2022 และ 2024 พบว่า Hpw, EC และ Ts มีความสัมพันธ์เชิงบวกกับฟลักซ์ CH₄ อย่างมีนัยสำคัญ (p < 0.05) ขณะที่ Eh มีผลเชิงลบ จากการเปรียบเทียบอัลกอริทึม ML ห้าแบบ แบบจำลอง Decision Tree Regressor (DTR) ให้ความแม่นยำสูงสุด โดยกลุ่มตัวแปร**ดินอย่างเดียว**ให้ **R² = 0.84** สูงกว่ากลุ่มน้ำ–ดิน (0.83) น้ำ–ดิน–อากาศ (0.55) และอากาศ–ดิน (0.45) ตัวแปรสำคัญคือ Eh, EC, pH ดิน และ Ts (แต่ละตัว R² > 0.80) ดังนั้น “ความถี่สูง” ในที่นี้หมายถึงการอ่านปัจจัยสิ่งแวดล้อมและ**ประมาณ**ฟลักซ์ได้บ่อยกว่า chamber แบบ manual ไม่ใช่การวัดฟลักซ์ด้วย chamber ทุกครั้ง งานนี้ใกล้เคียง use case ของงานวิจัยนี้มากที่สุดในด้านการใช้ ML ทำนาย CH₄ ในนาข้าวและการติดตามต้นทุนต่ำ แต่ยัง **ไม่ได้ใช้สัญญาณจากเซ็นเซอร์ MOS/eNose** เป็นตัวแปรหลัก จึงเปิดช่องว่างสำหรับการบูรณาการจมูกอิเล็กทรอนิกส์เข้ากับ ML โดยตรง

เมื่อมองภาพรวมของวิธีทางเลือก จะเห็นว่าเครื่องมือความแม่นยำสูง (TGA/สเปกโทรสโกปี) แลกมาด้วยต้นทุนและ throughput ที่ต่างจาก GC ขณะที่ remote sensing เหมาะกับระดับภูมิภาค และเซ็นเซอร์ต้นทุนต่ำหรือ ML จากปัจจัยสิ่งแวดล้อมยังไม่ได้รวม eNose array เข้ากับการให้ค่า ppm ในนาข้าวอย่างครบวงจร ซึ่งนำไปสู่ประเด็นถัดไป

---

## 4.2.4 เทคโนโลยีจมูกอิเล็กทรอนิกส์และเทคนิคการเรียนรู้ของเครื่อง

**จมูกอิเล็กทรอนิกส์ (electronic nose, eNose)** เป็นระบบที่เลียนแบบการรับกลิ่นของมนุษย์ ประกอบด้วยอาเรย์ของเซ็นเซอร์ก๊าซที่มีความเลือกจำเพาะบางส่วน (partially selective) ระบบเก็บสัญญาณ และซอฟต์แวร์วิเคราะห์รูปแบบ [24] เมื่อก๊าซเป้าหมายสัมผัสพื้นผิวเซ็นเซอร์ โดยเฉพาะเซ็นเซอร์ชนิดโลหะออกไซด์ (metal oxide semiconductor, MOS) ความต้านทานของวัสดุจะเปลี่ยนแปลงตามความเข้มข้นของก๊าซ สัญญาณรวมจากเซ็นเซอร์หลายตัวจึงกลายเป็นเวกเตอร์หลายมิติ (smell print) ที่นำไปจำแนกชนิดหรือประเมินความเข้มข้นได้ Ye et al. [24] สรุปว่าการนำการเรียนรู้ของเครื่องมาใช้ทำให้ eNose สามารถทำงานได้ทั้งเชิงคุณภาพ (จำแนกชนิดก๊าซ) และเชิงปริมาณ (ประเมินความเข้มข้น)

งานที่เป็นหมุดหมายสำคัญที่สุดสำหรับงานวิจัยนี้คือ Domènech-Gil et al. [10] ซึ่งพัฒนา **eNose ต้นทุนต่ำสำหรับการติดตาม CH₄ ในบรรยากาศ** โดยใช้เซ็นเซอร์ MOS หลายตัว (Figaro TGS2611) ควบคู่กับเซ็นเซอร์วัดอุณหภูมิ ความชื้น และความดัน (BME680) แล้วใช้แบบจำลอง Partial Least Squares Regression (PLSR) ชดเชยผลกระทบจากสภาพแวดล้อม ในห้องปฏิบัติการ ระบบให้ R² > 0.9 และ RMSE < 100 ppb ในช่วง 0–9 ppm CH₄ ส่วนในสภาพภาคสนามสามารถวัดได้ถึงระดับความเข้มข้นบรรยากาศ (ราว **2 ppm**) โดยให้ค่าความคลาดเคลื่อน **RMSE ต่ำสุดถึง 33 ppb** และค่า **R² สูงสุดถึง 0.91** [10] ผลลัพธ์นี้ยืนยันความเป็นไปได้ของแนวทาง eNose+ML สำหรับ CH₄ แต่บริบทการใช้งานและช่วงความเข้มข้นยังต่างจากนาข้าวที่มีความชื้นสูงและสภาพแวดล้อมซับซ้อน จึงไม่สามารถถ่ายโอนแบบจำลองมาใช้โดยตรงได้

เซ็นเซอร์ MOS มีข้อได้เปรียบด้าน **ต้นทุนต่ำและขนาดเล็ก** แต่ข้อจำกัดที่ปรากฏซ้ำในวรรณกรรมคือ **cross-sensitivity** ต่อความชื้น อุณหภูมิ และก๊าซรบกวนอื่น Ahmad et al. [12] ทบทวนศักยภาพของเซ็นเซอร์ MOS ต้นทุนต่ำสำหรับ precision agriculture และเน้นว่าความไวต่อสารอินทรีย์ระเหยง่าย (VOC) และการเปลี่ยนแปลงของสภาพแวดล้อมยังเป็นข้อจำกัดหลักที่ต้องชดเชยด้วยแบบจำลองหลายตัวแปร งานสนับสนุนอื่น ๆ ในคลังวรรณกรรมยังแสดงถึงความเป็นไปได้ของ MOS สำหรับมีเทน เช่น การออกแบบ eNose เจ็ดเซ็นเซอร์เพื่อจำแนก CH₄/CO ในก๊าซผสม [25] และการทบทวนวัสดุ MOS chemiresistive สำหรับ CH₄ [26]

ในด้าน **การเรียนรู้ของเครื่อง** Baruah และ Mazumder [11] ทบทวนการประยุกต์ ML ร่วมกับ eNose และสรุปว่าเทคนิค PCA และ SVM ถูกใช้บ่อยในงานจำแนกและวิเคราะห์รูปแบบ แต่การทำ **regression เพื่อประเมินความเข้มข้นเชิงตัวเลข** ยังต้องการการออกแบบ feature การแบ่งชุดข้อมูล และการสอบเทียบกับวิธีอ้างอิงอย่างเป็นระบบ ในบริบทของ CH₄ โดยเฉพาะ มีงานแสดงศักยภาพของ ML calibration หลายชิ้น เช่น Andrews et al. [27] ที่ใช้ ML สอบเทียบเซ็นเซอร์ก๊าซสำหรับติดตาม methane emissions และ Mitchell et al. [28] ที่สาธิตการสอบเทียบเซ็นเซอร์ Figaro ต้นทุนต่ำด้วย ML ในพื้นที่พรุ ซึ่งใกล้เคียงกับสภาพภาคสนามและรายงานว่าแบบจำลองสามารถให้ค่า R² สูงมากในการสอบเทียบ (ถึงระดับ ~0.997 ในเงื่อนไขที่ควบคุมได้) พร้อม RMSE ในหน่วย ppm สำหรับการเลือกชนิดแบบจำลอง Lakhmi et al. [29] เปรียบเทียบแบบจำลองเชิงเส้นกับไม่เชิงเส้นบนอาเรย์เซ็นเซอร์ที่มี CH₄ เป็นก๊าซเป้าหมาย ซึ่งสอดคล้องโดยตรงกับคำถามของงานวิจัยนี้ว่าการถดถอยเชิงเส้น (log-linear regression) เพียงพอหรือไม่เมื่อเทียบกับ random forest ขณะที่งานล่าสุดเริ่มใช้ deep learning บนสัญญาณเชิงเวลา เช่น TFA-CNN [30] และ graph neural network ที่รายงาน R² > 0.96 บนชุดข้อมูลมาตรฐาน [31] เพื่อทำนายความเข้มข้น แต่มักแลกมาด้วยความซับซ้อนและความต้องการข้อมูลที่สูงกว่าแบบจำลองเชิงเส้น

โดยสรุป วรรณกรรมชี้ตรงกันว่าการชดเชย cross-sensitivity ของ MOS ด้วยเซ็นเซอร์สภาพแวดล้อม (T/H/P) ร่วมกับ ML เป็นเงื่อนไขจำเป็นต่อความแม่นยำ [10], [12], [27] อย่างไรก็ตาม **ยังไม่พบงานวิจัยที่รวมทั้งสามองค์ประกอบ — eNose แบบอาเรย์ MOS, ML regression ให้ค่า ppm ต่อเนื่อง และบริบทนาข้าว — ไว้ในงานเดียวพร้อมการตรวจสอบเทียบกับ chamber–GC** งานที่มีอยู่แยกเป็นสามสาย ได้แก่ eNose+ML สำหรับ CH₄ ทั่วไป [10], เซ็นเซอร์ MOS ในนาข้าวโดยไม่ใช้ ML [5] และ ML ทำนาย CH₄ ในนาข้าวโดยไม่ใช้ eNose [23] งานวิจัยนี้จึงมุ่งเติมช่องว่างดังกล่าว โดยพัฒนาระบบ eNose บนแพลตฟอร์ม Raspberry Pi ที่ใช้เซ็นเซอร์ MOS ต้นทุนต่ำร่วมกับ BME280 และสร้างแบบจำลอง ML ที่ชดเชยผลจากอุณหภูมิ ความชื้น และความดัน แล้วประเมินความแม่นยำเทียบกับ GC-FID ภายใต้ขอบเขตการศึกษาที่กำหนด

---

## บรรณานุกรม (ชุดรวมกับ Proposal §4.1)

รูปแบบ: `[#] Author (Year). Title. *Journal*. DOI — docs/paper/...`

### `[1]`–`[12]` — ชุด IEEE ของ Proposal (§4.1 + reuse ใน §4.2)

**[1]** C. Sowcharoensuk (2026). Industry Outlook 2026-2028: Rice Industry. Krungsri Research. — *(นอกคลัง)*

**[2]** The Nation (2026). Thai farm incomes face pressure from global rice market shifts. — *(นอกคลัง)*

**[3]** Thairath (2026). Thai Rice Exports in 2025 Surpass Targets… — *(นอกคลัง; §4.1–4.2 ไม่ cite)*

**[4]** H. Nguyen et al. (2023). Carbon Footprint Reduction from Closing Rice Yield Gaps. In *Carbon Footprint of Rice Production*, pp. 149–176. — `methane/2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.pdf`

**[5]** P. Rajasekar & J. A. V. Selvi (2022). Sensing and Analysis of Greenhouse Gas Emissions from Rice Fields to the Near Field Atmosphere. *Sensors*, 22(11), 4141. https://doi.org/10.3390/s22114141 — `methods-field/2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf`

**[6]** M. Zaman et al. (2021). Methodology for measuring GHG emissions from agricultural soils using non-isotopic techniques. Springer, pp. 11–108. — `methods-chamber-gc/2021_Zaman_GHG_measurement_agricultural_soils_methodology.pdf`

**[7]** N. J. Mumu et al. (2024). Methodological progress in the measurement of agricultural greenhouse gases. *Carbon Manage.*, 15(1), 2366527. — `methods-chamber-gc/2024_Mumu_methodological_progress_agricultural_GHG.pdf`

**[8]** L. Tyagi et al. (2025). Environmental impacts and recent advancements in the sensing of methane: a review. *Environ. Technol. Rev.*, 14(1), 191–212. — `methods-spectroscopy/2025_Tyagi_methane_sensing_environmental_review.pdf`

**[9]** M. S. Borhan & M. M. Khanaum (2022). Sensors and methods for measuring GHG emissions from livestock production facilities. *J. Geosci. Environ. Prot.*, 10(12), 242–272. — `methods-chamber-gc/2022_Borhan_sensors_methods_GHG_livestock.pdf`

**[10]** G. Domènech-Gil et al. (2024). Electronic Nose for Improved Environmental Methane Monitoring. *Environ. Sci. Technol.*, 58(1), 352–361. https://doi.org/10.1021/acs.est.3c06945 — `enose/2024_Domenech-Gil_eNose_environmental_methane_monitoring.pdf`

**[11]** S. Baruah & D. H. Mazumder (2025). A Review on Application of Machine Learning Techniques Coupled With E-Nose in Healthcare, Agriculture and Allied Domains. *IEEE Access*. — `algorithm/2025_Baruah_ML_eNose_healthcare_agriculture_review.pdf`

**[12]** A. Ahmad et al. (2026). The Promise of Low-Cost Metal-Oxide Semiconductor Gas Sensors for Precision Agriculture. *Adv. Sensor Res.* — `enose/2026_Ahmad_MOS_sensors_precision_agriculture.pdf`

### `[13]`–`[23]` — §4.2.1–4.2.3 เพิ่มเติม

**[13]** H. Zhou, F. Tao, Y. Chen, et al. (2024). Paddy rice methane emissions, controlling factors, and mitigation potentials across Monsoon Asia. *Sci. Total Environ.* https://doi.org/10.1016/j.scitotenv.2024.173441 — `methane/2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review.md` *(stub)*

**[14]** (2024). Advances in mitigating methane emissions from rice cultivation: past, present, and future strategies. *(Firecrawl discovery — รองรับตัวเลข ~11% ของ 308 Tg; ใส่ DOI ก่อนส่ง)*

**[15]** A. Rafy, M. Hannan, M. Mohammed, N. Khan (2025). Meta-Analysis of Alternate Wetting and Drying (AWD) Irrigation Effects on Methane and Nitrous Oxide Emissions. *Eur. J. Ecol. Biol. Agric.*, 2(5), 181–200. https://doi.org/10.59324/ejeba.2025.2(5).13 *(Firecrawl discovery — CH₄ ↓64.5%)*

**[16]** S. S. Anapalli et al. (2023). Eddy covariance assessment of AWD on rice methane emissions. *Heliyon*, 9(4), e14696. — `methane/2023_Anapalli_eddy_covariance_AWD_rice_methane.pdf`

**[17]** (2024). Effects of rice root development and rhizosphere soil on methane emission. — `methane/2024_rice_root_rhizosphere_methane_emission.pdf`

**[18]** (2025/2026). Methane emissions from rice paddies regulated by carbon availability and soil pH. — `methane/2025_methane_emissions_carbon_availability_soil_pH_gradient.pdf`

**[19]** T. Yang, M. Wang, X. Wang, C. Xu, F. Fang, F. Li (2022). Product Type, Rice Variety, and Agronomic Measures Determined the Efficacy of Enhanced-Efficiency Nitrogen Fertilizer on the CH₄ Emission and Rice Yields in Paddy Fields: A Meta-Analysis. *Agronomy*, 12, 2240. https://doi.org/10.3390/agronomy12102240 — `methane/2025_product_type_rice_variety_agronomic_CH4_emissions.pdf`

**[20]** Q. Hu et al. (2024). Global methane emissions from rice paddies: CH4MOD model development and application. *iScience*, 27(11), 111237. https://doi.org/10.1016/j.isci.2024.111237 — `methane/2025_CH4MOD_global_methane_emissions_rice_paddies.pdf`

**[21]** T. B. T. Vo, R. Wassmann, R. R. Romasanta, et al. (2026). Measurement approaches for greenhouse gas emissions from rice II: advanced technology for accelerating throughput. *Front. Agron.*, 7, 1693620. https://doi.org/10.3389/fagro.2025.1693620 — `methods-spectroscopy/2022_Vo_TGA_vs_GC_methane_agricultural_soils.pdf` *(TGA = Trace Gas Analyzer)*

**[22]** (2025). AI/ML for methane in rice via remote sensing. — `methods-remote/2025_Xu_AI_ML_methane_rice_remote_sensing.pdf`

**[23]** Q. Zhang et al. (2025). Machine learning-driven method for in-situ high-frequency CH₄ measurement in paddy fields based on water-soil-air factors. *J. Environ. Manage.*, 393, 127132. https://doi.org/10.1016/j.jenvman.2025.127132 — `methane/_zhang2025_extract.txt` *(PDF ต้นฉบับยังไม่มีในคลัง; ไฟล์ชื่อ `2025_Zhang_...pdf` เดิมเป็นงาน Basheer 2024 — ดู `_MISFILED_Basheer2024_GHG_agricultural_soil.pdf`)*

### `[24]`–`[31]` — §4.2.4 eNose + ML เพิ่มเติม

**[24]** Z. Ye, Y. Liu, Q. Li (2021). Recent Progress in Smart Electronic Nose Technologies Enabled with Machine Learning Methods. *Sensors*, 21(22), 7620. — `enose/2021_Ye_smart_eNose_machine_learning_review.pdf`

**[25]** J. Yin et al. (2023). Rapid Identification Method for CH₄/CO/CH₄-CO Gas Mixtures Based on Electronic Nose. *Sensors*, 23(6), 2975. — `enose/2023_Yin_eNose_CH4_CO_mixed_gas_identification.pdf`

**[26]** (2023). Application of Semiconductor Metal Oxide in Chemiresistive Methane Gas Sensor (review). — `enose/2023_MOS_chemiresistive_methane_sensor_review.pdf`

**[27]** B. Andrews et al. (2023). Application of Machine Learning for Calibrating Gas Sensors for Methane Emissions Monitoring. *Sensors*, 23(24), 9898. — `algorithm/2023_Andrews_ML_calibrating_gas_sensors_methane_emissions.pdf`

**[28]** H. L. Mitchell et al. (2024). Calibration of a Low-Cost Methane Sensor Using Machine Learning. *Sensors*, 24(4), 1066. — `algorithm/2024_Mitchell_Figaro_lowcost_methane_ML_calibration.pdf`

**[29]** R. Lakhmi et al. (2024). Linear and Non-Linear Modelling Methods for a Gas Sensor Array (CH₄). *Sensors*, 24(11), 3499. — `algorithm/2024_Lakhmi_linear_nonlinear_gas_sensor_array_CH4.pdf`

**[30]** M. Jiang et al. (2024). E-Nose: Time-Frequency Attention CNN for Gas Classification and Concentration Prediction. *Sensors*, 24(13), 4126. — `algorithm/2024_Jiang_TFA-CNN_gas_classification_concentration_prediction.pdf`

**[31]** D. Wang et al. (2024). Graph-Driven Models for Gas Mixture Concentration Estimation. *arXiv:2412.13891*. — `algorithm/2024_Wang_graph_models_gas_mixture_concentration_estimation.pdf`

---

## หมายเหตุตัวเลขที่ตรวจสอบผ่าน Firecrawl Research / PDF

| ตัวเลข | ค่า | ที่มา |
|--------|-----|-------|
| สัดส่วน CH₄ นาข้าวต่อ CH₄ มนุษย์โลก | ~10–12% (≈11% ของ 308 Tg/ปี) | [13], [14] |
| AWD ลด CH₄ (meta-analysis 47 งาน) | 64.5 ± 12.3% (เขตร้อน 68.2%, ดินเหนียว 71.3%) | [15] |
| AWD ลด GWP โดยรวม | ~42.1% | [15] |
| EENF+IS: ลด CH₄ ไฮบริด vs อินเบรด | 23.6% vs 8.2% | [19] |
| EENF+IS: late rice DRS / intermittent flooding | ↓40.6% / ↓24.9% | [19] |
| Vo TGA vs GC: ANOVA วิธีวัด / interaction | p = 0.47 / p = 0.728 | [21] |
| Vo TGA: R² > 0.9 ของข้อมูล / chamber time | ~90% / 4 นาที (เทียบ GC 30 นาที) | [21] |
| Vo throughput: multi-valve vs manual GC | >110 vs ~48 แปลง/วัน | [21] |
| Domènech-Gil eNose: RMSE / R² (field) | 33 ppb / 0.91 ที่ระดับ ~2 ppm | [10] |
| Domènech-Gil lab: R² / RMSE | >0.9 / <100 ppb (0–9 ppm) | [10] |
| Zhang ML นาข้าว: ประมาณฟลักซ์จากปัจจัยดิน (R²) / น้ำ–ดิน–อากาศ | 0.84 / 0.55 (Decision Tree Regressor; chamber เป็นข้อมูลอ้างอิง) | [23] |
| Wang graph models: R² | >0.96 (benchmark) | [31] |
