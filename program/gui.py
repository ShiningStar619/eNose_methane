"""
eNose Hardware Control GUI
===========================
GUI สำหรับควบคุม Relay และอุปกรณ์ต่างๆ บน Raspberry Pi
รองรับ 2 โหมด: Manual และ Auto

Author: eNose Project
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import json
import os
import sys
from pathlib import Path
import traceback

# เพิ่ม path สำหรับ import hardware controller และ modules อื่นๆ
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_project_root)
sys.path.append(str(Path(_project_root) / "reading"))
sys.path.append(str(Path(_project_root) / "acquisition"))
sys.path.append(str(Path(_project_root) / "humid record"))

# Import Hardware Controller
from hardware_control.hardware import HardwareController, is_raspberry_pi, DEFAULT_GPIO_PINS

# Import Data Collection and Processing modules
try:
    from reading.main import run_collection
    DATA_COLLECTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import reading.main: {e}")
    DATA_COLLECTION_AVAILABLE = False
    run_collection = None

try:
    from acquisition.acquisiton import process_data
    DATA_PROCESSING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import acquisition.acquisiton: {e}")
    DATA_PROCESSING_AVAILABLE = False
    process_data = None

# Import Humidity Logger
try:
    from humid_logger import run_humidity_collection
    HUMIDITY_COLLECTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import humid_logger: {e}")
    HUMIDITY_COLLECTION_AVAILABLE = False
    run_humidity_collection = None


# ==================== CONFIG FILE ====================
# ใช้ absolute path เพื่อให้ทำงานได้บน Raspberry Pi ไม่ว่าจะรันจาก directory ไหน
CONFIG_FILE = os.path.join(_project_root, "program", "hardware_config.json")

DEFAULT_CONFIG = {
    "operation_times": {
        "heating": 1800,         # 30 นาที - Op1: Heating
        "baseline": 30,          # 30 วินาที - Op2: Baseline
        "vacuum": 10,            # 10 วินาที - Op3: Vacuum
        "mix_air": 10,           # 10 วินาที - Op4: Mix Air
        "measure": 60,           # 60 วินาที - Op5: Measure (เก็บข้อมูล)
        "vacuum_return": 10,     # 10 วินาที - Op6: Vacuum Return (process data)
        "recovery": 60,          # 60 วินาที - Op7: Recovery
        "break_time": 1620       # 27 นาที (1620 วินาที) - Break
    },
    "auto_settings": {
        "loop_count": 0,
        "infinite_loop": True
    }
}


def load_config():
    """โหลด config จากไฟล์"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"✓ Loaded config from {CONFIG_FILE}")
                return config
        except json.JSONDecodeError as e:
            print(f"⚠ Error parsing config file {CONFIG_FILE}: {e}")
            print("  Using default config instead")
        except Exception as e:
            print(f"⚠ Error loading config file {CONFIG_FILE}: {e}")
            print("  Using default config instead")
    else:
        print(f"⚠ Config file not found: {CONFIG_FILE}")
        print("  Using default config instead")
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """บันทึก config ลงไฟล์"""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f"✓ Saved config to {CONFIG_FILE}")
    except Exception as e:
        print(f"✗ Error saving config to {CONFIG_FILE}: {e}")
        raise


