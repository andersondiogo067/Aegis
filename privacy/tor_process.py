"""Dedicated, ephemeral Tor session process configuration."""

import shutil
import socket
import subprocess
import tempfile
import time
from pathlib import Path
from types import TracebackType

from .tor_controller import TorHealthVerifier, TorUnavailable


def _quote(path: Path) -> str:
    return '"' + str(path).replace("\\", "\\\\").replace('"', '\\"') + '"'


def torrc_text(session_root: Path, socks_port: int, control_port: int) -> str:
    if not 1 <= socks_port <= 65535 or not 1 <= control_port <= 65535:
        raise ValueError("Tor ports must be between 1 and 65535")
    if socks_port == control_port:
        raise ValueError("Tor SOCKS and control ports must differ")
    data = session_root / "data"
    cookie = session_root / "control.authcookie"
    return "\n".join(
        [
            "ClientOnly 1",
            f"DataDirectory {_quote(data)}",
            f"SocksPort 127.0.0.1:{socks_port} IsolateDestAddr IsolateDestPort",
            f"ControlPort 127.0.0.1:{control_port}",
            "CookieAuthentication 1",
            f"CookieAuthFile {_quote(cookie)}",
            "CookieAuthFileGroupReadable 0",
            "SafeSocks 1",
            "TestSocks 1",
            "AvoidDiskWrites 1",
            "RunAsDaemon 0",
            "Log notice stdout",
            "",
        ]
    )


def _free_loopback_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


class TorSession:
    """Own a dedicated Tor process and delete all session data at exit."""

    def __init__(
        self,
        state_root: Path,
        tor_executable: Path | None = None,
        timeout: float = 120.0,
    ):
        resolved = str(tor_executable) if tor_executable is not None else shutil.which("tor")
        self.tor_executable = Path(resolved) if resolved else Path("/missing/tor")
        self.state_root = state_root.expanduser().resolve()
        self.timeout = timeout
        self.session_root: Path | None = None
        self.process: subprocess.Popen[str] | None = None
        self.socks_port: int | None = None
        self.control_port: int | None = None
        self.verifier: TorHealthVerifier | None = None

    def __enter__(self) -> "TorSession":
        if not self.tor_executable.is_file():
            raise FileNotFoundError(f"Tor executable not found: {self.tor_executable}")
        self.state_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.session_root = Path(tempfile.mkdtemp(prefix="anonymous-", dir=self.state_root))
        self.session_root.chmod(0o700)
        self.socks_port = _free_loopback_port()
        self.control_port = _free_loopback_port()
        while self.control_port == self.socks_port:
            self.control_port = _free_loopback_port()
        torrc = self.session_root / "torrc"
        torrc.write_text(torrc_text(self.session_root, self.socks_port, self.control_port))
        torrc.chmod(0o600)
        try:
            self.process = subprocess.Popen(
                [str(self.tor_executable), "-f", str(torrc)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                text=True,
            )
            self.verifier = TorHealthVerifier(
                ("127.0.0.1", self.socks_port),
                ("127.0.0.1", self.control_port),
                self.session_root / "control.authcookie",
            )
            deadline = time.monotonic() + self.timeout
            while time.monotonic() < deadline and self.process.poll() is None:
                if self.verifier.is_ready():
                    return self
                time.sleep(0.25)
            raise TorUnavailable("Tor did not reach verified 100% bootstrap before timeout")
        except BaseException:
            self._stop_and_clean()
            raise

    def _stop_and_clean(self) -> None:
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)
        if self.session_root is not None and self.session_root.exists():
            if self.session_root.parent != self.state_root:
                raise RuntimeError("refusing to remove Tor data outside session root")
            shutil.rmtree(self.session_root)
        self.session_root = None

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._stop_and_clean()
