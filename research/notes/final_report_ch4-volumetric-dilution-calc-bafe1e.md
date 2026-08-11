# Calculating CH₄ concentration in a newly mixed calibration bag

**Vault tag:** `ch4-volumetric-dilution-calc-bafe1e`  
**Query:** ฉันจะคำนวณความเข้มของ methane ที่ผสมขึ้นมาใหม่ ยังไง (ทฤษฎี + textbook)  
**Tier:** light · **Format:** structured

This report answers how to compute the methane concentration of a bag mixture prepared from a certified mother cylinder plus diluent air, with textbook and standards framing suitable for an eNose calibration write-up.

---

## 1. Ideal-gas volume-fraction mixing basis

At a fixed temperature \(T\) and pressure \(P\), an ideal gas obeys \(PV = nRT\). Rearrangement shows that, for fixed \(T\) and \(P\), the amount of substance \(n\) is strictly proportional to the volume \(V\) occupied by that gas. LibreTexts and standard physical-chemistry treatments of the ideal-gas law make this proportionality explicit: equal volumes of ideal gases at the same \(T\) and \(P\) contain equal numbers of moles [[ideal-gas-law-libretexts]] [[wikipedia-ideal-gas]] [[ideal-gas-law-libretexts]].

When two ideal gases are combined into one container and allowed to reach a common \(T\) and \(P\), the mole fraction of species \(i\) equals the volume fraction contributed by that species [[wikipedia-ideal-gas]]:

\[
y_i = \frac{n_i}{n_{\text{total}}} = \frac{V_i}{V_{\text{total}}}
\]

Dalton’s law of partial pressures is the pressure-domain twin of the same idea: \(p_i = y_i P\). In the parts-per-million regime used for paddy and sensor work, methane is a dilute solute in air. Non-ideality corrections (virial coefficients, large compressibility differences) are negligible for ordinary laboratory temperature and near-atmospheric pressure. Therefore the operational definition of concentration used by GC-FID and by most sensor literature is volumetric:

\[
c\ [\mathrm{ppm}] = y_{\mathrm{CH_4}} \times 10^6
\]

Calculating the concentration of a newly mixed bag therefore reduces to computing the methane mole (volume) fraction after mixing, then scaling by \(10^6\). The hard part is not the algebra; it is measuring the volumes (or flows and times) that enter \(V_i\) and stating honestly whether the diluent itself already contains methane.

Two practical consequences follow. First, all volumes in the dilution equation must refer to the same \(T\) and \(P\) (or must be converted to a common reference state). A rotameter reading after a regulator is already a volumetric flow at the local line condition; a bag volume is the geometric capacity you actually fill. Second, ppm here is not mg/m³. Converting to mass concentration requires the ideal-gas density of CH₄ at the stated \(T,P\), which is a separate step used for flux calculations, not for the bag-label ppm used to train the eNose regressor.

---

## 2. Working equations for mother + diluent (zero air vs ambient)

### 2.1 Textbook dilution with analyte-free diluent

Analytical chemistry textbooks formalize standard preparation as transferring a known amount of analyte into a larger final volume. Harris presents the dilution factor for solutions as \(c_f = c_i V_i / V_f\) when the transferred aliquot and the final flask share a consistent concentration basis [[harris-qa-dilution-biblio]] [[harris-qa-dilution-biblio]]. Skoog and colleagues likewise treat quantitative analysis as comparison against standards of known composition [[skoog-fac-gas-standards-biblio]] [[skoog-fac-gas-standards-biblio]]. For ideal gases at matched \(T\) and \(P\), amount is proportional to volume [[ideal-gas-law-libretexts]], so the same algebra applies to a certified mother gas diluted with analyte-free diluent (zero air or high-purity nitrogen):

\[
c_f = c_m \times \frac{V_m}{V_f}
\]

Here \(c_m\) is the mother cylinder certificate value (for this project, typically \(1000\) ppm CH₄ in air), \(V_m\) is the volume of mother gas admitted to the bag, and \(V_f\) is the final bag volume after top-up. If \(V_f = 1000\,\mathrm{mL}\) and \(c_m = 1000\) ppm, then a \(50\,\mathrm{mL}\) mother slug targets \(50\) ppm when the diluent contributes zero methane.

### 2.2 Ambient-air diluent (air-pump protocol)

The locked eNose mixing design tops up bags with an air pump drawing room air. That diluent is not zero air. Global surface methane is on the order of two parts per million; a lab may be slightly higher. Let \(c_a\) be the ambient methane mole fraction in ppm and let \(V_a = V_f - V_m\). Conservation of methane amount then reads:

