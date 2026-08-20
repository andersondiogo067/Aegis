# Phase 5 — Interface and validation

## Interface

`scripts/aegis-browser` selects STANDARD, PRIVATE or ANONYMOUS and then launches Chromium's native tabs, navigation, address bar, downloads and applicable history/bookmarks. PRIVATE/ANONYMOUS are incognito plus independently ephemeral profiles. ANONYMOUS opens a purple, explicit warning dashboard and is monitored against Tor health.

The local dashboard is evidence-driven. It never prints a protection as active without a corresponding runtime/configuration fact, and never prints “Tor conectado” unless authenticated Tor control, circuit, listener and SOCKS evidence passed. Tracker counts and native fingerprint protection remain “não verificado” until native enforcement publishes counters/evidence.

```
scripts/aegis-browser --mode standard --chromium /path/to/chromium
scripts/aegis-browser --mode private --chromium /path/to/chromium
scripts/aegis-browser --mode anonymous --chromium /path/to/chromium
```

This is a development launcher, not the final patched Chromium UI. A native mode selector, chrome-level Anonymous color treatment and dashboard plumbing are blocked on the x86-64 Chromium build/patch environment.

## Fingerprint diagnostics

Open `diagnostics/fingerprint.html`. It locally records navigator/UA hints, locale/timezone, screen/DPR, Canvas hash, WebGL values, OfflineAudio hash and a small font availability cohort, and can save JSON for comparison. Nothing is uploaded.

Fixed screen values are not claimed without real letterboxing. Canvas/Audio/WebGL remain explicitly pending until a coherent renderer patch keeps JS, headers, Client Hints and media queries consistent.

## Network audit

`scripts/audit_external_connections.py --output report.json -- COMMAND ...` traces process-level IPv4 `connect()` destinations. It was exercised with curl and exposed DNS/TCP destinations. It is a triage tool, not a substitute for release packet capture covering IPv6, UDP, DNS, DoH and child sandbox behavior.

See `tests/privacy/TEST-MATRIX.md` for exact PASS/BLOCKED state.
