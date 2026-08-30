# Othman et al. (2026) — structured extract
# DOI: 10.37934/araset.60.5.3350
# PDF: docs/literature-review-4.2/pdf/2026_Othman_SVM_eNose_methane_paddy_ecosystems.pdf
# Ingest: 2026-08-20 (added after idea-evaluator novelty search; not in original 39-paper 4.2 sweep)

TITLE
A Robust Support Vector Machine Model for Monitoring Methane Emission Levels in Paddy Ecosystems using Electronic Nose Technology

AUTHORS
Mohd Muzamir Othman; Muhamad Khairul Ali Hassan; Sukhairi Sudin; Fathinul Syahir Ahmad Saad; Khairul Salleh Basaruddin; Muhammad Juhairi Aziz Safar; Shafriza Nisha Basah; Haniza Yazid; Mohd Hanafi Mat Som
(Universiti Malaysia Perlis)

JOURNAL
Journal of Advanced Research in Applied Sciences and Engineering Technology, Vol. 60, Issue 5 (2026), pp. 33–50
ISSN 2462-1943

ABSTRACT (summary — do not re-quote performance numbers in thesis without re-checking PDF tables)
Field E-Nose + SVM for carbon emission monitoring in tropical paddy. Dataset from three field locations (inlet / mid / outlet) with CH4 and CO2 concentrations, temperature, humidity, growth stage. Pre-processing: median imputation, IQR outlier removal, SelectKBest. SVM-RBF with All Features vs Selected Features.

HARDWARE / PROTOCOL (from Methods)
- MOS: TGS-2611 (CH4), MG-811 (CO2); ESP32; SD logger; weather enclosure
- Linked to static chamber over paddy (0.5 × 0.5 × 1.0 m); seal ~30 min; E-Nose at 1-min intervals
- DHT22 inside chamber and ambient
- Diurnal sessions: morning / afternoon / evening
- Stated ground truth: gas flux from concentration accumulation slope over the chamber window (E-Nose-derived), not GC-FID

FEATURES / TARGET (from Methods + Results text)
- Inputs include: CH4 ppm, CO2 ppm, ambient/chamber T and RH, location, diurnal session, growth stage; fluxes also appear among ranked drivers
- SelectKBest (f_regression) ranks growth stage, CH4 ppm, CO2 ppm (and fluxes / temperature in Results narrative) highest
- Target: “carbon emission” scaled to grams (SVM regression / monitoring of emission levels)

WHAT THIS PAPER IS (for gap positioning)
- Touches **นา + E-Nose/MOS + ML** in one system (tropical Malaysia field)
- Closest published competitor to the three-pillar “empty intersection” claim

WHAT THIS PAPER IS NOT (axes that still differentiate our work — verify before overclaiming)
- Not GC-FID (or other lab analyser) calibration of MOS → absolute ppm
- Not Baseline–Measure ΔV / waveform feature protocol on multi-channel ADS1263 Pi stack
- Target appears to be emission/flux-level prediction from already-derived concentration-style features + env, not the same claim as “eNose ΔV → ppm vs GC”
- Feature set that includes CH4/CO2 concentration (and flux) as predictors of carbon output needs careful reading; do not treat reported R² as SOTA on the same task as our thesis

USE IN §4.2.5
- Promote from “three empty pillars” to “four-way contrast”: Rajasekar (MOS+นา, weak ML→ppm); Domènech-Gil (eNose+ML, not rice); Zhang 2025 (ML+นา, not MOS); **Othman 2026 (E-Nose+ML+นา, field flux framing, no GC ppm calibration as stated)**
