"""Non-blocking cloud upload after each acquisition cycle."""
from __future__ import annotations

import re
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

from cloud.config import load_cloud_config
from cloud import queue as qmod

_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="enose_cloud")

_StatusCallback = Callable[[str, str], None] | None


def is_enabled() -> bool:
    """True if cloud upload is turned on in config (after env override)."""
    return bool(load_cloud_config().get("enabled"))


def _sanitize_device_id(device_id: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]", "_", device_id.strip())
    return s[:64] or "enose-device"


def _get_provider(cfg: dict[str, Any]):
    provider_name = (cfg.get("provider") or "gdrive").lower()
    if provider_name == "gdrive":
        from cloud.providers.gdrive import GoogleDriveProvider

        return GoogleDriveProvider(Path(cfg["credentials_path"]))
    raise ValueError(f"Unknown cloud provider: {provider_name}")


def _notify(cb: _StatusCallback, phase: str, message: str) -> None:
    if not cb:
        return
    try:
        cb(phase, message)
    except Exception:
        pass


def _folder_for_subfolder(subfolder: str, raw_id: str, proc_id: str) -> str:
    if subfolder == "processed":
        return proc_id
    return raw_id


def _try_upload_file(
    provider,
    local_path: Path,
    remote_folder_id: str,
) -> bool:
    """Return True if file is on Drive (uploaded or skipped as duplicate)."""
    provider.upload_file(local_path, remote_folder_id, skip_if_exists=True)
    return True


def _enqueue_failure(
    local_path: Path,
    subfolder: str,
    cfg: dict[str, Any],
) -> None:
    item = {
        "local_path": str(local_path.resolve()),
        "subfolder": subfolder,
        "attempts": 0,
        "dead_letter": False,
    }
    qmod.enqueue(item, max_size=int(cfg.get("max_queue_size", 200)))


def _bump_queue_failure(local_path: str, err: str, cfg: dict[str, Any]) -> None:
    max_attempts = int(cfg.get("retry_attempts", 3))
    items = qmod.load_queue()
    changed = False
    for i, it in enumerate(items):
        if str(it.get("local_path")) != str(local_path):
            continue
        attempts = int(it.get("attempts", 0)) + 1
        it["attempts"] = attempts
        it["last_error"] = err[:500]
        it["last_error_ts"] = time.time()
        if attempts >= max_attempts:
            it["dead_letter"] = True
            print(f"[cloud] Dead letter (max retries): {local_path}")
        items[i] = it
        changed = True
        break
    if changed:
        qmod.save_queue(items)


def _drain_queue(
    provider,
    raw_folder_id: str,
    proc_folder_id: str,
    cfg: dict[str, Any],
    on_status: _StatusCallback,
    budget_sec: float,
) -> None:
    deadline = time.monotonic() + max(0.0, budget_sec)
    retry_delay = float(cfg.get("retry_delay_sec", 5))

    while time.monotonic() < deadline:
        items = qmod.load_queue()
        pending = [x for x in items if not x.get("dead_letter")]
        if not pending:
            break
        item = pending[0]
        lp = Path(str(item.get("local_path", "")))
        sub = str(item.get("subfolder", "raw"))
        if not lp.is_file():
            print(f"[cloud] Drop queue item (missing file): {lp}")
            qmod.dequeue_success(str(lp))
            continue
        fid = _folder_for_subfolder(sub, raw_folder_id, proc_folder_id)
        try:
            _notify(on_status, "uploading", f"Retry queue: {lp.name}")
            _try_upload_file(provider, lp, fid)
            qmod.dequeue_success(str(lp))
            print(f"[cloud] Queue item uploaded: {lp.name}")
        except Exception as e:
            print(f"[cloud] Queue upload failed: {lp}: {e}")
            _bump_queue_failure(str(lp), str(e), cfg)
            time.sleep(min(retry_delay, max(0.0, deadline - time.monotonic())))


