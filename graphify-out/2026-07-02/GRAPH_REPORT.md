# Graph Report - .  (2026-06-27)

## Corpus Check
- Corpus is ~45,698 words - fits in a single context window. You may not need a graph.

## Summary
- 689 nodes · 1100 edges · 65 communities (34 shown, 31 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 85 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Cloud Upload ML|Cloud Upload ML]]
- [[_COMMUNITY_Sensor Data Acquisition|Sensor Data Acquisition]]
- [[_COMMUNITY_GPIO Hardware Control|GPIO Hardware Control]]
- [[_COMMUNITY_GPIO Pinout Diagram|GPIO Pinout Diagram]]
- [[_COMMUNITY_User Guide Docs|User Guide Docs]]
- [[_COMMUNITY_GUI Application|GUI Application]]
- [[_COMMUNITY_Auto Sequence Diagram|Auto Sequence Diagram]]
- [[_COMMUNITY_Screenshot Control UI|Screenshot Control UI]]
- [[_COMMUNITY_Screenshot Settings|Screenshot Settings]]
- [[_COMMUNITY_Screenshot Display|Screenshot Display]]
- [[_COMMUNITY_Screenshot Manual Mode|Screenshot Manual Mode]]
- [[_COMMUNITY_Screenshot Methane Result|Screenshot Methane Result]]
- [[_COMMUNITY_Screenshot Sequence Running|Screenshot Sequence Running]]
- [[_COMMUNITY_Screenshot Start Auto|Screenshot Start Auto]]
- [[_COMMUNITY_Screenshot Save Config|Screenshot Save Config]]
- [[_COMMUNITY_Auto Workflow Guide|Auto Workflow Guide]]
- [[_COMMUNITY_User Guide Concepts|User Guide Concepts]]
- [[_COMMUNITY_Requirements Dependencies|Requirements Dependencies]]
- [[_COMMUNITY_Autostart Setup|Autostart Setup]]
- [[_COMMUNITY_Test Result Data|Test Result Data]]
- [[_COMMUNITY_Cloud Config Module|Cloud Config Module]]
- [[_COMMUNITY_Google Drive Provider|Google Drive Provider]]
- [[_COMMUNITY_GUI Helper Widgets|GUI Helper Widgets]]
- [[_COMMUNITY_Hardware Config JSON|Hardware Config JSON]]
- [[_COMMUNITY_Sequence Controller|Sequence Controller]]
- [[_COMMUNITY_BME280 Reader|BME280 Reader]]
- [[_COMMUNITY_ADS1263 Reader|ADS1263 Reader]]
- [[_COMMUNITY_Data Processing|Data Processing]]
- [[_COMMUNITY_Methane Prediction|Methane Prediction]]
- [[_COMMUNITY_GUI Screenshots Misc|GUI Screenshots Misc]]
- [[_COMMUNITY_User Guide HTML|User Guide HTML]]
- [[_COMMUNITY_Loop Cloud Settings|Loop Cloud Settings]]
- [[_COMMUNITY_Stop Button UI|Stop Button UI]]
- [[_COMMUNITY_Display Graph Tab|Display Graph Tab]]
- [[_COMMUNITY_Operation Times Settings|Operation Times Settings]]
- [[_COMMUNITY_install_autostart.sh script  install_au|install_autostart.sh script / install_au]]
- [[_COMMUNITY_install_xdg_autostart.sh script  instal|install_xdg_autostart.sh script / instal]]
- [[_COMMUNITY_sync_to_pi.sh script  sync_to_pi.sh|sync_to_pi.sh script / sync_to_pi.sh]]
- [[_COMMUNITY_NEW Run ADCBME Duration ~546 sec  NEW|NEW Run ADC/BME Duration ~546 sec / NEW ]]
- [[_COMMUNITY_Step Countdown Timer 0432  Elapsed Tim|Step Countdown Timer 04:32 / Elapsed Tim]]
- [[_COMMUNITY_Heater Relay ON (green)  Heater|Heater Relay ON (green) / Heater]]
- [[_COMMUNITY_GUI Screenshot Shot List  capture_gui_s|GUI Screenshot Shot List / capture_gui_s]]
- [[_COMMUNITY_Processed CSV Data  Raw Sensor Data (.n|Processed CSV Data / Raw Sensor Data (.n]]
- [[_COMMUNITY_Stop|Stop]]
- [[_COMMUNITY_Empty predict_cell Notebook Ce|Empty predict_cell Notebook Ce]]
- [[_COMMUNITY_CRLF to LF Line Ending Fix|CRLF to LF Line Ending Fix]]
- [[_COMMUNITY_labwcWayland Desktop Session|labwc/Wayland Desktop Session]]
- [[_COMMUNITY_XDG Autostart (~.configautos|XDG Autostart (~/.config/autos]]
- [[_COMMUNITY_hardware_config.json|hardware_config.json]]
- [[_COMMUNITY_Manual Mode|Manual Mode]]
- [[_COMMUNITY_numpy=2.1 + pandas=2.2.3 ARM|numpy>=2.1 + pandas>=2.2.3 ARM]]
- [[_COMMUNITY_Auto Mode Parameters Panel|Auto Mode Parameters Panel]]
- [[_COMMUNITY_Status Ready|Status: Ready]]
- [[_COMMUNITY_Control Page with Methane Resu|Control Page with Methane Resu]]
- [[_COMMUNITY_Current Cycle 1 Status|Current Cycle: 1 Status]]
- [[_COMMUNITY_Cloud Provider Dropdown (empty|Cloud Provider Dropdown (empty]]
- [[_COMMUNITY_Use Timer 300 sec|Use Timer 300 sec]]
- [[_COMMUNITY_Break Time|Break Time]]
- [[_COMMUNITY_Fan|Fan]]
- [[_COMMUNITY_Pandoc HTML Export|Pandoc HTML Export]]
- [[_COMMUNITY_Keyboard Shortcuts F11ESC|Keyboard Shortcuts F11/ESC]]
- [[_COMMUNITY_ML ppm Is Not Legal Reference|ML ppm Is Not Legal Reference ]]

## God Nodes (most connected - your core abstractions)
1. `HardwareControlGUI` - 92 edges
2. `ADS1263` - 27 edges
3. `HardwareController` - 25 edges
4. `_window()` - 18 edges
5. `_font()` - 16 edges
6. `save()` - 16 edges
7. `GoogleDriveProvider` - 13 edges
8. `_upload_job()` - 12 edges
9. `_btn()` - 12 edges
10. `load_cloud_config()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `eNose Hardware Control GUI (Pi Desktop)` --semantically_similar_to--> `HardwareControlGUI`  [INFERRED] [semantically similar]
  docs/user-guide/assets/screenshots/01-pi-desktop-gui.png → program/gui.py
- `Save Config Button` --semantically_similar_to--> `save_config()`  [INFERRED] [semantically similar]
  docs/user-guide/eNose-User-Guide.md → program/gui.py
- `Auto Mode User Workflow` --semantically_similar_to--> `Auto Mode (7 Operations)`  [INFERRED] [semantically similar]
  docs/user-guide/eNose-User-Guide.md → README.md
- `eNose Hardware Control Program` --conceptually_related_to--> `HardwareControlGUI`  [INFERRED]
  docs/user-guide/eNose-User-Guide.md → program/gui.py
- `eNose User Guide (PDF)` --semantically_similar_to--> `eNose User Guide (Markdown)`  [INFERRED] [semantically similar]
  docs/user-guide/eNose-User-Guide.pdf → docs/user-guide/eNose-User-Guide.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **ADC + BME280 to NPZ to CSV Processing Pipeline** — readme_ads1263, readme_bme280, readme_process_all_data, result2_adc_ss_lp_ma_time_bins, result2_bme_temperature_lp_ma_bins [INFERRED 0.85]
- **Tiered Raspberry Pi Dependency Install** — requirements_pi_core_hardware_packages, requirements_pi_viz_data_viz_packages, requirements_pi_full_venv_stack, requirements_cloud_google_drive_packages, program_autostart_setup_venv_requirements_pi [EXTRACTED 1.00]
- **User Guide Build Artifacts MD HTML PDF Screenshots** — user_guide_enose_user_guide, user_guide_enose_user_guide_html, user_guide_enose_user_guide_pdf, screenshots_shotlist_gui_screenshot_spec, user_guide_readme_capture_gui_screenshots, user_guide_readme_export_pdf_script [EXTRACTED 1.00]
- **GPIO-to-Relay Hardware Mapping** — assets_raspberry_pi_gpio_pinout_gpio_13, assets_raspberry_pi_gpio_pinout_gpio_19, assets_raspberry_pi_gpio_pinout_gpio_26, assets_raspberry_pi_gpio_pinout_gpio_12, assets_raspberry_pi_gpio_pinout_gpio_16, assets_raspberry_pi_gpio_pinout_gpio_20, assets_raspberry_pi_gpio_pinout_gpio_21, assets_raspberry_pi_gpio_pinout_heater, assets_raspberry_pi_gpio_pinout_fan, assets_raspberry_pi_gpio_pinout_pump, assets_raspberry_pi_gpio_pinout_valve_1, assets_raspberry_pi_gpio_pinout_valve_2, assets_raspberry_pi_gpio_pinout_valve_3, assets_raspberry_pi_gpio_pinout_valve_4 [EXTRACTED 1.00]
- **Auto Mode Seven-Operation Cycle** — diagrams_auto_sequence_flow_op1_heat, diagrams_auto_sequence_flow_op2_baseline, diagrams_auto_sequence_flow_op3_vacuum, diagrams_auto_sequence_flow_op4_mix, diagrams_auto_sequence_flow_op5_measure, diagrams_auto_sequence_flow_op6_vac_ret, diagrams_auto_sequence_flow_op7_recovery [EXTRACTED 1.00]
- **BME280 I2C Wiring** — assets_raspberry_pi_gpio_pinout_bme280, assets_raspberry_pi_gpio_pinout_pin_3v3, assets_raspberry_pi_gpio_pinout_pin_sda, assets_raspberry_pi_gpio_pinout_pin_scl, assets_raspberry_pi_gpio_pinout_pin_gnd [EXTRACTED 1.00]
- **Control Page UI Layout** — screenshots_01_pi_desktop_gui_control_mode_section, screenshots_01_pi_desktop_gui_operation_sequence_section, screenshots_01_pi_desktop_gui_methane_display_section, screenshots_01_pi_desktop_gui_hardware_controls_section, screenshots_01_pi_desktop_gui_control_tab [EXTRACTED 1.00]
- **Auto Mode Seven Operations** — user_guide_enose_user_guide_op1_heating, user_guide_enose_user_guide_op2_baseline, user_guide_enose_user_guide_op3_vacuum, user_guide_enose_user_guide_op4_mix_air, user_guide_enose_user_guide_op5_measure, user_guide_enose_user_guide_op6_vac_return, user_guide_enose_user_guide_op7_recovery [EXTRACTED 1.00]
- **Main GUI Navigation Pages** — user_guide_enose_user_guide_control_page, user_guide_enose_user_guide_display_page, user_guide_enose_user_guide_settings_page [EXTRACTED 1.00]
- **Auto Mode Seven-Step Sequence** — user_guide_enose_user_guide_op1_heating, user_guide_enose_user_guide_op2_baseline, user_guide_enose_user_guide_op3_vacuum, user_guide_enose_user_guide_op4_mix_air, user_guide_enose_user_guide_op5_measure, user_guide_enose_user_guide_op6_vac_return, user_guide_enose_user_guide_op7_recovery [EXTRACTED 1.00]
- **Control Tab Layout Sections** — screenshots_02_control_overview_auto_selected, screenshots_02_control_overview_sequence_ready, screenshots_02_control_overview_methane_placeholder, screenshots_02_control_overview_nav_tabs [INFERRED 0.85]
- **Settings Page Configuration Groups** — screenshots_04_settings_full_operation_durations, screenshots_04_settings_full_cloud_section, screenshots_04_settings_full_loop_section, user_guide_enose_user_guide_save_config [INFERRED 0.85]

## Communities (65 total, 31 thin omitted)

### Community 0 - "Cloud Upload ML"
Cohesion: 0.05
Nodes (70): Any, _deep_merge(), load_cloud_config(), Load and save cloud upload configuration., Load cloud_config.json merged with defaults; apply env overrides., Merge updates into existing file (or defaults) and write known keys only., save_cloud_config(), Cloud upload integration for eNose. (+62 more)

### Community 1 - "Sensor Data Acquisition"
Cohesion: 0.05
Nodes (41): centered_moving_average(), get_latest_npz_file(), load_npz_arrays(), lowpass_filter(), process_all_data(), process_data(), กำหนด path ของ CSV ที่จะบันทึก (ดึง date_time จากชื่อไฟล์ input), ประมวลผล NPZ → CSV (low-pass + moving average ที่ vectorized)      Parameters (+33 more)

### Community 2 - "GPIO Hardware Control"
Cohesion: 0.06
Nodes (25): create_controller(), HardwareController, load_gpio_config(), eNose Hardware Controller ========================== Module สำหรับควบคุม Hardw, ซิงก์สถานะ relay จริงให้ตรงกับ device_states ใน memory (หลัง setup/re-init), Re-init GPIO หลังถูก cleanup โดยโมดูลอื่น แล้วคืนสถานะ relay ตาม memory, ตรวจสอบว่า GPIO ถูก setup แล้ว         ถ้าโมดูลอื่น (เช่น ADC) เรียก GPIO.clean, ควบคุมอุปกรณ์โดยตรง                  Args:             device_key (str): ชื่อ (+17 more)

### Community 3 - "GPIO Pinout Diagram"
Cohesion: 0.07
Nodes (34): Raspberry Pi GPIO Output Pinout Diagram, BME280 Environmental Sensor, Fan Relay, GPIO 12 (Physical Pin 32), GPIO 13 (Physical Pin 33), GPIO 16 (Physical Pin 36), GPIO 19 (Physical Pin 35), GPIO 20 (Physical Pin 38) (+26 more)

### Community 4 - "User Guide Docs"
Cohesion: 0.07
Nodes (32): บันทึก config ปัจจุบัน, save_config(), Display Tab, Settings Tab, Control Page Overview Screenshot, Bottom Nav: Control Display Settings, Cloud Upload Section, Input from UI Selected (+24 more)

### Community 5 - "GUI Application"
Cohesion: 0.11
Nodes (10): HardwareControlGUI, สร้างส่วน Auto Mode Parameters, Resize figure to match canvas so graph scales with display., Schedule graph refresh on main thread when Display page is visible (after new da, เปิด/ปิด entry ตาม checkbox 'Use Timer, สร้าง popup numpad (Toplevel) — เรียกครั้งเดียว แล้ว show/hide ทีหลัง, แสดง popup numpad ใกล้ ๆ entry, ผูก Entry: คลิก/โฟกัส → popup numpad (+2 more)

### Community 6 - "Auto Sequence Diagram"
Cohesion: 0.08
Nodes (15): Run callback on Tk UI thread., Thread-safe update of device UI, Set multiple devices and update UI (thread-safe), Update progress label and highlight operation frame, Mark an operation frame as complete (green), Mark operation as bypassed (duration=0 in Settings), เริ่มเก็บข้อมูลที่ Baseline หรือขั้นแรกหลัง bypass Baseline, Run countdown timer, returns False if stopped (+7 more)

### Community 8 - "Screenshot Settings"
Cohesion: 0.30
Nodes (23): Image, ImageDraw, _badge(), _btn(), _device_box(), _font(), _rounded_rect(), save() (+15 more)

### Community 9 - "Screenshot Display"
Cohesion: 0.12
Nodes (11): ABC, BaseProvider, Abstract cloud storage provider for uploads., Return folder id for `name` under `parent_id`, creating if missing., Upload file; return remote file id or None if skipped (duplicate)., Minimal interface: ensure folder hierarchy and upload a local file., GoogleDriveProvider, Google Drive upload using a service account. (+3 more)

### Community 10 - "Screenshot Manual Mode"
Cohesion: 0.11
Nodes (22): enose-gui.desktop Entry, eNose GUI Autostart Setup Guide, run_gui.sh Launcher, Pi venv + requirements-pi.txt, Active HIGH Relay Logic, ADS1263 SPI ADC, Auto Mode (7 Operations), BME280 I2C Environmental Sensor (+14 more)

### Community 11 - "Screenshot Methane Result"
Cohesion: 0.12
Nodes (10): Update status label in thread-safe way., Show/hide and start/stop the indeterminate progress bar (thread-safe)., Stop data collection threads (ADC + BME280) and wait for save to finish., Process latest collected data using stored input paths.          เรียกได้เฉพาะใน, Update cloud status label (must run on UI thread)., Schedule Drive upload if module enabled and config enabled., หยุด collection, ปิดอุปกรณ์ยกเว้น Heater (เหมือนหลัง Stop ใน Manual), และประมวลผ, รอให้ ADC + BME280 collection threads จบงาน save (เรียกหลัง set stop_event แล้ว) (+2 more)

### Community 13 - "Screenshot Start Auto"
Cohesion: 0.14
Nodes (18): Control Mode Section, Control Tab (Active), eNose Hardware Control GUI (Pi Desktop), Fan Button, Hardware Controls Section, Heater Button, Manual Button, Pump Button (+10 more)

### Community 14 - "Screenshot Save Config"
Cohesion: 0.15
Nodes (7): Placeholder - Hardware diagram removed, ตั้งค่าสถานะอุปกรณ์โดยตรง, Helper function สำหรับตั้งค่าหลายอุปกรณ์และอัพเดท UI, เมื่อ operation เสร็จสิ้น (auto sequence จบ หรือถูกผู้ใช้หยุด), Hardware Controls: two columns — left Value 1–4, right Pump/Fan/Heater (rounded, Draw rounded-rectangle box: light grey or green, black outline., Update device box to match ON/OFF state.

### Community 15 - "Auto Workflow Guide"
Cohesion: 0.19
Nodes (15): Op2 Baseline [Recording], Pump Relay ON (green), Value 1 Relay ON (green), Op1 Heating, Op2 Baseline, Op3 Vacuum, Op4 Mix Air, Op5 Measure (+7 more)

### Community 16 - "User Guide Concepts"
Cohesion: 0.16
Nodes (14): Auto Button (Selected), Operation Sequence Section, Ready to start State, Sequence Labels: Flush-VL-Hot-Mix-Meas-VR-Rec, Start Auto Sequence Button, Status: Ready, Stop Button, Auto Mode Selected (purple) (+6 more)

### Community 17 - "Requirements Dependencies"
Cohesion: 0.15
Nodes (6): Clean up any running collection threads from previous cycle (ADC + BME280), Reset collection variables, ปิดอุปกรณ์ทั้งหมดและซิงก์ UI ให้เป็นสถานะ OFF                  Args:, รีเซ็ต UI หลังหยุดการทำงาน (ใช้ร่วมกันทั้ง manual/auto), รีเซ็ตสี operation frames กลับเป็นปกติ, รันบน UI thread หลัง stop worker จบ — รีเซ็ตสถานะปุ่มและตัวแปร

### Community 18 - "Autostart Setup"
Cohesion: 0.22
Nodes (3): MockProvider, Tests for cloud uploader with a mock provider., TestUploaderJob

### Community 19 - "Test Result Data"
Cohesion: 0.27
Nodes (10): convert_all_npz_files(), convert_npz_to_csv(), main(), เปิด dialog สำหรับเลือกไฟล์ npz          Returns:         Path หรือ None: pat, เปิด dialog สำหรับเลือกโฟลเดอร์ output          Args:         initial_dir (st, ฟังก์ชันหลักสำหรับรันสคริปต์, แปลงไฟล์ npz เป็น CSV          Args:         npz_path (Path): path ของไฟล์ np, แปลงไฟล์ npz ทั้งหมดในโฟลเดอร์ data เป็น CSV          Args:         data_dir (+2 more)

### Community 20 - "Cloud Config Module"
Cohesion: 0.22
Nodes (11): Operation Duration Fields (7 ops + Break), Operation Time Input Fields Crop, Start Auto Sequence Button, Status: Running, Start Collection Button, Stop Button During Running, Operation Sequence (Op1-Op7), Start Auto Sequence (+3 more)

### Community 21 - "Google Drive Provider"
Cohesion: 0.20
Nodes (5): แถบแสดง Methane (ppm) ด้านล่างกราฟ — หน้า Display, Create display page with Process Data graph in the center., Load latest Process Data file and plot (thread-safe when called via root.after)., Fill the legend frame below the graph with color patch + label for each line., Draw placeholder when no data or error.

### Community 22 - "GUI Helper Widgets"
Cohesion: 0.36
Nodes (8): _ensure_demo_csv(), _find_labelframe(), _grab_bbox(), _grab_widget(), _grab_window(), main(), Tk, Widget

### Community 23 - "Hardware Config JSON"
Cohesion: 0.22
Nodes (5): load_config(), อัปเดตตัวเลข methane (ppm) ทั้งหน้า Control และหน้า Display (ถ้ามี), Toggle loop count entry based on infinite loop checkbox, อัพเดทตาม parameter source และแสดง box ปุ่มที่เลือกเป็น sunken, Extract features จาก proc_paths แล้วทำนาย ppm และแสดงผลบน UI.

### Community 24 - "Sequence Controller"
Cohesion: 0.33
Nodes (9): Methane Display Section, Methane Placeholder (----), ppm Unit Label, Methane Display ---- ppm, Methane Reading 12.45 ppm, Methane 12.45 ppm Panel, 09-methane-result.png Screenshot, Methane ppm Display (+1 more)

### Community 26 - "ADS1263 Reader"
Cohesion: 0.36
Nodes (7): run_gui.sh script, DISPLAY, log(), run_gui(), XAUTHORITY, run_gui.sh Launcher, Desktop/VNC Display Requirement

### Community 27 - "Data Processing"
Cohesion: 0.29
Nodes (3): Maximize window (cross-platform), Restore window from maximized (cross-platform), Toggle maximized window

### Community 28 - "Methane Prediction"
Cohesion: 0.29
Nodes (3): แปลงค่า seconds จากข้อความ คืน int หรือ None ถ้า invalid, Start manual collection mode (เก็บ ADC + BME280 พร้อมกัน), Start auto sequence mode.

### Community 29 - "GUI Screenshots Misc"
Cohesion: 0.29
Nodes (7): 08-sequence-running.png Screenshot, eNose User Guide (Markdown), eNose User Guide (HTML Export), eNose User Guide (PDF), Raspberry Pi GUI Deployment, export_pdf.py, User Guide Documentation Folder

### Community 30 - "User Guide HTML"
Cohesion: 0.60
Nodes (5): export_html(), export_pdf_chromium(), find_chromium(), find_pandoc(), main()

### Community 31 - "Loop Cloud Settings"
Cohesion: 0.33
Nodes (3): สร้างแถว Operation Sequence (ซ้าย) + Methane ppm (ขวา) สูงเท่ากัน, ช่องแสดง Methane (ppm) — สูงเท่ากับ Operation Sequence ในแถวเดียวกัน, สร้างปุ่ม Start/Stop — กว้าง/สูงเท่ากัน (grid + uniform columns)

### Community 32 - "Stop Button UI"
Cohesion: 0.50
Nodes (5): Loop Settings Section, Cycles Input Value 3, Infinite Loop Checkbox, Infinite Loop, Loop Settings

### Community 34 - "Operation Times Settings"
Cohesion: 0.67
Nodes (3): Google Drive Cloud Upload (optional), google-api-python-client, requirements-cloud.txt (Google API)

## Ambiguous Edges - Review These
- `Sequence Labels: Flush-VL-Hot-Mix-Meas-VR-Rec` → `Sequence Display: Heat-BL-Vac-Mix-Meas-VR-Rec`  [AMBIGUOUS]
  docs/user-guide/assets/screenshots/01-pi-desktop-gui.png · relation: semantically_similar_to
- `Value 2 Solenoid Valve` → `Operation Duration Fields (7 ops + Break)`  [AMBIGUOUS]
  docs/user-guide/assets/screenshots/04-settings-full.png · relation: conceptually_related_to

## Knowledge Gaps
- **89 isolated node(s):** `install_autostart.sh script`, `install_xdg_autostart.sh script`, `DISPLAY`, `XAUTHORITY`, `sync_to_pi.sh script` (+84 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **31 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Sequence Labels: Flush-VL-Hot-Mix-Meas-VR-Rec` and `Sequence Display: Heat-BL-Vac-Mix-Meas-VR-Rec`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Value 2 Solenoid Valve` and `Operation Duration Fields (7 ops + Break)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `HardwareControlGUI` connect `GUI Application` to `Cloud Upload ML`, `Sensor Data Acquisition`, `GPIO Hardware Control`, `Display Graph Tab`, `User Guide Docs`, `Auto Sequence Diagram`, `Screenshot Methane Result`, `Screenshot Start Auto`, `Screenshot Save Config`, `Requirements Dependencies`, `Google Drive Provider`, `GUI Helper Widgets`, `Hardware Config JSON`, `Data Processing`, `Methane Prediction`, `Loop Cloud Settings`?**
  _High betweenness centrality (0.351) - this node is a cross-community bridge._
- **Why does `HardwareController` connect `GPIO Hardware Control` to `Sensor Data Acquisition`, `Data Processing`, `GUI Application`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `Auto Mode User Workflow` connect `User Guide Concepts` to `User Guide Docs`, `Screenshot Manual Mode`, `Auto Workflow Guide`, `Cloud Config Module`, `GUI Screenshots Misc`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `HardwareControlGUI` (e.g. with `HardwareController` and `eNose Hardware Control GUI (Pi Desktop)`) actually correct?**
  _`HardwareControlGUI` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `หาไฟล์ NPZ ล่าสุดในโฟลเดอร์ (กรองตาม prefix ได้)`, `Load NPZ → (data ndarray, columns list, sample_rate float)`, `First-order IIR low-pass filter — vectorized via scipy when available.      สู` to the rest of the system?**
  _248 weakly-connected nodes found - possible documentation gaps or missing edges._