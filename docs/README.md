# เอกสารโปรเจกต์ eNose Methane Detection

โฟลเดอร์นี้รวบรวมเอกสารทั้งหมดของโปรเจกต์ ประกอบด้วย manuscript สำหรับการตีพิมพ์ คู่มือผู้ใช้ และคลังงานวิจัยที่เกี่ยวข้อง

---

## 📁 โครงสร้างโฟลเดอร์

```
docs/
├── MANUSCRIPT.md                          # 📄 Manuscript หลักสำหรับการตีพิมพ์
├── REFERENCES.md                          # 📚 บรรณานุกรมเต็มรูปแบบ
├── MANUSCRIPT_GUIDE.md                    # 📖 คู่มือการใช้งานและแนวทางการเขียน
├── README.md                              # ไฟล์นี้
│
├── paper/                                 # คลังงานวิจัย (60+ papers, 2020–2026)
│   ├── README.md
│   ├── literature-review-4.2.md          # สรุปวรรณกรรม 6 หัวข้อ
│   ├── literature-review-enose-ml-methane-rice.md
│   ├── methane/                          # 12 PDF + 7 stub
│   ├── methods-chamber-gc/               # 4 PDF
│   ├── methods-spectroscopy/             # 2 PDF
│   ├── methods-field/                    # 1 PDF
│   ├── methods-remote/                   # 1 PDF
│   ├── enose/                            # 13 PDF
│   ├── algorithm/                        # 13 PDF
│   └── archive/                          # งาน eNose ด้านอื่น (ไม่เกี่ยวข้องโดยตรง)
│
├── user-guide/                           # คู่มือผู้ใช้งานระบบ
│   ├── eNose-User-Guide.md
│   ├── eNose-User-Guide.pdf
│   ├── eNose-User-Guide.html
│   ├── assets/                           # ภาพประกอบ
│   └── scripts/                          # สคริปต์สร้าง PDF/HTML
│
├── figures/                              # รูปภาพสำหรับ manuscript (จะสร้างภายหลัง)
│   ├── fig1_sensor_response.png
│   ├── fig2_correlation_heatmap.png
│   ├── fig3_predicted_vs_true.png
│   ├── fig4_feature_importance.png
│   ├── fig5_residual_analysis.png
│   └── fig6_system_performance.png
│
└── supplementary/                        # เอกสารเสริม (Supplementary Materials)
    ├── S1_Hardware_Schematics.pdf
    ├── S2_Operation_Sequences.xlsx
    ├── S3_Feature_Extraction_Details.md
    ├── S4_Model_Training_Notebook.html
    ├── S5_Field_Deployment_Checklist.pdf
    └── S6_Calibration_Protocol.pdf
```

---

## 📄 เอกสารหลัก

### 1. MANUSCRIPT.md

**Manuscript สำหรับการตีพิมพ์วารสารวิชาการ**

- **หัวเรื่อง:** Electronic Nose System for Methane Detection in Rice Paddies: Integration of Low-cost MOS Sensors and Machine Learning
- **โครงสร้าง:** Abstract, Introduction, Materials & Methods, Results, Discussion, Conclusions
- **ความยาว:** ~7,000 words (เหมาะกับ Environmental Science & Technology, Sensors, หรือ Agriculture Ecosystems & Environment)
- **สถานะ:** Draft v1.0 — ต้องกรอกผลการทดลองจริง (ดูที่ `[TBD]` และ `[X.XX]`)

**การใช้งาน:**

```bash
# อ่าน manuscript
cat docs/MANUSCRIPT.md

# แปลงเป็น PDF (ใช้ pandoc)
pandoc docs/MANUSCRIPT.md -o docs/manuscript.pdf \
  --pdf-engine=xelatex \
  --bibliography=docs/references.bib
```

### 2. REFERENCES.md

**บรรณานุกรมครบถ้วน 50+ citations**

- จัดเป็นหมวดหมู่: Methane/Rice, Methods, eNose, ML, Field Applications
- มี DOI และลิงก์ถึงไฟล์ PDF ใน `paper/`
- รองรับ citation styles: APA, IEEE, numbered

**การใช้งาน:**

```bash
# ดูรายการ references
cat docs/REFERENCES.md

# สร้าง BibTeX file (จาก DOI)
# (สามารถใช้เครื่องมือ doi2bib.org หรือ Zotero)
```

### 3. MANUSCRIPT_GUIDE.md

**คู่มือการเขียนและการปรับแต่ง manuscript**

- แนวทางการกรอกข้อมูลผลการทดลอง
- วิธีสร้างรูปภาพและกราฟ (Python code examples)
- การปรับ manuscript ให้เหมาะกับ journal ต่างๆ
- Workflow สำหรับการตีพิมพ์

**สำหรับผู้เขียน/ผู้แก้ไข manuscript:**

