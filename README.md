# Aegis Browser

A personal Chromium downstream/patch stack focused on strong privacy defaults and an optional Tor-backed Anonymous mode.

## Current state

The preparation host cannot compile Chromium: it is ARM64/PRoot with 7.4 GiB RAM and only 69 GiB free, while the supported release target is native Linux x86-64 with at least 200 GiB free. No Chromium binary or native-patch build is falsely claimed.

Host-capable deliverables are implemented and tested:

- pinned Chromium 151.0.7922.173 build/update workflow;
- audited M151 privacy policy generation;
- STANDARD/PRIVATE/ANONYMOUS profile separation and cleanup;
- local verified filter-list/DNR tooling and tracking-URL cleanup core;
- deterministic anti-fingerprint specification with unverified surfaces explicitly marked pending;
- dedicated authenticated Tor sessions and fail-closed Anonymous development launcher;
- evidence-driven dashboard, fingerprint diagnostic page and external-network audit harness;
- x86-64 self-hosted CI build workflow and an exact PASS/BLOCKED test matrix.

## Quick checks

```bash
scripts/test_all.sh
AEGIS_LIVE_TOR=1 scripts/test_all.sh
```

## Development launcher

```bash
scripts/aegis-browser --mode standard --chromium /path/to/chromium
scripts/aegis-browser --mode private --chromium /path/to/chromium
scripts/aegis-browser --mode anonymous --chromium /path/to/chromium
```

This launcher is not a substitute for the pending native Chromium patches. For high-risk anonymity, use the official Tor Browser until Aegis's native egress gate and renderer changes compile, pass packet-capture/browser tests and receive independent review.

Security invariants: Chromium sandbox, Site Isolation, TLS certificate validation, process separation, component/security updates and critical-fix Variations remain enabled. Unsafe normal-use flags are rejected.
