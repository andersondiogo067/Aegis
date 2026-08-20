import unittest
from pathlib import Path


class DiagnosticPageTests(unittest.TestCase):
    def test_fingerprint_page_covers_required_browser_surfaces(self):
        page = (Path(__file__).resolve().parents[2] / "diagnostics/fingerprint.html").read_text()
        for token in (
            "navigator.hardwareConcurrency",
            "navigator.deviceMemory",
            "navigator.languages",
            "Intl.DateTimeFormat",
            "screen.width",
            "devicePixelRatio",
            "WEBGL_debug_renderer_info",
            "canvas",
            "OfflineAudioContext",
            "document.fonts.check",
        ):
            self.assertIn(token, page)


if __name__ == "__main__":
    unittest.main()
