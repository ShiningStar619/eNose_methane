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

# Matplotlib สำหรับกราฟการแสดงผล (Process Data)
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    from matplotlib.colors import to_hex
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    to_hex = None

# Pandas สำหรับโหลดข้อมูล processed (ใช้ในหน้าจอการแสดงผล)
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


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
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Maximized window (เต็มจอ แต่ยังมีปุ่ม minimize/maximize/close)
        self.is_maximized = True
        self._maximize()
        self.root.update_idletasks()
        screen_w = self.root.winfo_width()
        screen_h = self.root.winfo_height()
        
        # Bind window resize event
        self.root.bind('<Configure>', self.on_window_resize)
        self.root.bind('<F11>', self.toggle_maximized)
        self.root.bind('<Escape>', lambda e: self.exit_maximized() if self.is_maximized else None)
        
        # Store initial window size for scaling
        self.initial_width = screen_w
        self.initial_height = screen_h
        
        # Store font sizes and widget sizes for scaling
        self.base_fonts = {
            'title': 16,
            'mode_indicator': 14,
            'section_title': 13,
            'label_frame': 12,
            'button': 13,
            'label': 12,
            'entry': 12,
            'timer': 24,
            'status': 10,
            'small': 10
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
        
        # Page navigation
        self.current_page = tk.StringVar(value="control")
        self.pages = {}
        self.nav_buttons = {}
        
        # Create UI
        self.create_main_layout()
        
        # Update window after creating UI
        self.root.update_idletasks()
        
    # ==================== MAXIMIZE & RESIZE HANDLERS ====================
    def _maximize(self):
        """Maximize window (cross-platform)"""
        try:
            self.root.state('zoomed')
        except tk.TclError:
            self.root.attributes('-zoomed', True)

    def _unmaximize(self):
        """Restore window from maximized (cross-platform)"""
        try:
            self.root.state('normal')
        except tk.TclError:
            self.root.attributes('-zoomed', False)

    def toggle_maximized(self, event=None):
        """Toggle maximized window"""
        self.is_maximized = not self.is_maximized
        if self.is_maximized:
            self._maximize()
        else:
            self._unmaximize()
            self.root.geometry("1024x600")
    
    def exit_maximized(self, event=None):
        """Exit maximized mode"""
        self.is_maximized = False
        self._unmaximize()
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
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=5, pady=2)
        self.main_frame = main_frame
        
        # ==================== NAVIGATION BAR (ล่างซ้าย) ====================
        # pack ก่อน canvas เพื่อจองพื้นที่ด้านล่าง
        self.create_navigation_bar(main_frame)
        
        # Content area with Scrollbar
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
        
        def configure_scroll_region(event=None):
            self.content_canvas.update_idletasks()
            bbox = self.content_canvas.bbox('all')
            if bbox:
                self.content_canvas.configure(scrollregion=bbox)
        
        def configure_canvas_width(event=None):
            canvas_width = self.content_canvas.winfo_width()
            if canvas_width > 1:
                self.content_canvas.itemconfig(self.content_canvas_window, width=canvas_width)
        
        content_frame.bind('<Configure>', configure_scroll_region)
        self.content_canvas.bind('<Configure>', configure_canvas_width)
        
        def on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                self.content_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.content_canvas.yview_scroll(1, "units")
        
        self.content_canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.content_canvas.bind_all("<Button-4>", on_mousewheel)
        self.content_canvas.bind_all("<Button-5>", on_mousewheel)
        
        self.content_frame = content_frame
        
        # ==================== PAGE CONTAINER ====================
        self.page_container = tk.Frame(content_frame, bg='#f0f0f0')
        self.page_container.pack(fill='both', expand=False, anchor='n')
        
        # --- Page 1: Control (single-column layout) ---
        page_control = tk.Frame(self.page_container, bg='#f0f0f0')
        self.pages["control"] = page_control
        
        self.create_mode_selection(page_control)
        self.create_operation_sequence(page_control)
        self.create_action_buttons(page_control)
        self.create_manual_controls(page_control)
        
        # --- Page 2: Settings (Auto Mode Parameters) ---
        page_settings = tk.Frame(self.page_container, bg='#f0f0f0')
        self.pages["settings"] = page_settings
        
        self.create_auto_parameters(page_settings)
        
        # --- Page 3: Display (Process Data) ---
        page_display = tk.Frame(self.page_container, bg='#f0f0f0')
        self.pages["display"] = page_display
        
        self.create_display_page(page_display)
        
        # แสดงหน้าแรก
        self.show_page("control")
        
        # Initial mode update
        self.update_mode_ui()
    
    # ==================== NAVIGATION BAR ====================
    def create_navigation_bar(self, parent):
        nav_frame = tk.Frame(parent, bg='#2c3e50', pady=8)
        nav_frame.pack(side='bottom', fill='x')
        
        btn_container = tk.Frame(nav_frame, bg='#2c3e50')
        btn_container.pack(side='right', padx=15)
        
        pages_config = [
            ("control", "Control", '#e67e22'),
            ("display", "Display", '#3498db'),
            ("settings", "Settings", '#27ae60'),
        ]
        
        for page_key, label_text, active_color in pages_config:
            btn = tk.Button(
                btn_container,
                text=label_text,
                font=('Helvetica', 12, 'bold'),
                bg='#4a4a4a',
                fg='white',
                activebackground='#666',
                width=12,
                height=1,
                relief='flat',
                cursor='hand2',
                command=lambda key=page_key: self.show_page(key)
            )
            btn.pack(side='left', padx=5)
            self.nav_buttons[page_key] = (btn, active_color)
    
    # ==================== PAGE SWITCHING ====================
    def show_page(self, page_key):
        """สลับไปหน้าที่เลือก"""
        for key, frame in self.pages.items():
            frame.pack_forget()
        
        if page_key in self.pages:
            self.pages[page_key].pack(fill='both', expand=False, anchor='n')
            self.current_page.set(page_key)
        
        for key, (btn, active_color) in self.nav_buttons.items():
            if key == page_key:
                btn.configure(bg=active_color, relief='sunken')
            else:
                btn.configure(bg='#4a4a4a', relief='flat')
    # ==================== MODE SELECTION ====================
    def create_mode_selection(self, parent):
        """สร้างส่วนเลือกโหมด"""
        mode_frame = tk.LabelFrame(
            parent, 
            text="Control Mode", 
            font=('Helvetica', 15, 'bold'), 
            bg='#f0f0f0',
            fg='#2c3e50',  
            padx=12,
            pady=8
        )
        mode_frame.pack(fill='x', pady=(0, 10))
        
        # Mode buttons: fixed size, centered in Control Mode
        btn_container = tk.Frame(mode_frame, bg='#f0f0f0')
        btn_container.pack(fill='x')
        btn_center = tk.Frame(btn_container, bg='#f0f0f0')
        btn_center.pack(expand=True, anchor='center')
        btn_px_w, btn_px_h = 160, 44
        manual_frame = tk.Frame(btn_center, width=btn_px_w, height=btn_px_h, bg='#f0f0f0')
        manual_frame.pack_propagate(0)
        manual_frame.pack(side='left', padx=(0, 8))
        self.manual_btn = tk.Button(
            manual_frame,
            text="Manual",
            font=('Helvetica', 13, 'bold'),
            bg='#e67e22',
            fg='white',
            relief='raised',
            cursor='hand2',
            command=lambda: self.set_mode("manual")
        )
        self.manual_btn.pack(fill='both', expand=True)
        auto_frame = tk.Frame(btn_center, width=btn_px_w, height=btn_px_h, bg='#f0f0f0')
        auto_frame.pack_propagate(0)
        auto_frame.pack(side='left')
        self.auto_btn = tk.Button(
            auto_frame,
            text="Auto",
            font=('Helvetica', 13, 'bold'),
            bg='#95a5a6',
            fg='white',
            relief='raised',
            cursor='hand2',
            command=lambda: self.set_mode("auto")
        )
        self.auto_btn.pack(fill='both', expand=True)
        
        # Store for scaling
        if 'button' not in self.scalable_widgets:
            self.scalable_widgets['button'] = []
        self.scalable_widgets['button'].extend([self.manual_btn, self.auto_btn])
        
        # Mode description
        self.mode_desc = tk.Label(
            mode_frame,
            text="กดปุ่มเพื่อควบคุม hardware",
            font=('Helvetica', 11),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.mode_desc.pack(pady=(8, 0))
        
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
            self.manual_btn.configure(bg='#e67e22', relief='sunken')
            self.auto_btn.configure(bg='#95a5a6', relief='raised')
            self.mode_desc.configure(text="กดปุ่มเพื่อควบคุม hardware โดยตรง")
            self.manual_frame.pack(fill='x', pady=(0, 10))
            self.start_btn.configure(text="Start Collection", state='normal', bg='#27ae60')
            
        else:  # auto mode
            self.manual_btn.configure(bg='#95a5a6', relief='raised')
            self.auto_btn.configure(bg='#9b59b6', relief='sunken')
            self.mode_desc.configure(text="ตั้งค่าเวลาแล้วกด Start เพื่อรันอัตโนมัติ")
            self.manual_frame.pack(fill='x', pady=(0, 10))
            self.start_btn.configure(text="Start Auto Sequence", state='normal', bg='#27ae60')
            
    # ==================== MANUAL CONTROLS ====================
    def create_manual_controls(self, parent):
        """Hardware Controls: two columns — left Value 1–4, right Pump/Fan/Heater (rounded boxes)."""
        self.manual_frame = tk.LabelFrame(
            parent,
            text="Hardware Controls",
            font=('Helvetica', 15, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=16,
            pady=12
        )
        
        left_devices = [
            ('Value 1', 's_valve1'),
            ('Value 2', 's_valve2'),
            ('Value 3', 's_valve3'),
            ('Value 4', 's_valve4'),
        ]
        right_devices = [
            ('Pump', 'pump'),
            ('Fan', 'fan'),
            ('Heater', 'heater'),
        ]
        
        self.switch_indicators = {}
        self.device_display_names = {}
        self.device_states = {}
        for label_text, dk in left_devices + right_devices:
            self.device_display_names[dk] = label_text
            self.device_states[dk] = False
        
        self.device_names = {dk: label for label, dk in left_devices + right_devices}
        
        self.box_w, self.box_h = 170, 52
        pad_between = 14
        box_pady = 8
        
        two_cols = tk.Frame(self.manual_frame, bg='#f0f0f0')
        two_cols.pack(fill='x', pady=8)
        
        left_col = tk.Frame(two_cols, bg='#f0f0f0')
        left_col.pack(side='left', expand=True, fill='both', padx=(0, pad_between))
        for label_text, device_key in left_devices:
            c = tk.Canvas(left_col, width=self.box_w, height=self.box_h, bg='#f0f0f0', highlightthickness=0)
            c.pack(pady=box_pady)
            c.bind('<Button-1>', lambda e, k=device_key: self.toggle_device(k))
            c.bind('<Enter>', lambda e, c=c: c.configure(cursor='hand2'))
            self.switch_indicators[device_key] = c
            self._draw_device_box(c, label_text, False)
        
        right_col = tk.Frame(two_cols, bg='#f0f0f0')
        right_col.pack(side='left', expand=True, fill='both', padx=(pad_between, 0))
        for label_text, device_key in right_devices:
            c = tk.Canvas(right_col, width=self.box_w, height=self.box_h, bg='#f0f0f0', highlightthickness=0)
            c.pack(pady=box_pady)
            c.bind('<Button-1>', lambda e, k=device_key: self.toggle_device(k))
            c.bind('<Enter>', lambda e, c=c: c.configure(cursor='hand2'))
            self.switch_indicators[device_key] = c
            self._draw_device_box(c, label_text, False)
        
        self.name_labels = {}

    def _draw_device_box(self, canvas, text, is_on):
        """Draw rounded-rectangle box: light grey or green, black outline."""
        canvas.delete('all')
        w = getattr(self, 'box_w', 170)
        h = getattr(self, 'box_h', 52)
        r = min(10, w // 16, (h - 2) // 2)
        fill = '#27ae60' if is_on else '#e0e0e0'
        outline = '#1a1a1a'
        canvas.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=fill, outline=outline, width=1)
        canvas.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, fill=fill, outline=outline, width=1)
        canvas.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, fill=fill, outline=outline, width=1)
        canvas.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, fill=fill, outline=outline, width=1)
        canvas.create_rectangle(r, 0, w-r, h, fill=fill, outline=fill)
        canvas.create_rectangle(0, r, w, h-r, fill=fill, outline=fill)
        canvas.create_line(r, 0, w-r, 0, fill=outline, width=1)
        canvas.create_line(r, h, w-r, h, fill=outline, width=1)
        canvas.create_line(0, r, 0, h-r, fill=outline, width=1)
        canvas.create_line(w, r, w, h-r, fill=outline, width=1)
        canvas.create_text(w//2, h//2, text=text, font=('Helvetica', 12, 'bold'),
                          fill='#1a1a1a' if is_on else '#2c3e50')

    def draw_toggle_switch(self, canvas, is_on):
        """Legacy: now each device is a box; redraw using device_display_names."""
        pass

    def update_switch_button(self, device_key, is_on):
        """Update device box to match ON/OFF state."""
        self.device_states[device_key] = is_on
        c = self.switch_indicators[device_key]
        text = self.device_display_names.get(device_key, device_key)
        self._draw_device_box(c, text, is_on)
    
    # ==================== OPERATION SEQUENCE ====================
    def create_operation_sequence(self, parent):
        """สร้างส่วน Operation Sequence (ขนาดกระทัดรัด)"""
        seq_frame = tk.LabelFrame(
            parent,
            text="Operation Sequence",
            font=('Helvetica', 15, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=12,
            pady=8
        )
        seq_frame.pack(fill='x', pady=(0, 6))
        
        flow_text = "Heat → BL → Vac → Mix → Meas → VR → Rec"
        tk.Label(
            seq_frame,
            text=flow_text,
            font=('Helvetica', 9),
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack(pady=(3, 0))
        
        self.progress_label = tk.Label(
            seq_frame,
            text="Ready to start",
            font=('Helvetica', 11, 'bold'),
            bg='#f0f0f0',
            fg='#27ae60'
        )
        self.progress_label.pack(pady=(5, 0))
        
        self.timer_label = tk.Label(
            seq_frame,
            text="--:--",
            font=('Helvetica', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.timer_label.pack(pady=5)
        
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
            font=('Helvetica', 16, 'bold'),
            bg='#f0f0f0',
            fg='#9b59b6'
        )
        title.pack(pady=(0, 5), anchor='w')
        
        # Two-column container for settings page
        settings_cols = tk.Frame(parent, bg='#f0f0f0')
        settings_cols.pack(fill='both', expand=False, anchor='n')
        
        settings_left = tk.Frame(settings_cols, bg='#f0f0f0')
        settings_left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        settings_right = tk.Frame(settings_cols, bg='#f0f0f0')
        settings_right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Parameter source selection
        source_frame = tk.LabelFrame(
            settings_left,
            text="Parameter Source",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=12,
            pady=8
        )
        source_frame.pack(fill='x', pady=(0, 10))
        
        self.param_source = tk.StringVar(value="ui")
        
        # Row: box-style buttons (no radio circle, full rectangle)
        source_row = tk.Frame(source_frame, bg='#f0f0f0')
        source_row.pack(fill='x', pady=4)
        
        rb_ui = tk.Radiobutton(
            source_row,
            text="  Input from UI  ",
            variable=self.param_source,
            value="ui",
            font=('Helvetica', 12, 'bold'),
            indicatoron=False,
            bg='#e0e0e0',
            selectcolor='#3498db',
            activebackground='#d0d0d0',
            activeforeground='#1a1a1a',
            fg='#2c3e50',
            padx=24,
            pady=14,
            bd=2,
            relief='raised',
            command=self.update_param_source,
            cursor='hand2'
        )
        rb_ui.pack(side='left', padx=(0, 15))
        
        rb_config = tk.Radiobutton(
            source_row,
            text="  Load from config.json  ",
            variable=self.param_source,
            value="config",
            font=('Helvetica', 12, 'bold'),
            indicatoron=False,
            bg='#e0e0e0',
            selectcolor='#3498db',
            activebackground='#d0d0d0',
            activeforeground='#1a1a1a',
            fg='#2c3e50',
            padx=24,
            pady=14,
            bd=2,
            relief='raised',
            command=self.update_param_source,
            cursor='hand2'
        )
        rb_config.pack(side='left')
        
        self.param_source_buttons = (rb_ui, rb_config)
        rb_ui.configure(relief='sunken')  # initial selection is "Input from UI"
        
        # Operation times
        ops_frame = tk.LabelFrame(
            settings_left,
            text="Operation Duration (seconds)",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=12,
            pady=8
        )
        ops_frame.pack(fill='x', pady=(0, 10))
        
        operations = [
            ("Heating (30m)", 'heating', '#fff59d', "Heater ON"),
            ("Baseline (30s)", 'baseline', '#81d4fa', "SV1+SV3+Pump"),
            ("Vacuum (10s)", 'vacuum', '#b39ddb', "SV3+Pump"),
            ("Mix Air (10s)", 'mix_air', '#a5d6a7', "Fan ON"),
            ("Measure (60s)", 'measure', '#ffcc80', "SV2+Pump [Data]"),
            ("Vac Return (10s)", 'vacuum_return', '#f48fb1', "Pump+SV4 [Process]"),
            ("Recovery (60s)", 'recovery', '#80cbc4', "SV1+SV3+Pump")
        ]
        
        self.operation_entries = {}
        self.operation_frames = {}
        
        for label_text, key, color, desc in operations:
            frame = tk.Frame(ops_frame, bg=color, padx=8, pady=6)
            frame.pack(fill='x', pady=4)
            self.operation_frames[key] = frame
            
            # Label
            label = tk.Label(
                frame,
                text=label_text,
                font=('Helvetica', 11, 'bold'),
                bg=color,
                fg='#2c3e50',
                width=18,
                anchor='w'
            )
            label.pack(side='left')
            
            # Description
            desc_label = tk.Label(
                frame,
                text=desc,
                font=('Helvetica', 10),
                bg=color,
                fg='#555'
            )
            desc_label.pack(side='left', padx=(5, 0))
            
            # Time entry
            entry = tk.Entry(
                frame,
                textvariable=self.operation_durations[key],
                font=('Helvetica', 12),
                width=8,
                justify='center'
            )
            entry.pack(side='right', padx=5)
            self.operation_entries[key] = entry
            
            # Seconds label
            tk.Label(frame, text="sec", font=('Helvetica', 11), bg=color).pack(side='right')
        
        # Break Time Section (below Operation Duration)
        break_frame = tk.LabelFrame(
            settings_left,
            text="Break Time",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#e74c3c',
            padx=12,
            pady=8
        )
        break_frame.pack(fill='x', pady=(0, 10))
        
        break_inner = tk.Frame(break_frame, bg='#ffcdd2', padx=8, pady=6)
        break_inner.pack(fill='x')
        self.operation_frames['break_time'] = break_inner
        
        tk.Label(
            break_inner,
            text="Break",
            font=('Helvetica', 11, 'bold'),
            bg='#ffcdd2',
            fg='#c62828',
            width=18,
            anchor='w'
        ).pack(side='left')
        
        break_entry = tk.Entry(
            break_inner,
            textvariable=self.operation_durations['break_time'],
            font=('Helvetica', 12),
            width=8,
            justify='center'
        )
        break_entry.pack(side='right', padx=5)
        self.operation_entries['break_time'] = break_entry
        
        tk.Label(break_inner, text="sec", font=('Helvetica', 11), bg='#ffcdd2').pack(side='right')
        
        # Loop Settings (below Break Time)
        loop_frame = tk.LabelFrame(
            settings_left,
            text="Loop Settings",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=12,
            pady=8
        )
        loop_frame.pack(fill='x', pady=(0, 10))
        
        # Infinite loop checkbox
        inf_check = tk.Checkbutton(
            loop_frame,
            text="Infinite Loop",
            variable=self.infinite_loop,
            font=('Helvetica', 12),
            bg='#f0f0f0',
            command=self.toggle_loop_settings
        )
        inf_check.pack(anchor='w', pady=5)
        
        # Loop count
        loop_count_frame = tk.Frame(loop_frame, bg='#f0f0f0')
        loop_count_frame.pack(fill='x', pady=5)
        
        tk.Label(
            loop_count_frame,
            text="Cycles:",
            font=('Helvetica', 12),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.loop_count_entry = tk.Entry(
            loop_count_frame,
            textvariable=self.loop_count,
            font=('Helvetica', 12),
            width=8,
            justify='center',
            state='disabled'
        )
        self.loop_count_entry.pack(side='left', padx=10)
        
        tk.Label(
            loop_count_frame,
            text="(0 = infinite)",
            font=('Helvetica', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack(side='left')
        
        # Cycle counter display
        self.cycle_label = tk.Label(
            loop_frame,
            text="Current Cycle: 0",
            font=('Helvetica', 14, 'bold'),
            bg='#f0f0f0',
            fg='#9b59b6'
        )
        self.cycle_label.pack(pady=8)
        
        # Save config button (below Loop Settings)
        save_btn = tk.Button(
            settings_left,
            text="Save Config",
            font=('Helvetica', 13, 'bold'),
            bg='#3498db',
            fg='white',
            height=2,
            cursor='hand2',
            command=self.save_current_config
        )
        save_btn.pack(fill='x', pady=10)
        
    def toggle_loop_settings(self):
        """Toggle loop count entry based on infinite loop checkbox"""
        if self.infinite_loop.get():
            self.loop_count_entry.configure(state='disabled')
        else:
            self.loop_count_entry.configure(state='normal')
            
    def update_param_source(self):
        """อัพเดทตาม parameter source และแสดง box ปุ่มที่เลือกเป็น sunken"""
        src = self.param_source.get()
        if hasattr(self, 'param_source_buttons'):
            rb_ui, rb_config = self.param_source_buttons
            rb_ui.configure(relief='sunken' if src == 'ui' else 'raised')
            rb_config.configure(relief='sunken' if src == 'config' else 'raised')
        if src == "config":
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
    
    # ==================== DISPLAY PAGE (Process Data Graph) ====================
    def create_display_page(self, parent):
        """Create display page with Process Data graph in the center."""
        parent.configure(bg='#f0f0f0')
        
        title_label = tk.Label(
            parent,
            text="Display (Process Data)",
            font=('Helvetica', 14, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(10, 6))
        
        graph_frame = tk.Frame(parent, bg='#ffffff', relief='sunken', bd=2)
        graph_frame.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        if MATPLOTLIB_AVAILABLE and PANDAS_AVAILABLE:
            self.display_figure = Figure(figsize=(6, 4), dpi=100, facecolor='#ffffff')
            self.display_canvas = FigureCanvasTkAgg(self.display_figure, master=graph_frame)
            self.display_canvas_widget = self.display_canvas.get_tk_widget()
            self.display_canvas_widget.pack(fill='both', expand=True)
            self.display_canvas_widget.bind('<Configure>', self._on_display_canvas_configure)
            self.display_legend_frame = tk.Frame(parent, bg='#f5f5f5', relief='flat', bd=1, padx=20, pady=8)
            self.display_legend_frame.pack(fill='x', pady=(0, 4))
            self._plot_process_data()
        else:
            self.display_legend_frame = None
            msg = "Install matplotlib and pandas to show the Process Data graph."
            if not MATPLOTLIB_AVAILABLE:
                msg = "Install matplotlib to show the graph: pip install matplotlib"
            tk.Label(
                graph_frame,
                text=msg,
                font=('Helvetica', 11),
                bg='#ffffff',
                fg='#7f8c8d'
            ).pack(expand=True)
        
        if MATPLOTLIB_AVAILABLE and PANDAS_AVAILABLE:
            btn_frame = tk.Frame(parent, bg='#f0f0f0')
            btn_frame.pack(pady=(0, 10))
            refresh_btn = tk.Button(
                btn_frame,
                text="Refresh Graph",
                font=('Helvetica', 10),
                bg='#3498db',
                fg='white',
                command=self._plot_process_data
            )
            refresh_btn.pack()
    
    def _on_display_canvas_configure(self, event):
        """Resize figure to match canvas so graph scales with display."""
        if not MATPLOTLIB_AVAILABLE or not hasattr(self, 'display_figure') or not hasattr(self, 'display_canvas'):
            return
        w, h = event.width, event.height
        if w < 20 or h < 20:
            return
        dpi = self.display_figure.get_dpi()
        self.display_figure.set_size_inches(w / dpi, h / dpi)
        self.display_canvas.draw_idle()
    
    def _refresh_display_graph_if_visible(self):
        """Schedule graph refresh on main thread when Display page is visible (after new data)."""
        if self.current_page.get() != "display":
            return
        if not hasattr(self, 'display_figure') or not hasattr(self, 'display_canvas'):
            return
        self.root.after(0, self._plot_process_data)
    
    def _plot_process_data(self):
        """Load latest Process Data file and plot (thread-safe when called via root.after)."""
        if not MATPLOTLIB_AVAILABLE or not PANDAS_AVAILABLE:
            return
        if not hasattr(self, 'display_figure') or not hasattr(self, 'display_canvas'):
            return
        processed_dir = Path(_project_root) / "acquisition" / "processed_data"
        if not processed_dir.exists():
            self._draw_placeholder_graph("Folder processed_data not found")
            return
        csv_files = list(processed_dir.glob("*.csv"))
        if not csv_files:
            self._draw_placeholder_graph("No Process Data yet. Run a measurement and process first.")
            return
        latest = max(csv_files, key=os.path.getmtime)
        try:
            df = pd.read_csv(latest)
        except Exception as e:
            self._draw_placeholder_graph(f"Failed to read file: {e}")
            return
        plot_cols = [c for c in df.columns if c.endswith('_lp_ma')]
        time_col = 'elapsed_time_sec' if 'elapsed_time_sec' in df.columns else df.columns[0]
        if not plot_cols:
            self._draw_placeholder_graph("No plot columns found (_lp_ma)")
            return
        def _channel_to_sensor_name(col_base):
            """Map ch0_voltage .. ch3_voltage to sensor_1 .. sensor_4 for display."""
            for i in range(4):
                if col_base == f'ch{i}_voltage':
                    return f'sensor_{i+1}'
            return col_base
        
        self.display_figure.clear()
        ax = self.display_figure.add_subplot(111)
        lines = []
        for col in plot_cols:
            col_base = col.replace('_lp_ma', '')
            lbl = _channel_to_sensor_name(col_base)
            line, = ax.plot(df[time_col].values, df[col].values, label=lbl, alpha=0.8)
            lines.append(line)
        ax.set_xlabel('Time (s)', fontsize=10)
        ax.set_ylabel('Voltage (V)', fontsize=10)
        ax.set_title(f'Process Data - {latest.name}', fontsize=11)
        ax.grid(True, alpha=0.3)
        self.display_figure.tight_layout()
        self._update_display_legend(lines)
        self.display_canvas.draw()
    
    def _update_display_legend(self, lines):
        """Fill the legend frame below the graph with color patch + label for each line."""
        if not getattr(self, 'display_legend_frame', None) or not lines or to_hex is None:
            return
        for w in self.display_legend_frame.winfo_children():
            w.destroy()
        for line in lines:
            try:
                color = to_hex(line.get_color())
            except Exception:
                color = '#333333'
            label_text = line.get_label()
            row = tk.Frame(self.display_legend_frame, bg='#f5f5f5')
            row.pack(side='left', padx=(0, 16), pady=2)
            patch = tk.Frame(row, width=14, height=14, bg=color, relief='solid', bd=1)
            patch.pack(side='left', padx=(0, 6))
            patch.pack_propagate(0)
            tk.Label(row, text=label_text, font=('Helvetica', 9), bg='#f5f5f5', fg='#2c3e50').pack(side='left')

    def _draw_placeholder_graph(self, message):
        """Draw placeholder when no data or error."""
        if not MATPLOTLIB_AVAILABLE:
            return
        self.display_figure.clear()
        ax = self.display_figure.add_subplot(111)
        ax.text(0.5, 0.5, message, ha='center', va='center', fontsize=11)
        ax.axis('off')
        if getattr(self, 'display_legend_frame', None):
            for w in self.display_legend_frame.winfo_children():
                w.destroy()
        self.display_canvas.draw()
            
    # ==================== ACTION BUTTONS ====================
    def create_action_buttons(self, parent):
        """สร้างปุ่ม Start/Stop (ขนาดกระทัดรัด)"""
        btn_frame = tk.Frame(parent, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=8)
        
        action_btn_width, action_btn_height = 18, 1
        self.stop_btn = tk.Button(
            btn_frame,
            text="Stop",
            font=('Helvetica', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=action_btn_width,
            height=action_btn_height,
            cursor='hand2',
            command=self.stop_operation
        )
        self.stop_btn.pack(side='left', padx=(0, 8), expand=True, fill='x')
        self.start_btn = tk.Button(
            btn_frame,
            text="Start Collection",
            font=('Helvetica', 11, 'bold'),
            bg='#95a5a6',
            fg='white',
            width=action_btn_width,
            height=action_btn_height,
            state='disabled',
            cursor='hand2',
            command=self.start_operation
        )
        self.start_btn.pack(side='left', expand=True, fill='x')
        
        status_frame = tk.Frame(parent, bg='#f0f0f0')
        status_frame.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready",
            font=('Helvetica', 10, 'bold'),
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
        
        # Update UI (switch button)
        self.update_switch_button(device_key, is_on)
        
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
            
            # Update UI (switch button)
            self.update_switch_button(device_key, state)
            
            # Update diagram
            self.draw_circuit_diagram()
            
    # ==================== AUTO SEQUENCE HELPERS ====================
    def _update_device_ui_threadsafe(self, device_key, state):
        """Thread-safe update of device UI"""
        def update():
            self.update_switch_button(device_key, state)
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
        """Start ADC data collection thread"""
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
        
        self._reset_collection_vars()
    
    def _reset_collection_vars(self):
        """Reset collection variables"""
        self.stop_collection_event = None
        self.data_collection_thread = None
        self.data_collection_file_path = None
    
    # ==================== OPERATION CONTROL ====================
    def start_operation(self):
        """เริ่มการทำงาน"""
        if self.running:
            return
            
        mode = self.current_mode.get()
        
        if mode == "manual":
            # Manual mode: เริ่มการเก็บข้อมูลทันที
            if not DATA_COLLECTION_AVAILABLE:
                messagebox.showerror("Error", "Data collection modules not available")
                return
            
            self.running = True
            self.start_btn.configure(bg='#3498db', text="Collecting...", state='disabled')
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
            
            if DATA_COLLECTION_AVAILABLE:
                self.data_collection_thread = threading.Thread(target=adc_collection_wrapper, daemon=True)
                self.data_collection_thread.start()
            
        elif mode == "auto":
            # Auto mode: เริ่ม auto sequence
            self.running = True
            self.start_btn.configure(bg='#3498db', text="Running...", state='disabled')
            self.stop_btn.configure(bg='#c0392b')
            self.progress_label.configure(text="Starting sequence...", fg='#3498db')
            
            # Start thread
            thread = threading.Thread(target=self.run_auto_sequence, daemon=True)
            thread.start()
            
    def run_auto_sequence(self):
        """รันลำดับ Auto 7 Operations พร้อม Loop และ Break Time
        
        Operation Plan (heater ON ตลอด Op1-Op7):
        1. Heating:       heater ON (1800s)
        2. Baseline:      heater + s_valve1 + s_valve3 + pump ON (30s)
        3. Vacuum:        heater + s_valve3 + pump ON (10s) [seamless จาก Op2]
        4. Mix Air:       heater + fan ON (10s)
        5. Measure:       heater + s_valve2 + pump ON (60s) → เริ่มเก็บข้อมูล
        6. Vacuum Return: heater + pump + s_valve4 ON (10s) → หยุดเก็บข้อมูล + process_data
        7. Recovery:      heater + s_valve1 + s_valve3 + pump ON (60s)
        Break:            ทั้งหมด OFF รวม heater (1620s) → วน loop
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
            
            # heater ยังคง ON ต่อเนื่องตลอด Op1-Op7
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
            
            # เริ่มเก็บข้อมูล ADC
            if DATA_COLLECTION_AVAILABLE and self.running:
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
            
            # Wait for process_data to finish
            if process_thread is not None and process_thread.is_alive():
                print(f"Cycle {self.current_cycle}: Waiting for data processing to finish...")
                process_thread.join(timeout=30)
                if process_thread.is_alive():
                    print(f"Cycle {self.current_cycle}: Warning: Data processing did not finish in time")
            
            # Auto-update Display graph when new processed data is available
            self.root.after(0, self._refresh_display_graph_if_visible)
            
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
        self.start_btn.configure(bg='#27ae60', text="Start Auto Sequence", state='normal')
        self.stop_btn.configure(bg='#e74c3c')
        self.progress_label.configure(text="Sequence Complete!", fg='#27ae60')
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
                    self.root.after(0, self._refresh_display_graph_if_visible)
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
                    
                    # ใช้ Hardware Controller ปิดอุปกรณ์ทั้งหมด
                    self.hardware.all_off()
                    
                    # Update UI for all devices
                    for device_key in self.hardware.available_devices:
                        self.update_switch_button(device_key, False)
                    
                    # Reset UI
                    self.current_operation = None
                    self.current_operation_index = -1
                    
                    self.start_btn.configure(
                        text="Start Collection",
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
        else:
            # Auto mode หรือไม่มี data processing: reset ทันที
            # Reset collection variables
            self.stop_collection_event = None
            self.data_collection_thread = None
            self.data_collection_file_path = None
            
            # ใช้ Hardware Controller ปิดอุปกรณ์ทั้งหมด
            self.hardware.all_off()
            
            # Update UI for all devices
            for device_key in self.hardware.available_devices:
                self.update_switch_button(device_key, False)
            
            # Reset UI
            self.current_operation = None
            self.current_operation_index = -1
            
            self.start_btn.configure(
                bg='#27ae60' if mode == 'auto' else '#27ae60',
                text="Start Auto Sequence" if mode == 'auto' else "Start Collection",
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
