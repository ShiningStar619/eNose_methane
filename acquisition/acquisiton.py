import os
import traceback
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

try:
    from scipy.signal import lfilter, lfilter_zi
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# --- Configuration ---
CURRENT_DIR = Path(__file__).parent
READING_DATA_DIR = CURRENT_DIR.parent / "reading" / "data"
OUTPUT_DIR = CURRENT_DIR / "processed_data"

# Filter settings (sample_rate อ่านจากไฟล์ NPZ)
CUTOFF_FREQ = 50            # Hz
MOVING_AVG_WINDOW = 1000    # samples


def get_latest_npz_file(directory, prefix=None):
    """หาไฟล์ NPZ ล่าสุดในโฟลเดอร์ (กรองตาม prefix ได้)"""
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return None

    pattern = f"{prefix}_*.npz" if prefix else "*.npz"
    npz_files = list(directory.glob(pattern))
    if not npz_files:
        scope = f" with prefix '{prefix}'" if prefix else ""
        print(f"No NPZ files found in {directory}{scope}")
        return None

    return max(npz_files, key=os.path.getmtime)


def load_npz_arrays(npz_path):
    """Load NPZ → (data ndarray, columns list, sample_rate float)"""
    npz_data = np.load(npz_path, allow_pickle=True)
    data = npz_data['data']
    columns = list(npz_data['columns'])
    sample_rate = float(npz_data['sample_rate'])
    return data, columns, sample_rate


def lowpass_filter(data, cutoff_freq, sample_rate):
    """First-order IIR low-pass filter — vectorized via scipy when available.

    สูตร: y[n] = α·x[n] + (1-α)·y[n-1] โดย y[-1] = data[0]
    """
    arr = np.ascontiguousarray(data, dtype=np.float64)
    if arr.size == 0:
        return arr.astype(np.float32)

    dt = 1.0 / sample_rate
    rc = 1.0 / (2 * np.pi * cutoff_freq)
    alpha = dt / (rc + dt)

    if SCIPY_AVAILABLE:
        b = np.array([alpha], dtype=np.float64)
        a = np.array([1.0, -(1.0 - alpha)], dtype=np.float64)
        # zi ที่ทำให้ output[0] = data[0] (แทน initial condition y[-1] = data[0])
        zi = lfilter_zi(b, a) * arr[0]
        filtered, _ = lfilter(b, a, arr, zi=zi)
        return filtered.astype(np.float32)

    # Fallback: pure-numpy loop (จัดการเร็วกว่าเดิมเพราะ allocate ครั้งเดียว)
    filtered = np.empty_like(arr)
    filtered[0] = arr[0]
    one_minus_alpha = 1.0 - alpha
    for i in range(1, arr.size):
        filtered[i] = alpha * arr[i] + one_minus_alpha * filtered[i - 1]
    return filtered.astype(np.float32)


def centered_moving_average(data, window):
    """Centered moving average ผ่าน cumulative sum — O(n) ไม่ขึ้นกับขนาด window

    เลียนแบบพฤติกรรม pandas.Series.rolling(window, center=True, min_periods=1).mean()
    (ขอบใช้จำนวน sample ที่มีจริง ไม่เติม NaN)
    """
    arr = np.asarray(data, dtype=np.float64)
    n = arr.size
    if n == 0 or window <= 1:
        return arr.astype(np.float32)

    half_lo = (window - 1) // 2
    half_hi = window - 1 - half_lo

    csum = np.empty(n + 1, dtype=np.float64)
    csum[0] = 0.0
    np.cumsum(arr, out=csum[1:])

    idx = np.arange(n)
    starts = np.clip(idx - half_lo, 0, n)
    ends = np.clip(idx + half_hi + 1, 0, n)
    sums = csum[ends] - csum[starts]
    counts = (ends - starts).astype(np.float64)
    np.maximum(counts, 1, out=counts)
    return (sums / counts).astype(np.float32)


def _resolve_output_path(prefix, input_stem):
    """กำหนด path ของ CSV ที่จะบันทึก (ดึง date_time จากชื่อไฟล์ input)"""
    parts = input_stem.split('_')
    date_time = None
    for i in range(len(parts) - 1):
        if (
            len(parts[i]) == 8 and parts[i].isdigit()
            and len(parts[i + 1]) == 6 and parts[i + 1].isdigit()
        ):
            date_time = f"{parts[i]}_{parts[i + 1]}"
            break

    if date_time is None:
        date_time = datetime.now().strftime('%Y%m%d_%H%M%S')

    output_path = OUTPUT_DIR / f"{prefix}_{date_time}.csv"
    if output_path.exists():
        ts = datetime.now().strftime('%H%M%S_%f')[:-3]
        output_path = OUTPUT_DIR / f"{prefix}_{date_time}_{ts}.csv"
    return output_path


