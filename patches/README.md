# Chromium native integration patch map

The current host cannot build a supported x86-64 Chromium tree. `patches/series` therefore contains only patches that were authored against exact files from tag `151.0.7922.173` and passed an isolated `git am --3way` application test; compilation and browser verification remain explicitly blocked.

## Current series

1. `0001-privacy-defaults-background-prediction.patch`
   - changes the user-overridable native defaults for background mode (`false`) and network prediction (`kDisabled`);
   - applied successfully with `git am --3way` to clean copies of the exact M151 files;
   - not yet compiled or browser-tested.
2. `0002-tracking-url-utils.patch`
   - adds a pure conservative HTTP(S) query cleaner and five C++ unit tests;
   - preserves unknown query pieces, ordering, duplicates, fragments and raw values;
   - uses the exact M151 `GURL::query()` API and passed isolated `git am --3way`;
   - does not integrate a navigation throttle; native compilation/tests remain blocked.
3. `0003-anonymous-egress-gate.patch`
   - adds a default-deny generation state machine and six C++ unit tests;
   - accepts only canonical IPv4/IPv6 loopback SOCKS endpoints and exact TCP address lists;
   - stale generations fail and revocation is terminal for the installed generation;
   - foundational policy only: no NetworkContext/socket integration or native fail-closed claim yet.

## Planned order

Next downstream commits should cover:

1. product branding and remaining native defaults;
2. navigation integration invoking conservative tracking-parameter removal, gated by browser tests;
3. network-service tracker matcher fed only from local verified lists;
4. coherent fingerprint cohort enforcement across renderer and headers;
5. mode/profile controller and Anonymous fail-closed network delegate;
6. Privacy Dashboard signals sourced from actual enforcement counters.

Each patch must be exported with `git format-patch`, added to `patches/series`, applied by `scripts/apply_patches.sh`, and validated by a real Chromium build before it is marked complete.
