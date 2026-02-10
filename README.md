# eNose Methane Detection System

ระบบควบคุมและเก็บข้อมูลจาก eNose (Electronic Nose) สำหรับตรวจจับก๊าซมีเทน บน Raspberry Pi

## ภาพรวมโปรเจกต์

โปรเจกต์นี้เป็นระบบควบคุม hardware และเก็บข้อมูลจากเซ็นเซอร์ eNose โดยใช้ ADS1263 ADC สำหรับอ่านค่าจากเซ็นเซอร์ 8 ช่อง พร้อมเซ็นเซอร์อุณหภูมิ/ความชื้นผ่าน RS485 Modbus RTU และควบคุมอุปกรณ์ 7 ตัว (Solenoid Valves, Pump, Fan, Heater) ผ่าน GPIO Relay

## ฟีเจอร์หลัก

- **GUI Control Interface** — หน้าจอควบคุมแบบกราฟิก (1024x600) พร้อม Scrollbar และ Responsive Scaling
- **2 โหมดการทำงาน**
  - **Manual Mode** — ควบคุมอุปกรณ์ด้วยตนเอง
  - **Auto Mode** — รันลำดับ 7 Operations อัตโนมัติพร้อม Loop
- **Data Collection** — เก็บข้อมูลจาก ADS1263 ADC (8 channels, 100 Hz) และอุณหภูมิ/ความชื้น (RS485)
- **Data Processing** — กรองข้อมูลด้วย Low-pass IIR Filter และ Moving Average
- **Hardware Control** — ควบคุม 7 Relay ผ่าน GPIO (Active LOW): s_valve1, s_valve2, s_valve3, s_valve4, pump, fan, heater
- **Simulation Mode** — รองรับการทดสอบโดยไม่ต้องมี hardware จริง (ตรวจจับ platform อัตโนมัติ)
- **Autostart** — รองรับการเริ่มทำงานอัตโนมัติเมื่อ Raspberry Pi boot

## โครงสร้างโปรเจกต์

```
eNose_methane/
├── program/                  # GUI และการตั้งค่า
│   ├── gui.py               # หน้าจอควบคุมหลัก (HardwareControlGUI)
│   ├── hardware_config.json # การตั้งค่า hardware (operation times, GPIO pins, auto settings)
│   ├── run_gui.sh           # Shell script สำหรับรัน GUI (รองรับ autostart)
│   └── enose-gui.desktop    # Desktop file สำหรับ autostart บน Raspberry Pi
│
├── reading/                  # การอ่านข้อมูลจาก ADC
│   ├── main.py              # SensorDataCollector — เก็บข้อมูล ADC 8 channels
│   ├── ADS1263.py           # Driver สำหรับ ADS1263 ADC (SPI)
│   ├── config.py            # การตั้งค่า SPI/GPIO สำหรับ ADC
│   ├── covert.py            # ฟังก์ชันแปลงข้อมูล
│   └── data/                # ไฟล์ข้อมูลดิบ (.npz)
│
├── acquisition/              # การประมวลผลข้อมูล
│   ├── acquisiton.py        # Low-pass Filter + Moving Average → CSV
│   └── processed_data/      # ไฟล์ข้อมูลที่ประมวลผลแล้ว (.csv)
│
├── hardware_control/         # ควบคุม Hardware
│   ├── hardware.py          # HardwareController Class — GPIO Relay Control
│   └── __init__.py
│
└── humid record/             # บันทึกอุณหภูมิและความชื้น
    ├── humid_logger.py      # RS485 Temperature/Humidity Logger → NPZ
    ├── humid.py             # RS485TempHumiditySensor Class (Modbus RTU / ASCII)
    └── data/                # ไฟล์ข้อมูลอุณหภูมิ/ความชื้น (.npz)
```

## การติดตั้ง

### ความต้องการของระบบ

- **Hardware**: Raspberry Pi (รองรับทั้ง hardware จริงและ simulation mode)
- **Python**: Python 3.x
- **Libraries**:
  - `tkinter` — GUI
  - `numpy` — การประมวลผลข้อมูล
  - `pandas` — จัดการข้อมูล
  - `RPi.GPIO` — ควบคุม GPIO (สำหรับ Raspberry Pi เท่านั้น)
  - `spidev` — SPI communication (สำหรับ Raspberry Pi เท่านั้น)
  - `pyserial` — RS485 Serial communication (สำหรับเซ็นเซอร์อุณหภูมิ/ความชื้น)

