import unittest

from privacy.network_audit import parse_strace_destinations


class NetworkAuditTests(unittest.TestCase):
    def test_extracts_and_deduplicates_ipv4_connection_destinations(self):
        trace = '''
[pid 10] connect(3, {sa_family=AF_INET, sin_port=htons(443), sin_addr=inet_addr("203.0.113.7")}, 16) = 0
[pid 11] connect(4, {sa_family=AF_INET, sin_port=htons(443), sin_addr=inet_addr("203.0.113.7")}, 16) = 0
[pid 12] connect(5, {sa_family=AF_INET, sin_port=htons(9050), sin_addr=inet_addr("127.0.0.1")}, 16) = 0
'''

        self.assertEqual(
            parse_strace_destinations(trace),
            [
                {"family": "ipv4", "address": "127.0.0.1", "port": 9050},
                {"family": "ipv4", "address": "203.0.113.7", "port": 443},
            ],
        )


if __name__ == "__main__":
    unittest.main()
