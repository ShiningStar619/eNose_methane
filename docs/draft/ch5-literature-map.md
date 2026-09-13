# แผนที่หลักการและอ้างอิง — บทที่ 5 (`Proposal draft 12.docx`)

**อัปเดต:** 1 ก.ย. 2026 (รอบ 2 — Firecrawl authenticated)  
**แหล่งโครงหัวข้อ:** `docs/draft/_ch56_final.txt`  
**สถานะ docx:** โครงหัวข้อครบ · ยังไม่มีย่อหน้าทฤษฎี/สมการ/รูปในบท 5  
**วิธีค้น:** Firecrawl search+scrape (รอบ 2) + `docs/paper/screened/` + `project-knowledge` + `chapter-5-principles-theories-draft.md`  
**Firecrawl:** Authenticated · ใช้ ~131 credits ในรอบนี้ · cache ใน `.firecrawl/`

## คำถามวิจัย

| RQ | คำถาม |
|----|--------|
| **RQ1** | แต่ละหัวข้อ 5.x ควรอ้าง **ตำรา/หลักการ** อะไรเป็นแกน |
| **RQ2** | งานวิจัยใด **สนับสนุน** แต่ละหัวข้อ — ใช้อธิบายอะไร |
| **RQ3** | `project-knowledge` ใส่หัวใดได้ |

**มุมวิทยานิพนธ์:** วัด **ppm ในห้องทดลอง** · **GC = เพดาน** · ไม่สรุปฟลักซ์แปลงนาทั้งฤดู (6.1.4)

---

## สรุปภาพรวม (RQ3)

| ตำรา | บท 5 |
|------|------|
| **Deisenroth et al. (2020)** *MML* | **5.5 ทั้งหมด** — ERM, linear regression, overfitting, RMSE |
| **Madsen (2011)** *Statistics for Non-Statisticians* | **5.5.4–5.5.5** — uncertainty, การแบ่งข้อมูล |
| **Creswell / METU / Bonanno** | ไม่ใส่ทฤษฎี 5.1–5.4 |

### ตำรา e-nose (ยืนยัน Firecrawl + DOI)

| แหล่ง | DOI / URL | บทบาท | OA |
|-------|-----------|--------|-----|
| **Persaud & Gardner (1982)** | 10.1016/0925-4005(92)85001-D | ต้นกำเนิด multisensor array | ปิด (SciDirect) |
| **Gardner & Bartlett (1999)** | 10.1093/oso/9780198559559.001.0001 | นิยาม e-nose คลassic | ปิด (Oxford) |
| **Pearce et al. (2003)** *Handbook of Machine Olfaction* | 10.1002/3527601597 | MOS, headspace, สัญญาณ | ปิด (Wiley) |
| **Wilson & Baietto (2009)** | 10.3390/s90705099 | **ทดแทน OA** สำหรับ Gardner — รีวิว e-nose + นิยาม Gardner-Bartlett | **OA** → `.firecrawl/wilson-baietto-2009-v2.md` |

**นิยาม Gardner-Bartlett (ยืนยันจาก Wilson 2009):**  
*"an instrument which comprises an array of electronic chemical sensors with partial specificity and an appropriate pattern recognition system, capable of recognizing simple or complex odors"*

---

## ตารางแมปต่อหัวข้อ

**P** = แกน · **S** = สนับสนุน · **B** = บริบท/นอกขอบ · **T** = ตำรา · **F** = ยืนยัน Firecrawl รอบ 2

---

### 5.1 การเกิดและปล่อย CH₄ ในนาข้าวน้ำขัง

| บทบาท | แหล่ง | ใช้อธิบาย | หลักฐาน |
|-------|--------|-----------|---------|
| **P** | **Conrad (2020)** *Microorganisms* 8:881 | ลำดับตัวรับอิเล็กตรอน, methanogen ทน O₂, วัฏจักรท่วม–แห้ | PDF ในคลัง + **F** `.firecrawl/conrad-2020-mdpi.md` |
| **P** | **Nouchi et al. (1990)** *Plant Physiol.* 94:59 | ขนส่ง CH₄ ทาง aerenchyma | DOI 10.1104/pp.94.1.59 (PubMed 16667719) |
| **S** | Gu et al. (2022) | เมตา-วิเคราะห์ น้ำ–ปุ๋ย → CH₄ | PDF ในคลัง |
| **S** | Guan (2024), Dai (2026), Yang (2022) | ราก/คาร์บอน/pH/ปุ๋ย | PDF ในคลัง |
| **B** | Anapalli (2023) | AWD ลดฟลักซ์ ~50% | PDF ในคลัง |

