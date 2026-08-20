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

    def test_anonymous_command_is_pinned_to_tor_without_direct_fallback(self):
        command = build_chromium_command(
            executable=Path("/usr/bin/chromium"),
            mode=BrowserMode.ANONYMOUS,
            profile=Path("/tmp/aegis/anonymous"),
            urls=[],
            socks_port=19050,
        )

        self.assertIn("--proxy-server=socks5://127.0.0.1:19050", command)
        self.assertIn("--force-webrtc-ip-handling-policy=disable_non_proxied_udp", command)
        self.assertIn("--proxy-bypass-list=<-loopback>", command)
        self.assertIn("--disable-quic", command)

    def test_forbidden_security_flags_are_rejected(self):
        for unsafe in ("--no-sandbox", "--ignore-certificate-errors"):
            with self.assertRaisesRegex(ValueError, "forbidden"):
                build_chromium_command(
                    executable=Path("/usr/bin/chromium"),
                    mode=BrowserMode.STANDARD,
                    profile=Path("/tmp/aegis/standard"),
                    urls=[],
                    extra_flags=[unsafe],
                )

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
