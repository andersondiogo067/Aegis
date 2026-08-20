import socket
import tempfile
import threading
import unittest
from pathlib import Path

from privacy.tor_controller import (
    FailClosedGate,
    TorHealthVerifier,
    TorUnavailable,
    parse_bootstrap_progress,
)


class TorControllerTests(unittest.TestCase):
    @staticmethod
    def _serve_once(listener, handler, errors):
        try:
            connection, _ = listener.accept()
            with connection:
                handler(connection)
        except BaseException as error:
            errors.append(error)
        finally:
            listener.close()

    def test_health_verifier_requires_socks_handshake_and_complete_control_bootstrap(self):
        socks = socket.socket()
        socks.bind(("127.0.0.1", 0))
        socks.listen(1)
        socks_port = socks.getsockname()[1]
        control = socket.socket()
        control.bind(("127.0.0.1", 0))
        control.listen(1)

        def socks_handler(connection):
            self.assertEqual(connection.recv(3), b"\x05\x01\x00")
            connection.sendall(b"\x05\x00")

        def control_handler(connection):
            auth = connection.recv(256)
            self.assertIn(b"AUTHENTICATE 0102", auth)
            connection.sendall(b"250 OK\r\n")
            query = connection.recv(256)
            self.assertIn(b"GETINFO status/bootstrap-phase", query)
            connection.sendall(
                b'250-status/bootstrap-phase=NOTICE BOOTSTRAP PROGRESS=100 TAG=done SUMMARY="Done"\r\n250 OK\r\n'
            )
            circuit = connection.recv(256)
            self.assertIn(b"GETINFO status/circuit-established", circuit)
            connection.sendall(b"250-status/circuit-established=1\r\n250 OK\r\n")
            listeners = connection.recv(256)
            self.assertIn(b"GETINFO net/listeners/socks", listeners)
            expected = f'250-net/listeners/socks="127.0.0.1:{socks_port}"\r\n250 OK\r\n'
            connection.sendall(expected.encode("ascii"))

        errors = []
        threads = [
            threading.Thread(target=self._serve_once, args=(socks, socks_handler, errors)),
            threading.Thread(target=self._serve_once, args=(control, control_handler, errors)),
        ]
        for thread in threads:
            thread.start()
        with tempfile.TemporaryDirectory() as directory:
            cookie = Path(directory) / "control.authcookie"
            cookie.write_bytes(b"\x01\x02")
            verifier = TorHealthVerifier(
                socks_address=("127.0.0.1", socks_port),
                control_address=control.getsockname(),
                cookie_path=cookie,
                timeout=1,
            )
            ready = verifier.is_ready()
        for thread in threads:
            thread.join(timeout=2)
            self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        self.assertTrue(ready)

    def test_parses_only_complete_tor_bootstrap_as_ready(self):
        self.assertEqual(
            parse_bootstrap_progress('250-status/bootstrap-phase=NOTICE BOOTSTRAP PROGRESS=100 TAG=done SUMMARY="Done"\r\n250 OK\r\n'),
            100,
        )
        self.assertEqual(
            parse_bootstrap_progress('250-status/bootstrap-phase=NOTICE BOOTSTRAP PROGRESS=80 TAG=ap_conn SUMMARY="Connecting"\r\n250 OK\r\n'),
            80,
        )

    def test_gate_starts_blocked_and_fails_closed_after_health_loss(self):
        health = iter([True, False])
        gate = FailClosedGate(lambda: next(health))

        self.assertTrue(gate.refresh())
        gate.require_connection()
        self.assertFalse(gate.refresh())
        with self.assertRaises(TorUnavailable):
            gate.require_connection()


if __name__ == "__main__":
    unittest.main()