# ==================== MAIN GUI CLASS ====================
class HardwareControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("eNose Hardware Control")
        self.root.geometry("1024x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Fullscreen mode
        self.is_fullscreen = False
        
        # Bind window resize event
        self.root.bind('<Configure>', self.on_window_resize)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen() if self.is_fullscreen else None)
        
        # Store initial window size for scaling
        self.initial_width = 1024
        self.initial_height = 600
        
        # Store font sizes and widget sizes for scaling
        self.base_fonts = {
            'title': 18,
            'mode_indicator': 10,
            'section_title': 11,
            'label_frame': 9,
            'button': 10,
            'label': 9,
            'entry': 9,
            'timer': 18,
            'status': 9,
            'small': 8
        }
        
        # Store widget references for scaling
        self.scalable_widgets = {}
        
        # Load config
        self.config = load_config()
        
        # GPIO Pins Configuration - ดึงจาก hardware.py
        gpio_pins = DEFAULT_GPIO_PINS
        
        # สร้าง Hardware Controller
        self.hardware = HardwareController(gpio_pins)
        self.hardware.setup()
        
        # Operation durations (seconds) - จาก config
        op_times = self.config.get("operation_times", DEFAULT_CONFIG["operation_times"])
        self.operation_durations = {
            'heating': tk.StringVar(value=str(op_times.get("heating", 1800))),
            'baseline': tk.StringVar(value=str(op_times.get("baseline", 30))),
            'vacuum': tk.StringVar(value=str(op_times.get("vacuum", 10))),
            'mix_air': tk.StringVar(value=str(op_times.get("mix_air", 10))),
            'measure': tk.StringVar(value=str(op_times.get("measure", 60))),
            'vacuum_return': tk.StringVar(value=str(op_times.get("vacuum_return", 10))),
            'recovery': tk.StringVar(value=str(op_times.get("recovery", 60))),
            'break_time': tk.StringVar(value=str(op_times.get("break_time", 1620)))
        }
        
        # Auto settings
        auto_settings = self.config.get("auto_settings", DEFAULT_CONFIG["auto_settings"])
        self.loop_count = tk.StringVar(value=str(auto_settings.get("loop_count", 0)))
        self.infinite_loop = tk.BooleanVar(value=auto_settings.get("infinite_loop", True))
        
        # Control flags
        self.current_mode = tk.StringVar(value="manual")  # "manual" or "auto"
        self.running = False
        self.current_operation = None
        self.current_operation_index = -1
        self.current_cycle = 0
        
        # Data collection and processing threads
        self.stop_collection_event = None
        self.data_collection_thread = None
        self.data_collection_file_path = None  # เก็บ path ของไฟล์ที่เก็บข้อมูล ADC
        
        # Humidity collection thread
        self.humidity_collection_thread = None
        self.humidity_collection_file_path = None  # เก็บ path ของไฟล์ที่เก็บข้อมูลอุณหภูมิและความชื้น
        
        # Create UI
        self.create_main_layout()
        
        # Update window after creating UI
        self.root.update_idletasks()
        
    # ==================== FULLSCREEN & RESIZE HANDLERS ====================
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        if not self.is_fullscreen:
            self.root.geometry("1024x600")
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        self.is_fullscreen = False
        self.root.attributes('-fullscreen', False)
        self.root.geometry("1024x600")
    
    def on_window_resize(self, event):
        """Handle window resize event"""
        if event.widget == self.root:
            # Update window size for scaling calculations
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # Prevent division by zero
            if width > 0 and height > 0:
                # Scale UI elements if needed
                if hasattr(self, 'main_frame') and hasattr(self, 'scalable_widgets'):
                    self.scale_ui(width, height)
    
    def scale_ui(self, width, height):
        """Scale UI elements based on window size"""
        # Calculate scale factors
        width_scale = width / self.initial_width
        height_scale = height / self.initial_height
        scale = min(width_scale, height_scale, 1.5)  # Cap at 1.5x to prevent too large
        scale = max(scale, 0.7)  # Minimum 0.7x to prevent too small
        
        # Scale fonts
        if hasattr(self, 'scalable_widgets') and self.scalable_widgets:
            for widget_type, widgets in self.scalable_widgets.items():
                if not widgets:
                    continue
                    
                base_font_size = self.base_fonts.get(widget_type, 10)
                new_font_size = max(8, int(base_font_size * scale))  # Minimum 8px
                
                for widget in widgets:
                    try:
                        if widget and widget.winfo_exists():
                            current_font = widget.cget('font')
                            if isinstance(current_font, tuple):
                                font_name = current_font[0] if len(current_font) > 0 else 'Helvetica'
                                font_weight = current_font[2] if len(current_font) > 2 else 'normal'
                                widget.configure(font=(font_name, new_font_size, font_weight))
                            elif isinstance(current_font, str):
                                # Parse font string if needed
                                widget.configure(font=('Helvetica', new_font_size))
                    except (tk.TclError, AttributeError, Exception):
                        pass  # Skip if widget doesn't exist or doesn't support font change
        
    # ==================== MAIN LAYOUT ====================
    def create_main_layout(self):
        """สร้าง Layout หลัก"""
        # Main container (ลด padding สำหรับหน้าจอเล็ก)
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=8, pady=5)
        self.main_frame = main_frame
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', pady=(0, 5))
        
        title = tk.Label(
            title_frame, 
            text="eNose Hardware Control",
            font=('Helvetica', 18, 'bold'),  # ลดจาก 26 เป็น 18
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title.pack(side='left')
        
        # Store for scaling
        if 'title' not in self.scalable_widgets:
            self.scalable_widgets['title'] = []
        self.scalable_widgets['title'].append(title)
        
        # Mode indicator
        self.mode_indicator = tk.Label(
            title_frame,
            text="[ MANUAL MODE ]",
            font=('Helvetica', 10, 'bold'),  # ลดจาก 14 เป็น 10
            bg='#f0f0f0',
            fg='#e67e22'
        )
        self.mode_indicator.pack(side='right', padx=5)
        if 'mode_indicator' not in self.scalable_widgets:
            self.scalable_widgets['mode_indicator'] = []
        self.scalable_widgets['mode_indicator'].append(self.mode_indicator)
        
        # Fullscreen hint (ซ่อนหรือลดขนาด)
        fullscreen_hint = tk.Label(
            title_frame,
            text="F11: Fullscreen",
            font=('Helvetica', 7),  # ลดจาก 9 เป็น 7
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        fullscreen_hint.pack(side='right', padx=5)
        if 'small' not in self.scalable_widgets:
            self.scalable_widgets['small'] = []
        self.scalable_widgets['small'].append(fullscreen_hint)
        
        # Simulation mode indicator
        if self.hardware.is_simulation_mode:
            sim_label = tk.Label(
                title_frame,
                text="⚠️ SIMULATION",
                font=('Helvetica', 8, 'bold'),  # ลดขนาดและข้อความ
                bg='#fff3cd',
                fg='#856404',
                padx=5,
                pady=1
            )
            sim_label.pack(side='right', padx=5)
        
        # Content area with Scrollbar
        # สร้าง Canvas และ Scrollbar สำหรับ scroll
        canvas_container = tk.Frame(main_frame, bg='#f0f0f0')
        canvas_container.pack(fill='both', expand=True)
        
        # Canvas สำหรับ scroll
        self.content_canvas = tk.Canvas(canvas_container, bg='#f0f0f0', highlightthickness=0)
        self.content_canvas.pack(side='left', fill='both', expand=True)
        
        # Vertical Scrollbar
        v_scrollbar = ttk.Scrollbar(canvas_container, orient='vertical', command=self.content_canvas.yview)
        v_scrollbar.pack(side='right', fill='y')
        self.content_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        # Content frame (ใส่ใน Canvas)
        content_frame = tk.Frame(self.content_canvas, bg='#f0f0f0')
        self.content_canvas_window = self.content_canvas.create_window(0, 0, anchor='nw', window=content_frame)
        
        # Update scroll region เมื่อ content เปลี่ยน
        def configure_scroll_region(event=None):
            self.content_canvas.update_idletasks()
            # ตั้งค่า scroll region ให้ครอบคลุมเนื้อหาทั้งหมด
            bbox = self.content_canvas.bbox('all')
            if bbox:
                self.content_canvas.configure(scrollregion=bbox)
        
        # ปรับความกว้างของ content_frame ให้เท่ากับ canvas
        def configure_canvas_width(event=None):
            canvas_width = self.content_canvas.winfo_width()
            if canvas_width > 1:
                self.content_canvas.itemconfig(self.content_canvas_window, width=canvas_width)
        
        # Bind events
        content_frame.bind('<Configure>', configure_scroll_region)
        self.content_canvas.bind('<Configure>', configure_canvas_width)
        
        # Mouse wheel scrolling (Windows/Linux)
        def on_mousewheel(event):
            # Windows: event.delta, Linux: event.delta หรือ event.num
            if event.num == 4 or event.delta > 0:
                self.content_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.content_canvas.yview_scroll(1, "units")
        
        # Bind mouse wheel สำหรับ Windows และ Linux
        self.content_canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.content_canvas.bind_all("<Button-4>", on_mousewheel)  # Linux scroll up
        self.content_canvas.bind_all("<Button-5>", on_mousewheel)  # Linux scroll down
        
        # เก็บ reference
        self.content_frame = content_frame
        
        # Left Panel - Mode Selection & Controls (ใช้ weight แทน fixed width)
        left_panel = tk.Frame(content_frame, bg='#f0f0f0')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Middle Panel - Operation Parameters (Auto Mode) (ใช้ weight แทน fixed width)
        self.middle_panel = tk.Frame(content_frame, bg='#f0f0f0')
        self.middle_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Create sections
        self.create_mode_selection(left_panel)
        self.create_manual_controls(left_panel)
        self.create_operation_sequence(left_panel)  # ย้าย Operation Sequence ไปฝั่งซ้าย
        self.create_action_buttons(left_panel)
        self.create_auto_parameters(self.middle_panel)
        
        # Initial mode update
        self.update_mode_ui()
        
    # ==================== MODE SELECTION ====================
    def create_mode_selection(self, parent):
        """สร้างส่วนเลือกโหมด"""
        mode_frame = tk.LabelFrame(
            parent, 
            text="Control Mode", 
            font=('Helvetica', 10, 'bold'),  # ลดจาก 12 เป็น 10
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=8,
            pady=5
        )
        mode_frame.pack(fill='x', pady=(0, 5))
        
        # Mode buttons container
        btn_container = tk.Frame(mode_frame, bg='#f0f0f0')
        btn_container.pack(fill='x')
        
        # Manual Mode Button
        self.manual_btn = tk.Button(
            btn_container,
            text="🔧 Manual",
            font=('Helvetica', 10, 'bold'),  # ลดจาก 12 เป็น 10
            bg='#e67e22',
            fg='white',
            width=12,  # ลดจาก 15
            height=1,  # ลดจาก 2
            relief='raised',
            command=lambda: self.set_mode("manual")
        )
        self.manual_btn.pack(side='left', padx=(0, 5))
        
        # Auto Mode Button
        self.auto_btn = tk.Button(
            btn_container,
            text="⚡ Auto",
            font=('Helvetica', 10, 'bold'),  # ลดจาก 12 เป็น 10
            bg='#95a5a6',
            fg='white',
            width=12,  # ลดจาก 15
            height=1,  # ลดจาก 2
            relief='raised',
            command=lambda: self.set_mode("auto")
        )
        self.auto_btn.pack(side='left')
        
        # Store for scaling
        if 'button' not in self.scalable_widgets:
            self.scalable_widgets['button'] = []
        self.scalable_widgets['button'].extend([self.manual_btn, self.auto_btn])
        
        # Mode description (ซ่อนหรือลดขนาด)
        self.mode_desc = tk.Label(
            mode_frame,
            text="กดปุ่มเพื่อควบคุม hardware",
            font=('Helvetica', 8),  # ลดจาก 10 เป็น 8
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.mode_desc.pack(pady=(5, 0))
        
    def set_mode(self, mode):
        """เปลี่ยนโหมดการทำงาน"""
        if self.running:
            messagebox.showwarning("Warning", "กรุณาหยุดการทำงานก่อนเปลี่ยนโหมด")
            return
            
        self.current_mode.set(mode)
        self.update_mode_ui()
        
    def update_mode_ui(self):
        """อัพเดท UI ตามโหมด"""
        mode = self.current_mode.get()
        
        if mode == "manual":
            # Update buttons
            self.manual_btn.configure(bg='#e67e22', relief='sunken')
            self.auto_btn.configure(bg='#95a5a6', relief='raised')
            
            # Update indicator
            self.mode_indicator.configure(text="[ MANUAL MODE ]", fg='#e67e22')
            self.mode_desc.configure(text="กดปุ่มเพื่อควบคุม hardware โดยตรง")
            
            # Show manual controls
            self.manual_frame.pack(fill='x', pady=(0, 10))
            
            # Update start button
            self.start_btn.configure(text="▶ Start Collection", state='normal', bg='#27ae60')
            
        else:  # auto mode
            # Update buttons
            self.manual_btn.configure(bg='#95a5a6', relief='raised')
            self.auto_btn.configure(bg='#9b59b6', relief='sunken')
            
            # Update indicator
            self.mode_indicator.configure(text="[ AUTO MODE ]", fg='#9b59b6')
            self.mode_desc.configure(text="ตั้งค่าเวลาแล้วกด Start เพื่อรันอัตโนมัติ")
            
            # Show manual controls (for monitoring)
            self.manual_frame.pack(fill='x', pady=(0, 10))
            
            # Update start button
            self.start_btn.configure(text="▶ Start Auto Sequence", state='normal', bg='#27ae60')
            
    # ==================== MANUAL CONTROLS ====================
    def create_manual_controls(self, parent):
        """สร้างส่วนควบคุม Manual"""
        self.manual_frame = tk.LabelFrame(
            parent,
            text="Hardware Controls",
            font=('Helvetica', 10, 'bold'),  # ลดจาก 12 เป็น 10
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=8,
            pady=5
        )
        
        devices = [
            ('S_Valve1', 's_valve1', '#3498db'),
            ('S_Valve2', 's_valve2', '#3498db'),
            ('S_Valve3', 's_valve3', '#3498db'),
            ('S_Valve4', 's_valve4', '#3498db'),
            ('Pump', 'pump', '#27ae60'),
            ('Fan', 'fan', '#f39c12'),
            ('Heater', 'heater', '#e74c3c')
        ]
        
        self.toggle_buttons = {}
        self.status_indicators = {}
        
        for label_text, device_key, color in devices:
            frame = tk.Frame(self.manual_frame, bg='#f0f0f0')
            frame.pack(fill='x', pady=3)
            
            # Device name
            label = tk.Label(
                frame,
                text=label_text,
                font=('Helvetica', 9, 'bold'),  # ลดจาก 11 เป็น 9
                bg='#f0f0f0',
                fg='#2c3e50',
                width=8,  # ลดจาก 10
                anchor='e'
            )
            label.pack(side='left')
            
            # Activate button
            btn = tk.Button(
                frame,
                text="ACTIVATE",
                font=('Helvetica', 8, 'bold'),  # ลดจาก 9 เป็น 8
                bg='#4a4a4a',
                fg='white',
                width=10,  # ลดจาก 12
                activebackground='#666',
                command=lambda k=device_key: self.toggle_device(k)
            )
            btn.pack(side='left', padx=5)  # ลดจาก 10
            self.toggle_buttons[device_key] = btn
            
            # Status indicator
            indicator = tk.Canvas(frame, width=55, height=26, bg='#f0f0f0', highlightthickness=0)
            indicator.pack(side='left')
            indicator.bind('<Button-1>', lambda e, k=device_key: self.toggle_device(k))
            self.status_indicators[device_key] = indicator
            self.draw_toggle_switch(indicator, False)
            
    def draw_toggle_switch(self, canvas, is_on):
        """วาด toggle switch"""
        canvas.delete('all')
        
        if is_on:
            canvas.create_oval(3, 3, 52, 23, fill='#27ae60', outline='#1e8449', width=2)
            canvas.create_oval(30, 1, 54, 25, fill='white', outline='#1e8449', width=2)
        else:
            canvas.create_oval(3, 3, 52, 23, fill='#bdc3c7', outline='#95a5a6', width=2)
            canvas.create_oval(1, 1, 25, 25, fill='white', outline='#95a5a6', width=2)
    
    # ==================== OPERATION SEQUENCE ====================
    def create_operation_sequence(self, parent):
        """สร้างส่วน Operation Sequence (ย้ายไปฝั่งซ้าย)"""
        # Operation sequence display
        seq_frame = tk.LabelFrame(
            parent,
            text="Operation Sequence",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 10
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=8,
            pady=5
        )
        seq_frame.pack(fill='x', pady=(0, 5))
        
        # Flow diagram (ลดข้อความ)
        flow_text = "Heat→BL→Vac→Mix→Meas→VR→Rec"
        tk.Label(
            seq_frame,
            text=flow_text,
            font=('Helvetica', 8),  # ลดจาก 10
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack()
        
        # Progress indicator
        self.progress_label = tk.Label(
            seq_frame,
            text="Ready to start",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 11
            bg='#f0f0f0',
            fg='#27ae60'
        )
        self.progress_label.pack(pady=(5, 0))  # ลดจาก 10
        
        # Timer display
        self.timer_label = tk.Label(
            seq_frame,
            text="--:--",
            font=('Helvetica', 18, 'bold'),  # ลดจาก 24 เป็น 18
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.timer_label.pack(pady=3)  # ลดจาก 5
        
        # Store for scaling
        if 'timer' not in self.scalable_widgets:
            self.scalable_widgets['timer'] = []
        self.scalable_widgets['timer'].append(self.timer_label)
            
    # ==================== AUTO PARAMETERS ====================
    def create_auto_parameters(self, parent):
        """สร้างส่วน Auto Mode Parameters"""
        # Title
        title = tk.Label(
            parent,
            text="Auto Mode Parameters",
            font=('Helvetica', 11, 'bold'),  # ลดจาก 14 เป็น 11
            bg='#f0f0f0',
            fg='#9b59b6'
        )
        title.pack(pady=(0, 5))  # ลดจาก 10
        
        # Parameter source selection
        source_frame = tk.LabelFrame(
            parent,
            text="Parameter Source",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 10 เป็น 9
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=8,
            pady=3
        )
        source_frame.pack(fill='x', pady=(0, 5))  # ลดจาก 10
        
        self.param_source = tk.StringVar(value="ui")
        
        tk.Radiobutton(
            source_frame,
            text="📝 Input from UI",
            variable=self.param_source,
            value="ui",
            font=('Helvetica', 10),
            bg='#f0f0f0',
            command=self.update_param_source
        ).pack(anchor='w')
        
        tk.Radiobutton(
            source_frame,
            text="📁 Load from config.json",
            variable=self.param_source,
            value="config",
            font=('Helvetica', 10),
            bg='#f0f0f0',
            command=self.update_param_source
        ).pack(anchor='w')
        
        # Operation times
        ops_frame = tk.LabelFrame(
            parent,
            text="Operation Duration (seconds)",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 10 เป็น 9
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=8,
            pady=5
        )
        ops_frame.pack(fill='x', pady=(0, 5))  # ลดจาก 10
        
        operations = [
            ("Heating (30m)", 'heating', '#fff59d', '🔥', "Heater ON"),
            ("Baseline (30s)", 'baseline', '#81d4fa', '📊', "SV1+SV3+Pump"),
            ("Vacuum (10s)", 'vacuum', '#b39ddb', '🌀', "SV3+Pump"),
            ("Mix Air (10s)", 'mix_air', '#a5d6a7', '💨', "Fan ON"),
            ("Measure (60s)", 'measure', '#ffcc80', '📏', "SV2+Pump [Data]"),
            ("Vac Return (10s)", 'vacuum_return', '#f48fb1', '🔄', "Pump+SV4 [Process]"),
            ("Recovery (60s)", 'recovery', '#80cbc4', '♻', "SV1+SV3+Pump")
        ]
        
        self.operation_entries = {}
        self.operation_frames = {}
        
        for label_text, key, color, icon, desc in operations:
            frame = tk.Frame(ops_frame, bg=color, padx=5, pady=5)
            frame.pack(fill='x', pady=3)
            self.operation_frames[key] = frame
            
            # Icon + Label
            label = tk.Label(
                frame,
                text=f"{icon} {label_text}",
                font=('Helvetica', 8, 'bold'),  # ลดจาก 10 เป็น 8
                bg=color,
                fg='#2c3e50',
                width=18,  # ลดจาก 22
                anchor='w'
            )
            label.pack(side='left')
            
            # Time entry
            entry = tk.Entry(
                frame,
                textvariable=self.operation_durations[key],
                font=('Helvetica', 9),  # ลดจาก 11
                width=6,  # ลดจาก 8
                justify='center'
            )
            entry.pack(side='right', padx=3)  # ลดจาก 5
            self.operation_entries[key] = entry
            
            # Seconds label
            tk.Label(frame, text="sec", font=('Helvetica', 8), bg=color).pack(side='right')  # ลดจาก 9
            
            # Description tooltip (ซ่อนหรือลดขนาด)
            desc_label = tk.Label(
                frame,
                text="",  # ซ่อน description เพื่อประหยัดพื้นที่
                font=('Helvetica', 7),
                bg=color,
                fg='#666'
            )
            # desc_label.pack(side='right', padx=5)  # comment out
        
        # Break Time Section
        break_frame = tk.LabelFrame(
            parent,
            text="Break Time",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 10
            bg='#f0f0f0',
            fg='#e74c3c',
            padx=8,
            pady=5
        )
        break_frame.pack(fill='x', pady=(0, 5))
        
        break_inner = tk.Frame(break_frame, bg='#ffcdd2', padx=3, pady=3)
        break_inner.pack(fill='x')
        self.operation_frames['break_time'] = break_inner
        
        tk.Label(
            break_inner,
            text="⏸ Break",
            font=('Helvetica', 8, 'bold'),  # ลดจาก 10
            bg='#ffcdd2',
            fg='#c62828',
            width=18,  # ลดจาก 22
            anchor='w'
        ).pack(side='left')
        
        break_entry = tk.Entry(
            break_inner,
            textvariable=self.operation_durations['break_time'],
            font=('Helvetica', 9),  # ลดจาก 11
            width=6,  # ลดจาก 8
            justify='center'
        )
        break_entry.pack(side='right', padx=3)
        self.operation_entries['break_time'] = break_entry
        
        tk.Label(break_inner, text="sec", font=('Helvetica', 8), bg='#ffcdd2').pack(side='right')  # ลดจาก 9
        
        # Loop Settings
        loop_frame = tk.LabelFrame(
            parent,
            text="Loop Settings",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 10
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=8,
            pady=5
        )
        loop_frame.pack(fill='x', pady=(0, 5))
        
        # Infinite loop checkbox
        inf_check = tk.Checkbutton(
            loop_frame,
            text="🔄 Infinite Loop",
            variable=self.infinite_loop,
            font=('Helvetica', 8),  # ลดจาก 10
            bg='#f0f0f0',
            command=self.toggle_loop_settings
        )
        inf_check.pack(anchor='w')
        
        # Loop count (if not infinite)
        loop_count_frame = tk.Frame(loop_frame, bg='#f0f0f0')
        loop_count_frame.pack(fill='x', pady=3)
        
        tk.Label(
            loop_count_frame,
            text="Cycles:",
            font=('Helvetica', 8),  # ลดจาก 10 และลดข้อความ
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.loop_count_entry = tk.Entry(
            loop_count_frame,
            textvariable=self.loop_count,
            font=('Helvetica', 9),  # ลดจาก 11
            width=6,  # ลดจาก 8
            justify='center',
            state='disabled'
        )
        self.loop_count_entry.pack(side='left', padx=5)
        
        tk.Label(
            loop_count_frame,
            text="(0=∞)",
            font=('Helvetica', 8),  # ลดจาก 9 และลดข้อความ
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack(side='left')
        
        # Cycle counter display
        self.cycle_label = tk.Label(
            loop_frame,
            text="Current Cycle: 0",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 11
            bg='#f0f0f0',
            fg='#9b59b6'
        )
        self.cycle_label.pack(pady=3)
        
        # Save config button
        save_btn = tk.Button(
            parent,
            text="💾 Save Config",
            font=('Helvetica', 9),  # ลดจาก 10
            bg='#3498db',
            fg='white',
            command=self.save_current_config
        )
        save_btn.pack(pady=5)  # ลดจาก 10
        
    def toggle_loop_settings(self):
        """Toggle loop count entry based on infinite loop checkbox"""
        if self.infinite_loop.get():
            self.loop_count_entry.configure(state='disabled')
        else:
            self.loop_count_entry.configure(state='normal')
            
    def update_param_source(self):
        """อัพเดทตาม parameter source"""
        if self.param_source.get() == "config":
            # Load from config file
            config = load_config()
            op_times = config.get("operation_times", DEFAULT_CONFIG["operation_times"])
            auto_settings = config.get("auto_settings", DEFAULT_CONFIG["auto_settings"])
            
            # Default values for each operation
            defaults = {
                'heating': 1800,
                'baseline': 30,
                'vacuum': 10,
                'mix_air': 10,
                'measure': 60,
                'vacuum_return': 10,
                'recovery': 60,
                'break_time': 1620
            }
            for key, var in self.operation_durations.items():
                default_val = defaults.get(key, 60)
                var.set(str(op_times.get(key, default_val)))
                self.operation_entries[key].configure(state='disabled')
            
            self.loop_count.set(str(auto_settings.get("loop_count", 0)))
            self.infinite_loop.set(auto_settings.get("infinite_loop", True))
            self.loop_count_entry.configure(state='disabled')
        else:
            # Enable UI input
            for entry in self.operation_entries.values():
                entry.configure(state='normal')
            self.toggle_loop_settings()
                
    def save_current_config(self):
        """บันทึก config ปัจจุบัน"""
        try:
            self.config["operation_times"] = {
                key: int(var.get()) for key, var in self.operation_durations.items()
            }
            self.config["auto_settings"] = {
                "loop_count": int(self.loop_count.get()),
                "infinite_loop": self.infinite_loop.get()
            }
            save_config(self.config)
            messagebox.showinfo("Success", "บันทึก config เรียบร้อยแล้ว!")
        except ValueError:
            messagebox.showerror("Error", "กรุณาใส่ตัวเลขที่ถูกต้อง")
            
    # ==================== ACTION BUTTONS ====================
    def create_action_buttons(self, parent):
        """สร้างปุ่ม Start/Stop"""
        btn_frame = tk.Frame(parent, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=10)
        
        # Stop button
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ Stop",
            font=('Helvetica', 10, 'bold'),  # ลดจาก 12 เป็น 10
            bg='#e74c3c',
            fg='white',
            width=10,  # ลดจาก 12
            height=1,  # ลดจาก 2
            command=self.stop_operation
        )
        self.stop_btn.pack(side='left', padx=3)
        
        # Start button
        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start",
            font=('Helvetica', 10, 'bold'),  # ลดจาก 12 เป็น 10
            bg='#95a5a6',
            fg='white',
            width=15,  # ลดจาก 18
            height=1,  # ลดจาก 2
            state='disabled',
            command=self.start_operation
        )
        self.start_btn.pack(side='left', padx=3)
        
        # Status display
        status_frame = tk.Frame(parent, bg='#f0f0f0')
        status_frame.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready",
            font=('Helvetica', 9, 'bold'),  # ลดจาก 11 เป็น 9
            bg='#f0f0f0',
            fg='#27ae60'
        )
        self.status_label.pack()
        
        # Store for scaling
        if 'status' not in self.scalable_widgets:
            self.scalable_widgets['status'] = []
        self.scalable_widgets['status'].append(self.status_label)
        
    def draw_circuit_diagram(self):
        """Placeholder - Hardware diagram removed"""
        pass
        
    # ==================== DEVICE CONTROL ====================
    def toggle_device(self, device_key):
        """สลับสถานะอุปกรณ์"""
        # ใน Auto mode ขณะ Auto sequence กำลังรันอยู่ ไม่อนุญาตให้สั่ง manual (ป้องกันชนกัน)
        if self.current_mode.get() == "auto" and self.running:
            messagebox.showwarning(
                "Auto Mode Running",
                "ไม่สามารถสั่ง Manual ระหว่าง Auto Sequence กำลังทำงานอยู่\n"
                "กรุณากด Stop ก่อน แล้วจึงใช้ Manual ได้"
            )
            return
        
        # ใช้ Hardware Controller toggle
        is_on = self.hardware.toggle_device(device_key)
        
        # Update UI
        self.draw_toggle_switch(self.status_indicators[device_key], is_on)
        
        btn = self.toggle_buttons[device_key]
        if is_on:
            btn.configure(bg='#27ae60', text="DEACTIVATE")
        else:
            btn.configure(bg='#4a4a4a', text="ACTIVATE")
        
        # Update diagram
        self.draw_circuit_diagram()
        
        # Update status
        self.status_label.configure(text=f"Status: {device_key.title()} {'ON' if is_on else 'OFF'}")
        
    def set_device_state(self, device_key, state):
        """ตั้งค่าสถานะอุปกรณ์โดยตรง"""
        current_state = self.hardware.get_device_state(device_key)
        
        if current_state != state:
            # ใช้ Hardware Controller control
            self.hardware.control_device(device_key, state)
            
            # Update UI
            self.draw_toggle_switch(self.status_indicators[device_key], state)
            
            btn = self.toggle_buttons[device_key]
            if state:
                btn.configure(bg='#27ae60', text="DEACTIVATE")
            else:
                btn.configure(bg='#4a4a4a', text="ACTIVATE")
            
            # Update diagram
            self.draw_circuit_diagram()
            
    # ==================== AUTO SEQUENCE HELPERS ====================
    def _update_device_ui_threadsafe(self, device_key, state):
        """Thread-safe update of device UI"""
        def update():
            self.draw_toggle_switch(self.status_indicators[device_key], state)
            if state:
                self.toggle_buttons[device_key].configure(bg='#27ae60', text="DEACTIVATE")
            else:
                self.toggle_buttons[device_key].configure(bg='#4a4a4a', text="ACTIVATE")
        self.root.after(0, update)
    
    def _set_devices(self, on=None, off=None):
        """Set multiple devices and update UI (thread-safe)"""
        if off:
            for dev in off:
                self.hardware.control_device(dev, False)
                self._update_device_ui_threadsafe(dev, False)
        if on:
            for dev in on:
                self.hardware.control_device(dev, True)
                self._update_device_ui_threadsafe(dev, True)
        time.sleep(0.3)
    
    def _update_operation_ui(self, text, color, op_key=None):
        """Update progress label and highlight operation frame"""
        def update():
            self.progress_label.configure(text=text, fg=color)
            if op_key and op_key in self.operation_frames:
                self.operation_frames[op_key].configure(bg='#f39c12')
        self.root.after(0, update)
    
    def _mark_operation_complete(self, op_key):
        """Mark an operation frame as complete (green)"""
        if op_key in self.operation_frames:
            self.root.after(0, lambda k=op_key: self.operation_frames[k].configure(bg='#81c784'))
    
    def _countdown(self, duration, operation_name):
        """Run countdown timer, returns False if stopped"""
        for remaining in range(duration, 0, -1):
            if not self.running:
                return False
            mins, secs = divmod(remaining, 60)
            def update_timer(m=mins, s=secs, r=remaining, op=operation_name, c=self.current_cycle):
                self.timer_label.configure(text=f"{m:02d}:{s:02d}")
                self.status_label.configure(
                    text=f"Cycle {c} | {op} - {r}s remaining", fg='#f39c12')
            self.root.after(0, update_timer)
            time.sleep(1)
        return True
    
    def _countdown_break(self, duration):
        """Run break countdown timer, returns False if stopped"""
        for remaining in range(duration, 0, -1):
            if not self.running:
                return False
            mins, secs = divmod(remaining, 60)
            def update_timer(m=mins, s=secs, r=remaining):
                self.timer_label.configure(text=f"{m:02d}:{s:02d}")
                self.status_label.configure(
                    text=f"Break Time - Next cycle in {r}s", fg='#e74c3c')
            self.root.after(0, update_timer)
            time.sleep(1)
        return True
    
    def _start_data_collection(self):
        """Start ADC and humidity data collection threads"""
        self.stop_collection_event = threading.Event()
        
        if DATA_COLLECTION_AVAILABLE:
            def adc_wrapper():
                try:
                    print(f"Cycle {self.current_cycle}: Starting ADC data collection...")
                    file_path = run_collection(self.stop_collection_event)
                    self.data_collection_file_path = file_path
                    if file_path:
                        print(f"Cycle {self.current_cycle}: ADC data saved: {file_path}")
                        cycle_num = self.current_cycle
                        file_name = file_path.name
                        self.root.after(0, lambda: self.status_label.configure(
                            text=f"Cycle {cycle_num} | ADC data saved to {file_name}", fg='#27ae60'))
                    else:
                        print(f"Cycle {self.current_cycle}: ADC data collection returned None")
                except Exception as e:
                    print(f"Cycle {self.current_cycle}: ADC error: {e}")
                    traceback.print_exc()
            
            self.data_collection_thread = threading.Thread(target=adc_wrapper, daemon=True)
            self.data_collection_thread.start()
            print(f"Cycle {self.current_cycle}: ADC collection thread started")
        
        if HUMIDITY_COLLECTION_AVAILABLE:
            def humidity_wrapper():
                try:
                    print(f"Cycle {self.current_cycle}: Starting humidity collection...")
                    file_path = run_humidity_collection(
                        stop_event=self.stop_collection_event,
                        sampling_rate=0.5,
                        silent=False
                    )
                    self.humidity_collection_file_path = file_path
                    if file_path:
                        print(f"Cycle {self.current_cycle}: Humidity data saved: {file_path}")
                    else:
                        print(f"Cycle {self.current_cycle}: Humidity collection returned None")
                except Exception as e:
                    print(f"Cycle {self.current_cycle}: Humidity error: {e}")
                    traceback.print_exc()
            
            self.humidity_collection_thread = threading.Thread(target=humidity_wrapper, daemon=True)
            self.humidity_collection_thread.start()
            print(f"Cycle {self.current_cycle}: Humidity collection thread started")
    
    def _stop_data_collection(self):
        """Stop data collection threads and wait for them to finish"""
        if self.stop_collection_event is not None:
            self.stop_collection_event.set()
        
        if self.data_collection_thread is not None and self.data_collection_thread.is_alive():
            print(f"Cycle {self.current_cycle}: Stopping ADC collection...")
            self.data_collection_thread.join(timeout=10)
            if self.data_collection_thread.is_alive():
                print(f"Cycle {self.current_cycle}: Warning: ADC thread did not stop in time")
            else:
                print(f"Cycle {self.current_cycle}: ADC collection stopped successfully")
        
        if self.humidity_collection_thread is not None and self.humidity_collection_thread.is_alive():
            print(f"Cycle {self.current_cycle}: Stopping humidity collection...")
            self.humidity_collection_thread.join(timeout=10)
            if self.humidity_collection_thread.is_alive():
                print(f"Cycle {self.current_cycle}: Warning: Humidity thread did not stop in time")
            else:
                print(f"Cycle {self.current_cycle}: Humidity collection stopped successfully")
    
    def _start_data_processing(self):
        """Start data processing in a separate thread, returns the thread"""
        if not DATA_PROCESSING_AVAILABLE:
            return None
        
        def process_wrapper():
            try:
                print(f"Cycle {self.current_cycle}: Starting data processing...")
                process_data()
                print(f"Cycle {self.current_cycle}: Data processing completed")
                cycle_num = self.current_cycle
                self.root.after(0, lambda: self.status_label.configure(
                    text=f"Cycle {cycle_num} | Data processed!", fg='#27ae60'))
            except Exception as e:
                print(f"Cycle {self.current_cycle}: Processing error: {e}")
                traceback.print_exc()
                cycle_num = self.current_cycle
                self.root.after(0, lambda: self.status_label.configure(
                    text=f"Cycle {cycle_num} | Processing error", fg='#e74c3c'))
        
        thread = threading.Thread(target=process_wrapper, daemon=True)
        thread.start()
        return thread
    
    def _cleanup_collection_threads(self):
        """Clean up any running collection threads from previous cycle"""
        if self.data_collection_thread is not None and self.data_collection_thread.is_alive():
            if self.stop_collection_event is not None:
                self.stop_collection_event.set()
            self.data_collection_thread.join(timeout=2)
        
        if self.humidity_collection_thread is not None and self.humidity_collection_thread.is_alive():
            if self.stop_collection_event is not None:
                self.stop_collection_event.set()
            self.humidity_collection_thread.join(timeout=2)
        
        self._reset_collection_vars()
    
    def _reset_collection_vars(self):
        """Reset collection variables"""
        self.stop_collection_event = None
        self.data_collection_thread = None
        self.data_collection_file_path = None
        self.humidity_collection_thread = None
        self.humidity_collection_file_path = None
    
    # ==================== OPERATION CONTROL ====================
    def start_operation(self):
        """เริ่มการทำงาน"""
        if self.running:
            return
            
        mode = self.current_mode.get()
        
        if mode == "manual":
            # Manual mode: เริ่มการเก็บข้อมูลทันที
            if not DATA_COLLECTION_AVAILABLE and not HUMIDITY_COLLECTION_AVAILABLE:
                messagebox.showerror("Error", "Data collection modules not available")
                return
            
            self.running = True
            self.start_btn.configure(bg='#3498db', text="⏸ Collecting...", state='disabled')
            self.stop_btn.configure(bg='#c0392b')
            self.status_label.configure(text="Status: Collecting data...", fg='#3498db')
            
            # สร้าง stop event สำหรับการเก็บข้อมูล
            self.stop_collection_event = threading.Event()
            
            # เริ่มการเก็บข้อมูล ADC ใน thread แยก
            def adc_collection_wrapper():
                if DATA_COLLECTION_AVAILABLE:
                    try:
                        print("Starting ADC data collection in manual mode...")
                        self.data_collection_file_path = run_collection(self.stop_collection_event)
                        if self.data_collection_file_path:
                            print(f"ADC data collection completed: {self.data_collection_file_path}")
                            self.root.after(0, lambda: self.status_label.configure(
                                text=f"Status: ADC data saved to {self.data_collection_file_path.name}", 
                                fg='#27ae60'))
                    except Exception as e:
                        error_msg = f"ADC Collection error: {str(e)}"
                        print(error_msg)
                        traceback.print_exc()
                        self.root.after(0, lambda: self.status_label.configure(
                            text=f"Status: {error_msg}", fg='#e74c3c'))
                else:
                    print("ADC data collection not available")
            
            # เริ่มการเก็บข้อมูลอุณหภูมิและความชื้นใน thread แยก
            def humidity_collection_wrapper():
                if HUMIDITY_COLLECTION_AVAILABLE:
                    try:
                        print("Starting humidity/temperature collection in manual mode...")
                        self.humidity_collection_file_path = run_humidity_collection(
                            stop_event=self.stop_collection_event,
                            sampling_rate=0.5,  # 0.5 Hz (อ่านทุก 2 วินาที)
                            silent=False
                        )
                        if self.humidity_collection_file_path:
                            print(f"Humidity collection completed: {self.humidity_collection_file_path}")
                            self.root.after(0, lambda: self.status_label.configure(
                                text=f"Status: Humidity data saved to {self.humidity_collection_file_path.name}", 
                                fg='#27ae60'))
                    except Exception as e:
                        error_msg = f"Humidity Collection error: {str(e)}"
                        print(error_msg)
                        traceback.print_exc()
                        self.root.after(0, lambda: self.status_label.configure(
                            text=f"Status: {error_msg}", fg='#e74c3c'))
                else:
                    print("Humidity collection not available")
            
            # เริ่มทั้งสอง threads พร้อมกัน
            if DATA_COLLECTION_AVAILABLE:
                self.data_collection_thread = threading.Thread(target=adc_collection_wrapper, daemon=True)
                self.data_collection_thread.start()
            
            if HUMIDITY_COLLECTION_AVAILABLE:
                self.humidity_collection_thread = threading.Thread(target=humidity_collection_wrapper, daemon=True)
                self.humidity_collection_thread.start()
            
        elif mode == "auto":
            # Auto mode: เริ่ม auto sequence
            self.running = True
            self.start_btn.configure(bg='#3498db', text="⏸ Running...", state='disabled')
            self.stop_btn.configure(bg='#c0392b')
            self.progress_label.configure(text="Starting sequence...", fg='#3498db')
            
            # Start thread
            thread = threading.Thread(target=self.run_auto_sequence, daemon=True)
            thread.start()
            
    def run_auto_sequence(self):
        """รันลำดับ Auto 7 Operations พร้อม Loop และ Break Time
        
        Operation Plan:
        1. Heating:       heater ON (1800s) → ปิด heater เมื่อครบ
        2. Baseline:      s_valve1 + s_valve3 + pump ON (30s)
        3. Vacuum:        s_valve3 + pump ON (10s) [seamless จาก Op2]
        4. Mix Air:       fan ON (10s)
        5. Measure:       s_valve2 + pump ON (60s) → เริ่มเก็บข้อมูล
        6. Vacuum Return: pump + s_valve4 ON (10s) → หยุดเก็บข้อมูล + process_data
        7. Recovery:      s_valve1 + s_valve3 + pump ON (60s)
        Break:            ทั้งหมด OFF (1620s) → วน loop
        """
        
        # Get loop settings
        is_infinite = self.infinite_loop.get()
        try:
            max_cycles = int(self.loop_count.get()) if not is_infinite else 0
        except ValueError:
            max_cycles = 0
        
        self.current_cycle = 0
        ALL_DEVICES = ['s_valve1', 's_valve2', 's_valve3', 's_valve4', 'pump', 'fan', 'heater']
        
        # Main loop
        while self.running:
            self.current_cycle += 1
            
            # Update cycle counter
            self.root.after(0, lambda c=self.current_cycle: 
                          self.cycle_label.configure(text=f"Current Cycle: {c}"))
            
            # Clean up old threads from previous cycle
            self._cleanup_collection_threads()
            
            # Get durations from UI
            durations = {}
            dur_defaults = {
                'heating': 1800, 'baseline': 30, 'vacuum': 10, 'mix_air': 10,
                'measure': 60, 'vacuum_return': 10, 'recovery': 60, 'break_time': 1620
            }
            for key in dur_defaults:
                try:
                    durations[key] = int(self.operation_durations[key].get())
                except (ValueError, KeyError):
                    durations[key] = dur_defaults[key]
            
            process_thread = None  # สำหรับ process_data ใน Op6
            
            # ========== Op1: Heating ==========
            if not self.running:
                break
            
            self.current_operation = 'heating'
            self._update_operation_ui(
                f"Cycle {self.current_cycle} - Op1: Heating", '#f39c12', 'heating')
            
            # Heater ON, all others OFF
            self._set_devices(
                on=['heater'],
                off=['s_valve1', 's_valve2', 's_valve3', 's_valve4', 'pump', 'fan'])
            
            if not self._countdown(durations['heating'], "Op1: Heating"):
                break
            
            # ปิด heater เมื่อครบเวลา
            self._set_devices(off=['heater'])
            self._mark_operation_complete('heating')
            
            # ========== Op2: Baseline ==========
            if not self.running:
                break
            
            self.current_operation = 'baseline'
            self._update_operation_ui(
                f"Cycle {self.current_cycle} - Op2: Baseline", '#f39c12', 'baseline')
            
            # s_valve1 + s_valve3 + pump ON
            self._set_devices(on=['s_valve1', 's_valve3', 'pump'])
            
            if not self._countdown(durations['baseline'], "Op2: Baseline"):
                break
            
            self._mark_operation_complete('baseline')
            
            # ========== Op3: Vacuum (seamless จาก Op2 - แค่ปิด s_valve1) ==========
            if not self.running:
                break
            
            self.current_operation = 'vacuum'
            self._update_operation_ui(
                f"Cycle {self.current_cycle} - Op3: Vacuum", '#f39c12', 'vacuum')
            
            # s_valve3 + pump ยังทำงานต่อ, ปิด s_valve1
            self._set_devices(off=['s_valve1'])
            
            if not self._countdown(durations['vacuum'], "Op3: Vacuum"):
                break
            
            self._mark_operation_complete('vacuum')
            
            # ========== Op4: Mix Air ==========
            if not self.running:
                break
            
            self.current_operation = 'mix_air'
            self._update_operation_ui(
                f"Cycle {self.current_cycle} - Op4: Mix Air", '#f39c12', 'mix_air')
            
            # ปิด s_valve3 + pump, เปิด fan
            self._set_devices(on=['fan'], off=['s_valve3', 'pump'])
            
            if not self._countdown(durations['mix_air'], "Op4: Mix Air"):
                break
            
            self._mark_operation_complete('mix_air')
            
            # ========== Op5: Measure (เริ่มเก็บข้อมูล) ==========
            if not self.running:
                break
            
            self.current_operation = 'measure'
            self._update_operation_ui(
                f"Cycle {self.current_cycle} - Op5: Measure [Recording]", '#f39c12', 'measure')
            
            # ปิด fan, เปิด s_valve2 + pump
            self._set_devices(on=['s_valve2', 'pump'], off=['fan'])
            
            # เริ่มเก็บข้อมูล ADC + Humidity
            if (DATA_COLLECTION_AVAILABLE or HUMIDITY_COLLECTION_AVAILABLE) and self.running:
                self._start_data_collection()
            
            if not self._countdown(durations['measure'], "Op5: Measure [Recording]"):
                break
            
            # หยุดเก็บข้อมูลก่อนเข้า Op6
            self._stop_data_collection()
            self._mark_operation_complete('measure')
            
            # ========== Op6: Vacuum Return (process_data ขนานกับ hardware) ==========
            if not self.running:
                break
            
            self.current_operation = 'vacuum_return'
            self._update_operation_ui(
                f"Cycle {self.current_cycle} - Op6: Vacuum Return [Processing]", '#f39c12', 'vacuum_return')
            
            # ปิด s_valve2, เปิด s_valve4 (pump ยังทำงานต่อ - seamless)
            self._set_devices(on=['s_valve4'], off=['s_valve2'])
            
            # เริ่ม process_data ขนานกับ Op6 hardware
            if self.running and DATA_PROCESSING_AVAILABLE:
                process_thread = self._start_data_processing()
            
            if not self._countdown(durations['vacuum_return'], "Op6: Vacuum Return [Processing]"):
                break
            
            self._mark_operation_complete('vacuum_return')
            
            # ========== Op7: Recovery ==========
            if not self.running:
                break
            
            self.current_operation = 'recovery'
            self._update_operation_ui(
                f"Cycle {self.current_cycle} - Op7: Recovery", '#f39c12', 'recovery')
            
            # ปิด s_valve4, เปิด s_valve1 + s_valve3 (pump ยังทำงานต่อ - seamless)
            self._set_devices(on=['s_valve1', 's_valve3'], off=['s_valve4'])
            
            if not self._countdown(durations['recovery'], "Op7: Recovery"):
                break
            
            self._mark_operation_complete('recovery')
            
            # ========== ปิดอุปกรณ์ทั้งหมด ==========
            self.hardware.all_off()
            for dev in ALL_DEVICES:
                self._update_device_ui_threadsafe(dev, False)
            
            # รอ process_data ถ้ายังทำงานอยู่
            if process_thread is not None and process_thread.is_alive():
                print(f"Cycle {self.current_cycle}: Waiting for data processing to finish...")
                process_thread.join(timeout=30)
                if process_thread.is_alive():
                    print(f"Cycle {self.current_cycle}: Warning: Data processing did not finish in time")
            
            # Reset collection variables
            self._reset_collection_vars()
            
            # Check if should continue looping
            if not self.running:
                break
            
            if not is_infinite and self.current_cycle >= max_cycles:
                break
            
            # ========== Break Time ==========
            if durations['break_time'] > 0 and self.running:
                self.current_operation = 'break_time'
                self.current_operation_index = -1
                
                def update_break_ui(c=self.current_cycle):
                    self.progress_label.configure(
                        text=f"Cycle {c} Complete - Break Time", fg='#e74c3c')
                    if 'break_time' in self.operation_frames:
                        self.operation_frames['break_time'].configure(bg='#e57373')
                
                self.root.after(0, update_break_ui)
                
                self._countdown_break(durations['break_time'])
                
                # Reset break time frame color
                self.root.after(0, lambda: self.operation_frames['break_time'].configure(bg='#ffcdd2'))
                
                # Reset operation colors for next cycle
                self.root.after(0, self.reset_operation_colors)
        
        # Complete
        self.current_operation = None
        self.current_operation_index = -1
        self.running = False
        self.root.after(0, self.operation_complete)
        
    def _set_multiple_devices_ui(self, devices_off, devices_on):
        """Helper function สำหรับตั้งค่าหลายอุปกรณ์และอัพเดท UI"""
        # Turn OFF devices first
        for dev in devices_off:
            self.set_device_state(dev, False)
        
        # Turn ON devices
        for dev in devices_on:
            self.set_device_state(dev, True)
        
    def operation_complete(self):
        """เมื่อ operation เสร็จสิ้น"""
        self.start_btn.configure(bg='#27ae60', text="▶ Start Auto Sequence", state='normal')
        self.stop_btn.configure(bg='#e74c3c')
        self.progress_label.configure(text="✓ Sequence Complete!", fg='#27ae60')
        self.timer_label.configure(text="00:00")
        self.status_label.configure(text="Status: All operations completed!", fg='#27ae60')
        
        # Keep completed colors for a moment, then reset
        self.root.after(3000, self.reset_operation_colors)
        self.draw_circuit_diagram()
        
    def reset_operation_colors(self):
        """รีเซ็ตสี operation frames กลับเป็นปกติ"""
        colors = {
            'heating': '#fff59d',
            'baseline': '#81d4fa',
            'vacuum': '#b39ddb',
            'mix_air': '#a5d6a7',
            'measure': '#ffcc80',
            'vacuum_return': '#f48fb1',
            'recovery': '#80cbc4',
            'break_time': '#ffcdd2'
        }
        for key, color in colors.items():
            if key in self.operation_frames:
                self.operation_frames[key].configure(bg=color)
        
    def stop_operation(self):
        """หยุดการทำงาน"""
        mode = self.current_mode.get()
        was_running = self.running
        self.running = False
        
        # หยุดการเก็บข้อมูลถ้ากำลังรันอยู่
        if self.stop_collection_event is not None:
            print("Stopping data collection...")
            self.stop_collection_event.set()
            if self.data_collection_thread is not None:
                self.data_collection_thread.join(timeout=5)
                if self.data_collection_thread is not None and self.data_collection_thread.is_alive():
                    print("Warning: ADC data collection thread did not stop in time")
            if self.humidity_collection_thread is not None:
                self.humidity_collection_thread.join(timeout=5)
                if self.humidity_collection_thread is not None and self.humidity_collection_thread.is_alive():
                    print("Warning: Humidity collection thread did not stop in time")
        
        # ใน manual mode: รัน process_data() ก่อนหยุดการทำงาน
        if mode == "manual" and was_running and DATA_PROCESSING_AVAILABLE:
            self.status_label.configure(text="Status: Processing data...", fg='#9b59b6')
            self.root.update()
            
            def process_and_finish():
                """Wrapper function สำหรับ error handling"""
                try:
                    print("Manual mode: Starting data processing...")
                    process_data()
                    self.root.after(0, lambda: self.status_label.configure(
                        text="Status: Data processing completed!", fg='#27ae60'))
                    print("Manual mode: Data processing completed successfully")
                except Exception as e:
                    error_msg = f"Processing error: {str(e)}"
                    print(f"Processing error: {error_msg}")
                    traceback.print_exc()
                    self.root.after(0, lambda: self.status_label.configure(
                        text=f"Status: {error_msg}", fg='#e74c3c'))
                finally:
                    # Reset collection variables หลังจากประมวลผลเสร็จ
                    self.stop_collection_event = None
                    self.data_collection_thread = None
                    self.data_collection_file_path = None
                    self.humidity_collection_thread = None
                    self.humidity_collection_file_path = None
                    
                    # ใช้ Hardware Controller ปิดอุปกรณ์ทั้งหมด
                    self.hardware.all_off()
                    
                    # Update UI for all devices
                    for device_key in self.hardware.available_devices:
                        self.draw_toggle_switch(self.status_indicators[device_key], False)
                        self.toggle_buttons[device_key].configure(bg='#4a4a4a', text="ACTIVATE")
                    
                    # Reset UI
                    self.current_operation = None
                    self.current_operation_index = -1
                    
                    self.start_btn.configure(
                        text="▶ Start Collection",
                        state='normal',
                        bg='#27ae60'
                    )
                    self.progress_label.configure(text="Stopped", fg='#e74c3c')
                    self.timer_label.configure(text="--:--")
                    self.draw_circuit_diagram()
            
            # รัน process_data ใน thread แยก (ไม่ block UI)
            process_thread = threading.Thread(target=process_and_finish, daemon=True)
            process_thread.start()
            
            # รอให้ประมวลผลเสร็จ (timeout 60 วินาที)
            process_thread.join(timeout=60)
            if process_thread.is_alive():
                print("Warning: Data processing thread did not finish in time")
                # แม้จะ timeout ก็ยังต้อง reset UI
                self.stop_collection_event = None
                self.data_collection_thread = None
                self.data_collection_file_path = None
                self.humidity_collection_thread = None
                self.humidity_collection_file_path = None
        else:
            # Auto mode หรือไม่มี data processing: reset ทันที
            # Reset collection variables
            self.stop_collection_event = None
            self.data_collection_thread = None
            self.data_collection_file_path = None
            self.humidity_collection_thread = None
            self.humidity_collection_file_path = None
            
            # ใช้ Hardware Controller ปิดอุปกรณ์ทั้งหมด
            self.hardware.all_off()
            
            # Update UI for all devices
            for device_key in self.hardware.available_devices:
                self.draw_toggle_switch(self.status_indicators[device_key], False)
                self.toggle_buttons[device_key].configure(bg='#4a4a4a', text="ACTIVATE")
            
            # Reset UI
            self.current_operation = None
            self.current_operation_index = -1
            
            self.start_btn.configure(
                bg='#27ae60' if mode == 'auto' else '#27ae60',
                text="▶ Start Auto Sequence" if mode == 'auto' else "▶ Start Collection",
                state='normal'
            )
            self.progress_label.configure(text="Stopped", fg='#e74c3c')
            self.timer_label.configure(text="--:--")
            self.status_label.configure(text="Status: Stopped", fg='#e74c3c')
            
            # Reset operation frame colors (สำหรับ auto mode)
            if mode == 'auto':
                self.reset_operation_colors()
            
            self.draw_circuit_diagram()
        
    def on_closing(self):
        """Cleanup"""
        self.running = False
        
        # หยุดการเก็บข้อมูลถ้ากำลังรันอยู่
        self._cleanup_collection_threads()
        
        # ใช้ Hardware Controller cleanup
        self.hardware.cleanup()
            
        self.root.destroy()


def main():
    """Main function"""
    root = tk.Tk()
    
    # แก้ปัญหา GUI ไม่สามารถคลิกได้เมื่อเปิดขึ้นมา
    # ทำให้ window ได้ focus และอยู่ด้านบนก่อนสร้าง UI
    root.update_idletasks()
    root.lift()
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    
    app = HardwareControlGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # ทำให้ window ได้ focus อีกครั้งหลังจากสร้าง UI
    root.update_idletasks()
    root.focus_force()
    root.deiconify()
    
    root.mainloop()


if __name__ == "__main__":
    main()
