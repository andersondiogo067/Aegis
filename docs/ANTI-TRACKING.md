# Phase 3 — Anti-tracking and fingerprint design

## Tracker blocking

`tracker_blocking.py` parses hosts/plain-domain inputs and compiles local Chromium Declarative Net Request rules. Rules apply only to third-party subresources to reduce breakage. A small reviewed bootstrap set ships in-tree. A larger StevenBlack Unified Hosts snapshot is pinned by immutable Git commit and SHA-256; `update_filter_list.py` downloads at most 10 MB and atomically installs only an exact hash match. Browsing history and visited URLs never leave the machine for classification.

The development MV3 ruleset is a fallback/test harness, not a claim of complete native coverage. The release design moves matching into Chromium's network service so every profile/mode receives the same protection and the dashboard can use real counters.

## Tracking URLs

Only explicit known click identifiers and the `utm_` namespace are removed, only for HTTP(S). Unknown parameters, ordering, raw encoding and fragments are preserved. Native integration belongs in a navigation throttle with a per-site breakage escape hatch.

## Fingerprint cohort

`fingerprint.py` is the single deterministic cohort definition. It standardizes Canvas/WebGL/Audio behavior, a common font cohort, 1920×1080 at DPR 1, four logical CPUs, 8 GiB exposed memory, Linux x86-64 platform, Chromium-major UA strategy, en-US/en and UTC. A page/site is deliberately not an input: there is no per-page randomization that would create a unique fingerprint.

These values are specifications consumed by downstream Blink/content patches; Python cannot by itself change renderer APIs. Until those patches compile and browser tests pass, UI must not claim full fingerprint protection.

## WebRTC and DNS

STANDARD/PRIVATE restrict WebRTC candidates to the default public interface. ANONYMOUS disables non-proxied UDP, uses Tor SOCKS5 and maps normal host resolution to failure so names are resolved through SOCKS. Native network-service enforcement and leak tests remain mandatory before release.
