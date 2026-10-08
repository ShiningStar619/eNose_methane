# AGENTS

## Cursor Cloud specific instructions

This repo is the **eNose Methane Detection System** — a Raspberry Pi hardware app: a Tkinter GUI
(`program/gui.py`) that drives GPIO relays, reads gas/environment sensors (ADS1263 via SPI, BME280
via I2C), processes signals to CSV, and predicts methane ppm with a committed scikit-learn model
(`models/methane_linreg_model.joblib`). There is **no server, no database, and no network ports**.
See `README.md` for the product overview and standard commands.

### Environment on the cloud VM (x86, no hardware)

- The cloud VM is x86 with **no Raspberry Pi hardware**. The code degrades gracefully:
  `hardware_control/hardware.py` sets `ON_RASPBERRY_PI = False` (relay control runs in
  **simulation mode**) and `reading/main.py` disables ADC collection. This is expected — the GUI,
  signal processing, prediction, and cloud-queue logic all still run.
- The update script creates `.venv` and installs only the **x86-compatible** deps
  (numpy/pandas/matplotlib + google libs + scikit-learn/joblib). The Pi-only hardware deps
  (`RPi.GPIO`, `spidev`, `adafruit-*`) from `requirements-pi-core.txt` are intentionally **not**
  installed; they don't build/import on x86 and aren't needed for dev.
- `scikit-learn` is pinned to **1.6.1** to match the committed model bundle. Other versions load the
  model with an `InconsistentVersionWarning` and may give invalid predictions — keep it pinned.
- System packages `python3-tk` and `python3.12-venv` are already installed on the VM image (needed
  for the Tkinter GUI and venv). They are not in the update script.
- `reading/bme280.py` fails to import on x86 (`cannot import name 'WriteableBuffer'`); this is
  expected (BME needs the Pi's I2C hardware + adafruit libs) and is non-blocking — the GUI sets
  `BME_COLLECTION_AVAILABLE=False` and continues.

### Running things (use the venv)

- Activate implicitly via `.venv/bin/python`.
- Tests: `.venv/bin/python -m unittest discover -s tests` (8 tests; the gdrive smoke test is
  skipped unless `ENOSE_GDRIVE_SERVICE_ACCOUNT_JSON` and `ENOSE_GDRIVE_FOLDER_ID` are set).
- Lint / build: none configured (pure Python, no compile/bundle step).
- GUI (main product): a desktop is available on **`DISPLAY=:1`**. Run
  `DISPLAY=:1 .venv/bin/python program/gui.py`. It has no headless mode.
- Prediction: `predict_methane.predict_ppm(adc_csv, bme_csv)` needs *processed* CSVs — `adc1263_*`
  with `elapsed_time_sec` + `ss3_lp_ma`/`ss4_lp_ma`, and `bme280_*` with `temperature_c_lp_ma`. Real
  CSVs come from hardware acquisition (none are committed; `reading/data` and
  `acquisition/processed_data` are gitignored).
