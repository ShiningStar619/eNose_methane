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
    from reading.bme280 import run_bme_collection
    BME_COLLECTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import reading.bme280: {e}")
    BME_COLLECTION_AVAILABLE = False
    run_bme_collection = None

try:
    from acquisition.acquisiton import process_all_data
    DATA_PROCESSING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import acquisition.acquisiton: {e}")
    DATA_PROCESSING_AVAILABLE = False
    process_all_data = None

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

try:
    from cloud.uploader import is_enabled as cloud_upload_is_enabled, upload_cycle_files
    CLOUD_UPLOAD_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import cloud.uploader: {e}")
    CLOUD_UPLOAD_AVAILABLE = False
    cloud_upload_is_enabled = lambda: False  # noqa: E731
    upload_cycle_files = None

try:
    from cloud.config import load_cloud_config, save_cloud_config
    CLOUD_CONFIG_AVAILABLE = True
except ImportError:
    CLOUD_CONFIG_AVAILABLE = False
    load_cloud_config = None
    save_cloud_config = None

try:
    from ml.predict import predict_cycle
    ML_PREDICTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import ml.predict: {e}")
    ML_PREDICTION_AVAILABLE = False
    predict_cycle = None


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

STATUS_COLORS = {
    "idle": "#e74c3c",
    "running": "#3498db",
    "success": "#27ae60",
    "warning": "#f39c12",
    "processing": "#9b59b6",
}

# Max wait time (seconds) when stopping collection threads from Stop button.
# Prevents UI from feeling stuck if a sensor read blocks longer than expected.
STOP_THREAD_JOIN_TIMEOUT_SEC = 5

OPERATION_FRAME_COLORS = {
    'heating': '#fff59d',
    'baseline': '#81d4fa',
    'vacuum': '#b39ddb',
    'mix_air': '#a5d6a7',
    'measure': '#ffcc80',
    'vacuum_return': '#f48fb1',
    'recovery': '#80cbc4',
    'break_time': '#ffcdd2'
}

