#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
eNose BME280 Environmental Sensor Data Collection
==================================================
Script สำหรับเก็บข้อมูลจากเซ็นเซอร์ BME280 (Temperature/Humidity/Pressure)
ผ่าน I2C รองรับเฉพาะ hardware จริง

ออกแบบให้ทำงานคู่ขนานกับ ADS1263 ใน reading/main.py:
- ใช้ stop_event ตัวเดียวกันในการสั่งหยุด
- บันทึกในรูปแบบ NPZ เดียวกัน เพื่อให้ acquisition/acquisiton.py
  ประมวลผลด้วย pipeline เดียวกันได้

Author: eNose Project
"""

import numpy as np
import time
import signal
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional


def _ensure_circuitpython_typing():
    """Adafruit bus device ใช้ WriteableBuffer จาก circuitpython_typing บน Linux/Pi."""
    try:
        import circuitpython_typing as cpt
    except ImportError:
        import sys
        import types
        cpt = types.ModuleType("circuitpython_typing")
        sys.modules["circuitpython_typing"] = cpt
    if hasattr(cpt, "WriteableBuffer"):
        return
    try:
        from typing import WriteableBuffer
    except ImportError:
        from typing_extensions import WriteableBuffer
    cpt.WriteableBuffer = WriteableBuffer


_ensure_circuitpython_typing()

try:
    import board
    import busio
    try:
        from adafruit_bme280.basic import Adafruit_BME280_I2C
    except ImportError:
        # ไลบรารีรุ่นเก่าที่ export คลาสที่ระดับ top-level
        from adafruit_bme280 import Adafruit_BME280_I2C
    BME280_AVAILABLE = True
except ImportError:
    BME280_AVAILABLE = False
    board = None
    busio = None
    Adafruit_BME280_I2C = None
    print("BME280 libraries not found - BME280 collection disabled")

# ==================== CONFIGURATION ====================
BME_SAMPLE_INTERVAL_SEC = 0.1  # 1/0.1 = 10 Hz
BME_I2C_ADDRESS = 0x76         # อาจเปลี่ยนเป็น 0x77 ตาม jumper ของบอร์ด
BME_INITIAL_BUFFER_SIZE = 1000  # ~100 วินาทีของข้อมูลที่ 10 Hz

# คอลัมน์ของข้อมูล: [elapsed_time, temperature_c, humidity_pct, pressure_hpa]
BME_COLUMN_NAMES = ['elapsed_time_sec', 'temperature_c', 'humidity_pct', 'pressure_hpa']
BME_NUM_CHANNELS = 3  # T, H, P


class BMESensorDataCollector:
    """Class สำหรับเก็บข้อมูล BME280 ใน NumPy buffer แล้วบันทึกเป็น NPZ"""

    def __init__(self, buffer_size=BME_INITIAL_BUFFER_SIZE):
        self.num_channels = BME_NUM_CHANNELS
        self.buffer_size = buffer_size
        self.data = np.zeros((buffer_size, 1 + self.num_channels), dtype=np.float32)
        self.index = 0
        self.output_path = None
        self.columns = list(BME_COLUMN_NAMES)

    def prepare(self):
        """เตรียม output directory และชื่อไฟล์ bme280_YYYYMMDD_HHMMSS.npz"""
        output_dir = Path(__file__).parent / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_path = output_dir / f"bme280_{date_time}.npz"
        return self.output_path

    def append(self, elapsed_time, values):
        """เพิ่มข้อมูล 1 แถว (values = [temp, humidity, pressure])"""
        if self.index >= self.buffer_size:
            new_buffer = np.zeros((self.buffer_size, 1 + self.num_channels), dtype=np.float32)
            self.data = np.vstack([self.data, new_buffer])
            self.buffer_size *= 2

        self.data[self.index, 0] = elapsed_time
        self.data[self.index, 1:] = values
        self.index += 1

    def save(self):
        """บันทึกข้อมูลเป็นไฟล์ .npz (ไม่บีบอัด — เพิ่มความเร็วตอนกด Stop)"""
        if self.output_path is None or self.index == 0:
            print("No BME280 data to save")
            return None

        final_data = self.data[:self.index]

        # np.savez (uncompressed) เร็วกว่า savez_compressed มากบนข้อมูลขนาดใหญ่
        np.savez(
            self.output_path,
            data=final_data,
            columns=self.columns,
            sample_rate=1.0 / BME_SAMPLE_INTERVAL_SEC,
            num_channels=self.num_channels
        )

        print(f"\nSaved {self.index} BME280 samples to {self.output_path}")
        print(f"  File size: {self.output_path.stat().st_size / 1024:.2f} KB")
        return self.output_path


def run_bme_collection(stop_event: threading.Event, simulate: Optional[bool] = None):
    """รันการเก็บข้อมูล BME280 จนกว่า stop_event จะถูก set

    Args:
        stop_event (threading.Event): ใช้สั่งหยุด loop จากภายนอก
        simulate (bool | None): ไม่ได้ใช้งานแล้ว (เก็บไว้เพื่อ backward compatibility)
    Returns:
        pathlib.Path หรือ None: path ไฟล์ .npz ที่บันทึกได้
    """
    sensor = None
    collector = None
    try:
        if simulate:
            print("Simulation mode is disabled. BME280 collection aborted.")
            return None
        if not BME280_AVAILABLE or board is None or busio is None or Adafruit_BME280_I2C is None:
            print("BME280 hardware/library unavailable. BME280 collection aborted.")
            return None
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = Adafruit_BME280_I2C(i2c, address=BME_I2C_ADDRESS)
            print(f"BME280 initialized at I2C address 0x{BME_I2C_ADDRESS:02X}")
        except Exception as e:
            print(f"Failed to initialize BME280: {e}")
            return None

        collector = BMESensorDataCollector()
        output_path = collector.prepare()
        print(f"Recording BME280 data to: {output_path}")

        start_time = time.perf_counter()
        next_sample_time = start_time
        sample_count = 0

        while not stop_event.is_set():
            loop_start = time.perf_counter()
            elapsed_time = loop_start - start_time

            try:
                values = [
                    float(sensor.temperature),
                    float(sensor.humidity),
                    float(sensor.pressure),
                ]
            except Exception as e:
                # ถ้าอ่านพลาด ใช้ค่าเดิมแทน 0 เพื่อไม่ให้กราฟกระโดด
                print(f"BME280 read error: {e}")
                if collector.index > 0:
                    last = collector.data[collector.index - 1, 1:]
                    values = [float(last[0]), float(last[1]), float(last[2])]
                else:
                    values = [0.0, 0.0, 0.0]

            collector.append(elapsed_time, values)
            sample_count += 1

            if sample_count % 50 == 0:
                t_v, h_v, p_v = values
                print(
                    f"BME t={elapsed_time:.2f}s | {sample_count} samples | "
                    f"T={t_v:.2f}C H={h_v:.2f}% P={p_v:.2f}hPa"
                )

            next_sample_time += BME_SAMPLE_INTERVAL_SEC
            now = time.perf_counter()
            sleep_time = next_sample_time - now
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                next_sample_time = now

        print("\nStopping BME280 data collection...")

    except IOError as error:
        print(f"BME280 IO Error: {error}")
    except KeyboardInterrupt:
        print("\nCtrl+C received, saving BME280 data...")
    except Exception as e:
        print(f"BME280 Error: {e}")
    finally:
        saved_path = None
        if collector is not None:
            saved_path = collector.save()
        return saved_path


def main():
    """Main BME280 collection function (standalone)"""
    stop_event = threading.Event()

    def handle_signal(signum, frame):
        print(f"\nReceived signal {signum}, stopping...")
        stop_event.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    try:
        run_bme_collection(stop_event)
    finally:
        stop_event.set()


if __name__ == "__main__":
    main()