### การติดตั้ง Dependencies

สำหรับ Raspberry Pi:

```bash
sudo apt-get install python3-tk python3-numpy python3-pandas
sudo apt-get install python3-rpi.gpio python3-spidev python3-serial
```

สำหรับเครื่องอื่น (simulation mode):

```bash
pip install numpy pandas pyserial
```

## การตั้งค่า

### 1. Hardware Configuration (`program/hardware_config.json`)

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
| `heating` | เวลา Heating (วินาที) — ค่าเริ่มต้น 1800s (30 นาที) |
| `baseline` | เวลา Baseline (วินาที) — ค่าเริ่มต้น 30s |
| `vacuum` | เวลา Vacuum (วินาที) — ค่าเริ่มต้น 10s |
| `mix_air` | เวลา Mix Air (วินาที) — ค่าเริ่มต้น 10s |
| `measure` | เวลา Measure/เก็บข้อมูล (วินาที) — ค่าเริ่มต้น 60s |
| `vacuum_return` | เวลา Vacuum Return (วินาที) — ค่าเริ่มต้น 10s |
| `recovery` | เวลา Recovery (วินาที) — ค่าเริ่มต้น 60s |
| `break_time` | เวลาพัก Break (วินาที) — ค่าเริ่มต้น 1620s (27 นาที) |
| `loop_count` | จำนวนรอบ (0 = infinite) |
| `infinite_loop` | `true` = วน loop ไม่สิ้นสุด |

### 2. ADC Configuration (`reading/main.py`)

```python
REF = 5.08                    # Reference voltage
CHANNEL_LIST = [1, 2, 3, 4, 5, 6, 7, 8]  # ADC channels
SAMPLE_INTERVAL_SEC = 0.01    # 100 Hz sampling rate
ADC_SAMPLE_RATE = 'ADS1263_14400SPS'
```

### 3. Data Processing Configuration (`acquisition/acquisiton.py`)

```python
CUTOFF_FREQ = 50              # Hz (Low-pass filter cutoff)
MOVING_AVG_WINDOW = 1000      # Moving Average window size
```

### 4. Humidity Sensor Configuration (`humid record/humid_logger.py`)

```python
DEFAULT_SAMPLING_RATE_HZ = 1.0   # Sampling rate (Hz)
DEFAULT_BAUDRATE = 9600          # Baudrate
DEFAULT_SLAVE_ID = 1             # Modbus slave ID
```

## การใช้งาน

### รัน GUI

```bash
cd program
python3 gui.py
```

หรือใช้ script (รองรับ autostart):

```bash
./program/run_gui.sh
```

### โหมดการทำงาน

#### Manual Mode

1. เลือก "Manual Mode"
2. ใช้ปุ่ม ACTIVATE/DEACTIVATE เพื่อควบคุมอุปกรณ์แต่ละตัว (s_valve1-4, pump, fan, heater)
3. กด "Start Collection" เพื่อเริ่มเก็บข้อมูล ADC และอุณหภูมิ/ความชื้น
4. กด "Stop" เพื่อหยุดการทำงาน — ข้อมูลจะถูกบันทึกและประมวลผลอัตโนมัติ

#### Auto Mode

1. เลือก "Auto Mode"
2. ตั้งค่าเวลาทำงานของแต่ละ Operation (ปรับได้ผ่าน GUI)
3. ตั้งค่า Loop (Infinite หรือจำนวนรอบ)
4. กด "Start Auto Sequence" เพื่อเริ่มลำดับอัตโนมัติ

### ลำดับการทำงานใน Auto Mode (7 Operations)

```
Op1: Heating      (30 min)  → heater ON
Op2: Baseline     (30 sec)  → s_valve1 + s_valve3 + pump ON
Op3: Vacuum       (10 sec)  → s_valve3 + pump ON (ปิด s_valve1, seamless จาก Op2)
Op4: Mix Air      (10 sec)  → fan ON (ปิด s_valve3 + pump)
Op5: Measure      (60 sec)  → s_valve2 + pump ON → เริ่มเก็บข้อมูล ADC + อุณหภูมิ/ความชื้น
Op6: Vacuum Return(10 sec)  → s_valve4 + pump ON → หยุดเก็บข้อมูล + process_data (ขนาน)
Op7: Recovery     (60 sec)  → s_valve1 + s_valve3 + pump ON
Break Time        (27 min)  → ทั้งหมด OFF → วน loop
```

