# คู่มือการใช้งาน Manuscript สำหรับ eNose Methane Detection Project

เอกสารนี้อธิบายการใช้งาน และแนวทางในการปรับแต่ง manuscript (`MANUSCRIPT.md`) และ references (`REFERENCES.md`) สำหรับการตีพิมพ์

---

## 📋 โครงสร้างเอกสาร

### 1. MANUSCRIPT.md

Manuscript หลักประกอบด้วย 5 sections หลักตามมาตรฐานงานวิจัยวิทยาศาสตร์:

```
Abstract
1. Introduction
   1.1 Research Background
   1.2 Electronic Nose Technology
   1.3 Research Gap and Objectives
2. Materials and Methods
   2.1 Hardware System Design
   2.2 Experimental Design
   2.3 Feature Engineering
   2.4 Machine Learning Pipeline
   2.5 Model Deployment
   2.6 Software Implementation
3. Results
   3.1 Data Collection Summary
   3.2 Feature Analysis
   3.3 Model Performance
   3.4 Feature Importance
   3.5 System Operational Performance
   3.6 Comparison with Reference Method
4. Discussion
   4.1 Achievement of Research Objectives
   4.2 Sensor Response and Feature Engineering
   4.3 Model Selection
   4.4 Limitations
   4.5 Implications for Rice Paddy Monitoring
   4.6 Methodological Contributions
   4.7 Future Directions
5. Conclusions
Acknowledgments
References
Supplementary Materials
```

### 2. REFERENCES.md

บรรณานุกรมจัดเป็น 7 หมวดตาม literature review:

- Methane Emissions from Rice Paddies
- Reference Methods (Chamber–GC and Spectroscopy)
- Electronic Nose Technology and MOS Sensors
- Machine Learning for Gas Sensing
- Field Deployment and Agricultural Applications
- Supporting Literature
- Dataset and Model References

---

## ✏️ การกรอกข้อมูลผลการทดลอง

Manuscript มี placeholders สำหรับผลการทดลองที่ต้องกรอก:

### ส่วน Abstract

```markdown
**Results:** The final Linear Regression model achieved R² = [TBD], 
RMSE = [TBD] ppm, and MAE = [TBD] ppm on test data.
```

**แนวทางการกรอก:**

- หลังจากรัน `BuildML_PC/train/colab/methane_ppm_regression_colab.ipynb`
- ดูค่าจาก `models/methane_linreg_metrics.json`:
  ```json
  {
    "test_R2": 0.85,
    "test_RMSE": 1.23,
    "test_MAE": 0.98
  }
  ```
- แทนค่าลงใน manuscript: `R² = 0.85, RMSE = 1.23 ppm, MAE = 0.98 ppm`

### ส่วน Results (Section 3.3.1)

ตารางเปรียบเทียบโมเดล:

```markdown
| Model | Mean CV R² | Test R² | Test RMSE (ppm) | Test MAE (ppm) |
|-------|------------|---------|------------------|----------------|
| **Linear Regression** | **[X.XX]** | **[X.XX]** | **[Y.YY]** | **[Z.ZZ]** |
```

**แนวทางการกรอก:**

1. เปิด Notebook training results
2. หา cross-validation scores: `np.mean(cv_scores['test_r2'])`
3. หา test metrics จาก final model evaluation
4. กรอกค่าทุกโมเดลที่ทดสอบ (Linear, Ridge, Lasso, RF, GB, PLSR)

### ส่วน Results (Section 3.2.3)

ตารางความสำคัญของ features:

```markdown
| Rank | Feature | Correlation (r) |
|------|---------|-----------------|
| 1 | ss1_dV | [0.XX] |
```

**แนวทางการกรอก:**

- ใช้ `df[features].corrwith(df['ppm']).sort_values(ascending=False)`
- นำ top 10 features มาใส่ในตาราง

---

## 📊 การเพิ่มรูปภาพและกราฟ

Manuscript มีคำแนะนำสำหรับรูปที่ควรสร้าง:

