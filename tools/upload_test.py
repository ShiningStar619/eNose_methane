"""Generate fake eNose data and (optionally) upload it to the cloud.

Designed for smoke-testing the cloud upload pipeline without real hardware.

Each invocation creates one or more "cycles" of fake data. Each cycle is a
matched pair of files using the same timestamp:

  reading/data/adc1263_YYYYMMDD_HHMMSS.npz   (ADC, 4 channels @ 100 Hz)
  reading/data/bme280_YYYYMMDD_HHMMSS.npz    (BME280, T/H/P @ 10 Hz)
  acquisition/processed_data/adc1263_*.csv   (low-pass + moving avg)
  acquisition/processed_data/bme280_*.csv    (low-pass + moving avg)

Usage (from repo root, with venv activated):

  # 1 cycle, uploaded, files persist in reading/data/ and processed_data/
  python -m tools.upload_test

  # 5 cycles, 30-second gap between each timestamp
  python -m tools.upload_test --cycles 5 --gap 30

  # Just create files, do NOT upload
  python -m tools.upload_test --no-upload

  # Custom duration (seconds) and sample rate
  python -m tools.upload_test --duration 60

  # Use a temp folder (does not pollute reading/data/)
  python -m tools.upload_test --tmp
"""
from __future__ import annotations

import argparse
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from cloud.uploader import is_enabled, upload_cycle_files  # noqa: E402

try:
    from acquisition.acquisiton import process_all_data
    _HAS_PROCESSING = True
except ImportError:
    process_all_data = None
    _HAS_PROCESSING = False


def _adc_signal(num_samples: int, sample_rate: float, channels: int = 4) -> np.ndarray:
    """Synthesize realistic ADC voltages: 2.5 V base + slow drift + noise."""
    t = np.arange(num_samples) / sample_rate
    rng = np.random.default_rng()
    out = np.zeros((num_samples, 1 + channels), dtype=np.float32)
    out[:, 0] = t
    for ch in range(channels):
        freq = 0.1 + ch * 0.05
        base = 2.5 + 0.5 * np.sin(2 * np.pi * freq * t)
        noise = rng.normal(0, 0.01, size=num_samples)
        out[:, 1 + ch] = (base + noise).astype(np.float32)
    return out


def _bme_signal(num_samples: int, sample_rate: float) -> np.ndarray:
    """Synthesize realistic BME280 readings around 25°C / 50% / 1013 hPa."""
    t = np.arange(num_samples) / sample_rate
    rng = np.random.default_rng()
    out = np.zeros((num_samples, 4), dtype=np.float32)
    out[:, 0] = t
    out[:, 1] = (25.0 + 0.5 * np.sin(0.01 * t) + rng.normal(0, 0.05, num_samples)).astype(np.float32)
    out[:, 2] = (50.0 + 2.0 * np.sin(0.005 * t) + rng.normal(0, 0.2, num_samples)).astype(np.float32)
    out[:, 3] = (1013.0 + 0.5 * np.sin(0.002 * t) + rng.normal(0, 0.05, num_samples)).astype(np.float32)
    return out


def _save_npz(
    path: Path,
    data: np.ndarray,
    columns: list[str],
    sample_rate: float,
    num_channels: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        path,
        data=data,
        columns=columns,
        sample_rate=sample_rate,
        num_channels=num_channels,
    )


def _make_cycle(
    ts: datetime,
    raw_dir: Path,
    duration_sec: float,
    adc_hz: float = 100.0,
    bme_hz: float = 10.0,
) -> tuple[Path, Path]:
    stamp = ts.strftime("%Y%m%d_%H%M%S")
    adc_path = raw_dir / f"adc1263_{stamp}.npz"
    bme_path = raw_dir / f"bme280_{stamp}.npz"

    adc_n = int(duration_sec * adc_hz)
    bme_n = max(1, int(duration_sec * bme_hz))

    adc_data = _adc_signal(adc_n, adc_hz, channels=4)
    bme_data = _bme_signal(bme_n, bme_hz)

    _save_npz(
        adc_path,
        adc_data,
        columns=["elapsed_time_sec", "ss1", "ss2", "ss3", "ss4"],
        sample_rate=adc_hz,
        num_channels=4,
    )
    _save_npz(
        bme_path,
        bme_data,
        columns=["elapsed_time_sec", "temperature_c", "humidity_pct", "pressure_hpa"],
        sample_rate=bme_hz,
        num_channels=3,
    )
    return adc_path, bme_path


