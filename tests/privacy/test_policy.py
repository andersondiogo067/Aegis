import unittest

from privacy.policy import BrowserMode, chromium_managed_policy, policy_for


class PrivacyPolicyTests(unittest.TestCase):
    def test_standard_defaults_are_private_without_disabling_security(self):
        policy = policy_for(BrowserMode.STANDARD)

        self.assertTrue(policy.block_third_party_cookies)
        self.assertTrue(policy.https_only)
        self.assertFalse(policy.search_suggestions)
        self.assertFalse(policy.network_prediction)
        self.assertTrue(policy.site_isolation)
        self.assertTrue(policy.sandbox)
        self.assertTrue(policy.tls_validation)
        self.assertFalse(policy.ephemeral_profile)

    def test_chromium_policy_disables_remote_suggestions_and_prediction(self):
        managed = chromium_managed_policy(policy_for(BrowserMode.STANDARD))

        self.assertIs(managed["BlockThirdPartyCookies"], True)
        self.assertIs(managed["SearchSuggestEnabled"], False)
        self.assertEqual(managed["NetworkPredictionOptions"], 2)
        self.assertEqual(managed["HttpsOnlyMode"], "force_enabled")
        self.assertNotIn("DisableSiteIsolation", managed)

    def test_private_policy_requests_data_cleanup_at_exit(self):
        managed = chromium_managed_policy(policy_for(BrowserMode.PRIVATE))

        self.assertIn("cookies_and_other_site_data", managed["ClearBrowsingDataOnExitList"])
        self.assertIn("cached_images_and_files", managed["ClearBrowsingDataOnExitList"])

    def test_private_is_ephemeral_and_does_not_share_standard_storage(self):
        policy = policy_for(BrowserMode.PRIVATE)

        self.assertTrue(policy.ephemeral_profile)
        self.assertTrue(policy.separate_profile)
        self.assertTrue(policy.clear_on_exit)

    def test_sensitive_permissions_default_to_ask(self):
        policy = policy_for(BrowserMode.STANDARD)

        for permission in (
            "camera",
            "microphone",
            "geolocation",
            "notifications",
            "clipboard",
            "bluetooth",
            "usb",
            "serial",
            "midi",
            "filesystem",
        ):
            self.assertEqual(policy.permissions[permission], "ask", permission)


if __name__ == "__main__":
    unittest.main()