## ข้อมูลที่เก็บ

### 1. ADC Data (`reading/data/`)

| รายละเอียด | ค่า |
|---|---|
| รูปแบบ | `.npz` (NumPy compressed) |
| ข้อมูล | แรงดันจาก 8 channels + elapsed time |
| Sample Rate | 100 Hz |
| ชื่อไฟล์ | `adc1263_YYYYMMDD_HHMMSS.npz` |

### 2. Processed Data (`acquisition/processed_data/`)

| รายละเอียด | ค่า |
|---|---|
| รูปแบบ | `.csv` |
| ข้อมูล | ข้อมูลที่ผ่าน Low-pass IIR Filter + Moving Average |
| Columns | `elapsed_time_sec`, `ch1_voltage_lp_ma`, ..., `ch8_voltage_lp_ma` |
| ชื่อไฟล์ | `adc1263_YYYYMMDD_HHMMSS.csv` |

### 3. Temperature/Humidity Data (`humid record/data/`)

| รายละเอียด | ค่า |
|---|---|
| รูปแบบ | `.npz` (NumPy compressed) |
| ข้อมูล | อุณหภูมิ (C), ความชื้น (%RH), timestamps, metadata |
| Protocol | RS485 Modbus RTU / ASCII |
| ชื่อไฟล์ | `temperature_humidity_YYYYMMDD_HHMMSS.npz` |

## การประมวลผลข้อมูล

โปรแกรมจะประมวลผลข้อมูลอัตโนมัติหลังจาก:
- หยุดการเก็บข้อมูลใน Manual Mode
- เสร็จสิ้น Op5 (Measure) ใน Auto Mode — ทำงานขนานกับ Op6

**ขั้นตอนการประมวลผล:**
1. โหลดไฟล์ `.npz` ล่าสุดจาก `reading/data/`
2. กรองข้อมูลด้วย First-order IIR Low-pass Filter (cutoff 50 Hz)
3. กรองข้อมูลด้วย Moving Average (window=1000, center=True)
4. บันทึกเป็นไฟล์ `.csv` ใน `acquisition/processed_data/`

## คีย์บอร์ด Shortcuts

| คีย์ | การทำงาน |
|---|---|
| `F11` | สลับ Fullscreen mode |
| `ESC` | ออกจาก Fullscreen mode |

## Troubleshooting

### Permission Error (ไฟล์/โฟลเดอร์)

```bash
chmod 755 acquisition/processed_data
```

### GPIO Permission

```bash
sudo usermod -a -G gpio $USER
# ต้อง logout และ login ใหม่
```

### Serial Port Permission (สำหรับเซ็นเซอร์อุณหภูมิ/ความชื้น)

```bash
sudo usermod -a -G dialout $USER
# ต้อง logout และ login ใหม่
```

### Import Error

- ตรวจสอบว่าได้ติดตั้ง dependencies ครบแล้ว
- สำหรับ simulation mode: ไม่จำเป็นต้องมี `RPi.GPIO`, `spidev`, และ `pyserial`

## หมายเหตุ

- โปรแกรมรองรับ **Simulation Mode** สำหรับทดสอบโดยไม่ต้องมี hardware — ตรวจจับอัตโนมัติจาก platform
- Relay ทำงานแบบ **Active LOW** (GPIO LOW = ON, GPIO HIGH = OFF)
- GPIO จะถูก re-initialize อัตโนมัติถ้าถูก cleanup โดยโมดูลอื่น
- ไฟล์ที่ซ้ำจะถูกเพิ่ม timestamp เพื่อป้องกันการเขียนทับ
- GUI รองรับการ scale ตามขนาดหน้าต่าง (1024x600) พร้อม Scrollbar อัตโนมัติ
- `run_gui.sh` รองรับ autostart พร้อมระบบ retry และ logging

## Author

eNose Project

## License

โปรเจกต์นี้เป็นส่วนหนึ่งของงานวิจัย eNose สำหรับการตรวจจับก๊าซมีเทน
