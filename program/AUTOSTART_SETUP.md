# คู่มือการตั้งค่า Autostart สำหรับ eNose GUI

วิธีนี้จะทำให้โปรแกรม GUI รันอัตโนมัติเมื่อ Raspberry Pi boot เสร็จ

## วิธีที่ 1: ใช้ Desktop Autostart (แนะนำ)

วิธีนี้เหมาะสำหรับ Raspberry Pi ที่มี Desktop Environment

### ขั้นตอนการติดตั้ง:

1. **แก้ไข path ในไฟล์ `enose-gui.desktop` ให้ตรงกับตำแหน่งโปรเจกต์บน Pi:**
   - เปิดไฟล์แล้วแก้บรรทัด `Exec=` ให้ชี้ไปที่ path จริง เช่น:
   ```ini
   Exec=/home/pi/eNose_Methane/program/run_gui.sh
   ```
   (เปลี่ยน `/home/pi/eNose_Methane` เป็น path โปรเจกต์จริงบน Raspberry Pi)

2. **แก้ line ending ของ `run_gui.sh` (ถ้าแก้ไขไฟล์บน Windows):**
   ```bash
   sed -i 's/\r$//' /home/pi/eNose_Methane/program/run_gui.sh
   ```
   หรือถ้าติดตั้ง dos2unix: `dos2unix /home/pi/eNose_Methane/program/run_gui.sh`

3. **ให้สิทธิ์ execute แก่ shell script:**
   ```bash
   chmod +x /home/pi/eNose_Methane/program/run_gui.sh
   ```

4. **สร้างโฟลเดอร์ autostart (ถ้ายังไม่มี):**
   ```bash
   mkdir -p ~/.config/autostart
   ```

5. **คัดลอกไฟล์ .desktop ไปยัง autostart:**
   ```bash
   cp /home/pi/eNose_Methane/program/enose-gui.desktop ~/.config/autostart/
   ```
   (ใช้ path โปรเจกต์จริงของคุณ)

6. **ทดสอบการรัน script:**
   ```bash
   bash /home/pi/eNose_Methane/program/run_gui.sh
   ```
   ถ้า GUI เปิดขึ้นมา แสดงว่าพร้อมใช้

7. **รีสตาร์ท Raspberry Pi เพื่อทดสอบ autostart:**
   ```bash
   sudo reboot
   ```
   หลัง boot และล็อกอินเข้า Desktop แล้ว GUI ควรเปิดขึ้นอัตโนมัติ

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
- ทดสอบรัน script โดยตรง: `bash /home/pi/eNose_Methane/program/run_gui.sh`
- ถ้าเห็น error `$'\r': command not found` แสดงว่า line ending เป็น CRLF ให้รัน: `sed -i 's/\r$//' /home/pi/eNose_Methane/program/run_gui.sh`
- ตรวจสอบว่า Python3 ติดตั้งอยู่: `python3 --version`
- ตรวจสอบว่า GUI ทำงานได้: `python3 /home/pi/eNose_Methane/program/gui.py`

## หมายเหตุสำคัญ:

- **Path:** ต้องแก้ path ใน `enose-gui.desktop` (และในคำสั่งด้านบน) ให้ตรงกับโปรเจกต์บน Pi (เช่น `/home/pi/eNose_Methane`)
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
