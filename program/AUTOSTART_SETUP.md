# eNose GUI Autostart Setup (Raspberry Pi)

ตั้งค่าให้ `gui.py` รันอัตโนมัติทันทีเมื่อ Raspberry Pi เปิดเครื่อง

---

## วิธีหลัก: XDG Autostart (แนะนำ)

เหมาะกับ Raspberry Pi OS Bookworm + labwc/Wayland — เป็นทางที่ Pi OS รองรับโดยตรง

### ภาพรวม

```
Boot Pi
  -> Auto-Login as user pi
    -> labwc (Wayland compositor) start
      -> Desktop session ready
        -> XDG autostart scan ~/.config/autostart/
          -> เรียก enose-gui.desktop -> run_gui.sh
            -> รอ X server :0 / Xwayland พร้อม
              -> หา .venv/bin/python
                -> รัน gui.py
```

ข้อดี:
- เสถียรกับ labwc/Wayland (Pi OS Bookworm)
- Compatible ทั้ง X11 และ Wayland sessions
- ตั้งค่าง่าย — ไฟล์เดียวใน `~/.config/autostart/`
- ไม่มีปัญหา timing race condition กับ systemd target

---

## ไฟล์ที่เกี่ยวข้อง

| ไฟล์ | หน้าที่ |
|---|---|
| `program/gui.py` | ตัว GUI หลัก (ไม่ต้องแก้) |
| `program/run_gui.sh` | Launcher: รอ X พร้อม + หา venv + ตั้ง DISPLAY + รัน gui.py + retry |
| `program/enose-gui.desktop` | XDG autostart entry (จะถูก copy ไป `~/.config/autostart/`) |
| `program/install_xdg_autostart.sh` | สคริปต์ deploy ครบจบในขั้นตอนเดียว (วิธีหลัก) |
| `program/enose-gui.service` | systemd unit template (วิธีสำรอง — ดูส่วนล่าง) |
| `program/install_autostart.sh` | สคริปต์ deploy แบบ systemd (วิธีสำรอง) |

---

## Prerequisites

ก่อนติดตั้ง autostart ต้องเตรียมให้พร้อมก่อน

### 1. โครงสร้างโปรเจกต์บน Pi

วางโปรเจกต์ที่ `/home/pi/eNose_methane/` (path นี้ถูกระบุใน `enose-gui.desktop`)

```
/home/pi/eNose_methane/
├── .venv/                       <- virtual environment
├── program/
│   ├── gui.py
│   ├── run_gui.sh
│   ├── enose-gui.desktop
│   ├── enose-gui.service
│   ├── install_xdg_autostart.sh
│   ├── install_autostart.sh
│   └── ...
├── hardware_control/
├── reading/
└── acquisition/
```

> ถ้าใช้ path อื่น ต้องแก้ `Exec=` ใน `program/enose-gui.desktop` ก่อนติดตั้ง

### 2. เปิด Auto-Login เข้า Desktop

```bash
sudo raspi-config
```
ไป **System Options** -> **Boot / Auto Login** -> **Desktop Autologin**

### 3. เปิด I2C (สำหรับ BME280)

```bash
sudo raspi-config
```
ไป **Interface Options** -> **I2C** -> **Enable**

### 4. ติดตั้ง dependencies และสร้าง venv

```bash
cd /home/pi/eNose_methane

sudo apt update
sudo apt install -y python3-full python3-venv i2c-tools x11-xserver-utils

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

.venv/bin/python -m ensurepip --upgrade
.venv/bin/python -m pip install -r requirements-pi.txt

deactivate
```

> ใช้ `.venv/bin/python -m pip` เสมอ (บาง venv ไม่มีไฟล์ `pip` แยก) — อย่าใช้ `pip` ระดับระบบ (จะโดน PEP 668)

> `x11-xserver-utils` ให้คำสั่ง `xset` ที่ `run_gui.sh` ใช้รอ X server พร้อม

ตรวจว่าครบ:
```bash
.venv/bin/python -c "from adafruit_bme280.basic import Adafruit_BME280_I2C; import RPi.GPIO, matplotlib, pandas; print('OK')"
```

### 5. แก้ปัญหา CRLF (ถ้า edit ไฟล์ .sh จาก Windows)

ถ้ารัน `bash program/run_gui.sh` แล้วเห็น `$'\r': command not found` แปลว่าไฟล์เป็น **CRLF** — bash ต้องการเฉพาะ **LF**

```bash
file program/*.sh program/*.service program/*.desktop
```
ถ้าขึ้น "with CRLF line terminators" ให้แก้:
```bash
sed -i 's/\r$//' program/*.sh program/*.service program/*.desktop
```

