# Reproducible build

## Supported release builder

Use a native Linux x86-64 machine or CI runner with at least 16 GiB RAM (32 GiB recommended), 200 GiB free SSD space, and a supported Ubuntu/Debian release. The current ARM64 PRoot host is preparation/test-only.

## Source pin

`CHROMIUM_VERSION` pins the selected stable Chromium release. The initial pin is 151.0.7922.173, obtained from the official ChromiumDash Stable/Linux feed on 2026-08-20.

## Procedure

1. Install Git, Python 3, depot_tools and Chromium Linux build dependencies.
2. Run `scripts/bootstrap_source.sh` to fetch and sync the pinned source.
3. Run `scripts/apply_patches.sh` to apply the ordered patch series.
4. Generate with `gn gen src/out/Aegis --args="$(tr '
' ' ' < build/args.gn)"`.
5. Build with `autoninja -C src/out/Aegis chrome`.
6. Run `scripts/verify_security_flags.sh` and the privacy tests.

The scripts abort on non-x86-64 for a release build and never add `--no-sandbox` or `--ignore-certificate-errors`.

## Update flow

Update the pin, sync source, reapply/rebase every patch, build, run all privacy/regression tests, review external-connection audit results, then update `docs/CHANGES.md`.
