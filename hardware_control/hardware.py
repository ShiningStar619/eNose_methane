"""
eNose Hardware Controller
==========================
Module สำหรับควบคุม Hardware (GPIO) บน Raspberry Pi

Author: eNose Project
"""

import os
import json

# ตรวจสอบว่ารันบน Raspberry Pi หรือไม่
try:
    import RPi.GPIO as GPIO
    ON_RASPBERRY_PI = True
except ImportError:
    ON_RASPBERRY_PI = False


# ==================== CONFIG FILE ====================
# หา path ของ config file
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
CONFIG_FILE = os.path.join(_PROJECT_ROOT, "program", "hardware_config.json")

# Default GPIO Pin Configuration (fallback) - 7 Relays
_DEFAULT_GPIO_PINS = {
    "s_valve1": 21,
    "s_valve2": 20,
    "s_valve3": 16,
    "s_valve4": 12,
    "pump": 26,
    "fan": 19,
    "heater": 13
}


def load_gpio_config():
    """
    โหลด GPIO pins configuration จากไฟล์ config
    
    Returns:
        dict: GPIO pin mappings
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                gpio_pins = config.get("gpio_pins", _DEFAULT_GPIO_PINS)
                print(f"[OK] Loaded GPIO config from {CONFIG_FILE}")
                return gpio_pins
        except Exception as e:
            print(f"[WARN] Error loading config: {e}, using defaults")
    return _DEFAULT_GPIO_PINS.copy()


# โหลด GPIO pins จาก config file
DEFAULT_GPIO_PINS = load_gpio_config()


class HardwareController:
    """
    Class สำหรับควบคุม Hardware ผ่าน GPIO
    รองรับ Relay control แบบ Active HIGH (GPIO HIGH = ON, LOW = OFF)
    """
    
    def __init__(self, gpio_pins=None):
        """
        Initialize Hardware Controller
        
        Args:
            gpio_pins (dict): Dictionary ของ GPIO pin mappings
                             ถ้าไม่ระบุจะใช้ค่า default
        """
        self.gpio_pins = gpio_pins if gpio_pins else DEFAULT_GPIO_PINS.copy()
        self.device_states = {key: False for key in self.gpio_pins.keys()}
        self.is_initialized = False
        # True when running on a non-Raspberry Pi platform
        self.is_simulation_mode = not ON_RASPBERRY_PI

    @staticmethod
    def _gpio_level_for_state(state):
        """แปลง logical ON/OFF เป็นระดับ GPIO สำหรับ relay Active HIGH."""
        return GPIO.HIGH if state else GPIO.LOW
        
    def setup(self):
        """
        ตั้งค่า GPIO pins ทั้งหมด
        ต้องเรียกก่อนใช้งาน control functions อื่นๆ
        """
        if ON_RASPBERRY_PI:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            for pin in self.gpio_pins.values():
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)  # Relay ปิดเริ่มต้น (Active HIGH)

            self._apply_all_states_to_gpio()
            self.is_initialized = True
            print("[OK] GPIO initialized successfully")
        else:
            self.is_initialized = True
            print("[OK] Hardware Controller initialized")

    def _apply_all_states_to_gpio(self):
        """ซิงก์สถานะ relay จริงให้ตรงกับ device_states ใน memory (หลัง setup/re-init)"""
        if not ON_RASPBERRY_PI:
            return
        for device_key, state in self.device_states.items():
            pin = self.gpio_pins[device_key]
            GPIO.output(pin, self._gpio_level_for_state(state))

    def _reinitialize_gpio(self):
        """Re-init GPIO หลังถูก cleanup โดยโมดูลอื่น แล้วคืนสถานะ relay ตาม memory"""
        self.is_initialized = False
        self.setup()

    def _ensure_gpio_setup(self):
        """
        ตรวจสอบว่า GPIO ถูก setup แล้ว
        ถ้าโมดูลอื่น (เช่น ADC) เรียก GPIO.cleanup() จะ re-init ตอน control_device ล้มเหลว
        """
        if not ON_RASPBERRY_PI:
            return
        if not self.is_initialized:
            self.setup()
            
    def control_device(self, device_key, state):
        """
        ควบคุมอุปกรณ์โดยตรง
        
        Args:
            device_key (str): ชื่ออุปกรณ์ (valve1, valve2, pump, heater, etc.)
            state (bool): True = ON, False = OFF
            
        Returns:
            bool: True ถ้าสำเร็จ, False ถ้าล้มเหลว
        """
        if device_key not in self.gpio_pins:
            print(f"[WARN] Unknown device: {device_key}")
            return False
        
        # ตรวจสอบและ setup GPIO ใหม่ถ้าจำเป็น
        self._ensure_gpio_setup()
        
        pin = self.gpio_pins[device_key]
        self.device_states[device_key] = state

        if ON_RASPBERRY_PI:
            level = self._gpio_level_for_state(state)
            try:
                GPIO.output(pin, level)
            except (RuntimeError, ValueError) as e:
                # GPIO ถูก cleanup แล้ว ลอง setup ใหม่และลองอีกครั้ง
                error_msg = str(e)
                if 'unknown handle' in error_msg.lower() or 'lgpio' in error_msg.lower():
                    print(f"[WARN] GPIO handle error when controlling {device_key}, re-initializing... ({e})")
                else:
                    print(f"[WARN] GPIO error when controlling {device_key}, re-initializing... ({e})")
                self._reinitialize_gpio()
                try:
                    GPIO.output(pin, level)
                except Exception as retry_error:
                    print(f"[WARN] Failed to control {device_key} after re-initialization: {retry_error}")
                    return False
            except Exception as e:
                # จัดการ error อื่นๆ (เช่น lgpio.error)
                error_msg = str(e)
                if 'unknown handle' in error_msg.lower() or 'lgpio' in error_msg.lower():
                    print(f"[WARN] GPIO handle error when controlling {device_key}, re-initializing... ({e})")
                    try:
                        self._reinitialize_gpio()
                        GPIO.output(pin, level)
                    except Exception as retry_error:
                        print(f"[WARN] Failed to control {device_key} after re-initialization: {retry_error}")
                        return False
                else:
                    print(f"[WARN] Unexpected GPIO error when controlling {device_key}: {e}")
                    return False
            
        return True
        
    def turn_on(self, device_key):
        """
        เปิดอุปกรณ์
        
        Args:
            device_key (str): ชื่ออุปกรณ์
            
        Returns:
            bool: True ถ้าสำเร็จ
        """
        return self.control_device(device_key, True)
        
    def turn_off(self, device_key):
        """
        ปิดอุปกรณ์
        
        Args:
            device_key (str): ชื่ออุปกรณ์
            
        Returns:
            bool: True ถ้าสำเร็จ
        """
        return self.control_device(device_key, False)
        
    def toggle_device(self, device_key):
        """
        สลับสถานะอุปกรณ์ (ON <-> OFF)
        
        Args:
            device_key (str): ชื่ออุปกรณ์
            
        Returns:
            bool: สถานะใหม่ของอุปกรณ์
        """
        if device_key not in self.device_states:
            return False
            
        new_state = not self.device_states[device_key]
        self.control_device(device_key, new_state)
        return new_state
        
    def get_device_state(self, device_key):
        """
        อ่านสถานะปัจจุบันของอุปกรณ์
        
        Args:
            device_key (str): ชื่ออุปกรณ์
            
        Returns:
            bool: สถานะปัจจุบัน (True = ON, False = OFF)
        """
        # ใช้ state จาก memory เพราะ GPIO.input() อาจจะไม่ทำงานถูกต้องกับ OUTPUT pins
        # และ state ใน memory จะถูกอัพเดททุกครั้งที่เรียก control_device()
        return self.device_states.get(device_key, False)
        
    def get_all_states(self):
        """
        อ่านสถานะของอุปกรณ์ทั้งหมด
        
        Returns:
            dict: Dictionary ของสถานะอุปกรณ์ทั้งหมด
        """
        return self.device_states.copy()
        
    def set_multiple_devices(self, devices_on=None, devices_off=None):
        """
        ตั้งค่าหลายอุปกรณ์พร้อมกัน
        
        Args:
            devices_on (list): รายการอุปกรณ์ที่ต้องการเปิด
            devices_off (list): รายการอุปกรณ์ที่ต้องการปิด
        """
        if devices_off:
            for device in devices_off:
                self.turn_off(device)
                
        if devices_on:
            for device in devices_on:
                self.turn_on(device)
                
    def all_off(self):
        """
        ปิดอุปกรณ์ทั้งหมด
        """
        for device_key in self.device_states.keys():
            self.turn_off(device_key)
        print("[OK] All devices turned OFF")
        
    def cleanup(self):
        """
        Cleanup GPIO และปิดอุปกรณ์ทั้งหมด
        ควรเรียกก่อนปิดโปรแกรม
        """
        # ป้องกันการ cleanup หลายครั้ง
        if not self.is_initialized:
            return
        
        # ปิดอุปกรณ์ทั้งหมดก่อน
        try:
            self.all_off()
        except Exception as e:
            print(f"[WARN] Error turning off devices during cleanup: {e}")
        
        if ON_RASPBERRY_PI:
            try:
                # ตรวจสอบว่า GPIO ยัง setup อยู่ก่อน cleanup
                if self.is_initialized:
                    GPIO.cleanup()
                    print("[OK] GPIO cleanup completed")
            except Exception as e:
                # ถ้า cleanup แล้วหรือมี error อื่นๆ ไม่ต้องทำอะไร
                print(f"[WARN] GPIO cleanup warning: {e}")
        
        self.is_initialized = False
        print("[OK] Hardware Controller cleanup completed")
        
    def get_gpio_pin(self, device_key):
        """
        อ่าน GPIO pin number ของอุปกรณ์
        
        Args:
            device_key (str): ชื่ออุปกรณ์
            
        Returns:
            int: GPIO pin number หรือ None ถ้าไม่พบ
        """
        return self.gpio_pins.get(device_key, None)
        
    def update_gpio_pins(self, new_pins):
        """
        อัพเดท GPIO pin mappings
        
        Args:
            new_pins (dict): Dictionary ของ pin mappings ใหม่
        """
        self.gpio_pins.update(new_pins)
        
    @property
    def available_devices(self):
        """
        รายการอุปกรณ์ที่รองรับ
        
        Returns:
            list: รายชื่ออุปกรณ์ทั้งหมด
        """
        return list(self.gpio_pins.keys())


# ==================== Utility Functions ====================

# Expose platform check for GUI and other callers
def is_raspberry_pi():
    """
    ตรวจสอบว่าโค้ดกำลังรันบน Raspberry Pi หรือไม่
    
    Returns:
        bool: True ถ้ารันบน Raspberry Pi, False ถ้าไม่ใช่
    """
    return ON_RASPBERRY_PI

def create_controller(gpio_pins=None):
    """
    Factory function สำหรับสร้าง HardwareController
    
    Args:
        gpio_pins (dict): GPIO pin mappings (optional)
        
    Returns:
        HardwareController: Instance ที่พร้อมใช้งาน
    """
    controller = HardwareController(gpio_pins)
    controller.setup()
    return controller


# ==================== Test Code ====================

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Hardware Controller")
    print("=" * 50)
    
    # สร้าง controller
    hw = create_controller()
    
    print("\nAvailable devices:", hw.available_devices)
    
    # ทดสอบเปิด/ปิดอุปกรณ์
    print("\n--- Test individual control ---")
    hw.turn_on('pump')
    hw.turn_on('heater')
    print("States:", hw.get_all_states())
    
    hw.turn_off('pump')
    print("After pump off:", hw.get_all_states())
    
    # ทดสอบ toggle
    print("\n--- Test toggle ---")
    hw.toggle_device('valve1')
    print("After toggle valve1:", hw.get_device_state('valve1'))
    hw.toggle_device('valve1')
    print("After toggle valve1 again:", hw.get_device_state('valve1'))
    
    # ทดสอบ multiple devices
    print("\n--- Test multiple devices ---")
    hw.set_multiple_devices(
        devices_on=['valve1'],
        devices_off=['valve2']
    )
    print("States:", hw.get_all_states())
    
    # Cleanup
    print("\n--- Cleanup ---")
    hw.cleanup()
    print("States after cleanup:", hw.get_all_states())
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)

