"""
Optional smoke test against real Google Drive.
Skip unless:
  ENOSE_GDRIVE_SERVICE_ACCOUNT_JSON  (path to JSON key)
  ENOSE_GDRIVE_FOLDER_ID             (shared folder id)
"""
from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(
    os.environ.get("ENOSE_GDRIVE_SERVICE_ACCOUNT_JSON")
    and os.environ.get("ENOSE_GDRIVE_FOLDER_ID"),
    "Set ENOSE_GDRIVE_SERVICE_ACCOUNT_JSON and ENOSE_GDRIVE_FOLDER_ID for smoke test",
)
class TestGoogleDriveSmoke(unittest.TestCase):
    def test_upload_small_file(self):
        from cloud.providers.gdrive import GoogleDriveProvider

        cred = Path(os.environ["ENOSE_GDRIVE_SERVICE_ACCOUNT_JSON"])
        root = os.environ["ENOSE_GDRIVE_FOLDER_ID"].strip()
        self.assertTrue(cred.is_file(), cred)

        prov = GoogleDriveProvider(cred)
        sub = prov.ensure_folder(root, "_enose_smoke_test")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tf:
            tf.write("enose smoke\n")
            tmp = Path(tf.name)
        try:
            prov.upload_file(
                tmp,
                sub,
                remote_name="smoke_test_file.txt",
                skip_if_exists=True,
            )
        finally:
            tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
