"""Network leak-resistance flags for Chromium integration."""

from .policy import BrowserMode


def chromium_network_flags(mode: BrowserMode, socks_port: int | None = None) -> list[str]:
    if mode is not BrowserMode.ANONYMOUS:
        return ["--force-webrtc-ip-handling-policy=default_public_interface_only"]
    if socks_port is None or not 1 <= socks_port <= 65535:
        raise ValueError("Anonymous mode requires a valid Tor SOCKS port")
    return [
        "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
        f"--proxy-server=socks5://127.0.0.1:{socks_port}",
        "--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE 127.0.0.1",
    ]
