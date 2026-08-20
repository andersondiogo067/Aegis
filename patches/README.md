# Chromium native integration patch map

The current host cannot fetch/build a supported x86-64 Chromium tree, so no patch is falsely listed in `series`. The testable downstream components define the required behavior first. On the release builder, create upstream-applicable commits in this order:

1. product branding and default managed preferences;
2. navigation throttle invoking conservative tracking-parameter removal;
3. network-service tracker matcher fed only from local verified lists;
4. central Blink fingerprint cohort plumbing (Canvas, WebGL, Audio, fonts, screen/navigator/timezone);
5. mode/profile controller and Anonymous fail-closed network delegate;
6. Privacy Dashboard signals sourced from actual enforcement counters.

Each patch must be exported with `git format-patch`, added to `patches/series`, applied by `scripts/apply_patches.sh`, and validated by a real Chromium build before it is marked complete.