### Figure 1: Time-series sensor response

```markdown
*[Include figure: time-series plot of ss1–ss4 showing 
Baseline → Measure phases at 1 ppm vs. 10 ppm]*
```

**วิธีสร้าง:**

```python
import matplotlib.pyplot as plt
import pandas as pd

# โหลดข้อมูล
df_low = pd.read_csv('acquisition/processed_data/adc1263_1ppm.csv')
df_high = pd.read_csv('acquisition/processed_data/adc1263_10ppm.csv')

fig, axes = plt.subplots(2, 1, figsize=(10, 8))

# Plot 1 ppm
for col in ['ss1_lp_ma', 'ss2_lp_ma', 'ss3_lp_ma', 'ss4_lp_ma']:
    axes[0].plot(df_low['elapsed_time_sec'], df_low[col], label=col)
axes[0].axvspan(10, 30, alpha=0.2, color='blue', label='Baseline')
axes[0].axvspan(60, 120, alpha=0.2, color='red', label='Measure')
axes[0].set_title('1 ppm CH₄')
axes[0].legend()

# Plot 10 ppm
for col in ['ss1_lp_ma', 'ss2_lp_ma', 'ss3_lp_ma', 'ss4_lp_ma']:
    axes[1].plot(df_high['elapsed_time_sec'], df_high[col], label=col)
axes[1].axvspan(10, 30, alpha=0.2, color='blue')
axes[1].axvspan(60, 120, alpha=0.2, color='red')
axes[1].set_title('10 ppm CH₄')
axes[1].set_xlabel('Time (s)')
axes[1].legend()

plt.tight_layout()
plt.savefig('docs/figures/fig1_sensor_response.png', dpi=300)
```

บันทึกรูปไว้ใน `docs/figures/` และอ้างอิงใน manuscript

### Figure 2: Correlation heatmap

```markdown
*[Include figure: correlation heatmap of top 15 features + ppm]*
```

**วิธีสร้าง:**

```python
import seaborn as sns

# คำนวณ correlation matrix
top_features = ['ss1_dV', 'ss1_dV_pct', 'temperature_c_mean', 
                'ss1_slope', 'ss1_ss2_ratio', 'ppm']
corr_matrix = df[top_features].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            vmin=-1, vmax=1, square=True)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig('docs/figures/fig2_correlation_heatmap.png', dpi=300)
```

### Figure 3: Predicted vs. True scatter plot

```markdown
*[Include figure: predicted vs. true scatter plot with diagonal line]*
```

**วิธีสร้าง:**

```python
from sklearn.metrics import r2_score

plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.6, edgecolors='k', s=80,
            c=heater_setpoints_test, cmap='viridis')
plt.colorbar(label='Heater Setpoint (°C)')

# Diagonal line
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)

plt.xlabel('True CH₄ (ppm)', fontsize=14)
plt.ylabel('Predicted CH₄ (ppm)', fontsize=14)
plt.title(f'Prediction Accuracy (R² = {r2_score(y_test, y_pred):.3f})')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/figures/fig3_predicted_vs_true.png', dpi=300)
```

### Figure 4: Feature importance bar plot

```markdown
*[Include figure: bar plot of Linear Regression coefficients]*
```

**วิธีสร้าง:**

```python
# ดึง coefficients จากโมเดล
coeffs = model.coef_
feature_names = model.feature_names_in_

# เรียงตาม absolute value
importance_df = pd.DataFrame({
    'feature': feature_names,
    'coefficient': coeffs
}).sort_values('coefficient', key=abs, ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(importance_df['feature'][:10], importance_df['coefficient'][:10])
plt.xlabel('Coefficient Value')
plt.title('Top 10 Feature Importance (Linear Regression)')
plt.tight_layout()
plt.savefig('docs/figures/fig4_feature_importance.png', dpi=300)
```

---

## 📝 Supplementary Materials

Manuscript อ้างอิง 6 ไฟล์ Supplementary:

### S1_Hardware_Schematics.pdf