AUTO_OPERATION_STEPS = [
    {
        "op_key": "heating",
        "ui_title": "Op1: Heating",
        "duration_key": "heating",
        "countdown_title": "Op1: Heating",
        "on": ["heater"],
        "off": ['s_valve1', 's_valve2', 's_valve3', 's_valve4', 'pump', 'fan']
    },
    {
        "op_key": "baseline",
        "ui_title": "Op2: Baseline [Recording]",
        "duration_key": "baseline",
        "countdown_title": "Op2: Baseline",
        "on": ['s_valve1', 's_valve3', 'pump'],
        "off": None,
        "start_collection": True
    },
    {
        "op_key": "vacuum",
        "ui_title": "Op3: Vacuum",
        "duration_key": "vacuum",
        "countdown_title": "Op3: Vacuum",
        "on": None,
        "off": ['s_valve1']
    },
    {
        "op_key": "mix_air",
        "ui_title": "Op4: Mix Air",
        "duration_key": "mix_air",
        "countdown_title": "Op4: Mix Air",
        "on": ['fan'],
        "off": ['s_valve3', 'pump']
    },
    {
        "op_key": "measure",
        "ui_title": "Op5: Measure",
        "duration_key": "measure",
        "countdown_title": "Op5: Measure [Recording]",
        "on": ['s_valve2', 'pump'],
        "off": ['fan']
    },
    {
        "op_key": "vacuum_return",
        "ui_title": "Op6: Vacuum Return",
        "duration_key": "vacuum_return",
        "countdown_title": "Op6: Vacuum Return",
        "on": ['s_valve4'],
        "off": ['s_valve2']
    },
    {
        "op_key": "recovery",
        "ui_title": "Op7: Recovery",
        "duration_key": "recovery",
        "countdown_title": "Op7: Recovery",
        "on": ['s_valve1', 's_valve3'],
        "off": ['s_valve4']
    },
]


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
        self.bme_collection_thread = None  # thread สำหรับ BME280 (คู่ขนานกับ ADC)
        self.data_collection_file_path = None  # เก็บ path ของไฟล์ที่เก็บข้อมูล ADC
        self.bme_collection_file_path = None   # เก็บ path ของไฟล์ที่เก็บข้อมูล BME280
        self._stop_worker_thread = None        # worker ที่ทำงานหลังกด Stop (manual)
        self._stopping_in_progress = False     # กันการกด Stop ซ้ำ

        # Manual timer state
        self.manual_timer_thread = None
        self.manual_timer_stop_event = None

        # Virtual numpad (ช่องตัวเลขที่โฟกัสล่าสุด)
        self._numpad_target_entry = None
        self._numpad_mode = 'int'  # 'int' | 'mmss'
        self._numpad_suppress_focus_until = 0.0
        self.numpad_colon_btn = None
        
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

        middle_row = tk.Frame(page_control, bg='#f0f0f0')
        middle_row.pack(fill='x', pady=(0, 8))
        middle_row.grid_columnconfigure(0, weight=1, uniform='mid')
        middle_row.grid_columnconfigure(1, weight=1, uniform='mid')

        mid_left = tk.Frame(middle_row, bg='#f0f0f0')
        mid_left.grid(row=0, column=0, sticky='ew', padx=(0, 4))

        mid_right = tk.Frame(middle_row, bg='#f0f0f0')
        mid_right.grid(row=0, column=1, sticky='ew', padx=(4, 0))

        self.create_operation_sequence(mid_left)
        self.create_methane_display(mid_right)
        self.create_manual_controls(page_control)
        
        # --- Page 2: Settings (Auto Mode Parameters) ---
        page_settings = tk.Frame(self.page_container, bg='#f0f0f0')
        self.pages["settings"] = page_settings
        
        self.create_auto_parameters(page_settings)
        
        # --- Page 3: Display (Process Data) ---
        page_display = tk.Frame(self.page_container, bg='#f0f0f0')
        self.pages["display"] = page_display
        
        self.create_display_page(page_display)

        # แป้นตัวเลข — popup window (สร้างครั้งเดียว ใช้ซ้ำ)
        self.numpad_window = None
        self.numpad_colon_btn = None
        
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

        if page_key == 'display':
            self._hide_numpad()
        
        for key, (btn, active_color) in self.nav_buttons.items():
            if key == page_key:
                btn.configure(bg=active_color, relief='sunken')
            else:
                btn.configure(bg='#4a4a4a', relief='flat')

    # ==================== VIRTUAL NUMPAD (POPUP) ====================
    def _build_numpad_window(self):
        """สร้าง popup numpad (Toplevel) — เรียกครั้งเดียว แล้ว show/hide ทีหลัง"""
        win = tk.Toplevel(self.root)
        win.title("แป้นตัวเลข")
        win.transient(self.root)
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", self._hide_numpad)
        win.withdraw()

        outer = tk.Frame(win, bg='#ecf0f1', padx=10, pady=8)
        outer.pack(fill='both', expand=True)

        header = tk.Frame(outer, bg='#ecf0f1')
        header.pack(fill='x', pady=(0, 6))
        tk.Label(
            header, text="แป้นตัวเลข",
            font=('Helvetica', 12, 'bold'),
            bg='#ecf0f1', fg='#2c3e50'
        ).pack(side='left')

        inner = tk.Frame(outer, bg='#ecf0f1')
        inner.pack()

        def mk_btn(text, cmd, r, c, **extra):
            b = tk.Button(
                inner,
                text=text,
                font=('Helvetica', 16, 'bold'),
                width=5,
                height=2,
                cursor='hand2',
                bg='#bdc3c7',
                activebackground='#95a5a6',
                fg='#2c3e50',
                command=cmd,
                **extra
            )
            b.grid(row=r, column=c, padx=4, pady=4, sticky='ew')
            return b

        digits = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
        ]
        for d, r, c in digits:
            mk_btn(d, lambda x=d: self._numpad_insert_char(x), r, c)

        mk_btn('⌫', self._numpad_backspace, 3, 0)
        mk_btn('0', lambda: self._numpad_insert_char('0'), 3, 1)
        mk_btn('C', self._numpad_clear, 3, 2)

        tk.Button(
            outer, text='Enter',
            font=('Helvetica', 12, 'bold'),
            bg='#27ae60', fg='white',
            activebackground='#1e8449',
            relief='raised', cursor='hand2',
            command=self._on_numpad_enter
        ).pack(fill='x', pady=(8, 0))

        for col in range(3):
            inner.grid_columnconfigure(col, weight=1)

        win.bind('<Return>', self._on_numpad_enter)
        win.bind('<KP_Enter>', self._on_numpad_enter)
        self.numpad_window = win

    def _show_numpad(self, entry_widget):
        """แสดง popup numpad ใกล้ ๆ entry"""
        if self.numpad_window is None:
            self._build_numpad_window()

        self.numpad_window.deiconify()
        self.numpad_window.lift()
        self.numpad_window.update_idletasks()

        try:
            ex = entry_widget.winfo_rootx()
            ey = entry_widget.winfo_rooty()
            eh = entry_widget.winfo_height()
            ew = entry_widget.winfo_width()
        except tk.TclError:
            ex, ey, eh, ew = 0, 0, 0, 0

        nw = self.numpad_window.winfo_width()
        nh = self.numpad_window.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        x = ex + ew + 10
        if x + nw > sw:
            x = max(0, ex - nw - 10)
        y = ey
        if y + nh > sh:
            y = max(0, sh - nh - 20)

        self.numpad_window.geometry(f"+{x}+{y}")

    def _hide_numpad(self):
        # กัน popup เด้งกลับทันทีหลังสั่งปิด (เช่นกดปุ่ม X บน title bar)
        self._numpad_suppress_focus_until = time.monotonic() + 0.3
        try:
            self.root.focus_set()
        except tk.TclError:
            pass
        self._numpad_target_entry = None
        if self.numpad_window is not None:
            try:
                self.numpad_window.withdraw()
            except tk.TclError:
                pass

    def _register_numpad_entry(self, entry_widget, mode='int'):
        """ผูก Entry: คลิก/โฟกัส → popup numpad"""
        entry_widget.bind(
            '<FocusIn>',
            lambda e, w=entry_widget, m=mode: self._on_numpad_focus(w, m)
        )
        entry_widget.bind(
            '<Button-1>',
            lambda e, w=entry_widget, m=mode: self._on_numpad_focus(w, m)
        )
        entry_widget.bind('<Return>', self._on_numpad_enter)
        entry_widget.bind('<KP_Enter>', self._on_numpad_enter)

    def _on_numpad_focus(self, entry_widget, mode):
        if time.monotonic() < self._numpad_suppress_focus_until:
            return
        try:
            if str(entry_widget.cget('state')) == 'disabled':
                self._hide_numpad()
                return
        except tk.TclError:
            return

        self._numpad_target_entry = entry_widget
        self._numpad_mode = mode

        if self.numpad_window is None:
            self._build_numpad_window()
        if self.numpad_colon_btn is not None:
            self.numpad_colon_btn.configure(
                state='normal' if mode == 'mmss' else 'disabled'
            )

        self._show_numpad(entry_widget)

    def _numpad_target_ok(self):
        e = self._numpad_target_entry
        if e is None:
            return False
        try:
            if not e.winfo_exists():
                return False
            if str(e.cget('state')) == 'disabled':
                return False
        except tk.TclError:
            return False
        return True

    def _numpad_insert_char(self, ch):
        if not self._numpad_target_ok():
            return
        if self._numpad_mode != 'mmss' and ch == ':':
            return
        e = self._numpad_target_entry
        try:
            e.focus_set()
            pos = e.index(tk.INSERT)
            e.insert(pos, ch)
        except tk.TclError:
            pass

    def _numpad_backspace(self):
        if not self._numpad_target_ok():
            return
        e = self._numpad_target_entry
        try:
            e.focus_set()
            pos = e.index(tk.INSERT)
            if pos > 0:
                e.delete(pos - 1, pos)
        except tk.TclError:
            pass

    def _numpad_clear(self):
        if not self._numpad_target_ok():
            return
        e = self._numpad_target_entry
        try:
            e.focus_set()
            e.delete(0, tk.END)
        except tk.TclError:
            pass

    def _on_numpad_enter(self, event=None):
        """เมื่อกด Enter ให้ปิดแป้นตัวเลข และคงค่าที่กรอกไว้"""
        # กัน popup เด้งกลับทันทีจาก FocusIn ที่เกิดหลังแตะปุ่ม Enter บนหน้าจอสัมผัส
        self._numpad_suppress_focus_until = time.monotonic() + 0.3
        try:
            self.root.focus_set()
        except tk.TclError:
            pass
        self._hide_numpad()
        return "break"
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
        
        # --- Timer row ---
        timer_row = tk.Frame(self.manual_frame, bg='#f0f0f0')
        timer_row.pack(fill='x', pady=(0, 8))

        self.manual_timer_enabled = tk.BooleanVar(value=False)
        tk.Checkbutton(
            timer_row,
            text="Use Timer",
            variable=self.manual_timer_enabled,
            font=('Helvetica', 12),
            bg='#f0f0f0',
            activebackground='#f0f0f0',
            command=self._on_manual_timer_toggle
        ).pack(side='left')

        self.manual_timer_duration = tk.StringVar(value="300")
        self.manual_timer_entry = tk.Entry(
            timer_row,
            textvariable=self.manual_timer_duration,
            font=('Helvetica', 12),
            width=8,
            justify='center',
            state='disabled'
        )
        self.manual_timer_entry.pack(side='left', padx=8)

        self._register_numpad_entry(self.manual_timer_entry, mode='int')

        tk.Label(
            timer_row,
            text="(ss)",
            font=('Helvetica', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        ).pack(side='left')

        self.manual_timer_remaining_label = tk.Label(
            timer_row,
            text="",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.manual_timer_remaining_label.pack(side='right')

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
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50',
            padx=8,
            pady=6
        )
        seq_frame.pack(fill='x', anchor='n')

        flow_text = "Heat → BL → Vac → Mix → Meas → VR → Rec"
        tk.Label(
            seq_frame,
            text=flow_text,
            font=('Helvetica', 8),
            bg='#f0f0f0',
            fg='#7f8c8d',
            wraplength=200,
            justify='center',
        ).pack(pady=(2, 0))

        self.progress_label = tk.Label(
            seq_frame,
            text="Ready to start",
            font=('Helvetica', 10, 'bold'),
            bg='#f0f0f0',
            fg='#27ae60'
        )
        self.progress_label.pack(pady=(2, 0))

        self.timer_label = tk.Label(
            seq_frame,
            text="--:--",
            font=('Helvetica', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.timer_label.pack(pady=(2, 4))

        # Store for scaling
        if 'timer' not in self.scalable_widgets:
            self.scalable_widgets['timer'] = []
        self.scalable_widgets['timer'].append(self.timer_label)

        self.create_action_buttons(seq_frame, compact=True)

    def create_methane_display(self, parent):
        """กล่องแสดงค่าทำนายปริมาณ Methane (เปล่าไว้รอเชื่อมโมเดลในอนาคต)."""
        methane_frame = tk.LabelFrame(
            parent,
            text="Methane",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#e67e22',
            padx=8,
            pady=6,
            bd=2,
            relief='groove',
        )
        methane_frame.pack(fill='x', anchor='n')

        self.methane_ppm_value = tk.StringVar(value="----")

        value_center = tk.Frame(methane_frame, bg='#f0f0f0')
        value_center.pack(fill='x', pady=(4, 6))

        self.methane_value_label = tk.Label(
            value_center,
            textvariable=self.methane_ppm_value,
            font=('Helvetica', 22, 'bold'),
            bg='#f0f0f0',
            fg='#e67e22',
        )
        self.methane_value_label.pack()

        tk.Label(
            value_center,
            text="ppm",
            font=('Helvetica', 12, 'bold'),
            bg='#f0f0f0',
            fg='#e67e22',
        ).pack()

    def update_methane_ppm(self, value):
        """Update displayed methane ppm value.

        Args:
            value: float | None — None = ไม่มีค่า แสดง '----'
        """
        if value is None:
            self.methane_ppm_value.set("----")
        else:
            try:
                self.methane_ppm_value.set(f"{float(value):.1f}")
            except (TypeError, ValueError):
                self.methane_ppm_value.set("----")

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
            self._register_numpad_entry(entry, mode='int')
            
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
        self._register_numpad_entry(break_entry, mode='int')
        
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
        self._register_numpad_entry(self.loop_count_entry, mode='int')
        
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
        csv_files = list(processed_dir.glob("adc1263_*.csv"))
        if not csv_files:
            self._draw_placeholder_graph("No ADC Process Data yet. Run a measurement and process first.")
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
        ax.set_title(f'ADC Process Data - {latest.name}', fontsize=11)
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
    def create_action_buttons(self, parent, compact=False):
        """สร้างปุ่ม Start/Stop (ขนาดกระทัดรัด)"""
        btn_frame = tk.Frame(parent, bg='#f0f0f0')
        btn_frame.pack(fill='x', pady=(4 if compact else 8, 2 if compact else 8))

        btn_font = ('Helvetica', 10, 'bold') if compact else ('Helvetica', 11, 'bold')
        action_btn_height = 1
        self.stop_btn = tk.Button(
            btn_frame,
            text="Stop",
            font=btn_font,
            bg='#e74c3c',
            fg='white',
            height=action_btn_height,
            cursor='hand2',
            command=self.stop_operation
        )
        self.stop_btn.pack(side='left', padx=(0, 4), expand=True, fill='x')
        self.start_btn = tk.Button(
            btn_frame,
            text="Start Collection",
            font=btn_font,
            bg='#95a5a6',
            fg='white',
            height=action_btn_height,
            state='disabled',
            cursor='hand2',
            command=self.start_operation
        )
        self.start_btn.pack(side='left', expand=True, fill='x')

        status_frame = tk.Frame(parent, bg='#f0f0f0')
        status_frame.pack(fill='x', pady=(2 if compact else 5, 0))
        
        status_font = ('Helvetica', 9, 'bold') if compact else ('Helvetica', 10, 'bold')
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready",
            font=status_font,
            bg='#f0f0f0',
            fg='#27ae60',
            wraplength=200 if compact else 0,
            justify='center',
        )
        self.status_label.pack()

        # Cloud upload (optional)
        cloud_row = tk.Frame(status_frame, bg='#f0f0f0')
        cloud_row.pack(fill='x', pady=(4 if compact else 6, 0))
        cloud_enabled_init = False
        if CLOUD_CONFIG_AVAILABLE and load_cloud_config is not None:
            try:
                cloud_enabled_init = bool(load_cloud_config().get("enabled"))
            except Exception:
                cloud_enabled_init = False
        self.cloud_upload_enabled = tk.BooleanVar(value=cloud_enabled_init)
        self.cloud_upload_checkbox = tk.Checkbutton(
            cloud_row,
            text="Auto-upload to Cloud",
            variable=self.cloud_upload_enabled,
            font=('Helvetica', 9),
            bg='#f0f0f0',
            fg='#2c3e50',
            command=self._on_cloud_upload_toggle,
            state='normal' if CLOUD_CONFIG_AVAILABLE else 'disabled',
            cursor='hand2',
        )
        self.cloud_upload_checkbox.pack(side='left')
        self.cloud_status_label = tk.Label(
            cloud_row,
            text="Cloud: —",
            font=('Helvetica', 9),
            bg='#f0f0f0',
            fg='#7f8c8d',
        )
        self.cloud_status_label.pack(side='right', padx=(8, 0))

        # Indeterminate progress bar — แสดงเฉพาะตอนกำลัง save / process
        self.status_progressbar = ttk.Progressbar(
            status_frame, mode='indeterminate', length=160 if compact else 240
        )
        # ไม่ pack ตอนเริ่มต้น (ซ่อนไว้)

        # Store for scaling
        if 'status' not in self.scalable_widgets:
            self.scalable_widgets['status'] = []
        self.scalable_widgets['status'].append(self.status_label)
        self.scalable_widgets['status'].append(self.cloud_status_label)
        self.scalable_widgets['status'].append(self.cloud_upload_checkbox)
        
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
    def _run_on_ui_thread(self, callback):
        """Run callback on Tk UI thread."""
        self.root.after(0, callback)

    def _set_status_text(self, text, color):
        """Update status label in thread-safe way."""
        self._run_on_ui_thread(lambda: self.status_label.configure(text=text, fg=color))

    def _show_progress(self, visible):
        """Show/hide and start/stop the indeterminate progress bar (thread-safe)."""
        def update():
            bar = getattr(self, 'status_progressbar', None)
            if bar is None:
                return
            try:
                if visible:
                    if not bar.winfo_ismapped():
                        bar.pack(pady=(4, 0))
                    bar.start(12)
                else:
                    bar.stop()
                    bar.pack_forget()
            except tk.TclError:
                pass
        self._run_on_ui_thread(update)

    def _update_device_ui_threadsafe(self, device_key, state):
        """Thread-safe update of device UI"""
        self._run_on_ui_thread(lambda: self.update_switch_button(device_key, state))
    
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
                self.operation_frames[op_key].configure(bg=STATUS_COLORS["warning"])
        self._run_on_ui_thread(update)
    
    def _mark_operation_complete(self, op_key):
        """Mark an operation frame as complete (green)"""
        if op_key in self.operation_frames:
            self._run_on_ui_thread(lambda k=op_key: self.operation_frames[k].configure(bg='#81c784'))
    
    def _countdown(self, duration, operation_name):
        """Run countdown timer, returns False if stopped"""
        for remaining in range(duration, 0, -1):
            if not self.running:
                return False
            mins, secs = divmod(remaining, 60)
            def update_timer(m=mins, s=secs, r=remaining, op=operation_name, c=self.current_cycle):
                self.timer_label.configure(text=f"{m:02d}:{s:02d}")
                self.status_label.configure(
                    text=f"Cycle {c} | {op} - {r}s remaining", fg=STATUS_COLORS["warning"])
            self._run_on_ui_thread(update_timer)
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
                    text=f"Break Time - Next cycle in {r}s", fg=STATUS_COLORS["idle"])
            self._run_on_ui_thread(update_timer)
            time.sleep(1)
        return True
    
    def _start_data_collection(self):
        """Start ADC + BME280 data collection threads (ใช้ stop_event ตัวเดียวกัน)"""
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
                        self._set_status_text(
                            f"Cycle {cycle_num} | ADC data saved to {file_name}",
                            STATUS_COLORS["success"]
                        )
                    else:
                        print(f"Cycle {self.current_cycle}: ADC data collection returned None")
                except Exception as e:
                    print(f"Cycle {self.current_cycle}: ADC error: {e}")
                    traceback.print_exc()
            
            self.data_collection_thread = threading.Thread(target=adc_wrapper, daemon=True)
            self.data_collection_thread.start()
            print(f"Cycle {self.current_cycle}: ADC collection thread started")
        
        if BME_COLLECTION_AVAILABLE:
            def bme_wrapper():
                try:
                    print(f"Cycle {self.current_cycle}: Starting BME280 data collection...")
                    file_path = run_bme_collection(self.stop_collection_event)
                    self.bme_collection_file_path = file_path
                    if file_path:
                        print(f"Cycle {self.current_cycle}: BME280 data saved: {file_path}")
                    else:
                        print(f"Cycle {self.current_cycle}: BME280 data collection returned None")
                except Exception as e:
                    print(f"Cycle {self.current_cycle}: BME280 error: {e}")
                    traceback.print_exc()
            
            self.bme_collection_thread = threading.Thread(target=bme_wrapper, daemon=True)
            self.bme_collection_thread.start()
            print(f"Cycle {self.current_cycle}: BME280 collection thread started")
    
    def _stop_data_collection(self):
        """Stop data collection threads (ADC + BME280) and wait for save to finish.

        เรียกจาก auto-sequence thread ดังนั้น join() ไม่บล็อก UI
        ใช้ timeout ยาว (60s) เพื่อให้แน่ใจว่า np.savez() เสร็จสมบูรณ์ก่อนประมวลผล
        """
        if self.stop_collection_event is not None:
            self.stop_collection_event.set()

        if self.data_collection_thread is not None and self.data_collection_thread.is_alive():
            print(f"Cycle {self.current_cycle}: Stopping ADC collection...")
            self.data_collection_thread.join(timeout=60)
            if self.data_collection_thread.is_alive():
                print(f"Cycle {self.current_cycle}: Warning: ADC thread did not stop in time")
            else:
                print(f"Cycle {self.current_cycle}: ADC collection stopped successfully")

        if self.bme_collection_thread is not None and self.bme_collection_thread.is_alive():
            print(f"Cycle {self.current_cycle}: Stopping BME280 collection...")
            self.bme_collection_thread.join(timeout=60)
            if self.bme_collection_thread.is_alive():
                print(f"Cycle {self.current_cycle}: Warning: BME280 thread did not stop in time")
            else:
                print(f"Cycle {self.current_cycle}: BME280 collection stopped successfully")
    
    def _run_data_processing(self):
        """Process latest collected data using stored input paths.

        เรียกได้เฉพาะใน background thread (เช่น auto-sequence thread หรือ stop worker)
        เพราะ process_all_data เป็นงานที่ใช้ CPU/IO หนัก

        Returns
        -------
        tuple[bool, dict | None]
            (success, process_all_data results) — results keys: adc1263, bme280 → Path | None
        """
        if not DATA_PROCESSING_AVAILABLE:
            return False, None

        cycle_num = self.current_cycle
        try:
            print(f"Cycle {cycle_num}: Starting data processing...")
            input_paths = {
                'adc1263': self.data_collection_file_path,
                'bme280': self.bme_collection_file_path,
            }
            results = process_all_data(input_paths=input_paths)
            print(f"Cycle {cycle_num}: Data processing completed")
            return True, results
        except Exception as e:
            print(f"Cycle {cycle_num}: Processing error: {e}")
            traceback.print_exc()
            return False, None

    def _on_cloud_upload_toggle(self):
        """Persist Auto-upload checkbox to program/cloud_config.json."""
        if not CLOUD_CONFIG_AVAILABLE or save_cloud_config is None:
            return
        try:
            save_cloud_config({"enabled": bool(self.cloud_upload_enabled.get())})
        except Exception as e:
            print(f"[cloud] Could not save cloud_config: {e}")

    def _update_cloud_status(self, phase: str, message: str):
        """Update cloud status label (must run on UI thread)."""
        colors = {
            "uploading": STATUS_COLORS["processing"],
            "ok": STATUS_COLORS["success"],
            "warning": STATUS_COLORS["warning"],
            "error": STATUS_COLORS["idle"],
            "idle": "#7f8c8d",
        }
        fg = colors.get(phase, "#2c3e50")
        if hasattr(self, "cloud_status_label"):
            try:
                self.cloud_status_label.configure(text=message, fg=fg)
            except tk.TclError:
                pass

    def _maybe_cloud_upload(
        self,
        adc_npz,
        bme_npz,
        proc_paths,
    ):
        """Schedule Drive upload if module enabled and config enabled."""
        if not CLOUD_UPLOAD_AVAILABLE or upload_cycle_files is None:
            return
        if not cloud_upload_is_enabled():
            self._run_on_ui_thread(
                lambda: self._update_cloud_status("idle", "Cloud: off")
            )
            return
        adc_csv = None
        bme_csv = None
        if proc_paths:
            adc_csv = proc_paths.get("adc1263")
            bme_csv = proc_paths.get("bme280")
        if adc_npz is None and bme_npz is None and adc_csv is None and bme_csv is None:
            return

        def on_status(phase, msg):
            self.root.after(0, lambda p=phase, m=msg: self._update_cloud_status(p, m))

        try:
            upload_cycle_files(adc_npz, bme_npz, adc_csv, bme_csv, on_status=on_status)
        except Exception as e:
            print(f"[cloud] upload_cycle_files: {e}")
            self._run_on_ui_thread(
                lambda m=str(e): self._update_cloud_status("error", f"Cloud: {m[:80]}")
            )
    
    def _cleanup_collection_threads(self):
        """Clean up any running collection threads from previous cycle (ADC + BME280)"""
        adc_alive = self.data_collection_thread is not None and self.data_collection_thread.is_alive()
        bme_alive = self.bme_collection_thread is not None and self.bme_collection_thread.is_alive()
        
        if adc_alive or bme_alive:
            if self.stop_collection_event is not None:
                self.stop_collection_event.set()
            
            if adc_alive:
                self.data_collection_thread.join(timeout=2)
            if bme_alive:
                self.bme_collection_thread.join(timeout=2)
        
        self._reset_collection_vars()
    
    def _reset_collection_vars(self):
        """Reset collection variables"""
        self.stop_collection_event = None
        self.data_collection_thread = None
        self.bme_collection_thread = None
        self.data_collection_file_path = None
        self.bme_collection_file_path = None

    def _get_operation_durations(self):
        """อ่านค่า duration จาก UI พร้อม fallback ค่า default"""
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
        durations = {}
        for key, default_value in defaults.items():
            try:
                durations[key] = int(self.operation_durations[key].get())
            except (ValueError, KeyError):
                durations[key] = default_value
        return durations

    def _sync_all_devices_off(self, preserve=None):
        """ปิดอุปกรณ์ทั้งหมดและซิงก์ UI ให้เป็นสถานะ OFF
        
        Args:
            preserve: list of device keys ที่จะไม่ปิด (เช่น ['heater'])
        """
        preserve = preserve or []
        for device_key in self.hardware.available_devices:
            if device_key not in preserve:
                self.hardware.control_device(device_key, False)
                self.update_switch_button(device_key, False)

    def _reset_ui_after_stop(self, mode, status_text="Status: Stopped", status_color='#e74c3c', preserve_devices=None):
        """รีเซ็ต UI หลังหยุดการทำงาน (ใช้ร่วมกันทั้ง manual/auto)"""
        self._reset_collection_vars()
        self._sync_all_devices_off(preserve=preserve_devices)

        self.current_operation = None
        self.current_operation_index = -1

        self.start_btn.configure(
            text="Start Auto Sequence" if mode == 'auto' else "Start Collection",
            state='normal',
            bg='#27ae60'
        )
        self.stop_btn.configure(bg=STATUS_COLORS["idle"], state='normal')
        self.progress_label.configure(text="Stopped", fg='#e74c3c')
        self.timer_label.configure(text="--:--")
        if status_text is not None:
            self.status_label.configure(text=status_text, fg=status_color)

        if mode == 'auto':
            self.reset_operation_colors()

        self.draw_circuit_diagram()

    def _run_auto_step(
        self,
        op_key,
        ui_title,
        duration,
        countdown_title,
        on=None,
        off=None,
        start_collection=False
    ):
        """รันหนึ่ง operation step ใน auto sequence"""
        if not self.running:
            return False

        if start_collection and DATA_COLLECTION_AVAILABLE and self.running:
            self._start_data_collection()

        self.current_operation = op_key
        self._update_operation_ui(
            f"Cycle {self.current_cycle} - {ui_title}",
            STATUS_COLORS["warning"],
            op_key
        )
        self._set_devices(on=on, off=off)

        if not self._countdown(duration, countdown_title):
            return False

        self._mark_operation_complete(op_key)
        return True

    def _finalize_cycle_devices_and_processing(self):
        """หยุด collection, ปิดอุปกรณ์ทั้งหมด, และประมวลผลข้อมูล (รันใน auto-thread)"""
        cycle_num = self.current_cycle
        self._set_status_text(
            f"Cycle {cycle_num} | Saving data...", STATUS_COLORS["processing"]
        )
        self._show_progress(True)

        self._stop_data_collection()

        self.hardware.all_off()
        for dev in self.hardware.available_devices:
            self._update_device_ui_threadsafe(dev, False)

        if self.running and DATA_PROCESSING_AVAILABLE:
            self._set_status_text(
                f"Cycle {cycle_num} | Processing...", STATUS_COLORS["processing"]
            )
            adc_npz = self.data_collection_file_path
            bme_npz = self.bme_collection_file_path
            ok, proc_paths = self._run_data_processing()
            if ok:
                self._set_status_text(
                    f"Cycle {cycle_num} | Data processed!", STATUS_COLORS["success"]
                )
                self._maybe_predict_methane(proc_paths)
                self._maybe_cloud_upload(adc_npz, bme_npz, proc_paths)
            else:
                self._set_status_text(
                    f"Cycle {cycle_num} | Processing error", STATUS_COLORS["idle"]
                )

        self._show_progress(False)
        self._run_on_ui_thread(self._refresh_display_graph_if_visible)
        self._reset_collection_vars()

    def _maybe_predict_methane(self, proc_paths):
        """Predict methane ppm from processed CSVs (Auto Mode cycle end only)."""
        if not ML_PREDICTION_AVAILABLE or predict_cycle is None:
            return
        if not proc_paths:
            return
        adc_csv = proc_paths.get("adc1263")
        bme_csv = proc_paths.get("bme280")
        if adc_csv is None or bme_csv is None:
            print("[WARN] ML predict skipped: missing processed CSV paths")
            return
        try:
            durations = self._get_operation_durations()
            op_times = {
                key: float(durations[key])
                for key in (
                    "baseline",
                    "vacuum",
                    "mix_air",
                    "measure",
                    "vacuum_return",
                    "recovery",
                )
                if key in durations
            }
            ppm = predict_cycle(adc_csv, bme_csv, op_times)
            self._run_on_ui_thread(lambda p=ppm: self.update_methane_ppm(p))
        except Exception as exc:
            print(f"[WARN] ML predict skipped: {exc}")

    def _run_break_time_if_needed(self, break_duration):
        """รัน break time ระหว่าง cycle ถ้าตั้งเวลาไว้"""
        if break_duration <= 0 or not self.running:
            return

        self.current_operation = 'break_time'
        self.current_operation_index = -1

        def update_break_ui(c=self.current_cycle):
            self.progress_label.configure(
                text=f"Cycle {c} Complete - Break Time", fg=STATUS_COLORS["idle"])
            if 'break_time' in self.operation_frames:
                self.operation_frames['break_time'].configure(bg='#e57373')

        self._run_on_ui_thread(update_break_ui)
        self._countdown_break(break_duration)
        self._run_on_ui_thread(lambda: self.operation_frames['break_time'].configure(bg=OPERATION_FRAME_COLORS['break_time']))
        self._run_on_ui_thread(self.reset_operation_colors)
    
    # ==================== MANUAL TIMER HELPERS ====================
    def _on_manual_timer_toggle(self):
        """เปิด/ปิด entry ตาม checkbox 'Use Timer'"""
        if self.manual_timer_enabled.get():
            self.manual_timer_entry.configure(state='normal')
        else:
            self.manual_timer_entry.configure(state='disabled')
            self.manual_timer_remaining_label.configure(text="")

    def _parse_seconds(self, text):
        """แปลงค่า seconds จากข้อความ คืน int หรือ None ถ้า invalid"""
        text = text.strip()
        try:
            total = int(text)
            return total if total > 0 else None
        except ValueError:
            return None

    def _run_manual_timer(self, total_seconds):
        """รัน countdown timer ใน background thread สำหรับ Manual mode
        
        อัพเดท remaining label ทุก 1 วินาที เมื่อหมดเวลาเรียก stop_operation อัตโนมัติ
        ออกเงียบเมื่อ manual_timer_stop_event ถูก set (ผู้ใช้กด Stop ก่อนครบเวลา)
        """
        stop_evt = self.manual_timer_stop_event
        for remaining in range(total_seconds, 0, -1):
            if stop_evt.is_set() or not self.running:
                return
            mins, secs = divmod(remaining, 60)
            display = f"{mins:02d}:{secs:02d}"
            self._run_on_ui_thread(
                lambda t=display: self.manual_timer_remaining_label.configure(
                    text=f"เหลือ {t}"
                )
            )
            stop_evt.wait(timeout=1)

        if not stop_evt.is_set() and self.running:
            self._run_on_ui_thread(
                lambda: self.manual_timer_remaining_label.configure(text="หมดเวลา")
            )
            self.root.after(0, self.stop_operation)

    # ==================== OPERATION CONTROL ====================
    def _start_manual_mode(self):
        """Start manual collection mode (เก็บ ADC + BME280 พร้อมกัน)"""
        if not DATA_COLLECTION_AVAILABLE:
            messagebox.showerror("Error", "Data collection modules not available")
            return

        # ตรวจสอบ timer ก่อนเริ่ม
        timer_seconds = None
        if self.manual_timer_enabled.get():
            timer_seconds = self._parse_seconds(self.manual_timer_duration.get())
            if timer_seconds is None:
                messagebox.showerror(
                    "Timer Error",
                    "รูปแบบเวลาไม่ถูกต้อง\nกรุณาใส่เป็นวินาที (ss) เช่น 300 หรือ 60"
                )
                return

        self.running = True
        self.start_btn.configure(bg=STATUS_COLORS["running"], text="Collecting...", state='disabled')
        self.stop_btn.configure(bg='#c0392b', state='normal')
        self.status_label.configure(text="Status: Collecting data...", fg=STATUS_COLORS["running"])
        self.stop_collection_event = threading.Event()

        def adc_collection_wrapper():
            if DATA_COLLECTION_AVAILABLE:
                try:
                    print("Starting ADC data collection in manual mode...")
                    self.data_collection_file_path = run_collection(self.stop_collection_event)
                    if self.data_collection_file_path:
                        print(f"ADC data collection completed: {self.data_collection_file_path}")
                        self._set_status_text(
                            f"Status: ADC data saved to {self.data_collection_file_path.name}",
                            STATUS_COLORS["success"]
                        )
                except Exception as e:
                    error_msg = f"ADC Collection error: {str(e)}"
                    print(error_msg)
                    traceback.print_exc()
                    self._set_status_text(f"Status: {error_msg}", STATUS_COLORS["idle"])
            else:
                print("ADC data collection not available")

        self.data_collection_thread = threading.Thread(target=adc_collection_wrapper, daemon=True)
        self.data_collection_thread.start()

        if BME_COLLECTION_AVAILABLE:
            def bme_collection_wrapper():
                try:
                    print("Starting BME280 data collection in manual mode...")
                    bme_path = run_bme_collection(self.stop_collection_event)
                    self.bme_collection_file_path = bme_path
                    if bme_path:
                        print(f"BME280 data collection completed: {bme_path}")
                except Exception as e:
                    error_msg = f"BME280 Collection error: {str(e)}"
                    print(error_msg)
                    traceback.print_exc()

            self.bme_collection_thread = threading.Thread(target=bme_collection_wrapper, daemon=True)
            self.bme_collection_thread.start()

        # เริ่ม timer thread ถ้าผู้ใช้เปิดใช้งาน
        if timer_seconds is not None:
            self.manual_timer_stop_event = threading.Event()
            self.manual_timer_thread = threading.Thread(
                target=self._run_manual_timer,
                args=(timer_seconds,),
                daemon=True
            )
            self.manual_timer_thread.start()

    def _start_auto_mode(self):
        """Start auto sequence mode."""
        self.running = True
        self.start_btn.configure(bg=STATUS_COLORS["running"], text="Running...", state='disabled')
        self.stop_btn.configure(bg='#c0392b', state='normal')
        self.progress_label.configure(text="Starting sequence...", fg=STATUS_COLORS["running"])
        thread = threading.Thread(target=self.run_auto_sequence, daemon=True)
        thread.start()

    def start_operation(self):
        """เริ่มการทำงาน"""
        if self.running:
            return
            
        mode = self.current_mode.get()
        
        if mode == "manual":
            self._start_manual_mode()
        elif mode == "auto":
            self._start_auto_mode()
            
    def run_auto_sequence(self):
        """รันลำดับ Auto 7 Operations พร้อม Loop และ Break Time
        
        Operation Plan (heater ON ตลอด Op1-Op7, ADC recording ตลอด Op2-Op7):
        1. Heating:       heater ON (1800s)
        [เริ่มเก็บข้อมูล ADC]
        2. Baseline:      heater + s_valve1 + s_valve3 + pump ON (30s)
        3. Vacuum:        heater + s_valve3 + pump ON (10s) [seamless จาก Op2]
        4. Mix Air:       heater + fan ON (10s)
        5. Measure:       heater + s_valve2 + pump ON (60s)
        6. Vacuum Return: heater + pump + s_valve4 ON (10s)
        7. Recovery:      heater + s_valve1 + s_valve3 + pump ON (60s)
        [หยุดเก็บข้อมูล ADC → ปิดอุปกรณ์ทั้งหมด → process_data]
        Break:            ทั้งหมด OFF (1620s) → วน loop
        """
        
        # Get loop settings
        is_infinite = self.infinite_loop.get()
        try:
            max_cycles = int(self.loop_count.get()) if not is_infinite else 0
        except ValueError:
            max_cycles = 0
        
        self.current_cycle = 0
        
        # Main loop
        while self.running:
            self.current_cycle += 1
            
            # Update cycle counter
            self.root.after(0, lambda c=self.current_cycle: 
                          self.cycle_label.configure(text=f"Current Cycle: {c}"))
            
            # Clean up old threads from previous cycle
            self._cleanup_collection_threads()
            
            # Get durations from UI
            durations = self._get_operation_durations()
            
            for step in AUTO_OPERATION_STEPS:
                if not self._run_auto_step(
                    step["op_key"],
                    step["ui_title"],
                    durations[step["duration_key"]],
                    step["countdown_title"],
                    on=step.get("on"),
                    off=step.get("off"),
                    start_collection=step.get("start_collection", False)
                ):
                    break
            else:
                self._finalize_cycle_devices_and_processing()
                
                # Check if should continue looping
                if not self.running:
                    break
                
                if not is_infinite and self.current_cycle >= max_cycles:
                    break
                
                self._run_break_time_if_needed(durations['break_time'])
                continue

            break
        
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
        """เมื่อ operation เสร็จสิ้น (auto sequence จบ หรือถูกผู้ใช้หยุด)"""
        self.start_btn.configure(bg=STATUS_COLORS["success"], text="Start Auto Sequence", state='normal')
        self.stop_btn.configure(bg=STATUS_COLORS["idle"], state='normal')

        # ถ้าผู้ใช้กด Stop เอง ให้คงข้อความที่ stop worker ตั้งไว้ ไม่ทับด้วย "completed"
        if self._stopping_in_progress:
            self.progress_label.configure(text="Stopped", fg=STATUS_COLORS["idle"])
        else:
            self.progress_label.configure(text="Sequence Complete!", fg=STATUS_COLORS["success"])
            self.timer_label.configure(text="00:00")
            self.status_label.configure(
                text="Status: All operations completed!", fg=STATUS_COLORS["success"]
            )

        self._run_on_ui_thread(lambda: self.root.after(3000, self.reset_operation_colors))
        self.draw_circuit_diagram()
        
    def reset_operation_colors(self):
        """รีเซ็ตสี operation frames กลับเป็นปกติ"""
        for key, color in OPERATION_FRAME_COLORS.items():
            if key in self.operation_frames:
                self.operation_frames[key].configure(bg=color)

    def _wait_for_collection_threads(self, timeout=STOP_THREAD_JOIN_TIMEOUT_SEC):
        """รอให้ ADC + BME280 collection threads จบงาน save (เรียกหลัง set stop_event แล้ว)"""
        if self.data_collection_thread is not None and self.data_collection_thread.is_alive():
            self.data_collection_thread.join(timeout=timeout)
            if self.data_collection_thread.is_alive():
                print("Warning: ADC data collection thread did not stop in time")
        if self.bme_collection_thread is not None and self.bme_collection_thread.is_alive():
            self.bme_collection_thread.join(timeout=timeout)
            if self.bme_collection_thread.is_alive():
                print("Warning: BME280 data collection thread did not stop in time")

    def _stop_and_process_worker(self, mode):
        """Background worker หลังกด Stop:
        1) รอ collection threads save NPZ ให้เสร็จ
        2) ประมวลผลข้อมูล (manual mode เท่านั้น)
        3) คืน UI ผ่าน root.after เพื่อไม่บล็อก main thread
        """
        try:
            self._set_status_text("Status: Saving data...", STATUS_COLORS["processing"])
            self._wait_for_collection_threads(timeout=STOP_THREAD_JOIN_TIMEOUT_SEC)

            if mode == "manual" and DATA_PROCESSING_AVAILABLE:
                self._set_status_text("Status: Processing data...", STATUS_COLORS["processing"])
                adc_npz = self.data_collection_file_path
                bme_npz = self.bme_collection_file_path
                ok, proc_paths = self._run_data_processing()
                if ok:
                    self._set_status_text(
                        "Status: Data processing completed!", STATUS_COLORS["success"]
                    )
                    self._maybe_cloud_upload(adc_npz, bme_npz, proc_paths)
                    self._run_on_ui_thread(self._refresh_display_graph_if_visible)
                else:
                    self._set_status_text(
                        "Status: Processing error (see console)", STATUS_COLORS["idle"]
                    )
            else:
                self._set_status_text("Status: Stopped", STATUS_COLORS["idle"])
        except Exception as e:
            traceback.print_exc()
            self._set_status_text(
                f"Status: Stop error: {e}", STATUS_COLORS["idle"]
            )
        finally:
            self._show_progress(False)
            self._run_on_ui_thread(lambda: self._finish_stop(mode))

    def _finish_stop(self, mode):
        """รันบน UI thread หลัง stop worker จบ — รีเซ็ตสถานะปุ่มและตัวแปร"""
        self._stopping_in_progress = False
        self._stop_worker_thread = None

        # เคลียร์ manual timer refs
        self.manual_timer_thread = None
        self.manual_timer_stop_event = None
        if hasattr(self, 'manual_timer_remaining_label'):
            try:
                self.manual_timer_remaining_label.configure(text="")
            except tk.TclError:
                pass

        # ใน manual mode คงสถานะ Heater ตามที่ผู้ใช้ตั้งไว้
        preserve = []
        if mode == "manual" and self.hardware.get_device_state('heater'):
            preserve = ['heater']

        # รักษาข้อความ status ที่ worker ตั้งล่าสุดไว้ (ส่ง None)
        self._reset_ui_after_stop(mode, status_text=None, preserve_devices=preserve)

    def stop_operation(self):
        """หยุดการทำงาน — ไม่บล็อก main thread; ใช้ worker thread เพื่อรอ save + process"""
        if self._stopping_in_progress:
            return

        mode = self.current_mode.get()
        was_running = self.running
        self.running = False

        # ส่งสัญญาณให้ collection threads หยุดทันที (ไม่ join บน main thread)
        if self.stop_collection_event is not None:
            print("Stopping data collection...")
            self.stop_collection_event.set()

        # หยุด manual timer thread (ถ้ามี) ก่อนที่มันจะเรียก stop_operation ซ้ำ
        if self.manual_timer_stop_event is not None:
            self.manual_timer_stop_event.set()

        if not was_running:
            preserve = []
            if mode == "manual" and self.hardware.get_device_state('heater'):
                preserve = ['heater']
            self._reset_ui_after_stop(
                mode, status_text="Status: Stopped",
                status_color=STATUS_COLORS["idle"],
                preserve_devices=preserve
            )
            return

        # ปิดปุ่มกันกดซ้ำ และแสดงสถานะ "กำลังบันทึก..."
        self._stopping_in_progress = True
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='disabled', bg=STATUS_COLORS["idle"])
        self._set_status_text("Status: Saving data...", STATUS_COLORS["processing"])
        self._show_progress(True)

        # Auto mode: auto-sequence thread จะ finalize เอง — worker นี้แค่รอ save จบ
        # Manual mode: worker รับผิดชอบทั้งรอ save + process + รีเซ็ต UI
        self._stop_worker_thread = threading.Thread(
            target=self._stop_and_process_worker,
            args=(mode,),
            daemon=True,
        )
        self._stop_worker_thread.start()
        
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
