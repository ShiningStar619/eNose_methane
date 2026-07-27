# คลังงานวิจัย (คัดกรองแล้ว)

**ผลการคัดกรอง:** [`project-relevance-screening.md`](project-relevance-screening.md)  
**ซิงก์ citation:** [`citation-sync-report.md`](citation-sync-report.md) · [`citation-sync-report-2026-07-23.md`](citation-sync-report-2026-07-23.md)  
**Reorg + EndNote master:** [`citation-reorg-report-2026-07-23.md`](citation-reorg-report-2026-07-23.md) · [`screened/references.bib`](screened/references.bib) · [`screened/references.ris`](screened/references.ris)  
**Literature review:** [`literature-review-4.2.md`](literature-review-4.2.md) · [`literature-review-enose-ml-methane-rice.md`](literature-review-enose-ml-methane-rice.md)

## โครงสร้างปัจจุบัน

Paper ที่ผ่านการคัดกรองอยู่ภายใต้ [`screened/`](screened/) เป็น **single source of truth** (ดู taxonomy ใน [`screened/README.md`](screened/README.md)):

| หมวด | โฟลเดอร์ | ความหมาย (หลัง reorg 23 ก.ค. 2026) | bib/ris |
|------|---------|--------------------------------------|--------:|
| คัดเข้าโดยตรง | [`screened/direct/`](screened/direct/) | eNose/MOS+CH₄, ML calibration, chamber–GC นา/เกษตร, field low-cost | 22 |
| หลักฐานสนับสนุน | [`screened/supporting/`](screened/supporting/) | agronomy/AWD, model, review, remote sensing, companion | 31 |
| คัดออก | [`screened/excluded/`](screened/excluded/) | นอกประเด็น / stub ชน DOI / classification | 2 |

แต่ละหมวดมี `cite/` สำหรับ BibTeX + RIS คู่กัน · import EndNote ครั้งเดียวใช้ `screened/references.ris`

โฟลเดอร์หมวดเก่า (`methane/`, `enose/`, `algorithm/`, `methods-*`, `archive/`) ถูกลบแล้ว เพราะไม่มี paper เหลือ หรือย้ายเข้า `screened/` แล้ว

## ไฟล์สำคัญที่มี full text / extract

| บทบาท | ไฟล์ |
|-------|------|
| ML + in-situ CH₄ นาข้าว (extract) | `screened/direct/2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze_extract.txt` |
| eNose / MOS / chamber–GC (PDF) | `screened/direct/*.pdf` |
| agronomy / review / companion (PDF) | `screened/supporting/*.pdf` |

งาน eNose / ML / chamber หลายเรื่องยังมีเฉพาะ BibTeX+RIS ใน `screened/*/cite/` — ต้องดาวน์โหลด PDF เพิ่มถ้าจะอ่าน full text
