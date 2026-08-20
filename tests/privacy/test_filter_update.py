import hashlib
import tempfile
import unittest
from pathlib import Path

from privacy.filter_update import install_verified_filter


class FilterUpdateTests(unittest.TestCase):
    def test_installs_only_content_matching_pinned_sha256(self):
        payload = b"0.0.0.0 tracker.example\n"
        expected = hashlib.sha256(payload).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "trackers.txt"
            install_verified_filter(payload, expected, target)
            self.assertEqual(target.read_bytes(), payload)

    def test_rejects_hash_mismatch_without_replacing_existing_list(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "trackers.txt"
            target.write_bytes(b"known-good")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                install_verified_filter(b"tampered", "0" * 64, target)
            self.assertEqual(target.read_bytes(), b"known-good")


if __name__ == "__main__":
    unittest.main()
