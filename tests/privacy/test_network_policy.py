import unittest

from privacy.network_policy import chromium_network_flags
from privacy.policy import BrowserMode


class NetworkPolicyTests(unittest.TestCase):
    def test_standard_limits_webrtc_to_default_public_interface(self):
        flags = chromium_network_flags(BrowserMode.STANDARD)
        self.assertIn("--force-webrtc-ip-handling-policy=default_public_interface_only", flags)

    def test_anonymous_disables_non_proxied_udp_and_uses_socks_remote_dns(self):
        flags = chromium_network_flags(BrowserMode.ANONYMOUS, socks_port=9150)
        self.assertIn("--force-webrtc-ip-handling-policy=disable_non_proxied_udp", flags)
        self.assertIn("--proxy-server=socks5://127.0.0.1:9150", flags)
        self.assertIn("--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1", flags)
        self.assertNotIn("--proxy-bypass-list=*", flags)


if __name__ == "__main__":
    unittest.main()
