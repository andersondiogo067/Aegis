import tempfile
import unittest
from pathlib import Path

from privacy.tor_process import TorSession, torrc_text


class TorProcessTests(unittest.TestCase):
    def test_missing_tor_executable_fails_without_leaving_session_data(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)
            session = TorSession(state, tor_executable=Path("/does/not/exist"), timeout=0.1)
            with self.assertRaises(FileNotFoundError):
                session.__enter__()
            self.assertEqual(list(state.iterdir()), [])

    def test_torrc_binds_loopback_and_uses_supported_isolation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = torrc_text(root, socks_port=19050, control_port=19051)

        self.assertIn("SocksPort 127.0.0.1:19050 IsolateDestAddr IsolateDestPort", config)
        self.assertIn("ControlPort 127.0.0.1:19051", config)
        self.assertIn("CookieAuthentication 1", config)
        self.assertIn("SafeSocks 1", config)
        self.assertIn("AvoidDiskWrites 1", config)
        self.assertNotIn("0.0.0.0", config)


if __name__ == "__main__":
    unittest.main()
