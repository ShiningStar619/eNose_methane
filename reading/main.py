#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
eNose Sensor Data Collection
=============================
Script สำหรับเก็บข้อมูลจาก ADS1263 ADC
รองรับทั้ง Raspberry Pi (hardware จริง) และ Simulation Mode

Author: eNose Project
"""

import numpy as np
import time
import signal
import sys
import math
import threading
from datetime import datetime
from pathlib import Path

# ตรวจสอบว่ารันบน Raspberry Pi หรือไม่
try:
    import ADS1263
    ON_RASPBERRY_PI = True
except ImportError:
    ON_RASPBERRY_PI = False
    ADS1263 = None
    print("ADS1263 not found - Running in simulation mode")

# ==================== CONFIGURATION ====================
REF = 5.08  
CHANNEL_LIST = [1, 2, 3, 4, 5, 6, 7, 8]
SAMPLE_INTERVAL_SEC = 0.01  # 1/0.01 = 100 Hz
ADC_SAMPLE_RATE = 'ADS1263_14400SPS'
INITIAL_BUFFER_SIZE = 1000  # Pre-allocate buffer for ~100 seconds of data

class SensorDataCollector:
    """Class for collecting and storing sensor data using NumPy"""
    
    def __init__(self, num_channels, buffer_size=INITIAL_BUFFER_SIZE):
        self.num_channels = num_channels
        self.buffer_size = buffer_size
        # Pre-allocate buffer: [elapsed_time, ch0, ch1, ..., ch9]
        self.data = np.zeros((buffer_size, 1 + num_channels), dtype=np.float32)
        self.index = 0
        self.output_path = None
    
    def prepare(self, channel_list):
        """Prepare output directory and filename"""
        output_dir = Path(__file__).parent / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        # ใช้รูปแบบ adc1263_date_time
        date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_path = output_dir / f"adc1263_{date_time}.npz"
        self.columns = ['elapsed_time_sec'] + [f"ch{ch}_voltage" for ch in channel_list]
        return self.output_path
    
    def append(self, elapsed_time, voltages):
        """Append a single row of data"""
        # Expand buffer if needed
        if self.index >= self.buffer_size:
            new_buffer = np.zeros((self.buffer_size, 1 + self.num_channels), dtype=np.float32)
            self.data = np.vstack([self.data, new_buffer])
            self.buffer_size *= 2
        
        # Store data
        self.data[self.index, 0] = elapsed_time
        self.data[self.index, 1:] = voltages
        self.index += 1
    
    def save(self):
        """Save collected data to .npz file"""
        if self.output_path is None or self.index == 0:
            print("No data to save")
            return None
        
        # Trim unused buffer space
        final_data = self.data[:self.index]
        
        np.savez_compressed(
            self.output_path,
            data=final_data,
            columns=self.columns,
            sample_rate=1.0 / SAMPLE_INTERVAL_SEC,
            num_channels=self.num_channels
        )
        
        print(f"\nSaved {self.index} samples to {self.output_path}")
        print(f"  File size: {self.output_path.stat().st_size / 1024:.2f} KB")
        return self.output_path


def _simulate_voltages(t):
    """สร้างข้อมูลจำลองสำหรับทดสอบบนเครื่องที่ไม่มี ADC"""
    voltages = []
    for ch in CHANNEL_LIST:
        freq = 0.1 + ch * 0.05
        noise = np.random.normal(0, 0.01)
        voltages.append(2.5 + 0.5 * math.sin(t * 2 * math.pi * freq) + noise)
    return voltages


def raw_to_voltage(raw_value):
    """Convert raw ADC value to voltage"""
    if raw_value & 0x80000000:
        raw_value -= 0x100000000
    return raw_value * REF / 0x7FFFFFFF


def run_collection(stop_event: threading.Event, simulate: bool | None = None):
    """
    รันการเก็บข้อมูลจนกว่า stop_event จะถูก set
    Args:
        stop_event (threading.Event): ใช้สั่งหยุด loop จากภายนอก
        simulate (bool | None): True = บังคับ simulation, False = บังคับใช้ ADC,
                                None = auto (ใช้ ADC ถ้ามี ไม่งั้น simulation)
    Returns:
        pathlib.Path หรือ None: path ไฟล์ .npz ที่บันทึกได้
    """
    adc = None
    collector = None
    try:
        use_sim = simulate if simulate is not None else (not ON_RASPBERRY_PI)

        if not use_sim:
            adc = ADS1263.ADS1263()
            if adc.ADS1263_init_ADC1(ADC_SAMPLE_RATE) == -1:
                print("Failed to initialize ADC")
                return None
            adc.ADS1263_SetMode(0)
            print("ADC initialized successfully")
        else:
            print("Running in SIMULATION mode (no real ADC)")

        collector = SensorDataCollector(num_channels=len(CHANNEL_LIST))
        output_path = collector.prepare(CHANNEL_LIST)
        print(f"Recording data to: {output_path}")

        start_time = time.perf_counter()
        next_sample_time = start_time
        sample_count = 0

        while not stop_event.is_set():
            loop_start = time.perf_counter()

            if use_sim:
                voltages = _simulate_voltages(loop_start - start_time)
            else:
                raw_values = adc.ADS1263_GetAll(CHANNEL_LIST)
                voltages = []
                for index, channel in enumerate(CHANNEL_LIST):
                    raw_value = raw_values[index]
                    voltage = raw_to_voltage(raw_value)
                    voltages.append(voltage)

            elapsed_time = loop_start - start_time

            collector.append(elapsed_time, voltages)
            sample_count += 1

            if sample_count % 100 == 0:
                voltage_text = " ".join(
                    f"CH{ch}={v:.4f}V" for ch, v in zip(CHANNEL_LIST[:3], voltages[:3])
                )
                print(f"t={elapsed_time:.2f}s | {sample_count} samples | {voltage_text} ...")

            next_sample_time += SAMPLE_INTERVAL_SEC
            now = time.perf_counter()
            sleep_time = next_sample_time - now
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                next_sample_time = now

        print("\nStopping data collection...")

    except IOError as error:
        print(f"IO Error: {error}")
    except KeyboardInterrupt:
        print("\nCtrl+C received, saving data...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        saved_path = None
        if collector is not None:
            saved_path = collector.save()
        if adc is not None and ON_RASPBERRY_PI:
            adc.ADS1263_Exit()
            print("ADC cleanup completed")
        return saved_path


def main():
    """Main data collection function (standalone)"""
    stop_event = threading.Event()

    def handle_signal(signum, frame):
        print(f"\nReceived signal {signum}, stopping...")
        stop_event.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    try:
        run_collection(stop_event)
    finally:
        stop_event.set()


if __name__ == "__main__":
    main()
