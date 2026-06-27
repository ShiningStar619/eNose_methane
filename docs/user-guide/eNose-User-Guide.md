# คู่มือผู้ใช้ eNose Methane

คู่มือสำหรับผู้ใช้งาน GUI บน Raspberry Pi — ใช้วัดก๊าซมีเทนและอ่านค่า ppm  
โปรแกรมชื่อ **eNose Hardware Control**

---

## 1. ก่อนเริ่มใช้งาน

เครื่อง eNose อ่านสัญญาณจากเซ็นเซอร์ บันทึกข้อมูล ประมวลผลเป็น CSV แล้วแสดงความเข้มข้น **ppm มีเทน** บนหน้าจอ

**สิ่งที่ต้องพร้อมก่อนใช้งาน**

- Raspberry Pi เปิดเครื่องแล้ว
- มีจอภาพต่อกับ Pi หรือเชื่อม VNC ไปที่ Desktop
- หน้าต่าง GUI เปิดอยู่
- ตัวอย่างก๊าซและระบบท่อพร้อม (ตามขั้นตอนห้องแล็บ)

**วิธีเปิด GUI** (กรณียังไม่เห็นหน้าต่าง): เปิด Terminal บน Desktop ของ Pi แล้วรัน

```bash
cd ~/eNose_methane
bash program/run_gui.sh
```

> ต้องรันบนจอ Desktop ของ Pi — ถ้าเข้าผ่าน SSH อย่างเดียวโดยไม่มี display จะเปิด GUI ไม่ได้

---

## 2. วัดครั้งแรก (โหมด Auto)

งานวัดปกติใช้โหมด **Auto** ระบบจะรันครบ 7 ขั้นให้อัตโนมัติ (ขั้น Heating ในงานจริงอาจใช้เวลานานประมาณ 30 นาที)

**ก่อนกด Start:** เลือก Auto แล้ว · ตั้งค่าเวลาในหน้า Settings และกด **Save Config** · อย่ากด Stop ระหว่างวัด

| ขั้น | การทำงาน |
|------|----------|
| 1 | ไปหน้า **Control** แล้วกด **Auto** |
| 2 | ไปหน้า **Settings** ตรวจเวลาแต่ละขั้น Break และ Loop จากนั้นกด **Save Config** |
| 3 | กลับหน้า **Control** แล้วกด **Start Auto Sequence** |
| 4 | ดู **Operation Sequence** จนครบ Op1 ถึง Op7 |
| 5 | อ่านค่า **Methane (ppm)** หรือไปหน้า **Display** แล้วกด **Refresh Graph** |

![ภาพรวมหน้า Control — โหมด Auto](assets/screenshots/02-control-overview.png){.fig-main}

![เลือกโหมด Auto](assets/screenshots/03-select-auto.png){.fig-step}

![หน้า Settings — ตั้งค่าและ Save Config](assets/screenshots/04-settings-full.png){.fig-main}

![ระหว่างวัด — Operation Sequence และตัวนับเวลา](assets/screenshots/08-sequence-running.png){.fig-step}

| สิ่งที่เห็นบนจอ | ความหมาย |
|----------------|----------|
| `Heat → BL → Vac → Mix → Meas → VR → Rec` | ลำดับขั้นตอนทั้ง 7 ขั้น |
| `Op2: Baseline [Recording]` | ขั้นปัจจุบัน — กำลังบันทึกข้อมูล |
| ตัวเลขถอยหลัง | เวลาที่เหลือในขั้นนั้น |

![ผลการวัด — ค่า Methane (ppm)](assets/screenshots/09-methane-result.png){.fig-result}

**กรณีหยุดฉุกเฉิน:** กด **Stop** (ปุ่มสีแดง) ระบบจะบันทึกและประมวลผลข้อมูลที่เก็บได้จนถึงขณะนั้น

---

## 3. หน้าจอ GUI

สลับหน้าได้จากแถบด้านล่างขวา: **Control** · **Display** · **Settings**  
คีย์ลัด: **F11** ขยายเต็มจอ · **ESC** ออกจากเต็มจอ

### หน้า Control

| ส่วน | รายละเอียด |
|------|------------|
| Manual / Auto | Manual = ควบคุม relay เอง · Auto = วัดอัตโนมัติ |
| Hardware Controls | Value 1–4 (วาล์ว) Pump Fan Heater — สีเขียว = เปิด (ใช้ใน Manual เท่านั้น) |
| Operation Sequence | แสดงขั้นปัจจุบันและเวลาถอยหลัง (โหมด Auto) |
| Start / Stop | Auto: Start Auto Sequence · Manual: Start Collection |
| Methane | แสดง `----` เมื่อยังไม่มีผล · ตัวเลข = ค่า ppm โดยประมาณ |

### หน้า Display

แสดงกราฟ Process Data ค่า ppm และปุ่ม **Refresh Graph** (กดหลังจบรอบวัด)

![หน้า Display และกราฟ Process Data](assets/screenshots/10-display-graph.png){.fig-main}

### หน้า Settings

ใช้ตั้งเวลา 7 ขั้น Break Loop Cloud และบันทึกด้วย **Save Config** (รายละเอียดในหัวข้อ 4)

