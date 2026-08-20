import unittest

from privacy.fingerprint import fingerprint_profile
from privacy.policy import BrowserMode


class FingerprintTests(unittest.TestCase):
    def test_profile_is_stable_across_calls_and_sites(self):
        first = fingerprint_profile(BrowserMode.STANDARD)
        second = fingerprint_profile(BrowserMode.STANDARD)

        self.assertEqual(first, second)
        self.assertEqual(first.canvas, "standardize")
        self.assertEqual(first.webgl, "standardize")
        self.assertEqual(first.audio_context, "standardize")
        self.assertEqual(first.timezone, "UTC")
        self.assertEqual(first.hardware_concurrency, 4)
        self.assertEqual(first.device_memory_gib, 8)

    def test_anonymous_uses_common_fixed_cohort_not_random_values(self):
        profile = fingerprint_profile(BrowserMode.ANONYMOUS)

        self.assertEqual(profile.screen, (1920, 1080))
        self.assertEqual(profile.device_pixel_ratio, 1.0)
        self.assertEqual(profile.platform, "Linux x86_64")
        self.assertEqual(profile.languages, ("en-US", "en"))
        self.assertFalse(profile.per_site_randomization)


if __name__ == "__main__":
    unittest.main()
