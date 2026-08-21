# Changes

## 2026-08-20 — Native patch preparation

- Retrieved exact Chromium M151 source files through Gitiles after the promisor sparse clone repeatedly timed out.
- Added the first real `git am` patch for user-overridable background-mode and network-prediction defaults.
- Verified the patch with `git apply --check` and isolated `git am --3way` against clean exact M151 files; compilation remains blocked.
- Added a conservative native tracking-URL utility with C++ unit tests, using exact M151 `GURL` APIs; throttle/browser integration remains blocked.
- Produced isolated tracking/fingerprint candidate and Anonymous egress pseudodiff drafts for review without modifying unrelated native surfaces.
- Excluded ignored `build/work` research artifacts from the security flag scanner while retaining scans of build configuration, scripts and privacy code.

## 2026-08-20 — Phase 5

- Added unified STANDARD/PRIVATE/ANONYMOUS development launcher and evidence-driven Privacy Dashboard.
- Added local fingerprint diagnostics covering navigator, locale/timezone, screen, Canvas, WebGL, Audio and fonts.
- Added process-level external connection audit tooling and exercised it with a real HTTPS request.
- Expanded verified M151 privacy/background-network/permission policies while preserving component updates and critical-fix Variations.
- Corrected fingerprint scope: no fixed screen claim without letterboxing and no Canvas/Audio/WebGL claim before coherent native patches.
- Added exact PASS/BLOCKED privacy test matrix, host test runner and x86-64 self-hosted build workflow.

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
