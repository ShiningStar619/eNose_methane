"""Tests for cloud config helpers."""
from __future__ import annotations

import unittest

from cloud.config import normalize_drive_folder_id


class TestNormalizeDriveFolderId(unittest.TestCase):
    def test_bare_id(self):
        self.assertEqual(
            normalize_drive_folder_id("1_LxYg-o9e4uQekA-Zbj-iG-NkXVBGN8i"),
            "1_LxYg-o9e4uQekA-Zbj-iG-NkXVBGN8i",
        )

    def test_id_with_usp_query(self):
        self.assertEqual(
            normalize_drive_folder_id(
                "1_LxYg-o9e4uQekA-Zbj-iG-NkXVBGN8i?usp=drive_link"
            ),
            "1_LxYg-o9e4uQekA-Zbj-iG-NkXVBGN8i",
        )

    def test_folders_url(self):
        self.assertEqual(
            normalize_drive_folder_id(
                "https://drive.google.com/drive/folders/1ABCxyz?usp=sharing"
            ),
            "1ABCxyz",
        )

    def test_open_id_query(self):
        self.assertEqual(
            normalize_drive_folder_id(
                "https://drive.google.com/open?id=1DEFghi&usp=drive_link"
            ),
            "1DEFghi",
        )

    def test_empty(self):
        self.assertEqual(normalize_drive_folder_id(""), "")
        self.assertEqual(normalize_drive_folder_id(None), "")


if __name__ == "__main__":
    unittest.main()
