"""Abstract cloud storage provider for uploads."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseProvider(ABC):
    """Minimal interface: ensure folder hierarchy and upload a local file."""

    @abstractmethod
    def ensure_folder(self, parent_id: str, name: str) -> str:
        """Return folder id for `name` under `parent_id`, creating if missing."""

    @abstractmethod
    def upload_file(
        self,
        local_path: Path,
        remote_folder_id: str,
        remote_name: str | None = None,
        skip_if_exists: bool = True,
    ) -> str | None:
        """Upload file; return remote file id or None if skipped (duplicate)."""
