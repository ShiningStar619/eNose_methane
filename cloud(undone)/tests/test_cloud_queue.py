"""Tests for cloud/upload queue persistence."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cloud import queue as qmod


class TestUploadQueue(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmpdir.name) / "queue.json"

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_enqueue_and_dequeue(self):
        p = self.tmp
        self.assertEqual(qmod.load_queue(p), [])
        ok = qmod.enqueue(
            {"local_path": "/tmp/a.npz", "subfolder": "raw", "attempts": 0, "dead_letter": False},
            path=p,
            max_size=10,
        )
        self.assertTrue(ok)
        items = qmod.load_queue(p)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["local_path"], "/tmp/a.npz")

        qmod.dequeue_success("/tmp/a.npz", path=p)
        self.assertEqual(qmod.load_queue(p), [])

    def test_enqueue_duplicate_skips_second(self):
        p = self.tmp
        item = {"local_path": "/x/y.csv", "subfolder": "processed", "attempts": 0, "dead_letter": False}
        self.assertTrue(qmod.enqueue(item, path=p))
        self.assertTrue(qmod.enqueue(item, path=p))  # duplicate returns True, no second row
        self.assertEqual(len(qmod.load_queue(p)), 1)

    def test_max_queue_size(self):
        p = self.tmp
        for i in range(3):
            ok = qmod.enqueue(
                {
                    "local_path": f"/f{i}.npz",
                    "subfolder": "raw",
                    "attempts": 0,
                    "dead_letter": False,
                },
                path=p,
                max_size=3,
            )
            self.assertTrue(ok)
        ok = qmod.enqueue(
            {"local_path": "/overflow.npz", "subfolder": "raw", "attempts": 0, "dead_letter": False},
            path=p,
            max_size=3,
        )
        self.assertFalse(ok)

    def test_count_pending_and_dead_letter(self):
        p = self.tmp
        qmod.save_queue(
            [
                {"local_path": "/a", "subfolder": "raw", "dead_letter": False},
                {"local_path": "/b", "subfolder": "raw", "dead_letter": True},
            ],
            path=p,
        )
        self.assertEqual(qmod.count_pending(p), 1)


if __name__ == "__main__":
    unittest.main()
