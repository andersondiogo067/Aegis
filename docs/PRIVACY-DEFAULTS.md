# Phase 2 — Privacy defaults

## Enforced policy

The generated Chromium managed policy enables third-party-cookie blocking and HTTPS-only mode; disables remote search suggestions, network prediction, background mode and non-essential metrics reporting; and does not disable Safe Browsing or software/component updates. PRIVATE additionally requests clearing history, downloads, cookies/site data and cache on exit.

Common sensitive capabilities (camera, microphone, geolocation, clipboard and filesystem access) remain prompt-based: no silent grant. Higher-fingerprinting or abuse-prone capabilities (notifications, sensors, idle detection, local-font enumeration, Bluetooth, USB, serial, HID and MIDI) default to blocked and require an explicit user-created exception. The generated M151 policy also disables browser network-time queries, Domain Reliability and URL-keyed anonymized collection, while explicitly preserving component updates and critical-fix Variations.

## Profile separation

`BrowserProfile` creates mode-specific directories with mode 0700. STANDARD persists under `profiles/standard`. PRIVATE is created beneath a dedicated ephemeral root and recursively removed at shutdown. The cleanup guard refuses paths outside that root.

## Applying policy

Generate policy JSON with:

```
scripts/generate_policy.py --mode standard --output build/policies/aegis.json
```

For a system Chromium, install it in the browser's managed policy directory (commonly `/etc/chromium/policies/managed/`) using administrator-controlled deployment. For a downstream Aegis build, the same values become compiled defaults so they cannot be silently omitted by a launcher.

## External networking audit

The project deliberately avoids a blanket `--disable-background-networking`, because that can suppress security-relevant component activity. Network prediction, omnibox remote suggestions and metrics are independently controlled. Phase 5 includes a local capture harness to report browser-initiated destinations; security/update endpoints must be reviewed rather than blindly removed.
