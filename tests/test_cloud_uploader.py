"""Tests for cloud uploader with a mock provider."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cloud import queue as qmod


class MockProvider:
    def __init__(self, fail_names=None):
        self.fail_names = set(fail_names or ())
        self.folders: list[tuple[str, str]] = []
        self.uploads: list[tuple[str, str]] = []

    def ensure_folder(self, parent_id: str, name: str) -> str:
        self.folders.append((parent_id, name))
        return f"id_{parent_id}_{name}"

    def upload_file(self, local_path, remote_folder_id, remote_name=None, skip_if_exists=True):
        p = Path(local_path)
        if p.name in self.fail_names:
            raise RuntimeError("simulated network failure")
        self.uploads.append((str(p), remote_folder_id))


class TestUploaderJob(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.queue_path = Path(self._tmpdir.name) / "upload_queue.json"
        self._qp = patch.object(qmod, "DEFAULT_QUEUE_PATH", self.queue_path)
        self._qp.start()

    def tearDown(self):
        self._qp.stop()
        self._tmpdir.cleanup()

    def _base_cfg(self):
        return {
            "enabled": True,
            "provider": "gdrive",
            "credentials_path": str(Path.home() / ".enose" / "dummy.json"),
            "remote_root_folder_id": "root123",
            "device_id": "test-device",
            "include_raw_npz": True,
            "include_processed_csv": True,
            "retry_attempts": 2,
            "retry_delay_sec": 0,
            "max_queue_size": 50,
            "queue_retry_budget_sec": 1,
        }

    @patch("cloud.uploader.load_cloud_config")
    @patch("cloud.uploader._get_provider")
    def test_upload_all_success(self, mock_get_provider, mock_load_cfg):
        mock_load_cfg.return_value = self._base_cfg()
        prov = MockProvider()
        mock_get_provider.return_value = prov

        from cloud import uploader

        d = Path(self.queue_path).parent / "uploader_test_data"
        d.mkdir(exist_ok=True)
        f1 = d / "adc1263_20260101_120000.npz"
        f2 = d / "bme280_20260101_120000.npz"
        f3 = d / "adc1263_20260101_120000.csv"
        f4 = d / "bme280_20260101_120000.csv"
        for f in (f1, f2, f3, f4):
            f.write_text("x", encoding="utf-8")

        statuses = []

        def on_status(phase, msg):
            statuses.append((phase, msg))

        uploader._upload_job(f1, f2, f3, f4, on_status)
        self.assertEqual(len(prov.uploads), 4)
        mock_get_provider.assert_called_once()
        self.assertTrue(any(s[0] == "uploading" for s in statuses))

        for f in (f1, f2, f3, f4):
            f.unlink(missing_ok=True)
        try:
            d.rmdir()
        except OSError:
            pass

    @patch("cloud.uploader.load_cloud_config")
    @patch("cloud.uploader._get_provider")
    def test_upload_failure_enqueues(self, mock_get_provider, mock_load_cfg):
        mock_load_cfg.return_value = self._base_cfg()
        prov = MockProvider(fail_names={"adc1263_20260101_120000.npz"})
        mock_get_provider.return_value = prov

        from cloud import uploader

        d = Path(self.queue_path).parent / "uploader_fail_data"
        d.mkdir(exist_ok=True)
        f1 = d / "adc1263_20260101_120000.npz"
        f1.write_bytes(b"x")

        uploader._upload_job(f1, None, None, None, None)
        self.assertEqual(len(prov.uploads), 0)
        qitems = qmod.load_queue()
        self.assertTrue(any("adc1263_20260101_120000.npz" in str(x.get("local_path", "")) for x in qitems))

        for x in qitems:
            if "adc1263_20260101_120000.npz" in str(x.get("local_path", "")):
                qmod.dequeue_success(str(x["local_path"]))

        f1.unlink(missing_ok=True)
        try:
            d.rmdir()
        except OSError:
            pass

    @patch("cloud.uploader.load_cloud_config")
    def test_disabled_short_circuits(self, mock_load_cfg):
        mock_load_cfg.return_value = {**self._base_cfg(), "enabled": False}
        from cloud import uploader

        uploader._upload_job(Path("/nope"), None, None, None, None)


if __name__ == "__main__":
    unittest.main()
