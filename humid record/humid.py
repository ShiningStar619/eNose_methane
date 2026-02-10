#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RS485 Temperature and Humidity Sensor Reader (เวอร์ชันเรียบง่าย)
===============================================================
สคริปต์สำหรับอ่านค่าจากเซ็นเซอร์อุณหภูมิและความชื้นที่เชื่อมต่อผ่าน RS485
และ USB to RS485 adapter บน PC

Author: eNose Project
"""

import serial
import serial.tools.list_ports
import time
import struct
from datetime import datetime
from typing import Optional, Tuple
import sys


class RS485TempHumiditySensor:
    """คลาสสำหรับอ่านค่าจาก RS485 Temperature and Humidity Sensor (เวอร์ชันเรียบง่าย)"""
    
    def __init__(self, port: Optional[str] = None, baudrate: int = 9600, 
                 slave_id: int = 1, timeout: float = 1.0, debug: bool = False):
        """
        Initialize RS485 sensor connection
        
        Args:
            port: COM port (เช่น 'COM3' สำหรับ Windows, '/dev/ttyUSB0' สำหรับ Linux)
                 ถ้าเป็น None จะพยายามหา port อัตโนมัติ
            baudrate: ความเร็วในการสื่อสาร (default: 9600)
            slave_id: Modbus slave ID (default: 1)
            timeout: Timeout สำหรับการอ่านข้อมูล (วินาที)
            debug: แสดงข้อมูล debug (default: False)
        """
        self.baudrate = baudrate
        self.slave_id = slave_id
        self.timeout = timeout
        self.debug = debug
        self.serial_conn: Optional[serial.Serial] = None
        
        if port is None:
            port = self._find_rs485_port()
            if port is None:
                raise ValueError("ไม่พบ RS485 port กรุณาระบุ port เอง")
        
        self.port = port
        self._connect()
    
    def _find_rs485_port(self) -> Optional[str]:
        """ค้นหา RS485 port อัตโนมัติ"""
        print("กำลังค้นหา RS485 port...")
        ports = serial.tools.list_ports.comports()
        
        for port_info in ports:
            print(f"พบ port: {port_info.device} - {port_info.description}")
            # ตรวจสอบว่าเป็น USB to Serial adapter หรือไม่
            if any(keyword in port_info.description.lower() 
                   for keyword in ['usb', 'serial', 'ch340', 'cp210', 'ftdi', 'rs485']):
                return port_info.device
        
        return None
    
    def _connect(self):
        """เชื่อมต่อกับ serial port"""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            
            # รอให้ serial port พร้อม
            time.sleep(0.1)
            
            if self.serial_conn.is_open:
                print(f"เชื่อมต่อสำเร็จ: {self.port} @ {self.baudrate} baud")
            else:
                raise Exception("ไม่สามารถเปิด serial port ได้")
                
        except serial.SerialException as e:
            raise Exception(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {e}")
    
    def _calculate_crc16(self, data: bytes) -> bytes:
        """คำนวณ CRC16 สำหรับ Modbus RTU"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return struct.pack('<H', crc)  # Little-endian
    
    def _read_input_registers(self, start_address: int, num_registers: int):
        """อ่าน Input Registers ผ่าน Modbus RTU (Function Code 0x04)"""
        if self.serial_conn is None or not self.serial_conn.is_open:
            if self.debug:
                print("[DEBUG] Serial port ไม่ได้เปิดอยู่")
            return None
        
        # สร้าง Modbus RTU request - ใช้ Function Code 0x04 (Read Input Registers)
        function_code = 0x04
        request = struct.pack('>BBHH', 
                              self.slave_id,
                              function_code,
                              start_address,
                              num_registers)
        
        # เพิ่ม CRC
        crc = self._calculate_crc16(request)
        request += crc
        
        if self.debug:
            print(f"[DEBUG] Request: {' '.join(f'{b:02X}' for b in request)}")
            print(f"  Slave ID: {self.slave_id} (0x{self.slave_id:02X})")
            print(f"  Function Code: 0x{function_code:02X} (Read Input Registers)")
            print(f"  Start Address: {start_address} (0x{start_address:04X})")
            print(f"  Number of Registers: {num_registers}")
        
        # ล้าง buffer และส่ง request
        self.serial_conn.reset_input_buffer()
        self.serial_conn.reset_output_buffer()
        self.serial_conn.write(request)
        time.sleep(0.2)  # รอให้ข้อมูลส่งเสร็จ
        
        # อ่าน response
        expected_bytes = 5 + (num_registers * 2)  # Header + Data + CRC
        response = self.serial_conn.read(expected_bytes)
        
        # ถ้ายังอ่านไม่ครบ ให้รอเพิ่มอีกนิด
        if len(response) < expected_bytes:
            time.sleep(0.1)
            additional = self.serial_conn.read(expected_bytes - len(response))
            if additional:
                response += additional
        
        if self.debug:
            print(f"[DEBUG] Response: {' '.join(f'{b:02X}' for b in response) if response else 'None'}")
            print(f"  Response length: {len(response)} bytes (expected: {expected_bytes} bytes)")
        
        # ตรวจสอบ response
        if len(response) < 5:
            if self.debug:
                print(f"[DEBUG] ได้รับข้อมูลไม่ครบ: {len(response)} bytes (คาดหวังอย่างน้อย 5 bytes)")
            return None
        
        # ตรวจสอบ Slave ID
        if response[0] != self.slave_id:
            if self.debug:
                print(f"[DEBUG] Slave ID ไม่ตรง: ได้รับ {response[0]} (0x{response[0]:02X}), คาดหวัง {self.slave_id} (0x{self.slave_id:02X})")
            return None
        
        # ตรวจสอบ Function Code
        if response[1] != function_code:
            if response[1] == function_code + 0x80:  # Error response
                error_code = response[2]
                error_messages = {
                    0x01: "Illegal Function Code",
                    0x02: "Illegal Data Address",
                    0x03: "Illegal Data Value"
                }
                error_msg = error_messages.get(error_code, f"Unknown error (0x{error_code:02X})")
                if self.debug:
                    print(f"[DEBUG] Modbus Error 0x{error_code:02X}: {error_msg}")
            else:
                if self.debug:
                    print(f"[DEBUG] Function code ไม่ตรง: ได้รับ {response[1]} (0x{response[1]:02X}), คาดหวัง {function_code} (0x{function_code:02X})")
            return None
        
        # ตรวจสอบ CRC
        received_crc = response[-2:]
        calculated_crc = self._calculate_crc16(response[:-2])
        if received_crc != calculated_crc:
            if self.debug:
                print(f"[DEBUG] CRC ไม่ตรงกัน: ได้รับ {received_crc.hex()}, คำนวณได้ {calculated_crc.hex()}")
            return None
        
        # แปลงข้อมูล
        byte_count = response[2]
        if byte_count != num_registers * 2:
            if self.debug:
                print(f"[DEBUG] จำนวน bytes ไม่ตรง: ได้รับ {byte_count}, คาดหวัง {num_registers * 2}")
            return None
        
        # อ่านค่า registers (big-endian, signed) - ตาม datasheet ค่าอาจเป็นค่าลบได้
        registers = []
        for i in range(num_registers):
            byte_index = 3 + (i * 2)
            # ใช้ '>h' สำหรับ signed short (16-bit) เพื่อรองรับค่าลบ
            value = struct.unpack('>h', response[byte_index:byte_index+2])[0]
            registers.append(value)
        
        if self.debug:
            print(f"[DEBUG] Registers: {registers}")
        
        return registers
    
    def read_temperature_humidity_ascii(self) -> Optional[Tuple[float, float]]:
        """
        อ่านค่าอุณหภูมิและความชื้นแบบ ASCII protocol
        ส่งคำสั่ง "READ" และ parse response ที่เป็น text format
        
        Returns:
            Tuple (temperature, humidity) ในหน่วย C และ %RH
            หรือ None ถ้าเกิดข้อผิดพลาด
        """
        if self.serial_conn is None or not self.serial_conn.is_open:
            if self.debug:
                print("[DEBUG] Serial port ไม่ได้เปิดอยู่")
            return None
        
        # ล้าง buffer
        self.serial_conn.reset_input_buffer()
        self.serial_conn.reset_output_buffer()
        
        # ส่งคำสั่ง "READ" ตาม datasheet XY-MD03
        command = "READ\r\n"
        
        if self.debug:
            print(f"[DEBUG] Sending ASCII command: {repr(command)}")
        
        try:
            self.serial_conn.write(command.encode('ascii'))
            time.sleep(0.3)  # รอให้เซ็นเซอร์ตอบกลับ
            
            # อ่าน response (ตัวอย่าง: "27.4C,67.7%")
            response = self.serial_conn.readline().decode('ascii', errors='ignore').strip()
            
            # ถ้ายังไม่มี response ลองอ่านแบบ read
            if not response:
                time.sleep(0.2)
                available = self.serial_conn.in_waiting
                if available > 0:
                    response = self.serial_conn.read(available).decode('ascii', errors='ignore').strip()
            
            if self.debug:
                print(f"[DEBUG] ASCII Response: {repr(response)}")
            
            if not response:
                return None
            
            # Parse response: "27.4°C,67.7%" หรือ "27.4C,67.7%"
            try:
                parts = response.split(',')
                # ลบทั้ง °C และ C ออก
                temp_str = parts[0].replace('°C', '').replace('C', '').strip()
                hum_str = parts[1].replace('%', '').strip()
                
                temperature = float(temp_str)
                humidity = float(hum_str)
                
                return (temperature, humidity)
                
            except (ValueError, IndexError) as e:
                if self.debug:
                    print(f"[DEBUG] Parse error: {e}, Response: {response}")
                return None
                
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Exception: {e}")
            return None
    
    def read_temperature_humidity(self, use_ascii: bool = False) -> Optional[Tuple[float, float]]:
        """
        อ่านค่าอุณหภูมิและความชื้น
        
        Args:
            use_ascii: ถ้า True จะใช้ ASCII protocol (ส่งคำสั่ง READ) แทน Modbus RTU
        
        Returns:
            Tuple (temperature, humidity) ในหน่วย C และ %RH
            หรือ None ถ้าเกิดข้อผิดพลาด
            
        หมายเหตุ: 
        - ถ้า use_ascii=True จะส่งคำสั่ง "READ" และ parse response แบบ ASCII
        - ถ้า use_ascii=False จะใช้ Modbus RTU protocol (Function Code 0x04: Read Input Registers)
          - Input Register 0x0001 = Temperature (signed 16-bit, ค่าจริง × 10)
          - Input Register 0x0002 = Humidity (signed 16-bit, ค่าจริง × 10)
        """
        # ใช้ ASCII protocol
        if use_ascii:
            return self.read_temperature_humidity_ascii()
        
        # ใช้ Modbus RTU protocol
        # อ่าน 2 registers เริ่มจาก address 0x0001 (Temperature และ Humidity)
        # ตาม datasheet XY-MD03:
        # - Input Register 0x0001 = Temperature
        # - Input Register 0x0002 = Humidity
        registers = self._read_input_registers(0x0001, 2)
        
        if registers is None or len(registers) < 2:
            return None
        
        # Register 0x0001 = Temperature, Register 0x0002 = Humidity
        temperature_raw = registers[0]
        humidity_raw = registers[1]
        
        # แปลงค่า: ค่าจริง = raw_value / 10.0
        # ค่าเป็น signed ดังนั้นอาจเป็นค่าลบได้ (เช่น -20.5C)
        temperature = temperature_raw / 10.0
        humidity = humidity_raw / 10.0
        
        return (temperature, humidity)
    
    def close(self):
        """ปิดการเชื่อมต่อ"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("ปิดการเชื่อมต่อแล้ว")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def list_available_ports():
    """แสดงรายการ serial ports ที่มีอยู่"""
    print("\n=== Serial Ports ที่มีอยู่ ===")
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print("ไม่พบ serial port")
        return
    
    for i, port_info in enumerate(ports, 1):
        print(f"{i}. {port_info.device}")
        print(f"   Description: {port_info.description}")
        print()


def continuous_read(sensor: RS485TempHumiditySensor, interval: float = 1.0, use_ascii: bool = False):
    """อ่านค่าต่อเนื่อง"""
    print(f"\nเริ่มอ่านค่าต่อเนื่อง (ทุก {interval} วินาที)")
    if use_ascii:
        print("ใช้ ASCII Protocol (ส่งคำสั่ง READ)")
    else:
        print("ใช้ Modbus RTU Protocol (Function Code 0x04: Read Input Registers)")
    print("กด Ctrl+C เพื่อหยุด\n")
    print("-" * 60)
    print(f"{'เวลา':<20} {'อุณหภูมิ (C)':<15} {'ความชื้น (%RH)':<15}")
    print("-" * 60)
    
    try:
        while True:
            result = sensor.read_temperature_humidity(use_ascii=use_ascii)
            
            if result:
                temperature, humidity = result
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp:<20} {temperature:>12.2f}      {humidity:>12.2f}")
            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<20} {'ERROR':<15} {'ERROR':<15}")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nหยุดการอ่านข้อมูล")


def single_read(sensor: RS485TempHumiditySensor, use_ascii: bool = False):
    """อ่านค่าครั้งเดียว"""
    print("\nกำลังอ่านค่าจากเซ็นเซอร์...")
    if use_ascii:
        print("ใช้ ASCII Protocol (ส่งคำสั่ง READ)")
    else:
        print("ใช้ Modbus RTU Protocol (Function Code 0x04: Read Input Registers)")
    result = sensor.read_temperature_humidity(use_ascii=use_ascii)
    
    if result:
        temperature, humidity = result
        print(f"\nผลการอ่าน:")
        print(f"  อุณหภูมิ: {temperature:.2f} C")
        print(f"  ความชื้น: {humidity:.2f} %RH")
        return result
    else:
        print("เกิดข้อผิดพลาดในการอ่านข้อมูล")
        print("คำแนะนำ:")
        print("  1. ตรวจสอบ slave ID ที่ตั้งไว้ในเซ็นเซอร์ (ลองใช้ --try-slave-ids)")
        print("  2. ตรวจสอบการเชื่อมต่อ RS485")
        print("  3. ใช้ --debug เพื่อดูข้อมูลเพิ่มเติม")
        print("  4. ลองใช้ --use-ascii เพื่อใช้ ASCII protocol แทน Modbus RTU")
        return None


def try_slave_ids(port: str, baudrate: int, max_id: int = 10, use_ascii: bool = False):
    """ลอง slave ID หลายๆ ค่าเพื่อหาค่าที่ถูกต้อง"""
    if use_ascii:
        # สำหรับ ASCII protocol ไม่ต้องลอง slave ID หลายค่า
        print(f"\nกำลังลองอ่านด้วย ASCII Protocol...")
        print("-" * 60)
        try:
            sensor = RS485TempHumiditySensor(
                port=port,
                baudrate=baudrate,
                slave_id=1  # สำหรับ ASCII อาจไม่ใช้ slave ID
            )
            result = sensor.read_temperature_humidity(use_ascii=True)
            if result:
                temperature, humidity = result
                print(f"✓ อ่านข้อมูลสำเร็จด้วย ASCII Protocol")
                print(f"  อุณหภูมิ: {temperature:.2f} °C")
                print(f"  ความชื้น: {humidity:.2f} %RH")
                sensor.close()
                return
            else:
                print(f"✗ ไม่สามารถอ่านข้อมูลด้วย ASCII Protocol")
            sensor.close()
        except Exception as e:
            print(f"✗ เกิดข้อผิดพลาด: {e}")
        return
    
    print(f"\nกำลังลอง slave ID 1-{max_id} เพื่อหาค่าที่ถูกต้อง...")
    print("ใช้ Modbus RTU Protocol (Function Code 0x04: Read Input Registers)")
    print("-" * 60)
    
    found = False
    for slave_id in range(1, max_id + 1):
        try:
            sensor = RS485TempHumiditySensor(
                port=port,
                baudrate=baudrate,
                slave_id=slave_id
            )
            
            result = sensor.read_temperature_humidity(use_ascii=False)
            if result:
                temperature, humidity = result
                print(f"✓ พบ slave ID: {slave_id}")
                print(f"  อุณหภูมิ: {temperature:.2f} °C")
                print(f"  ความชื้น: {humidity:.2f} %RH")
                found = True
                sensor.close()
                break
            else:
                print(f"✗ Slave ID {slave_id}: ไม่สามารถอ่านข้อมูลได้")
            
            sensor.close()
            time.sleep(0.1)  # รอสักครู่ก่อนลอง ID ถัดไป
            
        except Exception as e:
            print(f"✗ Slave ID {slave_id}: {e}")
            continue
    
    if not found:
        print(f"\nไม่พบ slave ID ที่ถูกต้องใน range 1-{max_id}")
        print("คำแนะนำ:")
        print("  1. ตรวจสอบ DIP switch ในเซ็นเซอร์เพื่อดู slave ID ที่ตั้งไว้")
        print("  2. ลองเพิ่ม max_id หรือระบุ slave ID เองด้วย -s")
        print("  3. ลองใช้ --use-ascii เพื่อใช้ ASCII protocol แทน Modbus RTU")
    else:
        print(f"\n✓ ใช้ slave ID {slave_id} ในการอ่านข้อมูลต่อไป")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='อ่านค่าจาก RS485 Temperature and Humidity Sensor (เวอร์ชันเรียบง่าย)'
    )
    parser.add_argument('-p', '--port', type=str, default=None,
                       help='COM port (เช่น COM3 หรือ /dev/ttyUSB0) - ถ้าไม่ระบุจะค้นหาอัตโนมัติ')
    parser.add_argument('-b', '--baudrate', type=int, default=9600,
                       help='Baudrate (default: 9600)')
    parser.add_argument('-s', '--slave-id', type=int, default=1,
                       help='Modbus Slave ID (default: 1)')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                       help='ช่วงเวลาระหว่างการอ่าน (วินาที, default: 1.0)')
    parser.add_argument('-c', '--continuous', action='store_true',
                       help='อ่านค่าต่อเนื่อง')
    parser.add_argument('-l', '--list-ports', action='store_true',
                       help='แสดงรายการ serial ports')
    parser.add_argument('--debug', action='store_true',
                       help='แสดงข้อมูล debug สำหรับแก้ไขปัญหา')
    parser.add_argument('--try-slave-ids', action='store_true',
                       help='ลอง slave ID หลายๆ ค่าเพื่อหาค่าที่ถูกต้อง (1-10)')
    parser.add_argument('--use-ascii', action='store_true',
                       help='ใช้ ASCII Protocol (ส่งคำสั่ง READ) แทน Modbus RTU')
    
    args = parser.parse_args()
    
    # แสดงรายการ ports
    if args.list_ports:
        list_available_ports()
        return
    
    # ลอง slave ID หลายๆ ค่า
    if args.try_slave_ids:
        if args.port is None:
            print("กรุณาระบุ port ด้วย -p")
            sys.exit(1)
        try_slave_ids(args.port, args.baudrate, use_ascii=args.use_ascii)
        return
    
    # สร้าง sensor instance
    try:
        sensor = RS485TempHumiditySensor(
            port=args.port,
            baudrate=args.baudrate,
            slave_id=args.slave_id,
            debug=args.debug
        )
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        print("\nลองใช้ -l เพื่อดูรายการ ports ที่มีอยู่")
        sys.exit(1)
    
    try:
        # อ่านค่าต่อเนื่องหรือครั้งเดียว
        if args.continuous:
            continuous_read(sensor, args.interval, use_ascii=args.use_ascii)
        else:
            single_read(sensor, use_ascii=args.use_ascii)
    
    finally:
        sensor.close()


if __name__ == "__main__":
    main()