- วงจรไฟฟ้าของ ADC, BME280, relay connections
- PCB layout (ถ้ามี)
- Pin mapping table

**วิธีสร้าง:** Export จาก KiCad, EasyEDA, หรือ Fritzing

### S2_Operation_Sequences.xlsx

- ตารางแสดงสถานะ relay ในแต่ละ Operation (1–7 + Break)
- ระยะเวลาของแต่ละขั้น
- Timing diagram

**ตัวอย่างตาราง:**

| Operation | Duration (s) | Heater | Pump | Fan | s_valve1 | s_valve2 | s_valve3 | s_valve4 |
|-----------|--------------|--------|------|-----|----------|----------|----------|----------|
| Heating | 1800 | ON | OFF | OFF | OFF | OFF | OFF | OFF |
| Baseline | 30 | ON | ON | OFF | ON | ON | OFF | OFF |
| Vacuum | 10 | ON | ON | OFF | OFF | ON | ON | OFF |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### S3_Feature_Extraction_Details.md

- อธิบายขั้นตอนการคำนวณ features ทีละ feature
- Code snippets สำหรับแต่ละ feature

**ตัวอย่าง:**

```markdown
## Feature: ss1_dV

**Definition:** ΔV = mean(Measure window) - mean(Baseline window)

**Calculation:**

```python
baseline_window = df[(df['elapsed_time_sec'] >= 10) & 
                      (df['elapsed_time_sec'] <= 30)]
measure_window = df[(df['elapsed_time_sec'] >= 60) & 
                     (df['elapsed_time_sec'] <= 120)]

baseline_mean = baseline_window['ss1_lp_ma'].mean()
measure_mean = measure_window['ss1_lp_ma'].mean()

ss1_dV = measure_mean - baseline_mean
```

**Interpretation:** Larger ΔV indicates stronger sensor response to CH₄.
```

### S4_Model_Training_Notebook.ipynb

- คัดลอกหรือสร้าง cleaned version ของ Jupyter Notebook
- รันให้ครบทุก cell พร้อม output
- Export เป็น HTML หรือเก็บ `.ipynb` โดยตรง

### S5_Field_Deployment_Checklist.pdf

- ขั้นตอนการติดตั้งระบบในแปลงนาจริง
- รายการอุปกรณ์ที่ต้องเตรียม
- Safety precautions (ไฟฟ้า, ความชื้น, อุณหภูมิ)
- Calibration schedule

### S6_Calibration_Protocol.pdf

- วิธีการทำ GC-FID validation
- ความถี่ในการ re-calibrate (เช่น ทุก 2 สัปดาห์)
- QC criteria สำหรับข้อมูลที่ใช้ได้

---

## 🎯 การปรับแต่งตาม Journal

### Environmental Science & Technology (ACS)

**ความยาว:** 6,000–7,000 words (รวม abstract, ไม่รวม references)

**รูปแบบ:**

- Abstract: ≤150 words, structured (Background, Methods, Results, Conclusions)
- หัวข้อหลัก: Introduction, Materials and Methods, Results and Discussion (รวมกันได้), Conclusions
- References: ≤50 citations, numbered style
- Figures: ≤6, ความละเอียด 300–600 dpi

**การปรับ manuscript:**

1. ย่อ Abstract ให้สั้นลง (ปัจจุบัน ~200 words)
2. รวม Results & Discussion เป็นส่วนเดียว
3. ตัด references ที่ไม่จำเป็นให้เหลือ ≤50

### Sensors (MDPI)

**ความยาว:** ไม่จำกัด (แนะนำ 5,000–8,000 words)

**รูปแบบ:**

- Abstract: ≤200 words, เป็นพารากราฟเดียว
- Keywords: 5–7 คำ
- หัวข้อตามต้องการ (แนะนำ: Introduction, Materials and Methods, Results, Discussion, Conclusions)
- References: ไม่จำกัด, numbered style พร้อม DOI

**การปรับ manuscript:**