def process_data(prefix="adc1263", input_path=None, verbose=False):
    """ประมวลผล NPZ → CSV (low-pass + moving average ที่ vectorized)

    Parameters
    ----------
    prefix : str
        คำนำหน้าชื่อไฟล์ (เช่น "adc1263", "bme280")
    input_path : pathlib.Path | None
        ระบุไฟล์ตรงๆ; ถ้าเป็น None จะค้นหาไฟล์ล่าสุดของ prefix นั้น
    verbose : bool
        พิมพ์รายละเอียดเพิ่มเติม (ใช้ตอน debug)

    Returns
    -------
    pathlib.Path | None
        path ของ CSV ที่บันทึก หรือ None ถ้าไม่มีข้อมูล/บันทึกไม่สำเร็จ
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if input_path is None:
        input_path = get_latest_npz_file(READING_DATA_DIR, prefix=prefix)
    if input_path is None:
        return None
    input_path = Path(input_path)

    if verbose:
        print(f"Processing ({prefix}): {input_path.name}")

    try:
        data_arr, columns, sample_rate = load_npz_arrays(input_path)
    except Exception as e:
        print(f"Error reading NPZ {input_path.name}: {e}")
        return None

    n_rows = data_arr.shape[0]
    if n_rows == 0:
        print(f"Empty NPZ {input_path.name}")
        return None

    time_idx = columns.index('elapsed_time_sec') if 'elapsed_time_sec' in columns else 0
    sensor_indices = [
        i for i, col in enumerate(columns)
        if i != time_idx
        and not str(col).endswith('_lp')
        and not str(col).endswith('_lp_ma')
    ]
    if not sensor_indices:
        print(f"No sensor columns in {input_path.name}")
        return None

    # ประมวลผลเป็นอาร์เรย์โดยตรง — ไม่สร้าง DataFrame.copy()
    out_data = {'elapsed_time_sec': data_arr[:, time_idx].astype(np.float32)}

    if n_rows > 15:
        if verbose:
            print(
                f"Filters: lowpass {CUTOFF_FREQ}Hz @ fs={sample_rate}Hz "
                f"-> moving avg window={MOVING_AVG_WINDOW}"
            )
        for i in sensor_indices:
            col_name = columns[i]
            raw = data_arr[:, i]
            # จัดการ NaN เฉพาะกรณีที่จำเป็น (โดยทั่วไปไม่มี)
            if not np.all(np.isfinite(raw)):
                clean = pd.Series(raw).ffill().bfill().to_numpy()
            else:
                clean = raw
            lp = lowpass_filter(clean, CUTOFF_FREQ, sample_rate)
            out_data[f'{col_name}_lp_ma'] = centered_moving_average(lp, MOVING_AVG_WINDOW)
    else:
        if verbose:
            print(f"Not enough samples ({n_rows}) — skipping filter")
        for i in sensor_indices:
            col_name = columns[i]
            out_data[f'{col_name}_lp_ma'] = data_arr[:, i].astype(np.float32)

    df_final = pd.DataFrame(out_data)
    output_path = _resolve_output_path(prefix, input_path.stem)

    try:
        if not os.access(OUTPUT_DIR, os.W_OK):
            raise PermissionError(f"No write permission for: {OUTPUT_DIR}")
        df_final.to_csv(output_path, index=False, float_format='%.6g')
        if verbose:
            print(f"Saved processed data to: {output_path}")
    except PermissionError as e:
        print(f"Permission error: {e}")
        print(f"  Try: sudo chmod 755 {OUTPUT_DIR}")
        return None
    except Exception as e:
        print(f"Error saving {output_path}: {e}")
        return None

    return output_path


# ลำดับ prefix ที่ process_all_data() จะประมวลผล
DEFAULT_PREFIXES = ("adc1263", "bme280")


def process_all_data(prefixes=DEFAULT_PREFIXES, input_paths=None, verbose=False):
    """ประมวลผลไฟล์ล่าสุดของทุก prefix

    Parameters
    ----------
    prefixes : tuple[str, ...]
        ลำดับ prefix ที่จะประมวลผล
    input_paths : dict[str, pathlib.Path] | None
        ระบุ path ตรงๆ ต่อ prefix (เช่น {'adc1263': Path(...), 'bme280': Path(...)})
        เพื่อข้ามขั้นตอนค้นหาไฟล์ล่าสุด — ลด race และ ทำงานเร็วขึ้น
    verbose : bool
        พิมพ์รายละเอียดเพิ่ม

    Returns
    -------
    dict[str, pathlib.Path | None]
        path ของ CSV ที่บันทึกได้ของแต่ละ prefix (หรือ None ถ้าล้มเหลว)
    """
    results = {}
    for prefix in prefixes:
        path = input_paths.get(prefix) if input_paths else None
        try:
            if verbose:
                print(f"\n=== Processing prefix: {prefix} ===")
            results[prefix] = process_data(prefix=prefix, input_path=path, verbose=verbose)
        except Exception as e:
            print(f"Error processing prefix '{prefix}': {e}")
            traceback.print_exc()
            results[prefix] = None
    return results


if __name__ == "__main__":
    process_all_data(verbose=True)
