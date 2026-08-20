import unittest

from privacy.tracking_url import strip_tracking_parameters


class TrackingURLTests(unittest.TestCase):
    def test_removes_known_tracking_parameters_without_reordering_others(self):
        source = "https://shop.example/item?sku=42&utm_source=newsletter&color=blue&fbclid=abc#details"

        cleaned = strip_tracking_parameters(source)

        self.assertEqual(
            cleaned,
            "https://shop.example/item?sku=42&color=blue#details",
        )

    def test_leaves_non_http_and_unknown_parameters_unchanged(self):
        self.assertEqual(strip_tracking_parameters("mailto:a@example.test?utm_source=x"), "mailto:a@example.test?utm_source=x")
        self.assertEqual(strip_tracking_parameters("https://example.test/?custom_id=7"), "https://example.test/?custom_id=7")


if __name__ == "__main__":
    unittest.main()