def _upload_job(
    adc_npz: Path | None,
    bme_npz: Path | None,
    adc_csv: Path | None,
    bme_csv: Path | None,
    on_status: _StatusCallback,
) -> dict[str, bool]:
    """Runs in worker thread. Returns per-key success (True=ok or skipped)."""
    results = {
        "adc_npz": True,
        "bme_npz": True,
        "adc_csv": True,
        "bme_csv": True,
    }
    cfg = load_cloud_config()
    if not cfg.get("enabled"):
        _notify(on_status, "idle", "Cloud upload disabled")
        return results

    root_id = (cfg.get("remote_root_folder_id") or "").strip()
    if not root_id:
        msg = "remote_root_folder_id missing in cloud_config.json"
        print(f"[cloud] {msg}")
        _notify(on_status, "error", msg)
        return results

    try:
        provider = _get_provider(cfg)
    except Exception as e:
        print(f"[cloud] Provider init failed: {e}")
        _notify(on_status, "error", str(e))
        return results

    device_id = _sanitize_device_id(str(cfg.get("device_id", "enose-pi01")))
    try:
        dev_folder_id = provider.ensure_folder(root_id, device_id)
        raw_folder_id = provider.ensure_folder(dev_folder_id, "raw")
        proc_folder_id = provider.ensure_folder(dev_folder_id, "processed")
    except Exception as e:
        print(f"[cloud] Folder setup failed: {e}")
        _notify(on_status, "error", str(e))
        return results

    budget = float(cfg.get("queue_retry_budget_sec", 30))
    _drain_queue(provider, raw_folder_id, proc_folder_id, cfg, on_status, budget)

    specs: list[tuple[str, Path | None, str, str]] = []
    if cfg.get("include_raw_npz", True):
        specs.append(("adc_npz", adc_npz, "raw", "adc_npz"))
        specs.append(("bme_npz", bme_npz, "raw", "bme_npz"))
    if cfg.get("include_processed_csv", True):
        specs.append(("adc_csv", adc_csv, "processed", "adc_csv"))
        specs.append(("bme_csv", bme_csv, "processed", "bme_csv"))

    pending_n = qmod.count_pending()
    _notify(on_status, "uploading", f"Uploading… (queued: {pending_n})")

    for key, path, sub, _ in specs:
        if path is None:
            continue
        p = Path(path)
        if not p.is_file():
            results[key] = False
            continue
        fid = _folder_for_subfolder(sub, raw_folder_id, proc_folder_id)
        try:
            _notify(on_status, "uploading", f"Uploading {p.name}…")
            _try_upload_file(provider, p, fid)
            print(f"[cloud] Uploaded: {p.name}")
        except Exception as e:
            print(f"[cloud] Upload failed {p.name}: {e}")
            results[key] = False
            _enqueue_failure(p, sub, cfg)

    pending_after = qmod.count_pending()
    dead = sum(1 for x in qmod.load_queue() if x.get("dead_letter"))
    if pending_after == 0 and dead == 0:
        _notify(on_status, "ok", "Cloud: upload OK")
    elif dead:
        _notify(on_status, "warning", f"Cloud: {dead} failed permanently (see queue)")
    else:
        _notify(on_status, "warning", f"Cloud: {pending_after} file(s) queued for retry")

    return results


def upload_cycle_files(
    adc_npz: Path | None,
    bme_npz: Path | None,
    adc_csv: Path | None,
    bme_csv: Path | None,
    on_status: _StatusCallback = None,
) -> None:
    """Schedule upload (and queue drain) on a single-worker executor; returns immediately."""
    cfg = load_cloud_config()
    if not cfg.get("enabled"):
        return

    def run():
        try:
            _upload_job(adc_npz, bme_npz, adc_csv, bme_csv, on_status)
        except Exception as e:
            print(f"[cloud] Upload job error: {e}")
            _notify(on_status, "error", str(e))

    _executor.submit(run)
