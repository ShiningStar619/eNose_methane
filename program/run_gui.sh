#!/bin/bash
# สคริปต์สำหรับรัน eNose GUI เมื่อ Raspberry Pi boot เสร็จ

# สร้าง log file สำหรับ debug
LOG_FILE="$HOME/enose_gui_autostart.log"
echo "$(date): Starting eNose GUI autostart script" >> "$LOG_FILE"

# หา path ของโปรเจกต์ (parent directory ของ script นี้)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "$(date): Script directory: $SCRIPT_DIR" >> "$LOG_FILE"
echo "$(date): Project directory: $PROJECT_DIR" >> "$LOG_FILE"

# เปลี่ยนไปที่ directory ของโปรเจกต์
cd "$PROJECT_DIR" || {
    echo "$(date): ERROR: Cannot change to project directory: $PROJECT_DIR" >> "$LOG_FILE"
    exit 1
}

# รอให้ระบบ boot เสร็จ (รอ 10 วินาที แล้วเริ่ม GUI)
echo "$(date): Waiting 10 seconds after boot..." >> "$LOG_FILE"
sleep 10

# ตั้งค่า DISPLAY สำหรับ GUI
export DISPLAY=:0
export XAUTHORITY="$HOME/.Xauthority"
echo "$(date): DISPLAY set to: $DISPLAY" >> "$LOG_FILE"

# ตรวจสอบว่า Python3 พร้อม
if ! command -v python3 &> /dev/null; then
    echo "$(date): ERROR: python3 not found" >> "$LOG_FILE"
    exit 1
fi

echo "$(date): Python3 found: $(which python3)" >> "$LOG_FILE"

# ตรวจสอบว่าไฟล์ GUI มีอยู่
if [ ! -f "$SCRIPT_DIR/gui.py" ]; then
    echo "$(date): ERROR: GUI file not found: $SCRIPT_DIR/gui.py" >> "$LOG_FILE"
    exit 1
fi

echo "$(date): Starting GUI program..." >> "$LOG_FILE"

# รัน GUI program
python3 "$SCRIPT_DIR/gui.py" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "$(date): ERROR: GUI program exited with code $EXIT_CODE" >> "$LOG_FILE"
    echo "$(date): Waiting 5 seconds before retry..." >> "$LOG_FILE"
    sleep 5
    echo "$(date): Retrying GUI program..." >> "$LOG_FILE"
    python3 "$SCRIPT_DIR/gui.py" >> "$LOG_FILE" 2>&1
    RETRY_EXIT_CODE=$?
    if [ $RETRY_EXIT_CODE -ne 0 ]; then
        echo "$(date): ERROR: GUI program failed again with code $RETRY_EXIT_CODE" >> "$LOG_FILE"
    else
        echo "$(date): GUI program started successfully on retry" >> "$LOG_FILE"
    fi
else
    echo "$(date): GUI program started successfully" >> "$LOG_FILE"
fi
