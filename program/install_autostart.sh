#!/bin/bash
# install_autostart.sh - ติดตั้ง systemd user service สำหรับ eNose GUI บน Raspberry Pi
#
# วิธีใช้ (รันบน Pi เครื่องที่จะติดตั้ง):
#   chmod +x program/install_autostart.sh
#   ./program/install_autostart.sh
#
# สคริปต์นี้จะ:
#   1. ตรวจสอบสภาพแวดล้อม (path, ไฟล์ที่จำเป็น)
#   2. ลบ XDG autostart เดิม (ถ้ามี) เพื่อกันรันซ้อน
#   3. ทำให้ run_gui.sh executable
#   4. Copy enose-gui.service ไปที่ ~/.config/systemd/user/
#   5. enable-linger เพื่อให้ user service ทำงานหลัง boot
#   6. enable + start service
#   7. แสดงสถานะและคำสั่งสำหรับตรวจ log

set -e  # หยุดทันทีเมื่อมีคำสั่งใดล้มเหลว

# ====== Path detection ======
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_SRC="$SCRIPT_DIR/enose-gui.service"
RUN_SCRIPT="$SCRIPT_DIR/run_gui.sh"

USER_SYSTEMD_DIR="$HOME/.config/systemd/user"
SERVICE_DEST="$USER_SYSTEMD_DIR/enose-gui.service"
XDG_AUTOSTART="$HOME/.config/autostart/enose-gui.desktop"

echo "========================================"
echo " eNose GUI Autostart Installer"
echo "========================================"
echo "PROJECT_DIR : $PROJECT_DIR"
echo "SCRIPT_DIR  : $SCRIPT_DIR"
echo ""

# ====== 1. ตรวจไฟล์ที่จำเป็น ======
echo "[1/6] ตรวจสอบไฟล์ที่จำเป็น..."
for f in "$SERVICE_SRC" "$RUN_SCRIPT" "$SCRIPT_DIR/gui.py"; do
    if [ ! -f "$f" ]; then
        echo "  ERROR: ไม่พบไฟล์ $f"
        exit 1
    fi
    echo "  พบ: $f"
done

# ====== 2. ลบ XDG autostart เดิม (ถ้ามี) ======
echo ""
echo "[2/6] ตรวจ XDG autostart เดิม..."
if [ -f "$XDG_AUTOSTART" ]; then
    rm -f "$XDG_AUTOSTART"
    echo "  ลบ $XDG_AUTOSTART เพื่อกันรันซ้อน"
else
    echo "  ไม่มี XDG autostart เดิม - ข้าม"
fi

# ====== 3. chmod run_gui.sh ======
echo ""
echo "[3/6] ทำให้ run_gui.sh executable..."
chmod +x "$RUN_SCRIPT"
echo "  chmod +x $RUN_SCRIPT"

# ====== 4. Copy systemd service ======
echo ""
echo "[4/6] ติดตั้ง systemd user service..."
mkdir -p "$USER_SYSTEMD_DIR"
cp "$SERVICE_SRC" "$SERVICE_DEST"
echo "  Copy -> $SERVICE_DEST"

# ====== 5. Enable linger (ให้ user service start หลัง boot) ======
echo ""
echo "[5/6] เปิด linger สำหรับ user $USER..."
if loginctl show-user "$USER" 2>/dev/null | grep -q "Linger=yes"; then
    echo "  Linger เปิดอยู่แล้ว - ข้าม"
else
    sudo loginctl enable-linger "$USER"
    echo "  เปิด linger สำเร็จ"
fi

# ====== 6. Reload + enable + start ======
echo ""
echo "[6/6] เปิดใช้งาน service..."
systemctl --user daemon-reload
systemctl --user enable enose-gui.service
systemctl --user restart enose-gui.service
echo "  daemon-reload + enable + restart สำเร็จ"

# ====== สรุป ======
echo ""
echo "========================================"
echo " ติดตั้งสำเร็จ"
echo "========================================"
echo ""
echo "ตรวจสอบสถานะ:"
echo "  systemctl --user status enose-gui.service"
echo ""
echo "ดู log แบบ realtime:"
echo "  journalctl --user -u enose-gui.service -f"
echo "  tail -f ~/enose_gui_autostart.log"
echo "  tail -f ~/enose_gui_systemd.log"
echo ""
echo "ทดสอบ reboot:"
echo "  sudo reboot"
echo ""
echo "ปิด autostart ชั่วคราว:"
echo "  systemctl --user stop enose-gui.service"
echo ""
echo "ปิด autostart ถาวร:"
echo "  systemctl --user disable enose-gui.service"
echo ""
