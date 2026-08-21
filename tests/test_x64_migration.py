import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/setup-x64-builder.sh"
DOC = ROOT / "docs/X64-MIGRATION.md"


class X64MigrationTests(unittest.TestCase):
    def test_setup_script_has_guarded_reproducible_pipeline(self):
        self.assertTrue(SCRIPT.is_file())
        self.assertTrue(os.access(SCRIPT, os.X_OK))
        text = SCRIPT.read_text()
        for token in (
            "Linux",
            "x86_64",
            "CHROMIUM_VERSION",
            "depot_tools",
            "fetch --nohooks chromium",
            "gclient sync",
            "install-build-deps.sh",
            "apply_patches.sh",
            "gn gen",
            "autoninja",
            "-n",
            "verify_security_flags.sh",
        ):
            self.assertIn(token, text)
        self.assertNotIn("--no-sandbox", text)
        self.assertNotIn("--ignore-certificate-errors", text)

    def test_workflow_uses_the_single_x64_setup_entrypoint(self):
        workflow = (ROOT / ".github/workflows/chromium-x64.yml").read_text()
        self.assertIn("runs-on: [self-hosted, linux, x64, chromium-builder]", workflow)
        self.assertIn("scripts/setup-x64-builder.sh --build", workflow)
        self.assertIn("scripts/test_all.sh", workflow)

    def test_migration_document_names_exact_commands_and_blockers(self):
        self.assertTrue(DOC.is_file())
        text = DOC.read_text()
        for token in (
            "scripts/setup-x64-builder.sh",
            "151.0.7922.173",
            "patches/series",
            "git am --3way",
            "out/Aegis",
            "autoninja -C",
            "BLOCKED",
            "Tor Browser",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
