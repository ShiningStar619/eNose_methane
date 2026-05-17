"""ML module paths and feature schema for methane regression."""
from pathlib import Path

ML_ROOT = Path(__file__).resolve().parent
DATA_DIR = ML_ROOT / "data"
MODELS_DIR = ML_ROOT / "models"

DEFAULT_LABELS_PATH = DATA_DIR / "labels.csv"
DEFAULT_MODEL_PATH = MODELS_DIR / "methane_regressor_v1.joblib"
FEATURE_NAMES_PATH = MODELS_DIR / "feature_names.json"
METRICS_PATH = MODELS_DIR / "metrics.json"

# v1 feature vector (fixed column order for train + predict)
FEATURE_NAMES = [
    "delta_ss1",
    "delta_ss2",
    "delta_ss3",
    "delta_ss4",
    "ss1_measure_mean",
    "ss1_measure_std",
    "ss1_measure_max",
    "ss2_measure_mean",
    "ss2_measure_std",
    "ss2_measure_max",
    "ss3_measure_mean",
    "ss3_measure_std",
    "ss3_measure_max",
    "ss4_measure_mean",
    "ss4_measure_std",
    "ss4_measure_max",
    "temp_measure_mean",
    "humidity_measure_mean",
    "pressure_measure_mean",
]

ADC_SENSOR_COLUMNS = [f"ss{i}_lp_ma" for i in range(1, 5)]
BME_SENSOR_COLUMNS = [
    "temperature_c_lp_ma",
    "humidity_pct_lp_ma",
    "pressure_hpa_lp_ma",
]
BME_FEATURE_KEYS = [
    "temp_measure_mean",
    "humidity_measure_mean",
    "pressure_measure_mean",
]

MIN_TRAIN_SAMPLES_WARN = 20
CLIP_NEGATIVE_PREDICTIONS = True

# Keys used to slice Auto Mode timeline (collection starts at Op2 baseline, t=0)
PHASE_DURATION_KEYS = (
    "baseline",
    "vacuum",
    "mix_air",
    "measure",
    "vacuum_return",
    "recovery",
)
