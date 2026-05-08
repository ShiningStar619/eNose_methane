#!/bin/bash
# install_xdg_autostart.sh - ติดตั้ง XDG Autostart สำหรับ eNose GUI บน Raspberry Pi
#
# วิธีใช้ (รันบน Pi):
#   chmod +x program/install_xdg_autostart.sh
#   ./program/install_xdg_autostart.sh
#
# สคริปต์นี้จะ:
#   1. ตรวจสอบไฟล์ที่จำเป็น
#   2. หยุด + disable systemd user service เดิม (ถ้ามี) เพื่อกันรันซ้อน
#   3. ทำให้ run_gui.sh executable
#   4. Copy enose-gui.desktop ไปที่ ~/.config/autostart/
#   5. แสดงคำสั่งสำหรับตรวจ log

set -e

# ====== Path detection ======
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DESKTOP_SRC="$SCRIPT_DIR/enose-gui.desktop"
RUN_SCRIPT="$SCRIPT_DIR/run_gui.sh"

XDG_AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_DEST="$XDG_AUTOSTART_DIR/enose-gui.desktop"

echo "========================================"
echo " eNose GUI XDG Autostart Installer"
echo "========================================"
echo "PROJECT_DIR : $PROJECT_DIR"
echo "SCRIPT_DIR  : $SCRIPT_DIR"
echo ""

# ====== 1. ตรวจไฟล์ที่จำเป็น ======
echo "[1/4] ตรวจสอบไฟล์ที่จำเป็น..."
for f in "$DESKTOP_SRC" "$RUN_SCRIPT" "$SCRIPT_DIR/gui.py"; do
    if [ ! -f "$f" ]; then
        echo "  ERROR: ไม่พบไฟล์ $f"
        exit 1
    fi
    echo "  พบ: $f"
done

# ====== 2. หยุด + disable systemd service เดิม (ถ้ามี) ======
echo ""
echo "[2/4] ตรวจสอบ systemd user service เดิม..."
if systemctl --user list-unit-files 2>/dev/null | grep -q "^enose-gui.service"; then
    echo "  พบ enose-gui.service - หยุดและ disable เพื่อกันรันซ้อน"
    systemctl --user stop enose-gui.service 2>/dev/null || true
    systemctl --user disable enose-gui.service 2>/dev/null || true
    echo "  หยุด + disable เรียบร้อย (ไม่ลบไฟล์ unit)"
else
    echo "  ไม่มี systemd service เดิม - ข้าม"
fi

# ====== 3. chmod run_gui.sh ======
echo ""
echo "[3/4] ทำให้ run_gui.sh executable..."
chmod +x "$RUN_SCRIPT"
echo "  chmod +x $RUN_SCRIPT"

# ====== 4. Copy desktop entry ไป autostart folder ======
echo ""
echo "[4/4] ติดตั้ง XDG autostart entry..."
mkdir -p "$XDG_AUTOSTART_DIR"
cp "$DESKTOP_SRC" "$DESKTOP_DEST"
chmod +x "$DESKTOP_DEST"
echo "  Copy -> $DESKTOP_DEST"

# ====== สรุป ======
echo ""
echo "========================================"
echo " ติดตั้งสำเร็จ"
echo "========================================"
echo ""
echo "GUI จะเด้งอัตโนมัติหลัง reboot (รอ Desktop พร้อม + Xwayland ready)"
echo ""
echo "ทดสอบทันที (ที่หน้าจอ Pi):"
echo "  $RUN_SCRIPT &"
echo ""
echo "ทดสอบหลัง reboot:"
echo "  sudo reboot"
echo ""
echo "ดู log:"
echo "  tail -f ~/enose_gui_autostart.log"
echo ""
echo "ปิด autostart ชั่วคราว:"
echo "  rm $DESKTOP_DEST"
echo ""
echo "เปิดใหม่:"
echo "  $0"
echo ""
