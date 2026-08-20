import unittest

from privacy.dashboard import ProtectionEvidence, render_dashboard
from privacy.policy import BrowserMode


class DashboardTests(unittest.TestCase):
    def test_never_claims_tor_connected_without_verified_evidence(self):
        html = render_dashboard(
            ProtectionEvidence(mode=BrowserMode.ANONYMOUS, tor_verified=False)
        )

        self.assertNotIn("Tor: conectado", html)
        self.assertIn("Tor: BLOQUEADO / não verificado", html)

    def test_reports_only_supplied_verified_protections(self):
        html = render_dashboard(
            ProtectionEvidence(
                mode=BrowserMode.ANONYMOUS,
                trackers_blocked=7,
                cookies_third_party_blocked=True,
                fingerprint_verified=False,
                https_only=True,
                webrtc_protected=True,
                tor_verified=True,
            )
        )

        self.assertIn("Trackers bloqueados: 7", html)
        self.assertIn("Tor: conectado (verificado)", html)
        self.assertIn("Fingerprint: não verificado", html)


if __name__ == "__main__":
    unittest.main()
