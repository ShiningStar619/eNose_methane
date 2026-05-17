"""Load labeled cycles from ml/data/labels.csv into feature matrices."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from ml.config import DEFAULT_LABELS_PATH, FEATURE_NAMES
from ml.features import default_operation_times, extract_features, features_to_vector

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _resolve_path(path_str: str, base: Path | None = None) -> Path:
    path = Path(path_str)
    if path.is_absolute():
        return path
    root = base or PROJECT_ROOT
    return (root / path).resolve()


def load_labels_table(labels_path: Path | str | None = None) -> pd.DataFrame:
    path = Path(labels_path) if labels_path else DEFAULT_LABELS_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Labels file not found: {path}")
    return pd.read_csv(path)


def _parse_operation_times(row: pd.Series) -> dict[str, float]:
    raw = row.get("operation_times_json")
    if pd.isna(raw) or raw == "":
        return default_operation_times()
    try:
        data = json.loads(str(raw))
        return {k: float(v) for k, v in data.items()}
    except (json.JSONDecodeError, TypeError, ValueError):
        print(f"[WARN] ML dataset: invalid operation_times_json for run_id={row.get('run_id')}")
        return default_operation_times()


def build_dataset(
    labels_path: Path | str | None = None,
    split: str | None = None,
    project_root: Path | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Build X, y, groups, and run_ids from labels.csv.

    Parameters
    ----------
    split
        If set, keep only rows where ``split`` column matches (e.g. ``train``).
    project_root
        Base directory for relative adc_csv / bme_csv paths.

    Returns
    -------
    X, y, groups, run_ids
        groups holds session_id strings for GroupKFold.
    """
    root = project_root or PROJECT_ROOT
    df = load_labels_table(labels_path)

    required = {"run_id", "methane_ppm_ref", "adc_csv", "bme_csv"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"labels.csv missing columns: {sorted(missing)}")

    if split is not None and "split" in df.columns:
        df = df[df["split"].astype(str).str.lower() == split.lower()]

    X_rows: list[np.ndarray] = []
    y_list: list[float] = []
    groups: list[str] = []
    run_ids: list[str] = []

    for _, row in df.iterrows():
        op_times = _parse_operation_times(row)
        adc_csv = _resolve_path(str(row["adc_csv"]), root)
        bme_csv = _resolve_path(str(row["bme_csv"]), root)
        feats = extract_features(adc_csv, bme_csv, op_times)
        if feats is None:
            print(f"[WARN] ML dataset: skipping run_id={row['run_id']} (feature extraction failed)")
            continue

        X_rows.append(features_to_vector(feats))
        y_list.append(float(row["methane_ppm_ref"]))
        session = row.get("session_id")
        if pd.isna(session) or session == "":
            session = str(row["run_id"])[:8]
        groups.append(str(session))
        run_ids.append(str(row["run_id"]))

    if not X_rows:
        raise ValueError("No valid samples after feature extraction")

    X = np.vstack(X_rows)
    y = np.array(y_list, dtype=np.float64)
    return X, y, np.array(groups), run_ids
