"""Unit tests for methane ML feature extraction and prediction."""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from sklearn.cross_decomposition import PLSRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml.config import FEATURE_NAMES
from ml.features import build_phase_windows, extract_features, features_to_vector
from ml.predict import clear_model_cache, predict_cycle

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_OP_TIMES = {
    "baseline": 10.0,
    "vacuum": 10.0,
    "mix_air": 10.0,
    "measure": 20.0,
    "vacuum_return": 10.0,
    "recovery": 10.0,
}


def _write_synthetic_csvs(tmp: Path, ss_base: float, ss_meas: float) -> tuple[Path, Path]:
    """Build ADC/BME CSV long enough for baseline (0-10s) + measure (30-50s) windows."""
    duration_sec = 70.0
    dt = 0.01
    times = np.arange(0.0, duration_sec, dt)
    measure_start = 30.0
    in_baseline = times < 10.0
    in_measure = (times >= measure_start) & (times < measure_start + 20.0)
    adc_rows = {
        "elapsed_time_sec": times,
        "ss1_lp_ma": np.where(in_baseline, ss_base, np.where(in_measure, ss_meas, ss_base)),
        "ss2_lp_ma": np.where(in_baseline, ss_base + 0.1, np.where(in_measure, ss_meas + 0.1, ss_base + 0.1)),
        "ss3_lp_ma": np.where(in_baseline, ss_base + 0.2, np.where(in_measure, ss_meas + 0.2, ss_base + 0.2)),
        "ss4_lp_ma": np.where(in_baseline, ss_base + 0.3, np.where(in_measure, ss_meas + 0.3, ss_base + 0.3)),
    }
    adc_path = tmp / "adc.csv"
    pd.DataFrame(adc_rows).to_csv(adc_path, index=False)

    bme_times = np.arange(0.0, duration_sec, 0.1)
    bme_rows = {
        "elapsed_time_sec": bme_times,
        "temperature_c_lp_ma": 25.0,
        "humidity_pct_lp_ma": 50.0,
        "pressure_hpa_lp_ma": 1013.0,
    }
    bme_path = tmp / "bme.csv"
    pd.DataFrame(bme_rows).to_csv(bme_path, index=False)
    return adc_path, bme_path


class TestPhaseWindows(unittest.TestCase):
    def test_build_phase_windows_starts_at_zero(self):
        windows = build_phase_windows(DEFAULT_OP_TIMES)
        self.assertEqual(windows["baseline"], (0.0, 10.0))
        self.assertEqual(windows["measure"], (30.0, 50.0))


class TestFeatureExtraction(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_extract_features_vector_length(self):
        adc, bme = _write_synthetic_csvs(self.tmp, ss_base=2.0, ss_meas=3.0)
        feats = extract_features(adc, bme, DEFAULT_OP_TIMES)
        self.assertIsNotNone(feats)
        vec = features_to_vector(feats)
        self.assertEqual(vec.shape, (len(FEATURE_NAMES),))
        self.assertGreater(feats["delta_ss1"], 0.0)

    def test_extract_features_missing_file_returns_none(self):
        adc, bme = _write_synthetic_csvs(self.tmp, 2.0, 3.0)
        result = extract_features(adc, self.tmp / "missing.csv", DEFAULT_OP_TIMES)
        self.assertIsNone(result)


class TestPredictCycle(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        clear_model_cache()

    def tearDown(self):
        clear_model_cache()
        self._tmp.cleanup()

    def test_predict_cycle_with_toy_model(self):
        adc, bme = _write_synthetic_csvs(self.tmp, ss_base=1.0, ss_meas=2.0)
        feats = extract_features(adc, bme, DEFAULT_OP_TIMES)
        self.assertIsNotNone(feats)

        X_train = []
        y_train = []
        for meas, ppm in ((2.0, 10.0), (3.0, 50.0), (4.0, 90.0)):
            a, b = _write_synthetic_csvs(self.tmp, ss_base=1.0, ss_meas=meas)
            f = extract_features(a, b, DEFAULT_OP_TIMES)
            X_train.append(features_to_vector(f))
            y_train.append(ppm)

        pipe = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("regressor", PLSRegression(n_components=2)),
            ]
        )
        pipe.fit(np.vstack(X_train), np.array(y_train))
        model_path = self.tmp / "model.joblib"
        joblib.dump(pipe, model_path)

        ppm = predict_cycle(adc, bme, DEFAULT_OP_TIMES, model_path=model_path)
        self.assertIsNotNone(ppm)
        self.assertGreater(ppm, 0.0)


if __name__ == "__main__":
    unittest.main()