#### 5.1.1 ไร้ออกซิเจน + methanogen

| **P** | Conrad (2020) | O₂ หมด → NO₃⁻ → Fe³⁺ → SO₄²⁻ → CH₄; methanogen ไม่สร้าง resting stage แต่ทน O₂ ได้มากกว่าเดิมเชื่อ |
| **P** | Nouchi (1990) | ท่ออากาศในต้นข้าว |
| **S** | Gu (2022) | ภาพรวมเส้นทาง ebullition / diffusion / aerenchyma |

#### 5.1.2 ตัวแปร → ppm เหนือผิวนา

| **S** | Guan, Dai, Gu, Yang | ราก, C, pH, น้ำ, ปุ๋ย, พันธุ์ |
| **B** | Hu CH₄MOD (2024) | โมเดลกระบวนการ — ไม่ใช่ ppm รายจุด |

---

### 5.2 ความเข้มข้น vs ฟลักซ์

| บทบาท | แหล่ง | ใช้อธิบาย | หลักฐาน |
|-------|--------|-----------|---------|
| **P** | **Minamikawa et al. (2015)** GRA Guidelines | สมการฟลักซ์ static chamber | PDF 80 หน้า ในคลัง |
| **P** | **Khalil et al. (1998)** *JGR* 103:25211 | สมการ F = γ[M/N₀ρV/A]·dC/dt; การเลือก ΔT, N | **F** `.firecrawl/khalil-chamber-flux.pdf` |
| **S** | Zaman (2021) บทที่ 2 | SOP chamber–GC | PDF ในคลัง |
| **S** | Bertora et al. (2018) *J. Vis. Exp.* | โพรโตคอล chamber นา | PMC6235105 (ค้น Firecrawl) |

**ประโยคแกน:** งานนี้รายงาน **ppm** — ฟลักซ์อธิบายเพื่อแยกชั้น ไม่ claim ฟลักซ์ฤดู

#### 5.2.1 ppm/ppb

| **P** | Li (2022) | LOD 0.0567 ppm, กรaph มาตรฐาน |
| **S** | Shah (2023) | TGS2611 ถึง ~1000 ppm lab |
| **S** | Domènech-Gil (2024) | 1–150 ppm สนาม |

#### 5.2.2 static chamber + bullets

| หัวข้อ bullet | แหล่งหลัก | หมายเหตุ |
|--------------|-----------|----------|
| Static chamber | Minamikawa 2015; Khalil 1998 **F**; Tokida 2021 | สมการ flux + QC r²>0.9 |
| Dynamic flux chamber | Zaman ch.2 | contrast |
| Dissolved CH₄ / isotope | Conrad; Gu 2022 | **B** |
| Eddy covariance | Anapalli 2023 | **B** แปลง ~50 ha |
| Flux gradient / IHF | Zaman ch.2 | **B** |
| ดาวเทียม / inversion / ML upscaling | Saunois 2025; Zhang *Nat. Commun.* 2020; Hu CH₄MOD | **B** ภูมิภาค |

---

### 5.3 GC อ้างอิง

| บทบาท | แหล่ง | ใช้อธิบาย |
|-------|--------|-----------|
| **P** | Li et al. (2022) *Molecules* | GC-FID, split injection, y=2.4192x+0.1294, r=0.9998 |
| **P** | Zaman (2021) ch.2 | ขั้นตอน sampling → GC |
| **S** | Firecrawl search GC-FID | ACS 10.1021/ac5043076 — มาตรฐาน CH₄ gravimetric **[unconfirmed: ยังไม่ scrape]** |

#### 5.3.1 คอลัมน์ + FID — Li (2022), Zaman (2021)  
#### 5.3.2 ก๊าซมาตรฐาน — Li (2022); Minamikawa (2015)

---

### 5.4 e-nose / MOS

| บทบาท | แหล่ง | ใช้อธิบาย | หลักฐาน |
|-------|--------|-----------|---------|
| **T** | Persaud & Gardner (1982) | multisensor array ต้นกำเนิด | SciDirect (ค้น Firecrawl) |
| **T** | Gardner & Bartlett (1999) | นิยาม e-nose | Oxford (ปิด) |
| **T** | **Wilson & Baietto (2009)** | รีวิว OA + อ้างนิยาม Gardner-Bartlett + sensor types | **F** MDPI s90705099 |
| **T** | Pearce Handbook (2003) | MOS, headspace | ปิด |
| **S** | Ye (2021), Fu (2023) | รีวิว eNose+ML / MOS CH₄ | PDF ในคลัง |
| **S** | Domènech-Gil (2024) *ES&T* | TGS2611×2 + BME680, PLSR | PDF ในคลัง |
| **S** | Shah (2023) *AMT* | T/H รบกวน TGS2611; RMSE ±1 ppm ที่ 28 ppm | **F** `.firecrawl/shah-amt-2023.md` + PDF ในคลัง |
| **S** | Furuta (2022, 2024) | MOS ระดับต่ำ | PDF ในคลัง |
| **B** | Rajasekar (2022) | MOS ในนา แต่สูตรผู้ผลิต ไม่ใช่ ML |

