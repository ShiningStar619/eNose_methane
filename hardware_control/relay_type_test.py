"""
Relay Type Test Script (Active LOW / Active HIGH)
=================================================
สคริปต์นี้ช่วยตรวจสอบว่ารีเลย์บอร์ดของคุณเป็นชนิดใด โดยสลับสัญญาณ LOW/HIGH
แล้วให้ผู้ใช้สังเกตเสียงคลิก/ไฟ LED/สถานะโหลดจริง

Usage:
    python hardware_control/relay_type_test.py
    python hardware_control/relay_type_test.py --channel pump
    python hardware_control/relay_type_test.py --seconds 2.0
"""

import argparse
import json
import os
import sys
import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "program", "hardware_config.json")

DEFAULT_GPIO_PINS = {
    "s_valve1": 5,
    "s_valve2": 6,
    "s_valve3": 13,
    "s_valve4": 19,
    "pump": 26,
    "fan": 20,
    "heater": 21,
}


def load_gpio_pins():
    """Load GPIO mapping from config file (fallback to defaults)."""
    if not os.path.exists(CONFIG_FILE):
        print(f"[WARN] Config not found, using defaults: {CONFIG_FILE}")
        return DEFAULT_GPIO_PINS.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        pins = data.get("gpio_pins", DEFAULT_GPIO_PINS)
        print(f"[OK] Loaded GPIO config from: {CONFIG_FILE}")
        return pins
    except Exception as e:
        print(f"[WARN] Failed to read config ({e}), using defaults")
        return DEFAULT_GPIO_PINS.copy()


def parse_args(available_channels):
    parser = argparse.ArgumentParser(
        description="ทดสอบชนิดรีเลย์ว่า Active LOW หรือ Active HIGH"
    )
    parser.add_argument(
        "--channel",
        choices=available_channels,
        help="ทดสอบเฉพาะ channel เดียว (เช่น pump)",
    )
    parser.add_argument(
        "--seconds",
        type=float,
        default=1.5,
        help="เวลาค้างต่อสเตต (วินาที), default=1.5",
    )
    return parser.parse_args()


def print_header():
    print("=" * 64)
    print("Relay Type Test - Active LOW / Active HIGH")
    print("=" * 64)
    print("คำแปลผล:")
    print("- ถ้า GPIO LOW แล้วรีเลย์ติด  -> บอร์ดเป็น Active LOW")
    print("- ถ้า GPIO HIGH แล้วรีเลย์ติด -> บอร์ดเป็น Active HIGH")
    print("- สังเกตจาก: เสียงคลิก, LED บนรีเลย์, หรือโหลดจริง")
    print("=" * 64)


def set_all_safe_off(channel_map):
    """Set all outputs to HIGH first as a safe baseline for many relay boards."""
    for _, pin in channel_map.items():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)


def test_one_channel(name, pin, hold_seconds):
    print(f"\n--- Testing channel: {name} (GPIO {pin}) ---")
    GPIO.setup(pin, GPIO.OUT)

    # Step 1: LOW
    print("[1/2] Set GPIO -> LOW")
    GPIO.output(pin, GPIO.LOW)
    print("      สังเกต: รีเลย์ติด/ดับ?")
    time.sleep(hold_seconds)

    # Step 2: HIGH
    print("[2/2] Set GPIO -> HIGH")
    GPIO.output(pin, GPIO.HIGH)
    print("      สังเกต: รีเลย์ติด/ดับ?")
    time.sleep(hold_seconds)

    # Return to HIGH for safety
    GPIO.output(pin, GPIO.HIGH)
    print("      คืนค่าเป็น HIGH แล้ว")


def main():
    if GPIO is None:
        print("[ERROR] ไม่พบ RPi.GPIO (ต้องรันบน Raspberry Pi)")
        sys.exit(1)

    gpio_pins = load_gpio_pins()
    channels = list(gpio_pins.keys())
    args = parse_args(channels)

    print_header()
    print(f"Channels in config: {', '.join(channels)}")
    print(f"Hold seconds per step: {args.seconds}")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    try:
        # Initialize all channels to HIGH first.
        set_all_safe_off(gpio_pins)
        time.sleep(0.3)

        if args.channel:
            test_map = {args.channel: gpio_pins[args.channel]}
        else:
            test_map = gpio_pins

        print("\nเริ่มทดสอบ...")
        for ch_name, ch_pin in test_map.items():
            test_one_channel(ch_name, ch_pin, args.seconds)

        print("\nเสร็จสิ้นการทดสอบ")
        print("สรุปผลเองตามการสังเกต:")
        print("- LOW ติด = Active LOW")
        print("- HIGH ติด = Active HIGH")
    except KeyboardInterrupt:
        print("\n[INFO] ยกเลิกโดยผู้ใช้")
    finally:
        # Force all outputs HIGH before cleanup for safer shutdown on common boards.
        try:
            for _, pin in gpio_pins.items():
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.HIGH)
        except Exception:
            pass
        GPIO.cleanup()
        print("[OK] GPIO cleanup done")


if __name__ == "__main__":
    main()
