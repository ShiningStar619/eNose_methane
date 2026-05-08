# eNose Methane Detection System

ระบบควบคุมและเก็บข้อมูลจาก eNose (Electronic Nose) สำหรับตรวจจับก๊าซมีเทน บน Raspberry Pi

## ภาพรวมโปรเจกต์

โปรเจกต์นี้เป็นระบบควบคุม hardware และเก็บข้อมูลจากเซ็นเซอร์ eNose โดยใช้:

- **ADS1263** (SPI) อ่านค่าก๊าซเซ็นเซอร์หลายช่องตามที่ตั้งใน `reading/main.py`
- **BME280** (I2C) อ่านอุณหภูมิ ความชื้น และความดันอากาศ คู่ขนานกับ ADC ผ่าน `reading/bme280.py`

และควบคุมอุปกรณ์ 7 ตัว (Solenoid Valves, Pump, Fan, Heater) ผ่าน **GPIO Relay** จาก GUI หลัก

## ฟีเจอร์หลัก

- **GUI Control Interface** — หน้าจอควบคุมแบบกราฟิก รองรับย่อ-ขยายตามหน้าต่าง พร้อม Scrollbar และมุมมองกราฟข้อมูล (ใช้ Matplotlib เมื่อติดตั้งครบ)
- **สองโหมดการทำงาน**
  - **Manual Mode** — ควบคุมอุปกรณ์ด้วยตนเอง และเริ่ม/หยุดเก็บข้อมูล ADC
  - **Auto Mode** — รันลำดับ 7 Operations อัตโนมัติ พร้อมช่วง Break และ Loop
- **Data Collection** — เก็บข้อมูลจาก:
  - **ADS1263** ตาม `CHANNEL_LIST` และ `SAMPLE_INTERVAL_SEC` ใน `reading/main.py` (ค่าเริ่มต้นปัจจุบัน: 4 ช่อง, ~100 Hz)
  - **BME280** ตาม `BME_SAMPLE_INTERVAL_SEC` ใน `reading/bme280.py` (ค่าเริ่มต้น: 10 Hz, อ่าน T/H/P)
  - ทั้งสองเซ็นเซอร์เริ่ม/หยุดพร้อมกัน (ใช้ `stop_event` ตัวเดียวกัน) และเก็บลงไฟล์ `.npz` แยกกัน
- **Data Processing** — กรองข้อมูลด้วย Low-pass IIR และ Moving Average แล้วบันทึกเป็น CSV (`acquisition/acquisiton.py`) — `process_all_data()` ประมวลผลทั้งไฟล์ ADC และ BME280 ของรอบล่าสุดในคำสั่งเดียว
- **Hardware Control** — ควบคุม 7 Relay ผ่าน GPIO (Active LOW): `s_valve1`, `s_valve2`, `s_valve3`, `s_valve4`, `pump`, `fan`, `heater`
- **Simulation Mode** — ทดสอบบนเครื่องที่ไม่มี ADC/BME280 จริง (ตรวจจับจากการ import `ADS1263` และ `adafruit_bme280`)
- **Autostart** — รองรับการเปิด GUI หลัง boot ผ่าน `run_gui.sh` และไฟล์ `.desktop` (รายละเอียดใน `program/AUTOSTART_SETUP.md`)

สคริปต์ทดสอบเซ็นเซอร์แยก เช่น `reading/testing BME280.py` ใช้สำหรับทดลองฮาร์ดแวร์เพียงไฟล์เดียว — เวอร์ชันที่ใช้จริงในระบบคือ `reading/bme280.py`

## โครงสร้างโปรเจกต์

