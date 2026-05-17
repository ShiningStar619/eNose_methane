"""Extract per-cycle feature vectors from processed ADC/BME CSV files."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ml.config import (
    ADC_SENSOR_COLUMNS,
    BME_FEATURE_KEYS,
    BME_SENSOR_COLUMNS,
    FEATURE_NAMES,
    PHASE_DURATION_KEYS,
)

# Op2 baseline = elapsed_time 0; heating (Op1) is not in the recording timeline.
_PHASES_AFTER_BASELINE_START = ("baseline", "vacuum", "mix_air", "measure", "vacuum_return", "recovery")


def build_phase_windows(operation_times: dict[str, float]) -> dict[str, tuple[float, float]]:
    """Build [start, end) second windows for each Auto Mode phase after collection starts.

    Parameters
    ----------
    operation_times
        Durations in seconds (heating is ignored — recording begins at Op2).
    """
    t = 0.0
    windows: dict[str, tuple[float, float]] = {}
    for key in _PHASES_AFTER_BASELINE_START:
        duration = float(operation_times.get(key, 0.0))
        if duration < 0:
            duration = 0.0
        windows[key] = (t, t + duration)
        t += duration
    return windows


def _slice_phase(df: pd.DataFrame, start: float, end: float) -> pd.DataFrame:
    if df.empty or end <= start:
        return df.iloc[0:0]
    time_col = "elapsed_time_sec"
    if time_col not in df.columns:
        return df.iloc[0:0]
    mask = (df[time_col] >= start) & (df[time_col] < end)
    return df.loc[mask]


def _phase_mean(df: pd.DataFrame, column: str) -> float | None:
    if column not in df.columns or df.empty:
        return None
    values = df[column].astype(np.float64)
    if values.empty or values.isna().all():
        return None
    return float(values.mean())


def _phase_std(df: pd.DataFrame, column: str) -> float | None:
    if column not in df.columns or df.empty:
        return None
    values = df[column].astype(np.float64)
    if values.empty or values.isna().all():
        return None
    std = float(values.std())
    return 0.0 if np.isnan(std) else std


def _phase_max(df: pd.DataFrame, column: str) -> float | None:
    if column not in df.columns or df.empty:
        return None
    values = df[column].astype(np.float64)
    if values.empty or values.isna().all():
        return None
    return float(values.max())


def extract_features(
    adc_csv: Path | str,
    bme_csv: Path | str,
    operation_times: dict[str, float],
) -> dict[str, float] | None:
    """Extract one feature dict for a single measurement cycle.

    Returns None if files are missing or required phases have no samples.
    """
    adc_path = Path(adc_csv)
    bme_path = Path(bme_csv)
    if not adc_path.is_file() or not bme_path.is_file():
        print(f"[WARN] ML features: missing CSV adc={adc_path.is_file()} bme={bme_path.is_file()}")
        return None

    try:
        adc_df = pd.read_csv(adc_path)
        bme_df = pd.read_csv(bme_path)
    except Exception as exc:
        print(f"[WARN] ML features: could not read CSV: {exc}")
        return None

    windows = build_phase_windows(operation_times)
    baseline_win = windows.get("baseline")
    measure_win = windows.get("measure")
    if baseline_win is None or measure_win is None:
        print("[WARN] ML features: missing baseline/measure windows")
        return None

    baseline_df = _slice_phase(adc_df, baseline_win[0], baseline_win[1])
    measure_df = _slice_phase(adc_df, measure_win[0], measure_win[1])
    bme_measure_df = _slice_phase(bme_df, measure_win[0], measure_win[1])

    if baseline_df.empty or measure_df.empty:
        print(
            "[WARN] ML features: empty phase slice "
            f"(baseline rows={len(baseline_df)}, measure rows={len(measure_df)})"
        )
        return None

    features: dict[str, float] = {}

    for i, col in enumerate(ADC_SENSOR_COLUMNS, start=1):
        b_mean = _phase_mean(baseline_df, col)
        m_mean = _phase_mean(measure_df, col)
        m_std = _phase_std(measure_df, col)
        m_max = _phase_max(measure_df, col)
        if b_mean is None or m_mean is None or m_std is None or m_max is None:
            print(f"[WARN] ML features: incomplete ADC stats for {col}")
            return None
        features[f"delta_ss{i}"] = m_mean - b_mean
        features[f"ss{i}_measure_mean"] = m_mean
        features[f"ss{i}_measure_std"] = m_std
        features[f"ss{i}_measure_max"] = m_max

    for col, key in zip(BME_SENSOR_COLUMNS, BME_FEATURE_KEYS):
        val = _phase_mean(bme_measure_df, col)
        if val is None:
            print(f"[WARN] ML features: incomplete BME stats for {col}")
            return None
        features[key] = val

    return features


def features_to_vector(features: dict[str, float]) -> np.ndarray:
    """Order feature dict into a 1-D float64 vector matching FEATURE_NAMES."""
    return np.array([float(features[name]) for name in FEATURE_NAMES], dtype=np.float64)


def default_operation_times() -> dict[str, float]:
    """Fallback durations matching program/hardware_config.json defaults."""
    return {key: 10.0 for key in PHASE_DURATION_KEYS} | {"measure": 20.0}
