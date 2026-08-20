# Architecture

Aegis is maintained as a thin downstream of Chromium rather than a permanent source fork.

```
Chromium pinned stable source
        |
verified downstream patch series
        |
privacy policy/defaults + native integration
        |
GN release build (sandbox and Site Isolation preserved)
        |
privacy/regression tests
```

## Components

- `patches/`: ordered, reviewable patches applied to the pinned Chromium checkout.
- `privacy/`: declarative mode policies and testable controller code shared by tooling/tests.
- `scripts/`: bootstrap, patch application, build, launch and auditing helpers.
- `tests/`: unit and integration/privacy tests.
- `branding/`: product names and minimal visual assets.
- `build/`: pinned build metadata and GN arguments; generated outputs are ignored.

## Profiles and modes

- STANDARD: persistent dedicated profile, strong privacy defaults.
- PRIVATE: isolated ephemeral profile removed at shutdown.
- ANONYMOUS: isolated ephemeral profile, SOCKS5 through audited Tor, remote DNS through proxy, WebRTC restrictions, and fail-closed connectivity checks.

No mode disables sandboxing, Site Isolation, certificate validation, or process separation. Anonymous never falls back to a direct route.

## Upstream maintenance

The Chromium version is pinned in `CHROMIUM_VERSION`. Updating it requires reapplying the patch series, rebuilding, running privacy and regression tests, and recording the new version/toolchain in `docs/CHANGES.md`.