หรือซิงก์โค้ดจาก repo ที่มี `.gitattributes` แล้ว `git pull`

---

## ติดตั้ง Autostart

### วิธีอัตโนมัติ (แนะนำ)

```bash
cd /home/pi/eNose_methane
chmod +x program/install_xdg_autostart.sh
./program/install_xdg_autostart.sh
```

สคริปต์จะ:
1. ตรวจไฟล์ครบไหม
2. หยุด + disable systemd service เดิม (ถ้ามี) เพื่อกันรันซ้อน
3. `chmod +x run_gui.sh`
4. Copy `enose-gui.desktop` ไป `~/.config/autostart/`

จากนั้น:
```bash
sudo reboot
```
GUI จะเด้งเองหลังเข้า Desktop ภายใน ~5–15 วินาที

### วิธีทำมือทีละขั้น

```bash
cd /home/pi/eNose_methane

# 1) chmod
chmod +x program/run_gui.sh

# 2) หยุด systemd เก่า (ถ้ามี)
systemctl --user stop enose-gui.service 2>/dev/null
systemctl --user disable enose-gui.service 2>/dev/null

# 3) Copy desktop file
mkdir -p ~/.config/autostart
cp program/enose-gui.desktop ~/.config/autostart/

# 4) ตรวจ
ls -la ~/.config/autostart/enose-gui.desktop

# 5) Reboot
sudo reboot
```

---

## ตรวจสอบและ Debug

### ดู log
```bash
tail -f ~/enose_gui_autostart.log
```

ที่ควรเห็นหลัง reboot:
```
==================== Starting eNose GUI launcher ====================
SCRIPT_DIR=/home/pi/eNose_methane/program
PROJECT_DIR=/home/pi/eNose_methane
DISPLAY=:0
XAUTHORITY=/home/pi/.Xauthority
รอ X server :0 พร้อม...
X server :0 พร้อมที่วินาทีที่ 3
ใช้ venv Python: /home/pi/eNose_methane/.venv/bin/python
เริ่มรัน GUI: /home/pi/eNose_methane/.venv/bin/python /home/pi/eNose_methane/program/gui.py
```

### ตรวจว่า gui.py process รันอยู่
```bash
ps aux | grep gui.py | grep -v grep
```

### ตรวจ X session
```bash
ps aux | grep -E "Xorg|Xwayland|labwc|wayfire" | grep -v grep
loginctl
echo "DISPLAY=$DISPLAY"
```

### รัน gui.py manual (ตรวจว่าโค้ดทำงานก่อนเข้า autostart)
```bash
cd /home/pi/eNose_methane
.venv/bin/python program/gui.py
```

---

## การจัดการ XDG Autostart

| งาน | คำสั่ง |
|---|---|
| ปิด autostart | `rm ~/.config/autostart/enose-gui.desktop` |
| เปิด autostart ใหม่ | รัน `./program/install_xdg_autostart.sh` |
| รัน manual ตอนนี้ | `~/eNose_methane/program/run_gui.sh &` |
| ปิด GUI ตอนนี้ | `pkill -f gui.py` |

---

## วิธีสำรอง: systemd User Service

> ⚠️ **ไม่แนะนำสำหรับ Pi OS Bookworm + labwc** เพราะ `graphical-session.target` ไม่ active ตอน boot ทำให้ service ไม่เริ่มอัตโนมัติ — เก็บไว้เผื่อใช้บน Pi OS รุ่นเก่า (Bullseye, X11) เท่านั้น

```bash
chmod +x program/install_autostart.sh
./program/install_autostart.sh
```

ดู `enose-gui.service` และ `install_autostart.sh` สำหรับรายละเอียด

---

## Troubleshooting

### GUI ไม่ขึ้นหลัง reboot

1. ตรวจไฟล์ desktop:
   ```bash
   cat ~/.config/autostart/enose-gui.desktop
   ```

2. ตรวจ permission:
   ```bash
   ls -la ~/.config/autostart/enose-gui.desktop
   ls -la /home/pi/eNose_methane/program/run_gui.sh
   ```
   `run_gui.sh` ต้องมี `x` (executable)

3. ตรวจ log:
   ```bash
   tail -100 ~/enose_gui_autostart.log
   ```

4. ทดสอบ run_gui.sh ตรงๆ บนหน้าจอ Pi:
   ```bash
   /home/pi/eNose_methane/program/run_gui.sh
   ```

### `ModuleNotFoundError`

แสดงว่า venv ไม่ถูกใช้งาน หรือยังไม่ได้ติดตั้งแพ็กเกจ:
```bash
ls -la /home/pi/eNose_methane/.venv/bin/python
.venv/bin/pip list | grep -i -E "rpi|adafruit|matplotlib|pandas"
```