\[
c_f = \frac{c_m V_m + c_a V_a}{V_f} = \frac{c_m V_m + c_a (V_f - V_m)}{V_f}
\]

When \(c_a = 0\), the expression collapses to the textbook formula. When \(c_a \approx 2\) ppm, low targets such as \(5\)–\(15\) ppm are strongly biased if the experimenter still uses the zero-air equation. High targets such as \(50\)–\(100\) ppm move less in absolute terms, but the methods section should still name the procedure ambient air dilution rather than zero-air dilution.

### 2.3 Gas-metrology standards as the professional frame

ISO 6142 is the widely cited family of standards for preparation of calibration gas mixtures, historically centered on gravimetric preparation and related metrological controls [[iso-6142-page]] [[iso-6142-page]]. ISO 6145 covers dynamic volumetric methods in which metered flows prepare mixtures continuously or semi-continuously [[iso-6145-1-page]] [[iso-6145-1-page]]. A student protocol that opens a rotameter for a timed interval is conceptually closer to the volumetric spirit of ISO 6145 than to a full ISO 6142 gravimetric certificate [[iso-6145-1-page]]. That does not make a Tedlar bag an ISO-compliant calibrant. It does mean the thesis can honestly say the calculation follows the same conservation and flow-metering ideas that the standards formalize [[iso-6142-page]], while laboratory GC remains the project ground truth for labels. Textbook dilution algebra still supplies the transparent \(c_f\) formula used day to day [[harris-qa-dilution-biblio]] [[skoog-fac-gas-standards-biblio]].

---

## 3. Rotameter timing: V = Q × t

A rotameter indicates the volumetric flow rate \(Q\) of gas in the low-pressure line after the cylinder regulator. Dynamic volumetric calibration-gas practice is exactly the standards niche that meters such flows [[iso-6145-1-page]]. If the flow is approximately constant while a valve is open for duration \(t\), the admitted mother volume is

\[
V_m = Q \times t
\]

Unit consistency matters: with \(Q\) in mL/min and \(t\) in minutes, \(V_m\) is in mL; with \(t\) in seconds use \(t/60\). Substitute \(V_m\) into the dilution equation of Section 2.

For the common teaching choice \(Q = 100\,\mathrm{mL/min}\), \(V_f = 1000\,\mathrm{mL}\), \(c_m = 1000\) ppm, and provisional \(c_a = 0\),

\[
t\ [\mathrm{s}] \approx 0.6 \times c_{f,\text{target}}\ [\mathrm{ppm}]
\]

so a \(50\) ppm target opens for about \(30\) s and a \(100\) ppm target for about \(60\) s. Short openings for \(5\)–\(15\) ppm exaggerate human timing error; lowering \(Q\) (for example to \(50\,\mathrm{mL/min}\)) doubles \(t\) and usually improves repeatability.

Rotameters are gas- and condition-dependent. A scale calibrated for air at one pressure will mis-read if used casually on another gas or back-pressure. A cheap field check is to time how long the indicated \(Q\) takes to deliver a known volume into a marked bag or soap-bubble meter, then correct \(Q\) before building a full twelve-level series.

The project design places the rotameter only on the mother line. The air pump that finishes the bag does not need its own rotameter if the operator fills to a repeatable fraction of bag capacity (about \(75\)–\(80\) percent full). The mother volume is the quantity that sets concentration; the pump mainly sets \(V_f\).

---

## 4. Textbook and standards citations

| Source | What it contributes |
|--------|---------------------|
| [[harris-qa-dilution-biblio]] Harris, *Quantitative Chemical Analysis* | Dilution algebra \(c_f = c_i V_i/V_f\) for preparing standards |
| [[skoog-fac-gas-standards-biblio]] Skoog et al., *Fundamentals of Analytical Chemistry* | Calibration against known composition standards |
| [[ideal-gas-law-libretexts]] LibreTexts Ideal Gas Law | \(PV=nRT\); equal volumes at equal \(T,P\) imply equal moles |
| [[wikipedia-ideal-gas]] Ideal-gas overview | Mole fraction, Dalton partial pressures |
| [[iso-6142-page]] ISO 6142 | Preparation of calibration gas mixtures (metrology frame) |
| [[iso-6145-1-page]] ISO 6145-1 | Dynamic volumetric methods using metered flows |

Harris and Skoog are bibliographic vault notes in this light run (full textbook PDFs were not scraped). ISO entries are publisher landing pages confirming standard identity and scope; clause-level quotations require the library PDF. Together they are enough to defend the equations in a proposal methods paragraph: ideal-gas volume fractions, dilution conservation, and flow metering as the operational path to \(V_m\).

---

## 5. Error sources and GC verification

