"""Google Drive upload using a service account."""
from __future__ import annotations

from pathlib import Path

from cloud.providers.base import BaseProvider


class GoogleDriveProvider(BaseProvider):
    def __init__(self, credentials_path: Path):
        self._credentials_path = Path(credentials_path)
        self._service = None

    def _get_service(self):
        if self._service is not None:
            return self._service
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
        except ImportError as e:
            raise RuntimeError(
                "Google Drive dependencies missing. Install: "
                "pip install google-api-python-client google-auth"
            ) from e

        if not self._credentials_path.is_file():
            raise FileNotFoundError(
                f"Service account JSON not found: {self._credentials_path}"
            )

        scopes = ["https://www.googleapis.com/auth/drive.file"]
        creds = service_account.Credentials.from_service_account_file(
            str(self._credentials_path),
            scopes=scopes,
        )
        self._service = build("drive", "v3", credentials=creds, cache_discovery=False)
        return self._service

    def _find_folder_id(self, parent_id: str, name: str) -> str | None:
        service = self._get_service()
        from googleapiclient.errors import HttpError

        esc = name.replace("\\", "\\\\").replace("'", "\\'")
        q = (
            f"'{parent_id}' in parents and name = '{esc}' "
            "and mimeType = 'application/vnd.google-apps.folder' "
            "and trashed = false"
        )
        try:
            resp = (
                service.files()
                .list(q=q, spaces="drive", fields="files(id, name)", pageSize=10)
                .execute()
            )
        except HttpError as e:
            raise RuntimeError(f"Drive API list folders failed: {e}") from e
        files = resp.get("files", [])
        if not files:
            return None
        return files[0]["id"]

    def ensure_folder(self, parent_id: str, name: str) -> str:
        service = self._get_service()
        from googleapiclient.errors import HttpError

        existing = self._find_folder_id(parent_id, name)
        if existing:
            return existing
        body = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        try:
            created = (
                service.files()
                .create(body=body, fields="id")
                .execute()
            )
        except HttpError as e:
            raise RuntimeError(f"Drive API create folder failed: {e}") from e
        return created["id"]

    def _find_file_id(self, folder_id: str, filename: str) -> str | None:
        service = self._get_service()
        from googleapiclient.errors import HttpError

        esc = filename.replace("\\", "\\\\").replace("'", "\\'")
        q = (
            f"'{folder_id}' in parents and name = '{esc}' "
            "and mimeType != 'application/vnd.google-apps.folder' "
            "and trashed = false"
        )
        try:
            resp = (
                service.files()
                .list(q=q, spaces="drive", fields="files(id, name)", pageSize=5)
                .execute()
            )
        except HttpError:
            return None
        files = resp.get("files", [])
        return files[0]["id"] if files else None

    def upload_file(
        self,
        local_path: Path,
        remote_folder_id: str,
        remote_name: str | None = None,
        skip_if_exists: bool = True,
    ) -> str | None:
        service = self._get_service()
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaFileUpload

        local_path = Path(local_path)
        if not local_path.is_file():
            raise FileNotFoundError(str(local_path))

        name = remote_name or local_path.name
        if skip_if_exists and self._find_file_id(remote_folder_id, name):
            print(f"[cloud] Skip upload (already exists): {name}")
            return None

        media = MediaFileUpload(
            str(local_path),
            mimetype="application/octet-stream",
            resumable=True,
        )
        body = {"name": name, "parents": [remote_folder_id]}
        try:
            req = service.files().create(body=body, media_body=media, fields="id")
            response = None
            while response is None:
                status, response = req.next_chunk()
                if status:
                    print(f"[cloud] Upload {name}: {int(status.progress() * 100)}%")
            return response.get("id") if response else None
        except HttpError as e:
            raise RuntimeError(f"Drive API upload failed for {name}: {e}") from e
