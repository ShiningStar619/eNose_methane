"""Google Drive upload — supports both Service Account and OAuth user credentials.

Auto-detects which credentials are used from the JSON file:
- ``"type": "service_account"`` → service account flow (requires Shared Drive
  for production because service accounts have no storage quota since 2024).
- ``"type": "authorized_user"`` → OAuth user credentials (saved by running
  ``python -m cloud.oauth_setup``). Files uploaded count against the user's
  own Drive quota; works with personal Gmail accounts.
"""
from __future__ import annotations

import json
from pathlib import Path

from cloud.providers.base import BaseProvider


class GoogleDriveProvider(BaseProvider):
    def __init__(self, credentials_path: Path):
        self._credentials_path = Path(credentials_path)
        self._service = None
        self._is_oauth_user = False

    def _detect_cred_type(self) -> str:
        try:
            with open(self._credentials_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise RuntimeError(
                f"Could not read credentials JSON {self._credentials_path}: {e}"
            ) from e

        t = data.get("type")
        if t == "service_account":
            return "service_account"
        if t == "authorized_user":
            return "authorized_user"

        if "installed" in data or "web" in data:
            raise RuntimeError(
                "credentials_path points to an OAuth client_secret file, "
                "not user credentials. Run `python -m cloud.oauth_setup` first "
                "to produce a token.json and point credentials_path there."
            )

        # google-auth-oauthlib's Credentials.to_json() does not always include a
        # "type" key, so accept any blob that looks like a user token (has the
        # client_id + refresh_token fields).
        if "refresh_token" in data and "client_id" in data:
            return "authorized_user"

        raise RuntimeError(
            f"Unknown credentials JSON type: {t!r} (expected service_account or "
            "authorized_user). Keys found: " + ", ".join(sorted(data.keys()))
        )

    def _get_service(self):
        if self._service is not None:
            return self._service
        try:
            from googleapiclient.discovery import build
        except ImportError as e:
            raise RuntimeError(
                "Google Drive dependencies missing. Install: "
                "pip install google-api-python-client google-auth google-auth-oauthlib"
            ) from e

        if not self._credentials_path.is_file():
            raise FileNotFoundError(
                f"Credentials JSON not found: {self._credentials_path}"
            )

        cred_type = self._detect_cred_type()
        scopes = ["https://www.googleapis.com/auth/drive.file"]

        if cred_type == "service_account":
            from google.oauth2 import service_account

            scopes = ["https://www.googleapis.com/auth/drive"]
            creds = service_account.Credentials.from_service_account_file(
                str(self._credentials_path),
                scopes=scopes,
            )
            self._is_oauth_user = False
        else:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request

            creds = Credentials.from_authorized_user_file(
                str(self._credentials_path), scopes
            )
            if not creds.valid:
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    try:
                        with open(self._credentials_path, "w", encoding="utf-8") as f:
                            f.write(creds.to_json())
                    except OSError as e:
                        print(f"[cloud] Warning: could not persist refreshed token: {e}")
                else:
                    raise RuntimeError(
                        "OAuth user credentials are invalid / missing refresh_token. "
                        "Run `python -m cloud.oauth_setup` to re-authorize."
                    )
            self._is_oauth_user = True

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
                .list(
                    q=q,
                    spaces="drive",
                    fields="files(id, name)",
                    pageSize=10,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
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
                .create(
                    body=body,
                    fields="id",
                    supportsAllDrives=True,
                )
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
                .list(
                    q=q,
                    spaces="drive",
                    fields="files(id, name)",
                    pageSize=5,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
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
            req = service.files().create(
                body=body,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            )
            response = None
            while response is None:
                status, response = req.next_chunk()
                if status:
                    print(f"[cloud] Upload {name}: {int(status.progress() * 100)}%")
            return response.get("id") if response else None
        except HttpError as e:
            raise RuntimeError(f"Drive API upload failed for {name}: {e}") from e