Concentration calculated from \(Q\), \(t\), and assumed \(c_a\) is a recipe concentration [[harris-qa-dilution-biblio]]. Several error channels separate that recipe from the true bag content. Ideal-gas assumptions themselves remain adequate at dilute CH₄ and ambient \(T,P\) [[ideal-gas-law-libretexts]] [[wikipedia-ideal-gas]], so the dominant errors are metrological and procedural rather than equation form.

Rotameter bias scales every \(V_m\). Timing jitter dominates when \(t\) is only a few seconds. Bag volume error (under-fill, over-stretch, residual dead volume in tubing) changes \(V_f\). Ambient methane and humidity vary by day and room. Flexible bags can lose or exchange methane over hours to days; Tedlar is convenient but not a long-term primary standard. The mother cylinder itself is trustworthy only while the certificate and valve integrity hold; cylinders are exchanged or refilled by the supplier, not by laboratory improvisation.

Because GC-FID access is limited in this project, the practical verification plan is anchor-based rather than exhaustive. After each large mixing batch, analyze bags at approximately \(5\), \(50\), and \(100\) ppm (and one mid random point if quota allows). Use the GC value as the regression label for those bags. For intermediate recipe levels without GC, either interpolate cautiously from nearby anchors after checking that residuals are smooth, or accept higher label noise and document it. Bags stored overnight should be re-checked before they enter the training set.

None of this replaces metrological accreditation. The eNose output remains a machine-learning estimate under the trained envelope, complementary to chamber–GC workflows described in the thesis proposal.

---

## 6. Worked example for the eNose bag protocol

**Givens.** Mother certificate \(c_m = 1000\) ppm CH₄ in air. Final bag volume \(V_f = 1000\) mL. Rotameter set to \(Q = 100\) mL/min. Desired nominal level near \(50\) ppm.

**Step A — zero-air target recipe.**  
Apply the textbook dilution factor [[harris-qa-dilution-biblio]] [[skoog-fac-gas-standards-biblio]]:  
\(V_m = 1000 \times 50/1000 = 50\) mL.  
\(t = 50/100 = 0.5\) min \(= 30\) s (flow metering in the spirit of [[iso-6145-1-page]]).  
Open the mother valve path for \(30\) s, close, then top up with the air pump to about \(80\) percent of bag capacity, knead, and label.

**Step B — ambient correction with \(c_a = 2\) ppm.**  
Solve \(50 = (1000 V_m + 2(1000-V_m))/1000\).  
Approximately \(V_m \approx 48\) mL, so \(t \approx 29\) s.  
At \(50\) ppm the correction is small; repeat the algebra before trusting a \(5\) ppm recipe without GC.

**Step C — assign the training label.**  
Run GC-FID on an aliquot from the same bag (or a twin bag mixed identically). Store `bag_id`, recipe metadata (\(Q\), \(t\), \(c_a\) assumption), and \(c_{\mathrm{GC}}\). Train the eNose feature vector against \(c_{\mathrm{GC}}\) at anchors; do not train against the recipe number alone when GC is available.

**Step D — scale to other targets.**  
For a provisional zero-air table at the same \(Q\): \(5\) ppm → \(3\) s; \(10\) ppm → \(6\) s; \(100\) ppm → \(60\) s. Prefer longer times via lower \(Q\) at the bottom of the range. Rebuild the table with Section 2.2 if ambient methane is measured in the room that day.

**Thai operator checklist.**  
(1) คำนวณ \(V_m\) จากสูตร Section 2  
(2) แปลงเป็นเวลา \(t = V_m/Q\)  
(3) ผสมตามสายถังแม่ → เรกูเลเตอร์ → rotameter → ถุง แล้วเติมด้วย air pump  
(4) ติดป้ายเป้าหมาย  
(5) ส่งจุดสมอเข้า GC แล้วใช้ค่า GC เป็นคำตอบจริงของโมเดล

---

## Closing recommendation

Use the ideal-gas volume-fraction basis [[ideal-gas-law-libretexts]] [[wikipedia-ideal-gas]], the conservation dilution equation [[harris-qa-dilution-biblio]] [[skoog-fac-gas-standards-biblio]], and \(V_m = Q t\) as the transparent calculation chain aligned with volumetric metrology language [[iso-6145-1-page]] [[iso-6142-page]]. Prefer the ambient-air form whenever an air pump supplies the diluent. Cite Harris or Skoog for dilution algebra, LibreTexts or equivalent for \(PV=nRT\), and ISO 6142 / 6145 for the professional vocabulary of calibration-gas preparation. For this eNose project, treat calculated ppm as the mixing target and GC-FID anchors as the supervised labels.