```
eNose_methane/
├── program/                    # GUI และการตั้งค่า
│   ├── gui.py                  # หน้าจอควบคุมหลัก (HardwareControlGUI)
│   ├── hardware_config.json    # เวลาแต่ละ operation, GPIO, การวน loop
│   ├── run_gui.sh              # รัน GUI (รองรับ autostart)
│   ├── enose-gui.desktop       # ตัวอย่างไฟล์ autostart สำหรับ Desktop
│   └── AUTOSTART_SETUP.md      # คู่มือตั้งค่าเปิดอัตโนมัติบน Raspberry Pi
│
├── reading/                    # อ่านค่าเซ็นเซอร์และบันทึก NPZ
│   ├── main.py                 # SensorDataCollector / run_collection (ADS1263)
│   ├── bme280.py               # BMESensorDataCollector / run_bme_collection (BME280, I2C)
│   ├── ADS1263.py              # ไดรเวอร์ ADS1263 (SPI)
│   ├── config.py               # การตั้งค่า SPI/GPIO สำหรับ ADC
│   ├── covert.py               # ฟังก์ชันแปลงข้อมูล
│   └── data/                   # ไฟล์ดิบ .npz (`adc1263_*.npz`, `bme280_*.npz`)
│
├── acquisition/                # ประมวลผลหลังเก็บข้อมูล
│   ├── acquisiton.py           # Low-pass + Moving Average → CSV รองรับหลาย prefix (`process_all_data`)
│   └── processed_data/         # ไฟล์ .csv หลังประมวลผล (`adc1263_*.csv`, `bme280_*.csv`)
│
├── hardware_control/           # ชั้นควบคุม Relay
│   ├── hardware.py             # HardwareController
│   └── __init__.py
│
└── README.md
```

## การติดตั้ง

### ความต้องการของระบบ

- **Hardware**: Raspberry Pi สำหรับ SPI/GPIO จริง หรือโหมดจำลองบน PC
- **Python**: Python 3.x
- **ไลบรารีหลัก**:
  - `tkinter` — GUI
  - `numpy`, `pandas` — ข้อมูลและประมวลผล
  - `matplotlib` — แสดงกราฟใน GUI (ถ้าไม่ติดตั้ง บางส่วนของ GUI จะถูกปิดใช้)
  - `RPi.GPIO` — GPIO บน Raspberry Pi
  - `spidev` — SPI สำหรับ ADS1263 บน Raspberry Pi
  - `adafruit-circuitpython-bme280`, `adafruit-blinka` — I2C BME280 (ถ้าไม่ติดตั้งจะรันโหมดจำลอง BME280)

### การติดตั้ง Dependencies

บน Raspberry Pi (ตัวอย่าง):

```bash
sudo apt-get update
sudo apt-get install -y python3-tk python3-numpy python3-pandas python3-matplotlib
sudo apt-get install -y python3-rpi.gpio python3-spidev
pip install adafruit-circuitpython-bme280 adafruit-blinka
```

บนเครื่องพัฒนา (โหมดจำลอง ไม่มี ADC/BME280 จริง):

```bash
pip install numpy pandas matplotlib
```

## การตั้งค่า

### 1. Hardware Configuration (`program/hardware_config.json`)

ไฟล์นี้กำหนดระยะเวลาแต่ละขั้น (วินาที), แมป GPIO ของ relay และการตั้งค่า loop ใน Auto Mode  
ค่าตัวเลขจริงใน repo อาจถูกปรับเพื่อทดสอบสั้นๆ — แก้ให้ตรงกับงานจริงของคุณ

**โครงสร้างที่รองรับ:**

```json
{
    "operation_times": {
        "heating": 1800,
        "baseline": 30,
        "vacuum": 10,
        "mix_air": 10,
        "measure": 60,
        "vacuum_return": 10,
        "recovery": 60,
        "break_time": 1620
    },
    "gpio_pins": {
        "s_valve1": 5,
        "s_valve2": 6,
        "s_valve3": 13,
        "s_valve4": 19,
        "pump": 26,
        "fan": 20,
        "heater": 21
    },
    "auto_settings": {
        "loop_count": 0,
        "infinite_loop": true
    }
}
```

| พารามิเตอร์ | คำอธิบาย |
|---|---|
| `heating` … `recovery` | ระยะเวลาแต่ละ Operation ใน Auto Mode (วินาที) |
| `break_time` | เวลาพักระหว่างรอบ (วินาที) |
| `gpio_pins` | หมายเลข BCM ของแต่ละ relay |
| `loop_count` | จำนวนรอบเมื่อไม่ใช้ infinite (ใช้ร่วมกับ GUI) |
| `infinite_loop` | วนไม่สิ้นสุดเมื่อเป็น `true` |

### 2. ADC Configuration (`reading/main.py`)

```python
REF = 5.08
CHANNEL_LIST = [0, 1, 2, 3]   # ดัชนีช่อง ADC ที่ใช้ (ปรับจำนวนช่องได้)
SAMPLE_INTERVAL_SEC = 0.01    # ~100 Hz
ADC_SAMPLE_RATE = 'ADS1263_14400SPS'
INITIAL_BUFFER_SIZE = 1000
```

