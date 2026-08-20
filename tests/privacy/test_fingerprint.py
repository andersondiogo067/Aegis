import unittest

from privacy.fingerprint import fingerprint_profile
from privacy.policy import BrowserMode


class FingerprintTests(unittest.TestCase):
    def test_profile_is_stable_across_calls_and_sites(self):
        first = fingerprint_profile(BrowserMode.STANDARD)
        second = fingerprint_profile(BrowserMode.STANDARD)

        self.assertEqual(first, second)
        self.assertEqual(first.canvas, "pending-coherent-native-patch")
        self.assertEqual(first.webgl, "pending-coherent-native-patch")
        self.assertEqual(first.audio_context, "pending-coherent-native-patch")
        self.assertEqual(first.screen_strategy, "letterbox-required")
        self.assertEqual(first.timezone, "UTC")
        self.assertEqual(first.hardware_concurrency, 4)
        self.assertEqual(first.device_memory_gib, 8)

    def test_anonymous_uses_common_fixed_cohort_not_random_values(self):
        profile = fingerprint_profile(BrowserMode.ANONYMOUS)

        self.assertIsNone(profile.screen)
        self.assertEqual(profile.screen_strategy, "letterbox-required")
        self.assertEqual(profile.device_pixel_ratio, 1.0)
        self.assertEqual(profile.platform, "Linux x86_64")
        self.assertEqual(profile.languages, ("en-US", "en"))
        self.assertFalse(profile.per_site_randomization)


if __name__ == "__main__":
    unittest.main()