def _process_pair(adc_npz: Path, bme_npz: Path):
    if not _HAS_PROCESSING:
        print("[test] acquisition.acquisiton not available; skipping CSV processing")
        return None, None
    results = process_all_data(input_paths={"adc1263": adc_npz, "bme280": bme_npz})
    return results.get("adc1263"), results.get("bme280")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=1, help="Number of cycles to generate")
    parser.add_argument("--duration", type=float, default=30.0, help="Seconds of data per cycle")
    parser.add_argument("--gap", type=int, default=1, help="Seconds between timestamps")
    parser.add_argument("--no-upload", action="store_true", help="Generate files only")
    parser.add_argument("--tmp", action="store_true", help="Write to /tmp instead of reading/data/")
    parser.add_argument(
        "--wait",
        type=int,
        default=90,
        help="Max seconds to wait for the background upload to finish",
    )
    args = parser.parse_args(argv)

    if args.tmp:
        raw_dir = Path(tempfile.mkdtemp(prefix="enose_fake_"))
        print(f"[test] writing to temp dir: {raw_dir}")
    else:
        raw_dir = _PROJECT_ROOT / "reading" / "data"
        print(f"[test] writing to: {raw_dir}")

    if not args.no_upload and not is_enabled():
        print('[test] Cloud upload disabled in cloud_config.json — pass --no-upload to skip,')
        print('       or set "enabled": true if you want files to be uploaded.')
        return 1

    statuses: list[tuple[str, str]] = []

    def on_status(phase: str, msg: str) -> None:
        statuses.append((phase, msg))
        print(f"[STATUS] {phase}: {msg}")

    now = datetime.now()
    for i in range(args.cycles):
        ts = now + timedelta(seconds=i * args.gap)
        print(f"\n=== Cycle {i+1}/{args.cycles} @ {ts.strftime('%Y-%m-%d %H:%M:%S')} ===")
        adc_npz, bme_npz = _make_cycle(ts, raw_dir, args.duration)
        print(f"[test] ADC: {adc_npz.name} ({adc_npz.stat().st_size/1024:.1f} KB)")
        print(f"[test] BME: {bme_npz.name} ({bme_npz.stat().st_size/1024:.1f} KB)")

        adc_csv, bme_csv = _process_pair(adc_npz, bme_npz)
        if adc_csv:
            print(f"[test] ADC CSV: {Path(adc_csv).name}")
        if bme_csv:
            print(f"[test] BME CSV: {Path(bme_csv).name}")

        if args.no_upload:
            continue

        upload_cycle_files(adc_npz, bme_npz, adc_csv, bme_csv, on_status=on_status)

    if args.no_upload:
        print("\n[test] --no-upload was set; skipping upload wait")
        return 0

    print(f"\n[test] Waiting up to {args.wait}s for background upload to finish...")
    deadline = time.monotonic() + args.wait
    final_seen = False
    while time.monotonic() < deadline:
        if statuses and statuses[-1][0] in {"ok", "warning", "error", "idle"}:
            final_seen = True
            break
        time.sleep(1)

    if not final_seen:
        print("[test] Timed out before a final status; check console output above")
        return 2

    last_phase, last_msg = statuses[-1]
    print(f"[test] Final status: [{last_phase}] {last_msg}")
    return 0 if last_phase == "ok" else (0 if last_phase == "warning" else 3)


if __name__ == "__main__":
    raise SystemExit(main())
