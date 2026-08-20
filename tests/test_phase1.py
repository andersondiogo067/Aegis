import os
import re
import stat
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Phase1RepositoryTests(unittest.TestCase):
    def test_required_documents_exist_and_are_nonempty(self):
        for name in (
            "ARCHITECTURE.md",
            "PRIVACY-MODEL.md",
            "THREAT-MODEL.md",
            "BUILD.md",
            "CHANGES.md",
            "ENVIRONMENT.md",
        ):
            path = ROOT / "docs" / name
            self.assertTrue(path.is_file(), name)
            self.assertGreater(path.stat().st_size, 100, name)

    def test_chromium_pin_is_a_four_part_version(self):
        version = (ROOT / "CHROMIUM_VERSION").read_text().strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+\.\d+$")

    def test_release_args_preserve_security(self):
        args = (ROOT / "build" / "args.gn").read_text()
        self.assertIn("use_sandbox = true", args)
        self.assertNotIn("is_official_build = false", args)

    def test_security_verifier_rejects_unsafe_flags(self):
        probe = ROOT / "privacy" / ".unsafe-flag-probe"
        probe.write_text("--no-sandbox\n")
        try:
            result = subprocess.run(
                [str(ROOT / "scripts" / "verify_security_flags.sh")],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("forbidden", result.stderr)
        finally:
            probe.unlink(missing_ok=True)

    def test_required_scripts_are_executable(self):
        for name in (
            "bootstrap_source.sh",
            "apply_patches.sh",
            "build_linux_x64.sh",
            "verify_security_flags.sh",
        ):
            path = ROOT / "scripts" / name
            self.assertTrue(path.is_file(), name)
            self.assertTrue(path.stat().st_mode & stat.S_IXUSR, name)


if __name__ == "__main__":
    unittest.main()
