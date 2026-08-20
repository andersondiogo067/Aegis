# Phase 2 — Privacy defaults

## Enforced policy

The generated Chromium managed policy enables third-party-cookie blocking and HTTPS-only mode; disables remote search suggestions, network prediction, background mode and non-essential metrics reporting; and does not disable Safe Browsing or software/component updates. PRIVATE additionally requests clearing history, downloads, cookies/site data and cache on exit.

Sensitive capabilities (camera, microphone, geolocation, notifications, clipboard, Bluetooth, USB, serial, MIDI and filesystem) remain prompt-based: no silent grant. Native downstream integration must map the declarative `permissions` table to Chromium content-setting defaults and tests.

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
