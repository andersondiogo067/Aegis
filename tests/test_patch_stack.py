import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PatchStackTests(unittest.TestCase):
    def test_series_contains_existing_git_am_patches(self):
        entries = [
            line.strip()
            for line in (ROOT / "patches/series").read_text().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual(
            entries,
            [
                "0001-privacy-defaults-background-prediction.patch",
                "0002-tracking-url-utils.patch",
            ],
        )
        for entry in entries:
            payload = (ROOT / "patches" / entry).read_text()
            self.assertTrue(payload.startswith("From "), entry)
            self.assertIn("Subject: [PATCH]", payload)
            self.assertNotIn("--no-sandbox", payload)
            self.assertNotIn("--ignore-certificate-errors", payload)


if __name__ == "__main__":
    unittest.main()
