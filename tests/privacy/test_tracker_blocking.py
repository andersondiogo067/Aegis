import unittest

from privacy.tracker_blocking import compile_dnr_rules, parse_domain_list


class TrackerBlockingTests(unittest.TestCase):
    def test_parses_hosts_and_plain_domain_lists_locally(self):
        source = """
        # trusted list
        0.0.0.0 tracker.example
        analytics.example
        127.0.0.1 localhost
        invalid domain
        """

        self.assertEqual(
            parse_domain_list(source),
            ["analytics.example", "tracker.example"],
        )

    def test_compiles_third_party_block_rules(self):
        rules = compile_dnr_rules(["tracker.example"])

        self.assertEqual(rules[0]["action"], {"type": "block"})
        self.assertEqual(rules[0]["condition"]["urlFilter"], "||tracker.example^")
        self.assertEqual(rules[0]["condition"]["domainType"], "thirdParty")
        self.assertIn("script", rules[0]["condition"]["resourceTypes"])
        self.assertIn("image", rules[0]["condition"]["resourceTypes"])


if __name__ == "__main__":
    unittest.main()