- Manuscript ปัจจุบันเหมาะกับ Sensors แล้ว
- เพิ่ม section "Author Contributions" ตาม CRediT taxonomy
- เพิ่ม "Funding" section ถ้ามี

### Agriculture, Ecosystems & Environment (Elsevier)

**ความยาว:** 6,000–8,000 words

**รูปแบบ:**

- Abstract: ≤300 words, แบบ structured หรือ unstructured
- หัวข้อตามมาตรฐาน IMRAD
- References: author-year style (แทนที่ [1] → Smith et al., 2024)
- Graphical abstract: สร้างภาพสรุปงานวิจัย 1 รูป

**การปรับ manuscript:**

1. เปลี่ยน citations จาก `[4]` → `(Nguyen et al., 2023)`
2. เรียง references ตามตัวอักษร
3. สร้าง Graphical Abstract (แผนภาพ workflow: eNose → ML → ppm)

---

## 🔄 Workflow สำหรับการตีพิมพ์

### ขั้นตอนที่ 1: เติมข้อมูลผลการทดลอง

```bash
# 1. รัน training pipeline
cd BuildML_PC/train/colab/
jupyter notebook methane_ppm_regression_colab.ipynb

# 2. คัดลอก metrics
cat ../../models/methane_linreg_metrics.json

# 3. แก้ไข MANUSCRIPT.md
nano docs/MANUSCRIPT.md
# แทนที่ [TBD] และ [X.XX] ทั้งหมด
```

### ขั้นตอนที่ 2: สร้างรูปภาพ

```bash
mkdir -p docs/figures
python scripts/generate_manuscript_figures.py
# จะสร้าง fig1–fig6 ใน docs/figures/
```

*(สคริปต์ `generate_manuscript_figures.py` ควรสร้างขึ้นเพื่อ automate การสร้างกราฟทั้งหมด)*

### ขั้นตอนที่ 3: สร้าง Supplementary Materials

```bash
# S1: Export PCB
# (จาก KiCad/EasyEDA)

# S2: Operation sequences
# สร้างใน Excel หรือ export จาก hardware_config.json

# S3: Feature extraction details
cp docs/FEATURE_EXTRACTION.md docs/supplementary/S3_Feature_Extraction_Details.md

# S4: Notebook
jupyter nbconvert --to html BuildML_PC/train/colab/*.ipynb
mv *.html docs/supplementary/S4_Model_Training_Notebook.html

# S5 & S6: เขียนเอง หรือ adapt จาก README
```

### ขั้นตอนที่ 4: แปลงเป็น LaTeX (ถ้าต้องการ)

```bash
# ใช้ pandoc แปลง Markdown → LaTeX
pandoc docs/MANUSCRIPT.md -o docs/manuscript.tex \
  --bibliography=docs/references.bib \
  --csl=acs-environmental-science-technology.csl

# แก้ไข .tex ให้ตรงตาม journal template
```

### ขั้นตอนที่ 5: Submission Checklist

- [ ] Abstract ≤150/200/300 words (ตาม journal)
- [ ] Keywords ครบ 5–7 คำ
- [ ] Figures ความละเอียด 300+ dpi
- [ ] References format ถูกต้อง (numbered หรือ author-year)
- [ ] Supplementary Materials ครบทุกไฟล์
- [ ] Author contributions ระบุชัดเจน
- [ ] Data availability statement
- [ ] Conflict of interest statement
- [ ] Acknowledgments & Funding

---

## 📚 ทรัพยากรเพิ่มเติม

### Templates และ CSL Files

- **ACS Style:** https://github.com/citation-style-language/styles/blob/master/acs.csl
- **MDPI Sensors:** https://www.mdpi.com/authors/references
- **Elsevier Guide:** https://www.elsevier.com/authors/policies-and-guidelines

### เครื่องมือช่วยเขียน

- **Grammarly:** ตรวจ grammar และ style
- **Writefull:** AI-powered academic writing suggestions
- **Zotero:** จัดการ references และ citations
- **Overleaf:** LaTeX editor online (ถ้าแปลงเป็น .tex)

