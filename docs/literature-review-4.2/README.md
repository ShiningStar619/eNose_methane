# คลังอ้างอิงบทที่ 4.2 (Literature reviews)

โฟลเดอร์นี้เก็บงานที่คัดแล้วสำหรับเขียน **บทที่ 4.2 ใหม่** โดยยึดบันไดวัดในบทที่ 4.1 ของ *Proposal draft 12*  
ไม่ใช่คลังแม่ของทั้งวิทยานิพนธ์ — คลังแม่ยังอยู่ที่ [`docs/paper/screened/`](../paper/screened/)  
ร่างข้อเสนอ **ไม่ได้ถูกแก้** ในรอบนี้

## โครงที่จะรองรับ

- 4.2.1 นาข้าวน้ำขังและการปล่อย CH₄
- 4.2.2 static chamber–GC เป็นวิธีอ้างอิง
- 4.2.3 วิธีอื่นเพื่อตัดทาง (spectroscopy, remote sensing)
- 4.2.4 eNose / MOS + ML สำหรับประเมินความเข้มข้น CH₄
- 4.2.5 ช่องว่างการวิจัยและการจัดตำแหน่ง

## ไฟล์

| ไฟล์ | หน้าที่ |
|------|--------|
| [`selection.md`](selection.md) | ตารางเพิ่ม / คง / ลบ จากรายการอ้างอิง draft 12 |
| [`survey.md`](survey.md) | สำรวจวรรณกรรมตามคำถามจาก 4.1 |
| `pdf/` | PDF ที่โหลดได้ถูกกฎหมาย (32 ไฟล์) |
| `cite/*.ris` | RIS รายเรื่อง (40 ไฟล์) |
| [`references.ris`](references.ris) | RIS รวมสำหรับ EndNote |
| [`2026_Othman_extract.md`](2026_Othman_extract.md) | extract โครงสร้าง Othman 2026 |
| [`othman-2026-positioning.md`](othman-2026-positioning.md) | ร่างประโยคจัดตำแหน่งช่องว่างเทียบ Othman |

## ข้อจำกัดการค้นรอบนี้

เครื่องมือ `firecrawl_research_*` **ยังไม่พร้อม** บน MCP `user-firecrawl` (ต้องการ OAuth)  
`firecrawl_search` แบบไม่มีคีย์ถูกปฏิเสธ  
ใช้สำรอง: Crossref, หน้า OA (MDPI CDN, Copernicus, Frontiers, Europe PMC, IPCC, สำนักพิมพ์สถาบัน), และไฟล์ใน `docs/paper/screened/`

งานเพย์วอลล์มี RIS แล้ว แต่ยังไม่มี PDF — ดูตารางท้าย [`selection.md`](selection.md)

รอบ 2 เติม 13 เรื่อง OA จากผลค้นห้ามุม (กลไกนา, chamber นา, TROPOMI/XCH₄, ความชื้น MOS) โดยไม่ใส่งานเพย์วอลล์ที่แนะนำเพิ่ม