### 3. BME280 Configuration (`reading/bme280.py`)

```python
BME_SAMPLE_INTERVAL_SEC = 0.1   # 10 Hz
BME_I2C_ADDRESS = 0x76          # หรือ 0x77 ตาม jumper บนบอร์ด
BME_INITIAL_BUFFER_SIZE = 1000
```

อ่านค่า 3 ค่า: `temperature_c`, `humidity_pct`, `pressure_hpa` ผ่าน I2C  
เริ่ม/หยุดเก็บข้อมูลพร้อมกับ ADS1263 โดยใช้ `stop_event` ตัวเดียวกันใน GUI

### 4. Data Processing (`acquisition/acquisiton.py`)

```python
CUTOFF_FREQ = 50              # Hz (low-pass)
MOVING_AVG_WINDOW = 1000      # ขนาดหน้าต่าง moving average
```

## การใช้งาน

### รัน GUI

```bash
cd program
python3 gui.py
```

หรือ:

```bash
bash program/run_gui.sh
```

คู่มือตั้ง autostart: [program/AUTOSTART_SETUP.md](program/AUTOSTART_SETUP.md)

### Manual Mode

1. เลือก "Manual Mode"
2. ใช้ปุ่มควบคุมอุปกรณ์แต่ละตัว
3. กดปุ่มเริ่มเก็บข้อมูล (collection) ตามที่ GUI กำหนด
4. กดหยุด — ระบบจะบันทึกไฟล์ `.npz` และเรียกประมวลผลเป็น `.csv` (เมื่อโมดูล `acquisition` พร้อม)

### Auto Mode

1. เลือก "Auto Mode"
2. ตรวจสอบ/แก้เวลาแต่ละขั้นและ Break จาก GUI หรือจาก `hardware_config.json`
3. ตั้งค่า Loop (ไม่จำกัดหรือจำนวนรอบ)
4. เริ่มลำดับอัตโนมัติ

**การเก็บข้อมูลใน Auto Mode** (ทั้ง ADC และ BME280) เริ่มที่ **Op2: Baseline** (`start_collection` ใน `gui.py`) และรันต่อเนื่องจนจบรอบ จากนั้นระบบหยุดเก็บข้อมูล ปิดอุปกรณ์ และประมวลผล `process_all_data()` (ครอบคลุมทั้ง `adc1263_*.npz` และ `bme280_*.npz`) ก่อนเข้าช่วง Break (ถ้ามี)

### ลำดับ Auto Mode (7 Operations)

พฤติกรรม relay ในแต่ละขั้นถูกกำหนดใน `AUTO_OPERATION_STEPS` ใน `program/gui.py`  
**Heater** เปิดตั้งแต่ Op1 และจะไม่ถูกปิดด้วยคำสั่งของขั้นถัดไปจนกว่าจะจบรอบ (เพราะแต่ละขั้นเพิ่ม/ลดเฉพาะบางอุปกรณ์) — หลังจบ Op7 ระบบจะ `all_off()` ก่อนประมวลผล

| ขั้น | คำอธิบายโดยย่อ | หมายเหตุ |
|---|---|---|
| Op1 Heating | เปิด heater ปิดวาล์ว/ปั๊ม/พัดลมที่ไม่ใช้ | ระยะเวลา = `heating` |
| Op2 Baseline | เปิดบางวาล์ว + ปั๊ม | **เริ่มบันทึก ADC** |
| Op3 Vacuum | ปิดบางวาล์วตามลำดับ | ต่อเนื่องจาก Op2 |
| Op4 Mix Air | พัดลม + ปิดบางสายทาง | |
| Op5 Measure | วัด / เก็บข้อมูลต่อในขั้นนี้ | |
| Op6 Vacuum Return | ปรับวาล์วสำหรับดูดกลับ | |
| Op7 Recovery | กู้สภาพเส้นทางก๊าซ | จบรอบ → หยุดบันทึก + ประมวลผล |
| Break | ปิดทั้งหมดชั่วคราว | ระยะเวลา = `break_time` แล้ววนรอบใหม่ |

ระยะเวลาในตารางขึ้นกับค่าใน config ไม่ใช่คงที่

## ข้อมูลที่เก็บ

### 1. ADC Raw (`reading/data/`)

