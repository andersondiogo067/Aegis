# Chromium native integration patch map

The current host cannot build a supported x86-64 Chromium tree. `patches/series` therefore contains only patches that were authored against exact files from tag `151.0.7922.173` and passed an isolated `git am --3way` application test; compilation and browser verification remain explicitly blocked.

## Current series

1. `0001-privacy-defaults-background-prediction.patch`
   - changes the user-overridable native defaults for background mode (`false`) and network prediction (`kDisabled`);
   - applied successfully with `git am --3way` to clean copies of the exact M151 files;
   - not yet compiled or browser-tested.

## Planned order

Next downstream commits should cover:

1. product branding and default managed preferences;
2. navigation throttle invoking conservative tracking-parameter removal;
3. network-service tracker matcher fed only from local verified lists;
4. central Blink fingerprint cohort plumbing (Canvas, WebGL, Audio, fonts, screen/navigator/timezone);
5. mode/profile controller and Anonymous fail-closed network delegate;
6. Privacy Dashboard signals sourced from actual enforcement counters.

Each patch must be exported with `git format-patch`, added to `patches/series`, applied by `scripts/apply_patches.sh`, and validated by a real Chromium build before it is marked complete.