ใน `~/enose_gui_autostart.log` ควรเห็นบรรทัด:
```
ใช้ venv Python: /home/pi/eNose_methane/.venv/bin/python
```
ถ้าเห็น `WARNING: ไม่พบ venv` แสดงว่ายังไม่ได้สร้าง venv ที่ path นี้

### `cannot connect to display` หรือ "X connection broken"

1. ตรวจว่า Auto-Login เปิดและ Pi เข้า Desktop จริง:
   ```bash
   ps aux | grep -E "Xorg|Xwayland|labwc" | grep -v grep
   ```
   ต้องเห็น process อย่างน้อย 1 ตัว

2. ตรวจ DISPLAY:
   ```bash
   echo $DISPLAY
   xset q
   ```

3. ถ้าทดสอบผ่าน SSH โดย Pi monitor ยังไม่ได้เข้า Desktop -> X server ไม่มีอยู่จริง -> ต้องไปดูที่หน้าจอก่อน

### CRLF line endings (พบบ่อยถ้า edit จาก Windows)

อาการ: `run_gui.sh: line N: $'\r': command not found` หรือ `syntax error near unexpected token $'{\r''` — bash บน Linux อ่านไฟล์ **CRLF** ไม่ได้

```bash
file program/*.sh program/*.desktop
```
ถ้า "with CRLF line terminators" -> แก้:
```bash
sed -i 's/\r$//' program/*.sh program/*.desktop
```

Repo มี `.gitattributes` (`*.sh text eol=lf`) เพื่อให้ Git checkout เป็น LF — หลัง `git pull` ควรไม่กลับมาเป็น CRLF ถ้า clone ใหม่บน Pi

Relay ในโปรเจกต์นี้ใช้ **Active HIGH** (GPIO สูง = ON) ผ่าน `hardware_control/hardware.py` — ถ้า ON/OFF กลับด้าน ให้ตรวจบอร์ด relay ว่าเป็นโมดูล Active HIGH หรือไม่

ตรวจ user `pi` อยู่ใน group `gpio` และ `i2c`:
```bash
groups pi
```
ควรมี `gpio` และ `i2c` (ค่าเริ่มต้นของ Raspberry Pi OS มีอยู่แล้ว)

ถ้าไม่มี:
```bash
sudo usermod -aG gpio,i2c pi
sudo reboot
```

### Log แสดง pandas ล้ม (`_pandas_datetime_CAPI` / `partially initialized module 'pandas'`)

ข้อความลักษณะนี้มักไม่ใช่ปัญหา autostart แต่เป็น **แพ็กเกจใน `.venv` เสียหรือ `numpy` กับ `pandas` ไม่เข้าคู่กัน** (รวมถึง Python 3.13 บน Pi ที่ต้องใช้ wheel ชุดใหม่)

**สิ่งที่ไม่ควรทำ:** ติดตั้ง `python3-pandas` ผ่าน `apt` แล้วคาดหวังให้ venv ใช้ร่วมกัน — ให้ติดตั้งเฉพาะใน venv

**แก้แบบสะอาด (บน Pi):**

```bash
cd ~/eNose_methane
. .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip uninstall -y pandas numpy
python -m pip install --no-cache-dir "numpy>=2.1.0" "pandas>=2.2.3" "matplotlib>=3.9.0"
python -c "import pandas as pd; import numpy as np; print('OK', pd.__version__, np.__version__)"
.venv/bin/python program/gui.py   # ทดสอบเปิด GUI ก่อน reboot
```

ถ้ายัง error ให้ลองติดตั้งชุดเต็มใหม่จาก repo:

```bash
.venv/bin/python -m pip install -r requirements-pi.txt
```

### มี autostart 2 ที่รันซ้อนกัน

ถ้าเคยติดตั้งทั้ง systemd และ XDG พร้อมกัน:
```bash
# ปิด systemd
systemctl --user stop enose-gui.service
systemctl --user disable enose-gui.service

# เก็บแค่ XDG
ls -la ~/.config/autostart/enose-gui.desktop
```

---

## ถอนการติดตั้ง autostart ทั้งหมด

```bash
# XDG
rm -f ~/.config/autostart/enose-gui.desktop

# systemd (ถ้าเคยติดตั้ง)
systemctl --user stop enose-gui.service 2>/dev/null
systemctl --user disable enose-gui.service 2>/dev/null
rm -f ~/.config/systemd/user/enose-gui.service
systemctl --user daemon-reload
sudo loginctl disable-linger pi
```
