# Phase 4 — Anonymous mode with Tor

## Implemented controller

Anonymous creates both a unique 0700 browser profile and a dedicated ephemeral Tor process/data directory. Tor binds unique loopback-only SOCKS and authenticated control listeners. The SOCKS listener uses Tor-supported `IsolateDestAddr` and `IsolateDestPort`; a distinct listener/process per Anonymous session prevents cross-session circuit reuse without inventing a protocol.

The controller enters ready state only after all of these succeed:

1. SOCKS5 no-auth negotiation on the exact listener;
2. control-port COOKIE authentication;
3. `status/bootstrap-phase` reports `PROGRESS=100`;
4. `status/circuit-established=1`;
5. `net/listeners/socks` contains the exact expected endpoint.

The opt-in live test additionally requests the official Tor check API through `curl --socks5-hostname` and requires `IsTor=true`.

## Fail-closed behavior

Chromium receives a fixed SOCKS proxy, explicit removal of Chromium's implicit loopback bypass, system resolver denial, QUIC disabled, and `disable_non_proxied_udp` for WebRTC. There is no PAC/WPAD or DIRECT fallback. If the dedicated Tor process stops, the proxy listener disappears, so proxied TCP cannot silently switch direct; the monitor also terminates Chromium when health evidence is lost.

This is a strong launcher-level prototype, **not yet a claim of complete native egress confinement**. Chromium's SOCKS client transports TCP only and does not send Tor SOCKS-auth isolation credentials. A release-quality native patch must install an egress gate before any profile or system `NetworkContext`, deny all other TCP/UDP/DNS/DoH/DoT sockets, and invalidate contexts on Tor loss. Until that patch is compiled and packet-capture tests pass, the dashboard must label Anonymous as development/limited.

## Run

```
scripts/aegis-anonymous --chromium /path/to/chromium https://check.torproject.org/
```

Tor 0.4.9.6 was installed and tested on the preparation host. The live integration test confirmed a Tor route, fail-closed health after process termination, and deletion of ephemeral Tor data:

```
python3 tests/privacy/run_tor_integration.py
```

No perfect-anonymity claim is made. For high-risk use, prefer the official Tor Browser until the native egress and renderer patches are built and independently reviewed.