#### 5.4.1 นิยาม e-nose
Wilson (2009) **F** + Gardner (1999) + Ye (2021); แยกจากเซ็นเซอร์เดี่ยว (Rajasekar)

#### 5.4.2 MOS chemiresistive
Fu (2023); Pearce (2003); Shah (2023) — resistance ลดเมื่อเจอ reducing gas

#### 5.4.3 T/H/P
Shah (2023) **F**: "resistance sensitive to temperature and [H2O]"; fractional uncertainty <±3% ที่ 25°C, 1% H₂O  
Bastviken (2020); Collier-Oxandale (2018)

#### 5.4.4 สัญญาณ / ADC / divider
| **P** | **Reyes et al. (2020)** *Electronics* 9:525 "Circuit Topologies for MOS-Type Gas Sensor" | voltage divider, Wheatstone, load R ~10 kΩ | **F** `.firecrawl/mos-circuit-topologies.md` |
| **P** | Shah (2023) | resistance ratio vs [CH₄] |
| **S** | Figaro TGS2611/TGS2612 datasheet | จาก cache `.firecrawl/search-mos-equation.json` |
| **S** | `chapter-5-principles-theories-draft.md` | ΔV = V_measure − V_baseline |

---

### 5.5 Supervised learning

| บทบาท | แหล่ง | ใช้อธิบาย |
|-------|--------|-----------|
| **T** | Deisenroth (2020) *MML* | ERM, linear regression, train/test, overfitting |
| **T** | Madsen (2011) | estimate + uncertainty |
| **S** | Kiplimo (2024), Andrews (2023), Mitchell (2024), Lakhmi (2024) | ML calibrate MOS/Figaro |
| **S** | Domènech-Gil (2024) | PLSR, lab R²=0.97, RMSE 89 ppb |

| หัวข้อ | แกน |
|--------|-----|
| 5.5.1 | Deisenroth ch10 — supervised = คู่ (x,y) |
| 5.5.2 | Deisenroth — **regression** ไม่ใช่ classification (Yin 2023 = ตัวอย่าง B) |
| 5.5.3 | Deisenroth ch08,10 — least squares; Mitchell/Kiplimo = applied |
| 5.5.4 | Deisenroth overfitting; Madsen ch05 |
| 5.5.5 | RMSE/MAE/R² — Deisenroth + Domènech-Gil ตัวเลข |

---

## ช่องว่างวิจัย (ยืนยันหลังค้นครบ)

> ไม่มีงานในคลังที่ครบ: **MOS array + regression → ppm + chamber–GC ในนาข้าว**

Rajasekar ≈ สถานที่ · Domènech-Gil ≈ eNose+PLSR แต่ไม่ใช่นา/GC

---

## ไฟล์ Firecrawl รอบ 2 (อ้างอิงได้)

| ไฟล์ | เนื้อหา |
|------|---------|
| `conrad-2020-mdpi.md` | 5.1.1 methanogenesis |
| `wilson-baietto-2009-v2.md` | 5.4.1 นิยาม e-nose |
| `shah-amt-2023.md` | 5.4.3–5.4.4 TGS2611 |
| `mos-circuit-topologies.md` | 5.4.4 voltage divider |
| `khalil-chamber-flux.pdf` | 5.2.2 สมการ flux |
| `search-*.json` | ผลค้น 9+ หัวข้อ |

---

## References ย่อ

Conrad 2020 · Nouchi 1990 · Gu 2022 · Guan 2024 · Dai 2026 · Minamikawa 2015 · Khalil 1998 · Zaman 2021 · Li 2022 · Persaud 1982 · Gardner 1999 · Wilson 2009 · Pearce 2003 · Ye 2021 · Fu 2023 · Shah 2023 · Reyes 2020 · Domènech-Gil 2024 · Kiplimo 2024 · Andrews 2023 · Mitchell 2024 · Lakhmi 2024 · Deisenroth 2020 · Madsen 2011