---

## 4. การตั้งค่า (Settings)

**Parameter Source:** เลือก **Input from UI** แก้ค่าบนหน้าจอ แล้วกด **Save Config** (บันทึกลง `program/hardware_config.json`)

- ระยะเวลาแต่ละขั้นหน่วยเป็น **วินาที**
- ใส่ **0** เพื่อข้ามขั้นนั้น
- **Heater** เปิดตั้งแต่ Op1 และทำงานตลอดจนจบรอบ

| ขั้น | อุปกรณ์ที่เปิดเพิ่ม (นอกจาก Heater) | บันทึกข้อมูล |
|------|--------------------------------------|--------------|
| Op1 Heating | — | ไม่บันทึก |
| Op2 Baseline | Value 2, Value 3, Pump | **เริ่มบันทึก** |
| Op3 Vacuum | Value 3, Pump | ต่อเนื่อง |
| Op4 Mix Air | Fan | ต่อเนื่อง |
| Op5 Measure | Value 1, Value 4, Pump | ต่อเนื่อง |
| Op6 Vac Return | Value 4, Pump | ต่อเนื่อง |
| Op7 Recovery | Value 2, Value 3 | ต่อเนื่อง แล้วประมวลผล |

![แผนภาพลำดับ Auto Mode](assets/diagrams/auto-sequence-flow.svg){.fig-diagram}

> ข้อความย่อบนหน้า Settings (เช่น Baseline = SV1+SV3) อาจไม่ตรงกับ relay จริง — ให้อ้างอิงตารางด้านบน

**Break** — ช่วงพักหลังจบรอบ: Heater ยังเปิด วาล์ว ปั๊ม และพัดลมปิด

**Loop** — เปิด Infinite Loop = วนวัดต่อเนื่องจนกด Stop · ปิด = ใช้ Cycles กำหนดจำนวนรอบ

**Cloud** — ติ๊ก Auto-upload เมื่อผู้ดูแลระบบตั้งค่า Google Drive แล้ว · แสดง `Cloud: —` หมายถึงยังไม่ได้ตั้งค่า

---

## 5. โหมด Manual

ใช้เมื่อทดสอบ hardware หรือทำขั้นตอนพิเศษ (งานวัดทั่วไปใช้ Auto)

1. หน้า **Control** → กด **Manual**
2. (ถ้าต้องการ) คลิก Hardware Controls หรือติ๊ก Use Timer
3. กด **Start Collection** → กด **Stop** เมื่อเสร็จ

![โหมด Manual — Hardware Controls](assets/screenshots/13-manual-mode.png){.fig-step}

---

## 6. ผลลัพธ์และไฟล์ข้อมูล

| บนหน้าจอ | ความหมาย |
|----------|----------|
| `----` | ยังประมวลผลไม่เสร็จหรือยังวัดไม่จบ |
| ตัวเลข ppm | ค่าประมาณจากโมเดล ML — ไม่ใช่มาตรฐานอ้างอิงทางกฎหมาย |

| ประเภทไฟล์ | ตำแหน่งเก็บ |
|------------|-------------|
| ข้อมูลดิบ `.npz` | `reading/data/` |
| ข้อมูลหลังประมวลผล `.csv` | `acquisition/processed_data/` |

**นำข้อมูลออกจาก Pi:** ใช้ Cloud Upload คัดลอกลง USB หรือ SCP (ให้ผู้ดูแลระบบช่วย) — GUI ไม่มีปุ่ม Export

---

## 7. แก้ปัญหาเบื้องต้น

| อาการ | วิธีแก้ |
|-------|---------|
| GUI ไม่เปิด | ใช้จอ Pi หรือ VNC ไป Desktop → รัน `bash program/run_gui.sh` |
| ค่า ppm แสดง `----` | รอให้ครบ Op1–Op7 · ตรวจไฟล์ CSV ใน `processed_data/` · ปรับเวลา Baseline/Measure |
| กราฟไม่แสดง | กด Refresh Graph หลังจบรอบ · ให้ผู้ดูแลติดตั้ง matplotlib |
| ลำดับขั้นค้าง | ขั้น Heating อาจใช้เวลานาน — ดูตัวนับเวลา · ถ้าค้างจริงให้กด Stop |
| แสดง Cloud: — | ยังไม่ตั้งค่า Drive — ข้อมูลยังอยู่ใน Pi ตามปกติ |
| ไม่มีไฟล์ข้อมูล | ต้องกด Start ก่อน · Auto เริ่มบันทึกที่ Op2 · อย่าปิด Pi ก่อนกด Stop |

---

## คำศัพท์

| คำใน GUI | ความหมาย |
|---------|----------|
| Value 1–4 | Solenoid Valve (วาล์วโซลินอยด์) |
| Pump / Fan / Heater | ปั๊มสูญญากาศ / พัดลม / ฮีตเตอร์ |
| ppm | parts per million — ค่าความเข้มข้นมีเทนโดยประมาณ |
| Op1–Op7 | ขั้นตอนในโหมด Auto |
| Break | ช่วงพักระหว่างรอบวัด (Heater ยังเปิดอยู่) |