```bash
# อ่านคู่มือก่อนเริ่มเขียน
cat docs/MANUSCRIPT_GUIDE.md
```

---

## 📚 คลังงานวิจัย (paper/)

คลังงานวิจัย 60+ papers (2020–2026) จัดเป็น 7 หมวด:

| หมวด | จำนวน | เนื้อหา |
|------|------|---------|
| `methane/` | 12 PDF + 7 stub | การปล่อย CH₄ จากนาข้าว ปัจจัยควบคุม มาตรการลด |
| `methods-chamber-gc/` | 4 PDF | วิธีอ้างอิง static chamber + GC / flux methodology |
| `methods-spectroscopy/` | 2 PDF | TDLAS, FTIR, TGA และรีวิวเทคโนโลยีตรวจจับ CH₄ |
| `methods-field/` | 1 PDF | ระบบต้นทุนต่ำ / auto chamber ในแปลง |
| `methods-remote/` | 1 PDF | ดาวเทียม / UAV + ML ประเมิน CH₄ |
| `enose/` | 13 PDF | ฮาร์ดแวร์ eNose, MOS/TGS, การตรวจ CH₄ |
| `algorithm/` | 13 PDF | ML regression, calibration, รีวิว eNose+ML |

**งานวิจัยสำคัญที่ต้องอ่าน:**

1. **Domènech-Gil et al. (2024)** — eNose + ML ให้ R² = 0.91 สำหรับ atmospheric CH₄  
   → `enose/2024_Domenech-Gil_eNose_environmental_methane_monitoring.pdf`

2. **Zhang et al. (2025)** — ML-driven in-situ CH₄ measurement ในนาข้าว  
   → `methane/2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze.pdf`

3. **Rajasekar & Selvi (2022)** — TGS2611/MQ4 ในนาข้าว (closest to our work)  
   → `methods-field/2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf`

4. **Baruah & Mazumder (2025)** — รีวิว ML + eNose ครบถ้วน  
   → `algorithm/2025_Baruah_ML_eNose_healthcare_agriculture_review.pdf`

**วิธีดาวน์โหลดเพิ่มเติม (Open Access papers):**

```bash
cd docs/paper
python download_papers.py  # ดึง PDF จาก Europe PMC / arXiv / Unpaywall
```

---

## 📖 คู่มือผู้ใช้ (user-guide/)

**สำหรับผู้ปฏิบัติงานที่ใช้ระบบจริง** (ไม่ใช่นักพัฒนา)

- **Markdown:** `eNose-User-Guide.md`
- **PDF:** `eNose-User-Guide.pdf` (พร้อมภาพประกอบ)
- **HTML:** `eNose-User-Guide.html` (เปิดได้ใน browser)

**เนื้อหา:**

- การเปิด/ปิดระบบ
- การใช้งาน GUI (Control / Display / Settings)
- การเก็บข้อมูล (Manual & Auto Mode)
- การแก้ปัญหาเบื้องต้น
- คำเตือนด้านความปลอดภัย

**สร้าง PDF ใหม่:**

```bash
cd docs/user-guide
python scripts/export_pdf.py  # แปลง .md → .pdf
```

---

## 📊 รูปภาพและกราฟ (figures/)

โฟลเดอร์สำหรับเก็บรูปภาพที่ใช้ใน manuscript (จะสร้างหลังจากมีผลการทดลอง)

**รายการรูปที่ต้องสร้าง:**

| Figure | คำอธิบาย | ขนาด |
|--------|----------|------|
| `fig1_sensor_response.png` | Time-series ss1–ss4 ที่ 1 ppm vs 10 ppm | 10×8 inch, 300 dpi |
| `fig2_correlation_heatmap.png` | Correlation matrix ของ top 15 features | 10×8 inch, 300 dpi |
| `fig3_predicted_vs_true.png` | Scatter plot: predicted vs true ppm | 8×8 inch, 300 dpi |
| `fig4_feature_importance.png` | Bar plot: Linear Regression coefficients | 10×6 inch, 300 dpi |
| `fig5_residual_analysis.png` | Residual plots (3 subplots) | 12×8 inch, 300 dpi |
| `fig6_system_performance.png` | GUI screenshot + prediction example | 10×6 inch, 300 dpi |

**สร้างรูปอัตโนมัติ:**

```bash
# (สคริปต์ยังไม่มี — ควรสร้างตาม MANUSCRIPT_GUIDE.md)
python scripts/generate_manuscript_figures.py
```

---

## 📎 Supplementary Materials (supplementary/)

เอกสารเสริมที่ส่งพร้อม manuscript:

