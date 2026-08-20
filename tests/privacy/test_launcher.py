import unittest
from pathlib import Path

from privacy.launcher import build_chromium_command
from privacy.policy import BrowserMode


class LauncherTests(unittest.TestCase):
    def test_standard_command_uses_only_its_profile_and_safe_flags(self):
        command = build_chromium_command(
            executable=Path("/usr/bin/chromium"),
            mode=BrowserMode.STANDARD,
            profile=Path("/tmp/aegis/standard"),
            urls=["https://example.test"],
        )

        self.assertEqual(command[0], "/usr/bin/chromium")
        self.assertIn("--user-data-dir=/tmp/aegis/standard", command)
        self.assertIn("https://example.test", command)
        self.assertNotIn("--incognito", command)
        self.assertNotIn("--no-sandbox", command)
        self.assertNotIn("--ignore-certificate-errors", command)

    def test_private_command_adds_incognito_defense_in_depth(self):
        command = build_chromium_command(
            executable=Path("/usr/bin/chromium"),
            mode=BrowserMode.PRIVATE,
            profile=Path("/tmp/aegis/private"),
            urls=[],
        )

        self.assertIn("--incognito", command)


if __name__ == "__main__":
    unittest.main()
