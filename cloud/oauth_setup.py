"""One-time OAuth setup for Google Drive (personal Gmail).

Usage (run on a machine WITH a browser — your laptop / desktop):

    python -m cloud.oauth_setup --client-secret /path/to/client_secret.json

Optional flags:
    --token-out  path to save the resulting token.json (default: ./token.json)
    --no-browser use console flow (manual URL copy/paste) — useful on headless
                 hosts that can still open a browser elsewhere

After it finishes, copy the produced ``token.json`` to your Raspberry Pi
(e.g. ``~/.enose/gdrive_token.json``) and point
``credentials_path`` in ``program/cloud_config.json`` at it.

Steps to obtain ``client_secret.json``:
1. https://console.cloud.google.com/  → APIs & Services → Credentials
2. Create Credentials → OAuth client ID → Application type: **Desktop app**
3. Download JSON → that's your ``client_secret.json``
4. On the same project, under "OAuth consent screen" add your Gmail address
   to "Test users" if the app is still in Testing status.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--client-secret",
        required=True,
        help="Path to OAuth Desktop client_secret.json downloaded from Google Cloud Console",
    )
    parser.add_argument(
        "--token-out",
        default="token.json",
        help="Where to save the resulting user token (default: ./token.json)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use the console flow (prints a URL to copy into a browser yourself)",
    )
    args = parser.parse_args(argv)

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print(
            "Missing dependency: pip install google-auth-oauthlib",
            file=sys.stderr,
        )
        return 1

    secret_path = Path(args.client_secret).expanduser()
    if not secret_path.is_file():
        print(f"client_secret.json not found: {secret_path}", file=sys.stderr)
        return 1

    flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
    if args.no_browser:
        creds = flow.run_console()
    else:
        # run_local_server opens browser and listens on 127.0.0.1:<port>
        creds = flow.run_local_server(port=0)

    token_path = Path(args.token_out).expanduser()
    token_path.parent.mkdir(parents=True, exist_ok=True)
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    try:
        token_path.chmod(0o600)
    except OSError:
        pass

    print(f"\nSaved user token to: {token_path}")
    print("Copy this file to your Pi (e.g. ~/.enose/gdrive_token.json)")
    print('and set "credentials_path" in program/cloud_config.json to that path.')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
