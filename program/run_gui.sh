#!/bin/bash
# run_gui.sh - Launcher script สำหรับ eNose GUI บน Raspberry Pi
# ใช้กับ XDG Autostart (~/.config/autostart/enose-gui.desktop)
#
# หน้าที่:
#   1. ตั้งค่า DISPLAY/XAUTHORITY สำหรับ Tkinter GUI (รองรับทั้ง X11 และ Wayland/Xwayland)
#   2. รอ X server :0 พร้อมจริง (max 60s)
#   3. หา Python interpreter (เลือก venv ก่อน, fallback เป็น python3 ระบบ)
#   4. รัน gui.py พร้อม retry ถ้า crash 1 ครั้ง
#   5. เก็บ log ไปที่ ~/enose_gui_autostart.log

set -u  # error เมื่อใช้ตัวแปรที่ไม่ได้กำหนดค่า

LOG_FILE="$HOME/enose_gui_autostart.log"
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $*" >> "$LOG_FILE"
}

log "==================== Starting eNose GUI launcher ===================="

# หา path โปรเจกต์จากตำแหน่งของ script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
log "SCRIPT_DIR=$SCRIPT_DIR"
log "PROJECT_DIR=$PROJECT_DIR"

cd "$PROJECT_DIR" || {
    log "ERROR: เข้า PROJECT_DIR ไม่ได้: $PROJECT_DIR"
    exit 1
}

# ตั้งค่า environment สำหรับ GUI
# ในกรณี Wayland (labwc) ที่ Pi OS Bookworm Tkinter จะใช้ Xwayland ผ่าน DISPLAY=:0
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
log "DISPLAY=$DISPLAY"
log "XAUTHORITY=$XAUTHORITY"

# รอ X server :0 พร้อมจริง (สำคัญสำหรับ autostart หลัง boot)
# พยายาม xset query ทุก 1 วินาที สูงสุด 60 ครั้ง
log "รอ X server $DISPLAY พร้อม..."
X_READY=0
for i in $(seq 1 60); do
    if command -v xset &> /dev/null; then
        if xset q &> /dev/null; then
            log "X server $DISPLAY พร้อมที่วินาทีที่ $i"
            X_READY=1
            break
        fi
    else
        # ถ้าไม่มี xset ให้ใช้ sleep 10 แบบเดิม
        sleep 10
        log "ไม่มี xset, ใช้ sleep 10 แทน"
        X_READY=1
        break
    fi
    sleep 1
done

if [ "$X_READY" -ne 1 ]; then
    log "WARNING: รอ X server $DISPLAY ครบ 60 วินาทีแล้วยังไม่พร้อม - ลองรัน GUI ต่อไป"
fi

# ค้นหา Python interpreter (เลือก venv ก่อน, fallback ระบบ)
VENV_CANDIDATES=(
    "$PROJECT_DIR/.venv/bin/python"
    "$SCRIPT_DIR/.venv/bin/python"
    "$HOME/.venv/bin/python"
)

PYTHON_BIN=""
for candidate in "${VENV_CANDIDATES[@]}"; do
    if [ -x "$candidate" ]; then
        PYTHON_BIN="$candidate"
        log "ใช้ venv Python: $PYTHON_BIN"
        break
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    if command -v python3 &> /dev/null; then
        PYTHON_BIN="$(command -v python3)"
        log "WARNING: ไม่พบ venv, fallback ไปใช้ python3 ระบบ: $PYTHON_BIN"
    else
        log "ERROR: ไม่พบ venv และไม่มี python3 ในระบบ"
        exit 1
    fi
fi

# ตรวจสอบไฟล์ GUI
GUI_FILE="$SCRIPT_DIR/gui.py"
if [ ! -f "$GUI_FILE" ]; then
    log "ERROR: ไม่พบไฟล์ GUI: $GUI_FILE"
    exit 1
fi

run_gui() {
    log "เริ่มรัน GUI: $PYTHON_BIN $GUI_FILE"
    "$PYTHON_BIN" "$GUI_FILE" >> "$LOG_FILE" 2>&1
    return $?
}

run_gui
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    log "ERROR: GUI exit ด้วย code $EXIT_CODE - รอ 5 วินาทีแล้ว retry"
    sleep 5
    run_gui
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        log "ERROR: GUI ล้มเหลวซ้ำ exit code $EXIT_CODE"
        exit $EXIT_CODE
    else
        log "GUI เริ่มสำเร็จในครั้งที่ 2"
    fi
else
    log "GUI exit ปกติ (code 0)"
fi
