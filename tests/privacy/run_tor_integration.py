#!/usr/bin/env python3
"""Opt-in live Tor integration test; requires tor, curl and network."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from privacy.tor_process import TorSession


def main() -> int:
    tor = shutil.which("tor")
    curl = shutil.which("curl")
    if not tor or not curl:
        print("SKIP: tor and curl are required")
        return 77
    with tempfile.TemporaryDirectory(prefix="aegis-tor-test-") as directory:
        state = Path(directory)
        with TorSession(state) as session:
            assert session.socks_port is not None
            assert session.verifier is not None
            result = subprocess.run(
                [
                    curl,
                    "--fail",
                    "--silent",
                    "--show-error",
                    "--max-time",
                    "30",
                    "--socks5-hostname",
                    f"127.0.0.1:{session.socks_port}",
                    "https://check.torproject.org/api/ip",
                ],
                text=True,
                capture_output=True,
                check=True,
            )
            status = json.loads(result.stdout)
            if status.get("IsTor") is not True:
                raise RuntimeError(f"Tor endpoint did not confirm Tor route: {status}")
            print(json.dumps({"tor_ready": True, "route_confirmed": True}))
            verifier = session.verifier
        if verifier.is_ready():
            raise RuntimeError("fail-closed check failed: health remained ready after Tor stopped")
        if list(state.iterdir()):
            raise RuntimeError("ephemeral Tor session data was not removed")
        print("fail_closed_after_tor_stop: PASS")
        print("ephemeral_tor_data_cleanup: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
