"""Tor health verification and fail-closed connection gate."""

import re
import socket
from collections.abc import Callable
from pathlib import Path

_PROGRESS = re.compile(r"\bPROGRESS=(\d{1,3})\b")


class TorUnavailable(RuntimeError):
    pass


def parse_bootstrap_progress(control_response: str) -> int | None:
    match = _PROGRESS.search(control_response)
    if match is None:
        return None
    progress = int(match.group(1))
    return progress if 0 <= progress <= 100 else None


def _read_control_reply(connection: socket.socket) -> str:
    chunks: list[bytes] = []
    total = 0
    while total < 64 * 1024:
        chunk = connection.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        payload = b"".join(chunks)
        if payload.endswith(b"250 OK\r\n") or payload.startswith(b"5"):
            return payload.decode("utf-8", errors="replace")
    raise TorUnavailable("incomplete or oversized Tor control response")


class TorHealthVerifier:
    def __init__(
        self,
        socks_address: tuple[str, int],
        control_address: tuple[str, int],
        cookie_path: Path,
        timeout: float = 2.0,
    ):
        self.socks_address = socks_address
        self.control_address = control_address
        self.cookie_path = cookie_path
        self.timeout = timeout

    def _socks_ready(self) -> bool:
        with socket.create_connection(self.socks_address, timeout=self.timeout) as connection:
            connection.sendall(b"\x05\x01\x00")
            return connection.recv(2) == b"\x05\x00"

    def _control_ready(self) -> bool:
        cookie = self.cookie_path.read_bytes()
        if not cookie:
            return False
        with socket.create_connection(self.control_address, timeout=self.timeout) as connection:
            connection.sendall(f"AUTHENTICATE {cookie.hex()}\r\n".encode("ascii"))
            if not _read_control_reply(connection).startswith("250"):
                return False

            connection.sendall(b"GETINFO status/bootstrap-phase\r\n")
            if parse_bootstrap_progress(_read_control_reply(connection)) != 100:
                return False

            connection.sendall(b"GETINFO status/circuit-established\r\n")
            circuit = _read_control_reply(connection)
            if "status/circuit-established=1" not in circuit:
                return False

            connection.sendall(b"GETINFO net/listeners/socks\r\n")
            listeners = _read_control_reply(connection)
            expected = f'"{self.socks_address[0]}:{self.socks_address[1]}"'
            return expected in listeners

    def is_ready(self) -> bool:
        try:
            return self._socks_ready() and self._control_ready()
        except (OSError, TimeoutError, TorUnavailable):
            return False


class FailClosedGate:
    """Allow connections only after the current Tor health check succeeds."""

    def __init__(self, health_check: Callable[[], bool]):
        self._health_check = health_check
        self._allowed = False

    @property
    def allowed(self) -> bool:
        return self._allowed

    def refresh(self) -> bool:
        try:
            self._allowed = self._health_check() is True
        except (OSError, TimeoutError):
            self._allowed = False
        return self._allowed

    def require_connection(self) -> None:
        if not self._allowed:
            raise TorUnavailable("Tor is unavailable; Anonymous connections are blocked")