| ไฟล์ | เนื้อหา | สถานะ |
|------|---------|-------|
| S1_Hardware_Schematics.pdf | วงจรไฟฟ้า, PCB layout | ❌ ยังไม่สร้าง |
| S2_Operation_Sequences.xlsx | ตาราง relay states ทุก operation | ❌ ยังไม่สร้าง |
| S3_Feature_Extraction_Details.md | ขั้นตอนคำนวณ features พร้อม code | ❌ ยังไม่สร้าง |
| S4_Model_Training_Notebook.html | Jupyter notebook exported | ✅ มีอยู่แล้วใน `BuildML_PC/` |
| S5_Field_Deployment_Checklist.pdf | คู่มือติดตั้งภาคสนาม | ❌ ยังไม่สร้าง |
| S6_Calibration_Protocol.pdf | ขั้นตอน GC-FID validation | ❌ ยังไม่สร้าง |

---

## 🚀 Workflow การตีพิมพ์

### ขั้นตอนที่ 1: เก็บข้อมูลและ Train โมเดล

```bash
# 1. รัน GUI และเก็บข้อมูล
cd program
python gui.py

# 2. Train model
cd ../BuildML_PC/train/colab
jupyter notebook methane_ppm_regression_colab.ipynb

# 3. Deploy model
cp models/methane_linreg_model.joblib ../../models/
```

### ขั้นตอนที่ 2: กรอกผลการทดลองใน Manuscript

```bash
# แก้ไข MANUSCRIPT.md
nano docs/MANUSCRIPT.md

# แทนที่:
# - [TBD] → ค่าจริงจากการทดลอง
# - [X.XX] → ตัวเลข R², RMSE, MAE
# - [N] → จำนวน runs
```

### ขั้นตอนที่ 3: สร้างรูปภาพ

```bash
# สร้างกราฟทั้งหมด
python scripts/generate_manuscript_figures.py

# ตรวจสอบรูป
ls docs/figures/
```

### ขั้นตอนที่ 4: สร้าง Supplementary Materials

```bash
# S1: Export PCB จาก KiCad/EasyEDA
# S2: สร้าง Excel จาก hardware_config.json
# S3–S6: เขียนตามคู่มือใน MANUSCRIPT_GUIDE.md
```

### ขั้นตอนที่ 5: แปลง Markdown → PDF/LaTeX

```bash
# ใช้ pandoc
pandoc docs/MANUSCRIPT.md -o docs/manuscript.pdf \
  --bibliography=docs/references.bib \
  --csl=acs-environmental-science-technology.csl \
  --pdf-engine=xelatex

# หรือแปลงเป็น LaTeX
pandoc docs/MANUSCRIPT.md -o docs/manuscript.tex \
  --bibliography=docs/references.bib
```

### ขั้นตอนที่ 6: Submit

1. เลือก target journal (Environmental Science & Technology / Sensors / ...)
2. ปรับรูปแบบตาม journal guidelines
3. อัปโหลด manuscript + figures + supplementary materials
4. เขียน cover letter
5. Submit!

---

## 🎯 Target Journals

| Journal | Impact Factor | Open Access | Fit Score |
|---------|---------------|-------------|-----------|
| **Environmental Science & Technology** | ~11.4 | Hybrid | ⭐⭐⭐⭐⭐ |
| **Sensors (MDPI)** | ~3.9 | Full OA | ⭐⭐⭐⭐⭐ |
| **Agriculture, Ecosystems & Environment** | ~6.6 | Subscription | ⭐⭐⭐⭐ |
| **Biosensors and Bioelectronics** | ~12.6 | Subscription | ⭐⭐⭐ |
| **Journal of Environmental Management** | ~8.7 | Subscription | ⭐⭐⭐⭐ |

**คำแนะนำ:**

- **Environmental Science & Technology** — เหมาะสำหรับงานที่เน้น environmental monitoring + ML
- **Sensors (MDPI)** — Open access, fast review (~2 months), เหมาะสำหรับ sensor development
- **Agriculture, Ecosystems & Environment** — เน้น agricultural applications, ผู้อ่านเป้าหมายตรงกับ rice farming

---

## 📧 Contact

หากมีคำถามเกี่ยวกับเอกสาร:

- **ผู้เขียน manuscript:** [ชื่อ, อีเมล]
- **ผู้ดูแลโปรเจกต์:** [ชื่อ, อีเมล]
- **Repository:** https://github.com/[user]/eNose_methane

---

## 📜 License

เอกสารทั้งหมดในโฟลเดอร์นี้เป็นส่วนหนึ่งของงานวิจัย eNose Methane Detection Project

- **Manuscript และ References:** CC BY 4.0 (เมื่อตีพิมพ์แล้ว)
- **User Guide:** CC BY-SA 4.0
- **Literature Review และ Papers:** ตามลิขสิทธิ์ของแต่ละงานต้นฉบับ

---

**อัปเดตล่าสุด:** 2026-07-20  
**เวอร์ชัน:** 1.0

---

*เอกสารนี้สร้างขึ้นเพื่อรวบรวมและจัดระเบียบเอกสารทั้งหมดของโปรเจกต์ในที่เดียว*
