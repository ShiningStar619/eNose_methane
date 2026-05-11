"""Load and save cloud upload configuration."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

# Project root = parent of cloud/
_CLOUD_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _CLOUD_DIR.parent
DEFAULT_CONFIG_PATH = _PROJECT_ROOT / "program" / "cloud_config.json"

DEFAULT_CLOUD_CONFIG: dict[str, Any] = {
    "enabled": False,
    "provider": "gdrive",
    "credentials_path": str(Path.home() / ".enose" / "gdrive_service_account.json"),
    "remote_root_folder_id": "",
    "device_id": "enose-pi01",
    "include_raw_npz": True,
    "include_processed_csv": True,
    "retry_attempts": 3,
    "retry_delay_sec": 5,
    "max_queue_size": 200,
    "queue_retry_budget_sec": 30,
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_cloud_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load cloud_config.json merged with defaults; apply env overrides."""
    cfg_path = Path(path) if path else DEFAULT_CONFIG_PATH
    data = dict(DEFAULT_CLOUD_CONFIG)
    if cfg_path.is_file():
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                data = _deep_merge(DEFAULT_CLOUD_CONFIG, loaded)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[cloud] Warning: could not load {cfg_path}: {e}")

    env = os.environ.get("ENOSE_CLOUD_ENABLED")
    if env is not None:
        data["enabled"] = env.strip().lower() in ("1", "true", "yes", "on")

    cred = data.get("credentials_path", "")
    if isinstance(cred, str):
        data["credentials_path"] = os.path.expanduser(cred)

    return data


def save_cloud_config(updates: dict[str, Any], path: Path | str | None = None) -> None:
    """Merge updates into existing file (or defaults) and write known keys only."""
    cfg_path = Path(path) if path else DEFAULT_CONFIG_PATH
    on_disk: dict[str, Any] = {}
    if cfg_path.is_file():
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    on_disk = loaded
        except (json.JSONDecodeError, OSError):
            pass
    merged = _deep_merge(DEFAULT_CLOUD_CONFIG, on_disk)
    for k, v in updates.items():
        if k in DEFAULT_CLOUD_CONFIG:
            merged[k] = v
    out = {k: merged[k] for k in DEFAULT_CLOUD_CONFIG}
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = cfg_path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    tmp.replace(cfg_path)