| รายละเอียด | ค่า |
|---|---|
| รูปแบบ | `.npz` (บีบอัด) |
| เนื้อหา | เวลา `elapsed_time_sec` + คอลัมน์เซ็นเซอร์ `ss1`, `ss2`, … ตามจำนวนช่อง |
| อัตรา sampling | จาก `1 / SAMPLE_INTERVAL_SEC` (บันทึกในไฟล์) |
| ชื่อไฟล์ | `adc1263_YYYYMMDD_HHMMSS.npz` |

### 2. BME280 Raw (`reading/data/`)

| รายละเอียด | ค่า |
|---|---|
| รูปแบบ | `.npz` (บีบอัด) |
| เนื้อหา | `elapsed_time_sec`, `temperature_c`, `humidity_pct`, `pressure_hpa` |
| อัตรา sampling | จาก `1 / BME_SAMPLE_INTERVAL_SEC` (เริ่มต้น 10 Hz) |
| ชื่อไฟล์ | `bme280_YYYYMMDD_HHMMSS.npz` |

### 3. Processed Data (`acquisition/processed_data/`)

| รายละเอียด | ค่า |
|---|---|
| รูปแบบ | `.csv` |
| เนื้อหา | `elapsed_time_sec` + คอลัมน์ที่ลงท้าย `_lp_ma` (low-pass แล้วเฉลี่ยเลื่อน) เช่น `ss1_lp_ma`, `temperature_c_lp_ma` |
| ชื่อไฟล์ | `adc1263_YYYYMMDD_HHMMSS.csv` (ADC) และ `bme280_YYYYMMDD_HHMMSS.csv` (BME280) |

## การประมวลผลข้อมูล

โปรแกรมจะประมวลผลอัตโนมัติเมื่อ:

- หยุดการเก็บข้อมูลใน Manual Mode (หลังบันทึก `.npz` ของทั้ง ADC และ BME280)
- จบรอบ Auto Mode ครบ 7 ขั้น — เรียก `process_all_data()` หลังหยุด collection

**ขั้นตอน:** สำหรับแต่ละ prefix (`adc1263`, `bme280`) จะโหลด `.npz` ล่าสุดที่ตรงกับ prefix นั้นจาก `reading/data/` → low-pass ตาม `CUTOFF_FREQ` และ sample rate ในไฟล์ → moving average → บันทึก CSV ใน `acquisition/processed_data/` ด้วยชื่อตาม prefix เดิม

รันมือจากโฟลเดอร์โปรเจกต์ (จะรันทั้งสอง prefix):

```bash
python3 acquisition/acquisiton.py
```

หากต้องการประมวลผลเฉพาะ prefix เดียว สามารถเรียกใน Python ได้:

```python
from acquisition.acquisiton import process_data
process_data(prefix="adc1263")  # หรือ "bme280"
```

## คีย์บอร์ด Shortcuts

| คีย์ | การทำงาน |
|---|---|
| `F11` | สลับโหมดเต็มจอ (ตามการผูกใน `gui.py`) |
| `ESC` | ออกจากสถานะเต็มจอ (ถ้ามีการผูกไว้) |

## Troubleshooting

### Permission (โฟลเดอร์ผลลัพธ์)

```bash
chmod 755 acquisition/processed_data
```

### GPIO

```bash
sudo usermod -a -G gpio $USER
# ออกจากระบบแล้วเข้าใหม่
```

### SPI / Serial (ถ้าใช้พอร์ตอนุกรม)

```bash
sudo usermod -a -G dialout $USER
```

### Import Error

- ติดตั้งแพ็กเกจตามหัวข้อ **การติดตั้ง**
- บน PC ที่ไม่มี `RPi.GPIO` / `spidev` ระบบจะรันโหมดจำลอง ADC ได้ (ดูข้อความใน console)

## หมายเหตุ

- Relay แบบ **Active LOW** (GPIO ต่ำ = ON)
- GUI ปรับขนาดฟอนต์และเลย์เอาต์ตามขนาดหน้าต่าง
- ถ้าชื่อไฟล์ผลลัพธ์ชนกัน ระบบจะเติม timestamp เพื่อไม่ทับของเดิม
- ชื่อไฟล์ `acquisiton.py` เป็นการสะกดตามที่มีใน repo (ถ้าจะเปลี่ยนชื่อควรอัปเดต import ใน `gui.py` ด้วย)

## Author

eNose Project

## License

โปรเจกต์นี้เป็นส่วนหนึ่งของงานวิจัย eNose สำหรับการตรวจจับก๊าซมีเทน
