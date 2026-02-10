#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RS485 Temperature and Humidity Data Logger
==========================================
สคริปต์สำหรับอ่านและบันทึกค่าอุณหภูมิและความชื้นต่อเนื่องลงไฟล์ NPZ (NumPy)
อ้างอิงจาก humid.py

Author: eNose Project
"""

import sys
import os
import time
import platform
import numpy as np
from datetime import datetime
from typing import Optional, List
from pathlib import Path

# เพิ่ม path ของโฟลเดอร์ปัจจุบันเข้า sys.path เพื่อให้หา module ได้
# รองรับทั้ง Windows และ Linux/Raspberry Pi
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from humid import RS485TempHumiditySensor


# ============================================================================
# CONFIGURATION - จุดตั้งค่า Default Values
# ============================================================================
DEFAULT_SAMPLING_RATE_HZ = 1.0      # Default sampling rate (Hz)
DEFAULT_INTERVAL_SECONDS = 1.0      # Default interval (seconds) - ใช้เมื่อไม่ระบุ sampling_rate
DEFAULT_BAUDRATE = 9600             # Default baudrate
DEFAULT_SLAVE_ID = 1                 # Default Modbus slave ID
DEFAULT_PORT = None                  # None = auto-detect
DEFAULT_OUTPUT_DIR = None            # None = ใช้ "data" ใน humid record
# ============================================================================


def get_output_dir(output_dir: Optional[str] = None) -> str:
    """
    หา path ของโฟลเดอร์สำหรับเก็บไฟล์
    
    Args:
        output_dir: โฟลเดอร์ที่ระบุ (ถ้าเป็น None จะใช้ default)
    
    Returns:
        str: path ของโฟลเดอร์
    """
    if output_dir is None:
        # ใช้โฟลเดอร์ data ใน humid record
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "data")
    else:
        # ถ้าระบุ path แบบ relative ให้แปลงเป็น absolute
        if not os.path.isabs(output_dir):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(script_dir, output_dir)
    
    # สร้างโฟลเดอร์ถ้ายังไม่มี
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return output_dir


def create_log_file(output_dir: Optional[str] = None) -> str:
    """
    สร้าง path สำหรับไฟล์ log ใหม่
    
    Args:
        output_dir: โฟลเดอร์สำหรับเก็บไฟล์ (ถ้าเป็น None จะใช้ default)
    
    Returns:
        str: filepath ของไฟล์ที่จะบันทึก
    """
    output_dir = get_output_dir(output_dir)
    
    # สร้างชื่อไฟล์จาก timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"temperature_humidity_{timestamp}.npz"
    filepath = os.path.join(output_dir, filename)
    
    return filepath


def continuous_log(port: Optional[str] = None, 
                   baudrate: int = DEFAULT_BAUDRATE,
                   slave_id: int = DEFAULT_SLAVE_ID,
                   interval: Optional[float] = None,
                   sampling_rate: Optional[float] = None,
                   use_ascii: bool = False,
                   output_dir: Optional[str] = None,
                   debug: bool = False):
    """
    อ่านและบันทึกค่าอุณหภูมิและความชื้นต่อเนื่องลงไฟล์ NPZ
    
    Args:
        port: Serial port (เช่น 'COM3' สำหรับ Windows, '/dev/ttyUSB0' สำหรับ Linux/Raspberry Pi 
              หรือ None สำหรับ auto-detect)
        baudrate: Baudrate (default: จาก CONFIGURATION)
        slave_id: Modbus Slave ID (default: จาก CONFIGURATION)
        interval: ช่วงเวลาระหว่างการอ่าน (วินาที) - ถ้าไม่ระบุจะใช้ sampling_rate
        sampling_rate: อัตราการสุ่มตัวอย่าง (Hz) - ถ้าระบุจะคำนวณ interval อัตโนมัติ
        use_ascii: ใช้ ASCII Protocol แทน Modbus RTU
        output_dir: โฟลเดอร์สำหรับเก็บไฟล์ log (default: "data" ใน humid record)
        debug: แสดงข้อมูล debug
    
    Note:
        รองรับทั้ง Windows และ Linux/Raspberry Pi
        บน Raspberry Pi อาจต้องเพิ่ม user เข้า dialout group:
        sudo usermod -a -G dialout $USER
    """
    # คำนวณ interval จาก sampling_rate หรือใช้ interval ที่ระบุ
    if sampling_rate is not None:
        if sampling_rate <= 0:
            raise ValueError("sampling_rate ต้องมากกว่า 0")
        calculated_interval = 1.0 / sampling_rate
        if interval is not None:
            print(f"คำเตือน: ระบุทั้ง interval ({interval}s) และ sampling_rate ({sampling_rate}Hz)")
            print(f"  จะใช้ sampling_rate: {sampling_rate}Hz (interval = {calculated_interval:.4f}s)")
        interval = calculated_interval
    elif interval is None:
        interval = DEFAULT_INTERVAL_SECONDS  # ใช้ default จาก CONFIGURATION
    
    if interval <= 0:
        raise ValueError("interval ต้องมากกว่า 0")
    
    # ใช้ default values จาก CONFIGURATION
    if port is None:
        port = DEFAULT_PORT
    if baudrate == DEFAULT_BAUDRATE:  # ใช้ default ถ้าไม่ระบุ
        baudrate = DEFAULT_BAUDRATE
    if slave_id == DEFAULT_SLAVE_ID:  # ใช้ default ถ้าไม่ระบุ
        slave_id = DEFAULT_SLAVE_ID
    
    sensor = None
    filepath = None
    
    # เก็บข้อมูลใน list
    timestamps: List[str] = []
    temperatures: List[float] = []
    humidities: List[float] = []
    
    try:
        # สร้าง sensor instance
        print("กำลังเชื่อมต่อกับเซ็นเซอร์...")
        sensor = RS485TempHumiditySensor(
            port=port,
            baudrate=baudrate,
            slave_id=slave_id,
            debug=debug
        )
        
        # สร้างไฟล์ log
        filepath = create_log_file(output_dir)
        output_dir_path = get_output_dir(output_dir)
        print(f"\nบันทึกข้อมูลไปที่: {filepath}")
        
        # แสดงข้อมูลการตั้งค่า
        sampling_rate_display = 1.0 / interval
        system_info = platform.system()
        machine_info = platform.machine()
        print(f"\nการตั้งค่า:")
        print(f"  - Platform: {system_info} ({machine_info})")
        print(f"  - Port: {sensor.port}")
        print(f"  - Baudrate: {baudrate}")
        print(f"  - Slave ID: {slave_id}")
        print(f"  - Interval: {interval:.4f} วินาที")
        print(f"  - Sampling Rate: {sampling_rate_display:.4f} Hz ({sampling_rate_display:.4f} samples/second)")
        if use_ascii:
            print(f"  - Protocol: ASCII (READ command)")
        else:
            print(f"  - Protocol: Modbus RTU (Function Code 0x04)")
        print(f"  - Output Directory: {output_dir_path}")
        print(f"  - File Format: NPZ (NumPy)")
        
        print(f"\nเริ่มบันทึกข้อมูล...")
        print("กด Ctrl+C เพื่อหยุด\n")
        print("-" * 80)
        print(f"{'เวลา':<20} {'อุณหภูมิ (C)':<15} {'ความชื้น (%RH)':<15} {'สถานะ':<15}")
        print("-" * 80)
        
        count = 0
        error_count = 0
        
        while True:
            # อ่านค่าจากเซ็นเซอร์
            result = sensor.read_temperature_humidity(use_ascii=use_ascii)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if result:
                temperature, humidity = result
                
                # แสดงผลบนหน้าจอ
                print(f"{timestamp:<20} {temperature:>12.2f}      {humidity:>12.2f}      {'OK':<15}")
                
                # เก็บข้อมูลใน list
                timestamps.append(timestamp)
                temperatures.append(temperature)
                humidities.append(humidity)
                
                count += 1
            else:
                # แสดง error
                print(f"{timestamp:<20} {'ERROR':<15} {'ERROR':<15}      {'FAIL':<15}")
                
                # เก็บ error เป็น NaN
                timestamps.append(timestamp)
                temperatures.append(np.nan)
                humidities.append(np.nan)
                
                error_count += 1
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("หยุดการบันทึกข้อมูล")
        print("=" * 80)
        
        # บันทึกข้อมูลลงไฟล์ NPZ
        if len(timestamps) > 0:
            print("\nกำลังบันทึกข้อมูลลงไฟล์...")
            
            # แปลงเป็น numpy arrays
            timestamps_array = np.array(timestamps, dtype=object)
            temperatures_array = np.array(temperatures, dtype=np.float64)
            humidities_array = np.array(humidities, dtype=np.float64)
            
            # บันทึก metadata (เก็บ string เป็น object array)
            sampling_rate_value = 1.0 / interval
            save_dict = {
                'timestamps': timestamps_array,
                'temperatures': temperatures_array,
                'humidities': humidities_array,
                # Metadata - เก็บตัวเลขเป็น float/int
                'metadata_total_records': np.int32(count),
                'metadata_error_records': np.int32(error_count),
                'metadata_interval_seconds': np.float64(interval),
                'metadata_sampling_rate_hz': np.float64(sampling_rate_value),
                'metadata_baudrate': np.int32(baudrate),
                'metadata_slave_id': np.int32(slave_id),
            }
            
            # เก็บ string metadata เป็น object array
            if timestamps:
                save_dict['metadata_start_time'] = np.array([timestamps[0]], dtype=object)
                save_dict['metadata_end_time'] = np.array([timestamps[-1]], dtype=object)
            else:
                save_dict['metadata_start_time'] = np.array([''], dtype=object)
                save_dict['metadata_end_time'] = np.array([''], dtype=object)
            
            save_dict['metadata_protocol'] = np.array(['ASCII' if use_ascii else 'Modbus RTU'], dtype=object)
            save_dict['metadata_port'] = np.array([sensor.port if sensor else ''], dtype=object)
            save_dict['metadata_created_at'] = np.array([datetime.now().strftime("%Y-%m-%d %H:%M:%S")], dtype=object)
            
            # บันทึกเป็น NPZ (compressed)
            np.savez_compressed(filepath, **save_dict)
            
            print(f"บันทึกสำเร็จ: {filepath}")
            print(f"  - จำนวนข้อมูล: {len(timestamps)} records")
            print(f"  - ขนาดไฟล์: {os.path.getsize(filepath) / 1024:.2f} KB")
        
        print(f"\nสรุป:")
        print(f"  - บันทึกทั้งหมด: {count} ครั้ง")
        print(f"  - เกิดข้อผิดพลาด: {error_count} ครั้ง")
        if filepath:
            print(f"  - ไฟล์: {filepath}")
        
    except Exception as e:
        print(f"\nเกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
        
        # แสดงคำแนะนำสำหรับ Raspberry Pi/Linux
        if 'Permission denied' in str(e) or 'Access is denied' in str(e):
            print("\nคำแนะนำสำหรับ Raspberry Pi/Linux:")
            print("  - อาจต้องเพิ่ม user เข้า dialout group:")
            print("    sudo usermod -a -G dialout $USER")
            print("  - แล้ว logout และ login ใหม่")
            print("  - หรือใช้ sudo (ไม่แนะนำ): sudo python3 humid_logger.py ...")
        elif 'No such file or directory' in str(e) or 'could not open port' in str(e).lower():
            print("\nคำแนะนำ:")
            print("  - ตรวจสอบว่า serial port ถูกต้อง:")
            if platform.system() != 'Windows':
                print("    ls -l /dev/ttyUSB* /dev/ttyACM*")
                print("  - หรือใช้ auto-detect: python3 humid_logger.py -r 0.5")
            else:
                print("    python -m serial.tools.list_ports")
                print("  - หรือใช้ auto-detect: python humid_logger.py -r 0.5")
        
        # พยายามบันทึกข้อมูลที่มีอยู่แล้ว
        if len(timestamps) > 0 and filepath:
            try:
                print("\nกำลังบันทึกข้อมูลที่มีอยู่แล้ว...")
                timestamps_array = np.array(timestamps, dtype=object)
                temperatures_array = np.array(temperatures, dtype=np.float64)
                humidities_array = np.array(humidities, dtype=np.float64)
                
                np.savez_compressed(
                    filepath,
                    timestamps=timestamps_array,
                    temperatures=temperatures_array,
                    humidities=humidities_array
                )
                print(f"บันทึกข้อมูลบางส่วนสำเร็จ: {filepath}")
            except Exception as save_error:
                print(f"ไม่สามารถบันทึกข้อมูลได้: {save_error}")
        
    finally:
        if sensor:
            sensor.close()
            print("\nปิดการเชื่อมต่อแล้ว")


def run_humidity_collection(stop_event=None, 
                           port: Optional[str] = None,
                           baudrate: int = DEFAULT_BAUDRATE,
                           slave_id: int = DEFAULT_SLAVE_ID,
                           sampling_rate: Optional[float] = None,
                           interval: Optional[float] = None,
                           use_ascii: bool = False,
                           output_dir: Optional[str] = None,
                           debug: bool = False,
                           silent: bool = False) -> Optional[Path]:
    """
    ฟังก์ชัน wrapper สำหรับเรียกจาก GUI หรือ external modules
    ทำงานเหมือน run_collection() ใน reading.main
    
    Args:
        stop_event: threading.Event สำหรับหยุดการทำงาน (ถ้าเป็น None จะรันจนกว่าจะกด Ctrl+C)
        port: Serial port (None = auto-detect)
        baudrate: Baudrate
        slave_id: Modbus Slave ID
        sampling_rate: Sampling rate (Hz)
        interval: Interval (seconds)
        use_ascii: ใช้ ASCII Protocol
        output_dir: Output directory
        debug: Debug mode
        silent: ถ้า True จะไม่แสดง output บน console
    
    Returns:
        Path object ของไฟล์ที่บันทึก หรือ None ถ้าเกิดข้อผิดพลาด
    """
    # คำนวณ interval จาก sampling_rate
    if sampling_rate is not None:
        if sampling_rate <= 0:
            raise ValueError("sampling_rate ต้องมากกว่า 0")
        calculated_interval = 1.0 / sampling_rate
        interval = calculated_interval
    elif interval is None:
        interval = DEFAULT_INTERVAL_SECONDS
    
    if interval <= 0:
        raise ValueError("interval ต้องมากกว่า 0")
    
    sensor = None
    filepath = None
    
    # เก็บข้อมูลใน list
    timestamps: List[str] = []
    temperatures: List[float] = []
    humidities: List[float] = []
    
    try:
        # สร้าง sensor instance
        if not silent:
            print("กำลังเชื่อมต่อกับเซ็นเซอร์อุณหภูมิและความชื้น...")
        
        sensor = RS485TempHumiditySensor(
            port=port,
            baudrate=baudrate,
            slave_id=slave_id,
            debug=debug
        )
        
        # สร้างไฟล์ log
        filepath = create_log_file(output_dir)
        
        if not silent:
            print(f"บันทึกข้อมูลไปที่: {filepath}")
        
        count = 0
        error_count = 0
        
        # เริ่มเก็บข้อมูล
        while True:
            # ตรวจสอบ stop_event
            if stop_event is not None and stop_event.is_set():
                if not silent:
                    print("ได้รับสัญญาณหยุดการทำงาน...")
                break
            
            # อ่านค่าจากเซ็นเซอร์
            result = sensor.read_temperature_humidity(use_ascii=use_ascii)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if result:
                temperature, humidity = result
                
                if not silent:
                    print(f"{timestamp} - Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %RH")
                
                # เก็บข้อมูลใน list
                timestamps.append(timestamp)
                temperatures.append(temperature)
                humidities.append(humidity)
                
                count += 1
            else:
                if not silent:
                    print(f"{timestamp} - ERROR: ไม่สามารถอ่านข้อมูลได้")
                
                # เก็บ error เป็น NaN
                timestamps.append(timestamp)
                temperatures.append(np.nan)
                humidities.append(np.nan)
                
                error_count += 1
            
            # รอ interval (ตรวจสอบ stop_event ระหว่างรอ)
            if stop_event is not None:
                # แบ่ง interval เป็น chunks เล็กๆ เพื่อตรวจสอบ stop_event บ่อยขึ้น
                chunk_time = min(0.1, interval)
                elapsed = 0.0
                while elapsed < interval:
                    if stop_event.is_set():
                        break
                    time.sleep(chunk_time)
                    elapsed += chunk_time
            else:
                time.sleep(interval)
        
        # บันทึกข้อมูลลงไฟล์ NPZ
        if len(timestamps) > 0:
            if not silent:
                print(f"\nกำลังบันทึกข้อมูลลงไฟล์...")
            
            # แปลงเป็น numpy arrays
            timestamps_array = np.array(timestamps, dtype=object)
            temperatures_array = np.array(temperatures, dtype=np.float64)
            humidities_array = np.array(humidities, dtype=np.float64)
            
            # บันทึก metadata
            sampling_rate_value = 1.0 / interval
            save_dict = {
                'timestamps': timestamps_array,
                'temperatures': temperatures_array,
                'humidities': humidities_array,
                'metadata_total_records': np.int32(count),
                'metadata_error_records': np.int32(error_count),
                'metadata_interval_seconds': np.float64(interval),
                'metadata_sampling_rate_hz': np.float64(sampling_rate_value),
                'metadata_baudrate': np.int32(baudrate),
                'metadata_slave_id': np.int32(slave_id),
            }
            
            # เก็บ string metadata
            if timestamps:
                save_dict['metadata_start_time'] = np.array([timestamps[0]], dtype=object)
                save_dict['metadata_end_time'] = np.array([timestamps[-1]], dtype=object)
            else:
                save_dict['metadata_start_time'] = np.array([''], dtype=object)
                save_dict['metadata_end_time'] = np.array([''], dtype=object)
            
            save_dict['metadata_protocol'] = np.array(['ASCII' if use_ascii else 'Modbus RTU'], dtype=object)
            save_dict['metadata_port'] = np.array([sensor.port if sensor else ''], dtype=object)
            save_dict['metadata_created_at'] = np.array([datetime.now().strftime("%Y-%m-%d %H:%M:%S")], dtype=object)
            
            # บันทึกเป็น NPZ (compressed)
            np.savez_compressed(filepath, **save_dict)
            
            if not silent:
                print(f"บันทึกสำเร็จ: {filepath}")
                print(f"  - จำนวนข้อมูล: {len(timestamps)} records")
                print(f"  - ขนาดไฟล์: {os.path.getsize(filepath) / 1024:.2f} KB")
            
            return Path(filepath)
        else:
            if not silent:
                print("ไม่มีข้อมูลที่จะบันทึก")
            return None
        
    except KeyboardInterrupt:
        if not silent:
            print("\nหยุดการบันทึกข้อมูล")
        
        # บันทึกข้อมูลที่มีอยู่แล้ว
        if len(timestamps) > 0 and filepath:
            try:
                if not silent:
                    print("กำลังบันทึกข้อมูลที่มีอยู่แล้ว...")
                timestamps_array = np.array(timestamps, dtype=object)
                temperatures_array = np.array(temperatures, dtype=np.float64)
                humidities_array = np.array(humidities, dtype=np.float64)
                
                np.savez_compressed(
                    filepath,
                    timestamps=timestamps_array,
                    temperatures=temperatures_array,
                    humidities=humidities_array
                )
                if not silent:
                    print(f"บันทึกข้อมูลบางส่วนสำเร็จ: {filepath}")
                return Path(filepath)
            except Exception as save_error:
                if not silent:
                    print(f"ไม่สามารถบันทึกข้อมูลได้: {save_error}")
        return None
        
    except Exception as e:
        if not silent:
            print(f"เกิดข้อผิดพลาด: {e}")
            import traceback
            traceback.print_exc()
        
        # พยายามบันทึกข้อมูลที่มีอยู่แล้ว
        if len(timestamps) > 0 and filepath:
            try:
                if not silent:
                    print("กำลังบันทึกข้อมูลที่มีอยู่แล้ว...")
                timestamps_array = np.array(timestamps, dtype=object)
                temperatures_array = np.array(temperatures, dtype=np.float64)
                humidities_array = np.array(humidities, dtype=np.float64)
                
                np.savez_compressed(
                    filepath,
                    timestamps=timestamps_array,
                    temperatures=temperatures_array,
                    humidities=humidities_array
                )
                if not silent:
                    print(f"บันทึกข้อมูลบางส่วนสำเร็จ: {filepath}")
                return Path(filepath)
            except Exception as save_error:
                if not silent:
                    print(f"ไม่สามารถบันทึกข้อมูลได้: {save_error}")
        return None
        
    finally:
        if sensor:
            sensor.close()
            if not silent:
                print("ปิดการเชื่อมต่อแล้ว")


def main():
    """Main function"""
    import argparse
    
    # ตรวจสอบ platform เพื่อแสดงตัวอย่างที่เหมาะสม
    is_windows = platform.system() == 'Windows'
    port_example = 'COM3' if is_windows else '/dev/ttyUSB0'
    python_cmd = 'python' if is_windows else 'python3'
    
    parser = argparse.ArgumentParser(
        description='บันทึกค่าอุณหภูมิและความชื้นต่อเนื่องลงไฟล์ NPZ (NumPy)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
ตัวอย่างการใช้งาน:
  # ใช้ sampling rate (Hz) - แนะนำ
  {python_cmd} humid_logger.py -p {port_example} -r 0.5          # 0.5 Hz (อ่านทุก 2 วินาที)
  {python_cmd} humid_logger.py -p {port_example} -r 0.2          # 0.2 Hz (อ่านทุก 5 วินาที)
  {python_cmd} humid_logger.py -p {port_example} -r 0.1          # 0.1 Hz (อ่านทุก 10 วินาที)
  
  # ใช้ interval (วินาที)
  {python_cmd} humid_logger.py -p {port_example} -i 2.0          # อ่านทุก 2 วินาที
  {python_cmd} humid_logger.py -p {port_example} -i 5.0          # อ่านทุก 5 วินาที
  
  # Auto-detect port (แนะนำ)
  {python_cmd} humid_logger.py -r 0.5
  
  # ตั้งค่าอื่นๆ
  {python_cmd} humid_logger.py -p {port_example} --use-ascii
  {python_cmd} humid_logger.py -p {port_example} -o custom_data

หมายเหตุ: 
  - ไฟล์จะถูกบันทึกในโฟลเดอร์ "data" ภายใน "humid record" โดยอัตโนมัติ
  - ถ้าไม่ระบุ -i หรือ -r จะใช้ default จาก CONFIGURATION section
  - ถ้าระบุทั้ง -i และ -r จะใช้ -r (sampling_rate)
  - บน Raspberry Pi/Linux: ใช้ /dev/ttyUSB0 หรือ /dev/ttyACM0 แทน COM3
  - บน Raspberry Pi: อาจต้องเพิ่ม user เข้า dialout group (sudo usermod -a -G dialout $USER)
        """
    )
    
    port_help = f'Serial port (เช่น {port_example}) - ถ้าไม่ระบุจะค้นหาอัตโนมัติ'
    if not is_windows:
        port_help += ' (บน Linux/Raspberry Pi: /dev/ttyUSB0, /dev/ttyACM0)'
    port_help += f' (default: {DEFAULT_PORT})'
    
    parser.add_argument('-p', '--port', type=str, default=DEFAULT_PORT,
                       help=port_help)
    parser.add_argument('-b', '--baudrate', type=int, default=DEFAULT_BAUDRATE,
                       help=f'Baudrate (default: {DEFAULT_BAUDRATE})')
    parser.add_argument('-s', '--slave-id', type=int, default=DEFAULT_SLAVE_ID,
                       help=f'Modbus Slave ID (default: {DEFAULT_SLAVE_ID})')
    parser.add_argument('-i', '--interval', type=float, default=None,
                       help='ช่วงเวลาระหว่างการอ่าน (วินาที) - ถ้าไม่ระบุจะใช้ sampling-rate หรือ default')
    parser.add_argument('-r', '--sampling-rate', type=float, default=None,
                       help='อัตราการสุ่มตัวอย่าง (Hz, ตัวอย่างต่อวินาที) - ถ้าระบุจะคำนวณ interval อัตโนมัติ')
    parser.add_argument('-o', '--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                       help='โฟลเดอร์สำหรับเก็บไฟล์ log (default: data ใน humid record)')
    parser.add_argument('--use-ascii', action='store_true',
                       help='ใช้ ASCII Protocol (ส่งคำสั่ง READ) แทน Modbus RTU')
    parser.add_argument('--debug', action='store_true',
                       help='แสดงข้อมูล debug')
    
    args = parser.parse_args()
    
    try:
        continuous_log(
            port=args.port,
            baudrate=args.baudrate,
            slave_id=args.slave_id,
            interval=args.interval,
            sampling_rate=args.sampling_rate,
            use_ascii=args.use_ascii,
            output_dir=args.output_dir,
            debug=args.debug
        )
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

