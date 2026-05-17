"""Train methane PPM regression model from labeled cycles."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np
from sklearn.cross_decomposition import PLSRegression
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml.config import (
    DEFAULT_LABELS_PATH,
    DEFAULT_MODEL_PATH,
    FEATURE_NAMES,
    FEATURE_NAMES_PATH,
    METRICS_PATH,
    MIN_TRAIN_SAMPLES_WARN,
    MODELS_DIR,
)
from ml.dataset import build_dataset

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _make_pipeline(model_type: str = "pls") -> Pipeline:
    if model_type == "ridge":
        regressor = Ridge(alpha=1.0)
    else:
        regressor = PLSRegression(n_components=3)
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", regressor),
        ]
    )


def _param_grid(model_type: str, n_samples: int, n_features: int) -> dict:
    max_comp = min(n_samples - 1, n_features, 10)
    max_comp = max(1, max_comp)
    if model_type == "ridge":
        return {"regressor__alpha": [0.1, 1.0, 10.0]}
    components = [c for c in (2, 3, 4, 5) if c <= max_comp]
    if not components:
        components = [1]
    return {"regressor__n_components": components}


def train_model(
    labels_path: Path | None = None,
    model_path: Path | None = None,
    model_type: str = "pls",
    n_splits: int = 5,
) -> dict:
    labels_path = labels_path or DEFAULT_LABELS_PATH
    model_path = model_path or DEFAULT_MODEL_PATH
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    X, y, groups, run_ids = build_dataset(labels_path=labels_path, project_root=PROJECT_ROOT)
    n_samples = X.shape[0]

    if n_samples < MIN_TRAIN_SAMPLES_WARN:
        print(
            f"[WARN] ML train: only {n_samples} samples "
            f"(recommended >= {MIN_TRAIN_SAMPLES_WARN})"
        )

    n_unique_groups = len(np.unique(groups))
    cv_splits = min(n_splits, n_unique_groups)
    if cv_splits < 2:
        print("[WARN] ML train: fewer than 2 sessions — using 2-fold CV without groups")
        cv = 2
        groups_cv = None
    else:
        cv = GroupKFold(n_splits=cv_splits)
        groups_cv = groups

    pipeline = _make_pipeline(model_type)
    grid = GridSearchCV(
        pipeline,
        param_grid=_param_grid(model_type, n_samples, X.shape[1]),
        cv=cv,
        scoring="neg_mean_absolute_error",
        n_jobs=None,
    )
    grid.fit(X, y, groups=groups_cv)
    best: Pipeline = grid.best_estimator_

    y_pred_cv = cross_val_predict(best, X, y, cv=cv, groups=groups_cv)
    mae = float(mean_absolute_error(y, y_pred_cv))
    rmse = float(np.sqrt(mean_squared_error(y, y_pred_cv)))
    r2 = float(r2_score(y, y_pred_cv))

    joblib.dump(best, model_path)

    feature_meta = {"feature_names": FEATURE_NAMES, "model_type": model_type}
    FEATURE_NAMES_PATH.write_text(json.dumps(feature_meta, indent=2), encoding="utf-8")

    metrics = {
        "n_samples": n_samples,
        "n_features": int(X.shape[1]),
        "cv_mae_ppm": mae,
        "cv_rmse_ppm": rmse,
        "cv_r2": r2,
        "best_params": grid.best_params_,
        "run_ids": run_ids,
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"[OK] ML train: saved model -> {model_path}")
    print(f"[OK] ML train: CV MAE={mae:.3f} ppm RMSE={rmse:.3f} R2={r2:.3f}")
    return metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Train methane regression model")
    parser.add_argument(
        "--labels",
        type=Path,
        default=DEFAULT_LABELS_PATH,
        help="Path to labels.csv",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Output joblib path",
    )
    parser.add_argument(
        "--type",
        choices=("pls", "ridge"),
        default="pls",
        dest="model_type",
    )
    args = parser.parse_args(argv)

    try:
        train_model(
            labels_path=args.labels,
            model_path=args.model,
            model_type=args.model_type,
        )
        return 0
    except Exception as exc:
        print(f"[ERROR] ML train failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
