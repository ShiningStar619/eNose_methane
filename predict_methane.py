"""
predict_methane.py
==================
โหลดโมเดล Linear Regression จาก models/methane_linreg_model.joblib
แล้วทำนาย ppm จาก processed CSV (adc1263 + bme280)

ใช้ analysis_windows และ feature list ที่บันทึกไว้ใน model bundle
เพื่อให้ตรงกับที่ train ไว้เสมอ
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd

MODEL_PATH = Path(__file__).parent / "models" / "methane_linreg_model.joblib"
METRICS_PATH = Path(__file__).parent / "models" / "methane_linreg_metrics.json"
DEFAULT_BATCH_DIR = "BuildML_PC\build_dataset\testdata"
_bundle = None
_pipe = None
_selected_features: list[str] = []
_analysis_windows: dict = {}
_include_temp_set: bool = False


def _load_bundle():
    """โหลดโมเดลครั้งเดียว (lazy load)."""
    global _bundle, _pipe, _selected_features, _analysis_windows, _include_temp_set
    if _bundle is not None:
        return True
    try:
        import joblib
        _bundle = joblib.load(MODEL_PATH)
        _pipe = _bundle["pipeline"]
        _selected_features = _bundle["selected_features"]
        _analysis_windows = _bundle.get("analysis_windows", {
            "baseline": (250, 300),
            "measure": (305, 365),
        })
        _include_temp_set = _bundle.get("include_temp_set", False)
        print(f"[predict] โหลดโมเดลสำเร็จ — features: {_selected_features}")
        return True
    except Exception as e:
        print(f"[predict] โหลดโมเดลไม่สำเร็จ: {e}")
        return False


def _slice_window(df: pd.DataFrame, lo: float, hi: float) -> pd.DataFrame:
    t = df["elapsed_time_sec"]
    return df.loc[(t >= lo) & (t <= hi)]


def _nanmean(series: pd.Series) -> float:
    vals = series.dropna()
    return float(vals.mean()) if len(vals) > 0 else np.nan


def _extract_features(
    adc_csv: str | Path,
    bme_csv: Optional[str | Path],
    temp_set: Optional[float],
    windows: dict,
) -> dict[str, float]:
    """Extract ΔV / slope / BME features จาก processed CSV."""
    sensors = ["ss1", "ss2", "ss3", "ss4"]
    dv_max_sensors = {"ss3", "ss4"}
    adc_df = pd.read_csv(adc_csv)

    bl_lo, bl_hi = windows["baseline"]
    ms_lo, ms_hi = windows["measure"]
    bl = _slice_window(adc_df, bl_lo, bl_hi)
    ms = _slice_window(adc_df, ms_lo, ms_hi)

    features: dict[str, float] = {}

    for s in sensors:
        col = f"{s}_lp_ma"
        bl_avg = _nanmean(bl[col]) if col in bl.columns else np.nan
        if col not in ms.columns or not np.isfinite(bl_avg):
            features[f"dV_{s}"] = np.nan
            features[f"dVmax_{s}"] = np.nan
            features[f"ratio_{s}"] = np.nan
            features[f"hybrid_{s}"] = np.nan
            features[f"slope_{s}"] = np.nan
            continue

        ms_vals = ms[col].dropna()
        if ms_vals.empty:
            features[f"dV_{s}"] = np.nan
            features[f"dVmax_{s}"] = np.nan
            features[f"ratio_{s}"] = np.nan
            features[f"hybrid_{s}"] = np.nan
            features[f"slope_{s}"] = np.nan
            continue

        v_min = float(ms_vals.min())
        v_max = float(ms_vals.max())
        dv_max = v_max - bl_avg
        if s in dv_max_sensors:
            features[f"dV_{s}"] = dv_max
        else:
            features[f"dV_{s}"] = v_min - bl_avg
        features[f"dVmax_{s}"] = dv_max
        if bl_avg != 0:
            features[f"ratio_{s}"] = dv_max / bl_avg
            features[f"hybrid_{s}"] = (dv_max - bl_avg) / bl_avg
        else:
            features[f"ratio_{s}"] = np.nan
            features[f"hybrid_{s}"] = np.nan

        sub = ms[["elapsed_time_sec", col]].dropna()
        if len(sub) < 2:
            features[f"slope_{s}"] = np.nan
        else:
            idx_min, idx_max = sub[col].idxmin(), sub[col].idxmax()
            t_min = sub.loc[idx_min, "elapsed_time_sec"]
            t_max = sub.loc[idx_max, "elapsed_time_sec"]
            v_min = sub.loc[idx_min, col]
            v_max = sub.loc[idx_max, col]
            features[f"slope_{s}"] = float((v_max - v_min) / (t_max - t_min)) if t_max != t_min else np.nan

    # BME
    if bme_csv and Path(bme_csv).exists():
        bme_df = pd.read_csv(bme_csv)
        bl_bme = _slice_window(bme_df, bl_lo, bl_hi)
        ms_bme = _slice_window(bme_df, ms_lo, ms_hi)
        features["T_baseline"] = _nanmean(bl_bme["temperature_c_lp_ma"]) if "temperature_c_lp_ma" in bl_bme.columns else np.nan
        features["Humid_baseline"] = _nanmean(bl_bme["humidity_pct_lp_ma"]) if "humidity_pct_lp_ma" in bl_bme.columns else np.nan
        features["T_measure"] = _nanmean(ms_bme["temperature_c_lp_ma"]) if "temperature_c_lp_ma" in ms_bme.columns else np.nan
        features["Humid_measure"] = _nanmean(ms_bme["humidity_pct_lp_ma"]) if "humidity_pct_lp_ma" in ms_bme.columns else np.nan
        features["pressure_mean"] = _nanmean(ms_bme["pressure_hpa_lp_ma"]) if "pressure_hpa_lp_ma" in ms_bme.columns else np.nan
    else:
        for k in ("T_baseline", "Humid_baseline", "T_measure", "Humid_measure", "pressure_mean"):
            features[k] = np.nan

    if temp_set is not None:
        features["temp_set"] = float(temp_set)

    return features


def predict_ppm(
    adc_csv: str | Path,
    bme_csv: Optional[str | Path] = None,
    temp_set: Optional[float] = None,
    *,
    verbose: bool = True,
) -> Optional[float]:
    """ทำนาย methane ppm จาก processed CSV ที่ผ่าน filter แล้ว.

    Parameters
    ----------
    adc_csv : str | Path
        path ไฟล์ adc1263_*_lp_ma.csv (มีคอลัมน์ ss1_lp_ma..ss4_lp_ma)
    bme_csv : str | Path, optional
        path ไฟล์ bme280_*_lp_ma.csv
    temp_set : float, optional
        อุณหภูมิห้องทดลอง °C (30/40/50) — ต้องระบุถ้าโมเดล include temp_set
        ถ้าโมเดล train ด้วย INCLUDE_TEMP_SET=False ไม่ต้องส่งค่านี้

    Returns
    -------
    float หรือ None ถ้าโหลดโมเดล/extract ไม่สำเร็จ หรือ feature ที่โมเดลต้องใช้มี NaN
    """
    if not _load_bundle():
        return None

    try:
        features = _extract_features(adc_csv, bme_csv, temp_set, _analysis_windows)
        feat_row = {k: features.get(k, np.nan) for k in _selected_features}

        X = pd.DataFrame([feat_row])[_selected_features]
        missing = [c for c in _selected_features if not np.isfinite(X[c].iloc[0])]
        if missing:
            if verbose:
                print(f"[predict] ข้ามการทำนาย — feature ไม่ครบ: {missing}")
            return None

        ppm = float(_pipe.predict(X)[0])
        if verbose:
            print(f"[predict] ทำนาย: {ppm:.3f} ppm")
        return ppm
    except Exception as e:
        if verbose:
            print(f"[predict] error: {e}")
        return None


def _match_bme_for_adc(adc_path: Path, folder: Path) -> Optional[Path]:
    """จับคู่ bme280 ที่ timestamp ใกล้ adc ที่สุด (เหมือน notebook ทดสอบ)."""
    bme_files = sorted(folder.glob("bme280_*.csv"))
    if not bme_files:
        return None

    def _ts(p: Path) -> int:
        parts = p.stem.split("_")
        if len(parts) >= 2:
            try:
                return int(parts[-2] + parts[-1])
            except ValueError:
                pass
        return 0

    adc_ts = _ts(adc_path)
    return min(bme_files, key=lambda f: abs(_ts(f) - adc_ts))


def _latest_processed_pair(processed_dir: Path) -> tuple[Path, Optional[Path]]:
    adc_files = sorted(processed_dir.glob("adc1263_*.csv"))
    if not adc_files:
        raise FileNotFoundError(f"ไม่พบ adc1263_*.csv ใน {processed_dir}")
    adc_path = adc_files[-1]
    bme_path = _match_bme_for_adc(adc_path, processed_dir)
    return adc_path, bme_path


def parse_folder_meta(folder_name: str) -> dict[str, Any]:
    """แยก temp_set และ methane_ppm จากชื่อโฟลเดอร์.

    รูปแบบใหม่: 50_1ppm_28.5  → temp_set=50, methane_ppm=1.0
    รูปแบบ legacy: 5ppm       → temp_set=None, methane_ppm=5.0
    """
    name = folder_name.strip()

    # รูปแบบ: 50_1ppm_28.5 หรือ 30_1.5 ppm (มี/ไม่มีช่องว่างก่อน ppm)
    m = re.match(r"^(\d+)_(\d+(?:\.\d+)?)\s*ppm", name, re.IGNORECASE)
    if m:
        return {
            "temp_set": int(m.group(1)),
            "methane_ppm": float(m.group(2)),
        }

    m = re.match(r"^(\d+(?:\.\d+)?)ppm$", name, re.IGNORECASE)
    if m:
        return {
            "temp_set": None,
            "methane_ppm": float(m.group(1)),
        }

    raise ValueError(f"ไม่รู้จักรูปแบบชื่อโฟลเดอร์: {folder_name!r}")


def build_manifest(data_dir: str | Path) -> pd.DataFrame:
    """สแกนโฟลเดอร์ วนทุกไฟล์ adc → จับคู่ bme → สร้าง manifest ของทุก run."""
    data_dir = Path(data_dir)
    rows: list[dict[str, Any]] = []

    for folder in sorted(data_dir.iterdir()):
        if not folder.is_dir():
            continue
        try:
            meta = parse_folder_meta(folder.name)
        except ValueError as exc:
            print(f"[skip] {folder.name}: {exc}")
            continue

        adc_files = sorted(folder.glob("adc1263_*.csv"))
        bme_files = sorted(folder.glob("bme280_*.csv"))

        if not adc_files:
            print(f"[skip] {folder.name}: ไม่พบ adc1263_*.csv")
            continue

        for adc_file in adc_files:
            bme_file = _match_bme_for_adc(adc_file, folder)
            rows.append({
                "folder": folder.name,
                "folder_path": str(folder),
                "adc_csv": str(adc_file),
                "bme_csv": str(bme_file) if bme_file else None,
                "temp_set": meta["temp_set"],
                "methane_ppm": meta["methane_ppm"],
            })

    if not rows:
        raise FileNotFoundError(f"ไม่พบ run ใน {data_dir}")

    df = pd.DataFrame(rows)
    df = df.sort_values(["temp_set", "methane_ppm", "adc_csv"]).reset_index(drop=True)
    df["repeat"] = df.groupby(["temp_set", "methane_ppm"], dropna=False).cumcount() + 1
    df["group_id"] = (
        df["temp_set"].astype(str) + "_"
        + df["methane_ppm"].astype(str) + "_"
        + df["repeat"].astype(str)
    )
    return df


def _batch_summary_df(df: pd.DataFrame) -> pd.DataFrame:
    """สรุปผล batch เป็นคอลัมน์: ชื่อไฟล์, temp, actual_ppm, predict_ppm."""
    out = pd.DataFrame({
        "ชื่อไฟล์": df["adc_csv"].map(lambda p: Path(p).name),
        "temp": df["temp_set"],
        "actual_ppm": df["actual_ppm"],
        "predict_ppm": df["predicted_ppm"],
    })
    return out


def _save_batch_output(df: pd.DataFrame, output_path: str | Path) -> None:
    out = Path(output_path)
    summary = _batch_summary_df(df)
    if out.suffix.lower() in (".xlsx", ".xls"):
        summary.to_excel(out, index=False, sheet_name="predictions")
    else:
        summary.to_csv(out, index=False)
    print(f"\nบันทึกผล → {out}")


def _batch_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    err = predicted - actual
    ss_res = float(np.sum(err ** 2))
    ss_tot = float(np.sum((actual - actual.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return {
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(np.sqrt(np.mean(err ** 2))),
        "r2": r2,
    }


def load_model_metrics(metrics_path: str | Path | None = None) -> dict[str, Any] | None:
    """โหลด metrics จาก JSON (ใช้แสดงบริบท ไม่ใช้ในการทำนาย)."""
    path = Path(metrics_path) if metrics_path else METRICS_PATH
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def print_model_metrics(metrics_path: str | Path | None = None) -> None:
    """พิมพ์ metrics จาก train (CV / OOF) เพื่อเปรียบเทียบกับผล batch."""
    metrics = load_model_metrics(metrics_path)
    if metrics is None:
        print(f"[metrics] ไม่พบไฟล์ {metrics_path or METRICS_PATH}")
        return
    print("\n=== Model metrics (จาก train) ===")
    cv = metrics.get("cv", {})
    oof = metrics.get("oof", {})
    if cv:
        print(
            f"  CV:  RMSE={cv.get('rmse_mean', float('nan')):.4f} ± {cv.get('rmse_std', 0):.4f}"
            f"  MAE={cv.get('mae_mean', float('nan')):.4f}  R²={cv.get('r2_mean', float('nan')):.4f}"
        )
    if oof:
        print(
            f"  OOF: RMSE={oof.get('rmse', float('nan')):.4f}"
            f"  MAE={oof.get('mae', float('nan')):.4f}  R²={oof.get('r2', float('nan')):.4f}"
        )


def batch_predict(
    data_dir: str | Path,
    *,
    output_path: str | Path | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """ทำนาย ppm ทุก run ใน testdata แล้วเปรียบเทียบกับ methane_ppm จากชื่อโฟลเดอร์."""
    if not _load_bundle():
        raise RuntimeError("โหลดโมเดลไม่สำเร็จ")

    manifest = build_manifest(data_dir)
    results: list[dict[str, Any]] = []
    ok_count = 0
    fail_count = 0

    for _, row in manifest.iterrows():
        adc_path = Path(row["adc_csv"])
        bme_raw = row["bme_csv"]
        bme_path = Path(bme_raw) if bme_raw else None
        actual = float(row["methane_ppm"])
        temp_set = row["temp_set"]
        temp_set_val = float(temp_set) if temp_set is not None and pd.notna(temp_set) else None

        if bme_path is None or not bme_path.exists():
            fail_count += 1
            if verbose:
                print(f"[batch] skip {adc_path.name}: ไม่มี bme280")
            results.append({
                "folder": row["folder"],
                "adc_csv": row["adc_csv"],
                "bme_csv": bme_raw,
                "temp_set": temp_set,
                "repeat": row["repeat"],
                "actual_ppm": actual,
                "predicted_ppm": np.nan,
                "error": np.nan,
                "abs_error": np.nan,
                "status": "no_bme",
            })
            continue

        predicted = predict_ppm(
            adc_path,
            bme_path,
            temp_set_val if _include_temp_set else None,
            verbose=verbose,
        )

        if predicted is None:
            fail_count += 1
            results.append({
                "folder": row["folder"],
                "adc_csv": row["adc_csv"],
                "bme_csv": bme_raw,
                "temp_set": temp_set,
                "repeat": row["repeat"],
                "actual_ppm": actual,
                "predicted_ppm": np.nan,
                "error": np.nan,
                "abs_error": np.nan,
                "status": "predict_failed",
            })
            continue

        ok_count += 1
        error = predicted - actual
        results.append({
            "folder": row["folder"],
            "adc_csv": row["adc_csv"],
            "bme_csv": bme_raw,
            "temp_set": temp_set,
            "repeat": row["repeat"],
            "actual_ppm": actual,
            "predicted_ppm": predicted,
            "error": error,
            "abs_error": abs(error),
            "status": "ok",
        })

    df = pd.DataFrame(results)
    ok_df = df[df["status"] == "ok"]

    print(f"\n=== Batch predict: {data_dir} ===")
    print(f"Runs ทั้งหมด: {len(df)}  สำเร็จ: {ok_count}  ล้มเหลว: {fail_count}")

    if len(ok_df) > 0:
        actual_arr = ok_df["actual_ppm"].to_numpy(dtype=float)
        pred_arr = ok_df["predicted_ppm"].to_numpy(dtype=float)
        bm = _batch_metrics(actual_arr, pred_arr)
        print(
            f"Batch metrics ({len(ok_df)} runs): "
            f"MAE={bm['mae']:.4f}  RMSE={bm['rmse']:.4f}  R²={bm['r2']:.4f}"
        )

        display_cols = ["folder", "repeat", "actual_ppm", "predicted_ppm", "error", "status"]
        print("\n" + ok_df[display_cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    if output_path:
        _save_batch_output(df, output_path)

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ทดสอบทำนาย methane ppm จาก processed CSV บน Raspberry Pi / PC"
    )
    parser.add_argument(
        "--adc",
        type=Path,
        help="path ไฟล์ adc1263_*.csv (processed)",
    )
    parser.add_argument(
        "--bme",
        type=Path,
        help="path ไฟล์ bme280_*.csv (processed); ถ้าไม่ระบุจะจับคู่จากโฟลเดอร์เดียวกับ adc",
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="ใช้ไฟล์ล่าสุดจาก acquisition/processed_data/",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path(__file__).parent / "acquisition" / "processed_data",
        help="โฟลเดอร์ processed CSV (ใช้กับ --latest)",
    )
    parser.add_argument(
        "--show-features",
        action="store_true",
        help="พิมพ์ feature ที่โมเดลใช้ก่อนทำนาย",
    )
    parser.add_argument(
        "--batch",
        nargs="?",
        const=str(DEFAULT_BATCH_DIR),
        default=None,
        metavar="PATH",
        help="สแกน testdata ทุกโฟลเดอร์และทำนาย batch (default: BuildML_PC/build_dataset/testdata)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="บันทึกผล batch เป็น CSV (ใช้กับ --batch)",
    )
    parser.add_argument(
        "--show-metrics",
        action="store_true",
        help="พิมพ์ metrics จาก models/methane_linreg_metrics.json",
    )
    args = parser.parse_args()

    if args.show_metrics:
        print_model_metrics()

    if args.batch is not None:
        batch_dir = Path(args.batch)
        if not batch_dir.is_dir():
            parser.error(f"ไม่พบโฟลเดอร์ batch: {batch_dir}")
        batch_predict(batch_dir, output_path=args.output, verbose=False)
        raise SystemExit(0)

    if args.latest:
        adc_path, bme_path = _latest_processed_pair(args.processed_dir)
    elif args.adc:
        adc_path = args.adc
        bme_path = args.bme
        if bme_path is None:
            bme_path = _match_bme_for_adc(adc_path, adc_path.parent)
    else:
        parser.error("ระบุ --adc PATH, --latest หรือ --batch")

    print(f"ADC: {adc_path}")
    print(f"BME: {bme_path if bme_path and bme_path.exists() else '(ไม่มี)'}")

    if not _load_bundle():
        raise SystemExit(1)

    if args.show_features:
        feats = _extract_features(adc_path, bme_path, None, _analysis_windows)
        print("\n=== Features (model uses subset) ===")
        for name in _selected_features:
            val = feats.get(name, np.nan)
            print(f"  {name:20s} = {val}")
        print(f"\nanalysis_windows = {_analysis_windows}")

    ppm = predict_ppm(adc_path, bme_path)
    if ppm is None:
        raise SystemExit(1)
    print(f"\nResult: {ppm:.4f} ppm")
