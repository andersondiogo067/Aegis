# Changes

## 2026-08-20 — Phase 4

- Added dedicated ephemeral Tor session processes with loopback-only SOCKS/control listeners and Tor-supported isolation flags.
- Added authenticated control-port verification of bootstrap, circuit and exact SOCKS listener state.
- Added fixed-proxy Anonymous launch, remote-DNS enforcement, loopback-bypass removal, QUIC disablement and WebRTC non-proxied UDP denial.
- Added runtime Tor health monitoring, blocked-state behavior and ephemeral Tor/profile cleanup.
- Installed Tor 0.4.9.6 and passed the opt-in live Tor route and fail-closed integration test.
- Explicitly documented the remaining native egress-gate requirement instead of claiming complete anonymity.

## 2026-08-20 — Phase 3

- Added conservative tracking-parameter stripping with raw-query preservation.
- Added local domain-list parsing and third-party Chromium DNR compilation.
- Pinned a trusted filter-list snapshot by immutable commit and SHA-256; downloads are bounded and installed atomically only after verification.
- Added a deterministic shared fingerprint cohort specification with no per-site randomization.
- Added WebRTC/DNS leak-resistance network policy and documented required native Chromium integration.
- Added a development MV3 ruleset and an explicit upstream patch map without falsely claiming unbuilt patches.

## 2026-08-20 — Phase 2

- Added strong managed-policy defaults, prompt-based sensitive permissions and HTTPS-only mode.
- Added separate persistent/ephemeral profile lifecycle with guarded cleanup.
- Added atomic policy generation and safe Chromium command construction.

## 2026-08-20 — Phase 1

- Initialized the Aegis Browser downstream repository and directory layout.
- Recorded live environment diagnosis and local-build blocker honestly.
- Pinned Chromium Linux Stable 151.0.7922.173.
- Defined architecture, privacy model, threat model and reproducible x86-64 build process.
- Added minimal product branding and security-preserving GN defaults.
