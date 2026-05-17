"""Run methane regression inference for one processed cycle."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.pipeline import Pipeline

from ml.config import (
    CLIP_NEGATIVE_PREDICTIONS,
    DEFAULT_MODEL_PATH,
    FEATURE_NAMES,
)
from ml.features import extract_features, features_to_vector

_cached_model: Pipeline | None = None
_cached_model_path: Path | None = None


def _load_model(model_path: Path | None) -> Pipeline | None:
    global _cached_model, _cached_model_path
    path = Path(model_path) if model_path else DEFAULT_MODEL_PATH
    if _cached_model is not None and _cached_model_path == path:
        return _cached_model
    if not path.is_file():
        print(f"[WARN] ML predict: model not found at {path}")
        return None
    try:
        model = joblib.load(path)
    except Exception as exc:
        print(f"[WARN] ML predict: could not load model: {exc}")
        return None
    _cached_model = model
    _cached_model_path = path
    return model


def clear_model_cache() -> None:
    """Reset cached estimator (for tests)."""
    global _cached_model, _cached_model_path
    _cached_model = None
    _cached_model_path = None


def predict_cycle(
    adc_csv: Path | str,
    bme_csv: Path | str,
    operation_times: dict[str, float],
    model_path: Path | None = None,
) -> float | None:
    """Predict methane ppm for one Auto Mode cycle.

    Returns None if model or features are unavailable.
    """
    model = _load_model(model_path)
    if model is None:
        return None

    features = extract_features(adc_csv, bme_csv, operation_times)
    if features is None:
        return None

    missing = [name for name in FEATURE_NAMES if name not in features]
    if missing:
        print(f"[WARN] ML predict: missing features: {missing[:3]}...")
        return None

    X = features_to_vector(features).reshape(1, -1)
    try:
        pred = float(model.predict(X)[0])
    except Exception as exc:
        print(f"[WARN] ML predict: inference failed: {exc}")
        return None

    if CLIP_NEGATIVE_PREDICTIONS and pred < 0:
        pred = 0.0

    print(f"[ml] predicted ppm={pred:.1f}")
    return pred
