# คู่มือการตั้งค่า Autostart สำหรับ eNose GUI

วิธีนี้จะทำให้โปรแกรม GUI รันอัตโนมัติเมื่อ Raspberry Pi boot เสร็จ

## วิธีที่ 1: ใช้ Desktop Autostart (แนะนำ)

วิธีนี้เหมาะสำหรับ Raspberry Pi ที่มี Desktop Environment

### ขั้นตอนการติดตั้ง:

1. **แก้ไข path ในไฟล์ `enose-gui.desktop` ให้ตรงกับตำแหน่งโปรเจกต์ของคุณ:**
   ```bash
   nano /home/pi/eNose-/program/enose-gui.desktop
   ```
   
   แก้ไขบรรทัด `Exec=` ให้ชี้ไปที่ path ที่ถูกต้อง:
   ```ini
   Exec=/home/pi/eNose-/program/run_gui.sh
   ```
   (เปลี่ยน `/home/pi/eNose-` เป็น path จริงของโปรเจกต์บน Raspberry Pi)

2. **ให้สิทธิ์ execute แก่ shell script:**
   ```bash
   chmod +x /home/pi/eNose-/program/run_gui.sh
   ```

3. **สร้างโฟลเดอร์ autostart (ถ้ายังไม่มี):**
   ```bash
   mkdir -p ~/.config/autostart
   ```

4. **คัดลอกไฟล์ .desktop ไปยัง autostart directory:**
   ```bash
   cp /home/pi/eNose-/program/enose-gui.desktop ~/.config/autostart/
   ```

5. **ทดสอบการรัน script:**
   ```bash
   /home/pi/eNose-/program/run_gui.sh
   ```
   ถ้า GUI เปิดขึ้นมา แสดงว่าทำงานถูกต้อง

6. **รีสตาร์ท Raspberry Pi เพื่อทดสอบ autostart:**
   ```bash
   sudo reboot
   ```

## การตรวจสอบ:

- **ตรวจสอบว่าไฟล์อยู่ใน autostart:**
  ```bash
  ls -la ~/.config/autostart/
  ```

- **ดู logs (ถ้ามีปัญหา):**
  ```bash
  journalctl -f
  ```

- **ตรวจสอบว่า Desktop Environment ทำงานอยู่:**
  ```bash
  pgrep -x Xorg
  # หรือ
  pgrep -x wayland
  ```

## การแก้ปัญหา:

### GUI ไม่เปิดขึ้นมา:
- ตรวจสอบว่า Desktop Environment ทำงานอยู่
- ตรวจสอบ DISPLAY environment variable: `echo $DISPLAY`
- ตรวจสอบ path ในไฟล์ `.desktop` ว่าถูกต้องหรือไม่
- ดู logs: `journalctl -f`

### Permission denied:
- ให้สิทธิ์ execute: `chmod +x program/run_gui.sh`
- ตรวจสอบว่าไฟล์ `.desktop` มีสิทธิ์อ่าน: `chmod 644 ~/.config/autostart/enose-gui.desktop`

### Path ไม่ถูกต้อง:
- ตรวจสอบ path ทั้งหมดในไฟล์ config
- ใช้ `pwd` เพื่อดู path ปัจจุบัน
- ใช้ `ls -la` เพื่อตรวจสอบว่าไฟล์อยู่ที่ไหน

### Script ไม่ทำงาน:
- ทดสอบรัน script โดยตรง: `bash /home/pi/eNose-/program/run_gui.sh`
- ตรวจสอบว่า Python3 ติดตั้งอยู่: `python3 --version`
- ตรวจสอบว่า GUI program ทำงานได้: `python3 /home/pi/eNose-/program/gui.py`

## หมายเหตุสำคัญ:

- **Path:** ต้องแก้ไข path ในไฟล์ `enose-gui.desktop` ให้ตรงกับตำแหน่งโปรเจกต์ของคุณบน Raspberry Pi
- **Username:** ถ้า username ไม่ใช่ `pi` ต้องแก้ไข path ในไฟล์ `.desktop`
- **Display:** GUI ต้องการ display environment ถ้าใช้ headless อาจต้องใช้ X11 forwarding หรือ VNC
- **Permissions:** ต้องให้สิทธิ์ execute แก่ shell script (`chmod +x`)

## การปิดการใช้งาน Autostart:

ถ้าต้องการปิดการใช้งาน autostart ชั่วคราว:
```bash
mv ~/.config/autostart/enose-gui.desktop ~/.config/autostart/enose-gui.desktop.disabled
```

ถ้าต้องการเปิดใช้งานอีกครั้ง:
```bash
mv ~/.config/autostart/enose-gui.desktop.disabled ~/.config/autostart/enose-gui.desktop
```

หรือลบไฟล์ออก:
```bash
rm ~/.config/autostart/enose-gui.desktop
```
