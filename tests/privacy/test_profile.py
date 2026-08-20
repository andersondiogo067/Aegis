import tempfile
import unittest
from pathlib import Path

from privacy.policy import BrowserMode
from privacy.profile import BrowserProfile


class BrowserProfileTests(unittest.TestCase):
    def test_standard_profile_persists(self):
        with tempfile.TemporaryDirectory() as state:
            with BrowserProfile(BrowserMode.STANDARD, Path(state)) as path:
                marker = path / "marker"
                marker.write_text("keep")

            self.assertTrue(marker.exists())
            self.assertEqual(path.stat().st_mode & 0o777, 0o700)

    def test_private_profile_is_removed_on_exit(self):
        with tempfile.TemporaryDirectory() as state:
            with BrowserProfile(BrowserMode.PRIVATE, Path(state)) as path:
                self.assertTrue(path.exists())
                self.assertNotIn("standard", path.parts)
                (path / "Cookies").write_text("secret")

            self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
