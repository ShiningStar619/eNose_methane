# คู่มือการแก้ปัญหา Autostart

ถ้า GUI ไม่เปิดขึ้นมาหลังจาก reboot ให้ทำตามขั้นตอนนี้:

## 1. ตรวจสอบ Log File

สคริปต์จะสร้าง log file ที่ `~/enose_gui_autostart.log` เพื่อดู error:

```bash
cat ~/enose_gui_autostart.log
```

หรือดู log แบบ real-time:
```bash
tail -f ~/enose_gui_autostart.log
```

## 2. ตรวจสอบว่าไฟล์อยู่ใน autostart directory

```bash
ls -la ~/.config/autostart/
```

ควรเห็นไฟล์ `enose-gui.desktop` อยู่ที่นั่น

## 3. ตรวจสอบสิทธิ์ของไฟล์

```bash
# ตรวจสอบว่า script มีสิทธิ์ execute
ls -la /home/pi/eNose-/program/run_gui.sh

# ถ้าไม่มีสิทธิ์ ให้เพิ่มสิทธิ์
chmod +x /home/pi/eNose-/program/run_gui.sh

# ตรวจสอบว่าไฟล์ .desktop มีสิทธิ์อ่าน
ls -la ~/.config/autostart/enose-gui.desktop
```

## 4. ทดสอบรัน script โดยตรง

```bash
# รัน script โดยตรงเพื่อดู error
bash /home/pi/eNose-/program/run_gui.sh
```

ถ้า GUI เปิดขึ้นมา แสดงว่า script ทำงานได้ แต่ autostart อาจมีปัญหา

## 5. ตรวจสอบ Desktop Environment

```bash
# ตรวจสอบว่า Desktop Environment ทำงานอยู่
pgrep -x Xorg
pgrep -x wayland
pgrep -x xfce4-session
pgrep -x lxpanel

# ตรวจสอบ DISPLAY
echo $DISPLAY
```

ควรเห็น output จากคำสั่งเหล่านี้

## 6. ตรวจสอบ Path ในไฟล์ .desktop

```bash
cat ~/.config/autostart/enose-gui.desktop
```

ตรวจสอบว่า path ในบรรทัด `Exec=` ถูกต้อง:
- Path ต้องเป็น absolute path (เริ่มด้วย `/`)
- Path ต้องชี้ไปที่ไฟล์ `run_gui.sh` ที่ถูกต้อง
- ตรวจสอบว่า path มีอยู่จริง: `ls -la /home/pi/eNose-/program/run_gui.sh`

## 7. ทดสอบรัน GUI โดยตรง

```bash
# ตรวจสอบว่า GUI program ทำงานได้
cd /home/pi/eNose-
python3 program/gui.py
```

ถ้า GUI เปิดขึ้นมา แสดงว่าโปรแกรมทำงานได้

## 8. ตรวจสอบ Python และ Dependencies

```bash
# ตรวจสอบ Python version
python3 --version

# ตรวจสอบว่า Python modules ที่จำเป็นติดตั้งอยู่
python3 -c "import tkinter"
python3 -c "import hardware_control.hardware"
```

## 9. ตรวจสอบ System Logs

```bash
# ดู system logs
journalctl -f

# หรือดู logs ของ desktop session
journalctl --user -f
```

## 10. แก้ไขไฟล์ .desktop ให้แสดง Terminal

ถ้าต้องการดู error messages ให้แก้ไขไฟล์ `.desktop`:

```bash
nano ~/.config/autostart/enose-gui.desktop
```

เปลี่ยน `Terminal=false` เป็น `Terminal=true`

จากนั้น reboot อีกครั้ง จะเห็น terminal window เปิดขึ้นมาพร้อม error messages

## 11. ใช้วิธีทดสอบแบบ Manual

สร้างไฟล์ทดสอบใน autostart:

```bash
nano ~/.config/autostart/test.desktop
```

วางเนื้อหานี้:
```ini
[Desktop Entry]
Type=Application
Name=Test
Exec=/usr/bin/xterm -e "echo 'Autostart works!' && sleep 5"
Terminal=true
```

Reboot แล้วดูว่า terminal เปิดขึ้นมาหรือไม่

## 12. ตรวจสอบ Autostart Directory

บาง Desktop Environment อาจใช้ autostart directory ที่ต่างกัน:

- **LXDE**: `~/.config/autostart/`
- **XFCE**: `~/.config/autostart/`
- **GNOME**: `~/.config/autostart/`
- **KDE**: `~/.config/autostart/`

ตรวจสอบว่า Desktop Environment ของคุณใช้ directory ไหน

## 13. ใช้ Systemd Service แทน (ทางเลือก)

ถ้า Desktop Autostart ไม่ทำงาน ลองใช้ Systemd Service แทน:

ดูไฟล์ `enose-gui.service` ในโฟลเดอร์ `program/` สำหรับคำแนะนำ

## ปัญหาที่พบบ่อย:

### ปัญหา: "Permission denied"
**แก้ไข:**
```bash
chmod +x /home/pi/eNose-/program/run_gui.sh
```

### ปัญหา: "No such file or directory"
**แก้ไข:** ตรวจสอบ path ในไฟล์ `.desktop` ให้ถูกต้อง

### ปัญหา: "DISPLAY not set"
**แก้ไข:** Script จะตั้งค่า DISPLAY อัตโนมัติ แต่ถ้ายังมีปัญหา:
```bash
export DISPLAY=:0
```

### ปัญหา: Desktop Environment ยังไม่พร้อม
**แก้ไข:** Script จะรอให้ Desktop Environment พร้อม แต่ถ้ายังมีปัญหา ลองเพิ่มเวลา wait ใน script

### ปัญหา: Python modules ไม่พบ
**แก้ไข:** ตรวจสอบว่า dependencies ติดตั้งครบ:
```bash
pip3 list | grep -i tkinter
```

## ติดต่อขอความช่วยเหลือ:

ถ้ายังแก้ปัญหาไม่ได้ ให้ส่งข้อมูลต่อไปนี้:
1. เนื้อหาของ `~/enose_gui_autostart.log`
2. Output จาก `cat ~/.config/autostart/enose-gui.desktop`
3. Output จาก `ls -la /home/pi/eNose-/program/run_gui.sh`
4. Output จาก `python3 --version`
5. Desktop Environment ที่ใช้ (LXDE, XFCE, GNOME, etc.)
