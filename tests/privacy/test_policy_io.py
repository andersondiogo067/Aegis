import json
import tempfile
import unittest
from pathlib import Path

from privacy.policy import BrowserMode
from privacy.policy_io import write_managed_policy


class PolicyIOTests(unittest.TestCase):
    def test_writes_atomic_valid_json_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "managed" / "aegis.json"
            write_managed_policy(target, BrowserMode.STANDARD)

            data = json.loads(target.read_text())
            self.assertTrue(data["BlockThirdPartyCookies"])
            self.assertFalse(data["SearchSuggestEnabled"])
            self.assertEqual(target.stat().st_mode & 0o777, 0o644)


if __name__ == "__main__":
    unittest.main()
