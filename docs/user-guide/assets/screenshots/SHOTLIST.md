# แคปจาก GUI จริง

```bash
py docs/user-guide/scripts/capture_gui_screenshots.py
```

ไฟล์ PNG → `assets/screenshots/` (ใช้ใน `eNose-User-Guide.md`)

## รายการภาพ

| ไฟล์ | เนื้อหาที่ต้องจับ | Annotate |
|------|------------------|----------|
| `01-pi-desktop-gui.png` | Desktop Pi + หน้าต่าง GUI เต็ม | — |
| `02-control-overview.png` | หน้า Control | วงเลข ①–⑤ |
| `03-select-auto.png` | ปุ่ม Auto ถูกเลือก | ลูกศรชี้ Auto |
| `04-settings-full.png` | หน้า Settings ทั้งหมด | — |
| `05-operation-times.png` | crop ช่องเวลา 7 ขั้น + Break | — |
| `06-save-config.png` | ปุ่ม Save Config | วงกลม |
| `07-start-auto.png` | ปุ่ม Start Auto Sequence | ลูกศร |
| `08-sequence-running.png` | กำลังรัน + countdown | — |
| `09-methane-result.png` | ค่า ppm จริง | — |
| `10-display-graph.png` | กราฟ + Refresh Graph | — |
| `11-loop-settings.png` | crop Break + Cloud + Loop | — |
| `12-manual-mode.png` | Manual + Hardware Controls | — |
| `13-stop-button.png` | ปุ่ม Stop | — |

## เครื่องมือ annotate (แนะนำ)

- **ShareX** (Windows, ฟรี)
- **Greenshot** (ฟรี)
- **Snagit** (จ่าย)

สไตล์: ลูกศร/หมายเลข ①②③ สีแดงหรือส้ม, caption ใต้รูปในคู่มือเป็นภาษาไทย

## สร้าง placeholder ใหม่

```bash
pip install Pillow
python docs/user-guide/scripts/generate_placeholders.py
```
