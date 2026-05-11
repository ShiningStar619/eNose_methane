"""Persistent upload queue with optional file locking (Linux) or process lock (Windows)."""
from __future__ import annotations

import json
import os
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any

try:
    import fcntl  # type: ignore

    _HAS_FCNTL = True
except ImportError:
    fcntl = None  # type: ignore
    _HAS_FCNTL = False

# Same parent as cloud package
_QUEUE_DIR = Path(__file__).resolve().parent
DEFAULT_QUEUE_PATH = _QUEUE_DIR / "upload_queue.json"

_process_lock = threading.RLock()


@contextmanager
def _file_lock(fp):
    if _HAS_FCNTL and fp is not None:
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
    else:
        _process_lock.acquire()
        try:
            yield
        finally:
            _process_lock.release()


def load_queue(path: Path | None = None) -> list[dict[str, Any]]:
    """Return queue items (list of dicts)."""
    p = path or DEFAULT_QUEUE_PATH
    if not p.is_file():
        return []
    try:
        if _HAS_FCNTL:
            with open(p, "r", encoding="utf-8") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    raw = json.load(f)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        else:
            with _process_lock:
                with open(p, "r", encoding="utf-8") as f:
                    raw = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[cloud] Warning: could not read upload queue: {e}")
        return []
    if isinstance(raw, list):
        return [x for x in raw if isinstance(x, dict)]
    if isinstance(raw, dict) and "items" in raw:
        items = raw["items"]
        return [x for x in items if isinstance(x, dict)] if isinstance(items, list) else []
    return []


def save_queue(items: list[dict[str, Any]], path: Path | None = None) -> None:
    """Replace entire queue."""
    p = path or DEFAULT_QUEUE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    fp = None
    try:
        fp = open(p, "a+", encoding="utf-8")
        with _file_lock(fp):
            fp.seek(0)
            fp.truncate()
            json.dump(items, fp, indent=2, ensure_ascii=False)
            fp.write("\n")
            fp.flush()
            os.fsync(fp.fileno())
    except OSError as e:
        print(f"[cloud] Warning: could not save upload queue: {e}")
    finally:
        if fp is not None:
            fp.close()


def enqueue(
    item: dict[str, Any],
    path: Path | None = None,
    max_size: int = 200,
) -> bool:
    """Append one item; returns False if queue full."""
    p = path or DEFAULT_QUEUE_PATH
    fp = None
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        fp = open(p, "a+", encoding="utf-8")
        with _file_lock(fp):
            fp.seek(0)
            try:
                raw = json.load(fp)
            except json.JSONDecodeError:
                raw = []
            if not isinstance(raw, list):
                raw = []
            local = str(item.get("local_path", ""))
            for existing in raw:
                if not isinstance(existing, dict):
                    continue
                if (
                    str(existing.get("local_path")) == local
                    and not existing.get("dead_letter")
                ):
                    return True  # already queued
            if len(raw) >= max_size:
                print("[cloud] Upload queue full; cannot enqueue")
                return False
            raw.append(item)
            fp.seek(0)
            fp.truncate()
            json.dump(raw, fp, indent=2, ensure_ascii=False)
            fp.write("\n")
            fp.flush()
            os.fsync(fp.fileno())
    except OSError as e:
        print(f"[cloud] Warning: enqueue failed: {e}")
        return False
    finally:
        if fp is not None:
            fp.close()
    return True


def dequeue_success(local_path: str, path: Path | None = None) -> None:
    """Remove item matching local_path from queue."""
    items = load_queue(path)
    local_path = str(local_path)
    new_items = [x for x in items if str(x.get("local_path")) != local_path]
    if len(new_items) != len(items):
        save_queue(new_items, path)


def update_item(
    local_path: str,
    updates: dict[str, Any],
    path: Path | None = None,
) -> None:
    """Merge updates into the first queue item with matching local_path."""
    items = load_queue(path)
    local_path = str(local_path)
    changed = False
    for i, it in enumerate(items):
        if str(it.get("local_path")) == local_path:
            items[i] = {**it, **updates}
            changed = True
            break
    if changed:
        save_queue(items, path)


def count_pending(path: Path | None = None) -> int:
    """Count items not marked dead_letter."""
    return sum(1 for x in load_queue(path) if not x.get("dead_letter"))