### Preprint Servers

อัปโหลด preprint ก่อนส่ง journal:

- **bioRxiv** (ถ้า journal อนุญาต): https://www.biorxiv.org/
- **arXiv** (Computer Science section): https://arxiv.org/
- **ResearchSquare** (multi-disciplinary): https://www.researchsquare.com/

---

## 💡 เคล็ดลับการเขียน

### Abstract

- ประโยคแรกต้อง hook ผู้อ่าน (ระบุปัญหาที่สำคัญ)
- ใช้ตัวเลขเด่นๆ (R² = 0.XX, RMSE = Y.YY ppm)
- สรุปความสำคัญของงานใน 1–2 ประโยคสุดท้าย

### Introduction

- วรรคแรก: background กว้างๆ (ทำไม CH₄ จากข้าวสำคัญ)
- วรรคกลาง: วิธีวัดที่มีอยู่และข้อจำกัด
- วรรคสุดท้าย: ช่องว่างงานวิจัยและ objectives ของงานนี้
- หลีกเลี่ยงคำซ้ำซาก เช่น "in this study" ใช้บ่อยเกินไป

### Results

- นำเสนอข้อมูลอย่างเป็นระบบ (จากข้อมูลดิบ → features → model → validation)
- ใช้ตารางสำหรับตัวเลขหลายชุด
- ใช้กราฟสำหรับ trends และ comparisons
- อธิบายรูปภาพใน caption อย่างละเอียด (ผู้อ่านควรเข้าใจได้โดยไม่ต้องอ่าน main text)

### Discussion

- เริ่มด้วยสรุปผลลัพธ์หลัก (1 วรรค)
- เชื่อมโยงกับงานวิจัยอื่น (เหมือน/ต่าง/ดีกว่า อย่างไร)
- ยอมรับข้อจำกัดอย่างตรงไปตรงมา
- เสนอ future work ที่เป็นรูปธรรม (ไม่ใช่ "more research is needed" ทั่วไป)

### Conclusions

- ไม่ต้องยาว (3–5 ประโยค)
- สรุป key findings และความสำคัญ
- ไม่ควรมีข้อมูลใหม่ที่ไม่เคยพูดถึงใน Results/Discussion

---

## 🚀 การ Commit และ Version Control

ใช้ Git สำหรับ track changes:

```bash
# สร้าง branch สำหรับ manuscript
git checkout -b manuscript-draft

# เพิ่มไฟล์เข้า Git
git add docs/MANUSCRIPT.md docs/REFERENCES.md docs/figures/

# Commit พร้อมข้อความ
git commit -m "feat: Add complete manuscript draft v1.0

- Complete IMRAD structure (Introduction, Methods, Results, Discussion)
- Full references with 50+ citations
- 6 figure placeholders with generation instructions
- Supplementary materials outline"

# Push ไปที่ remote
git push -u origin manuscript-draft
```

### Naming Conventions

- **Manuscript versions:** `MANUSCRIPT_v1.0.md`, `MANUSCRIPT_v1.1.md`
- **Figures:** `fig1_sensor_response.png`, `fig2_correlation_heatmap.png`
- **Supplementary:** `S1_Hardware_Schematics.pdf`, `S2_Operation_Sequences.xlsx`

---

## 📧 Contact และ Support

หากมีคำถามเกี่ยวกับการเขียน manuscript:

- ดูตัวอย่างจากงานตีพิมพ์ใน `docs/paper/`
- อ้างอิง `docs/paper/literature-review-4.2.md` สำหรับโครงสร้างการทบทวนวรรณกรรม
- ศึกษาจาก Domènech-Gil et al. (2024) เป็น template methodology

**Good luck with your publication! 🎓📄**

---

*เอกสารนี้สร้างขึ้นเพื่อช่วยให้การเขียน manuscript เป็นไปอย่างเป็นระบบและมีประสิทธิภาพ*
