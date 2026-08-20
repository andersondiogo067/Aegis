# Privacy model

Aegis aims to reduce routine cross-site tracking and accidental network disclosure while retaining Chromium security mechanisms.

## Default principles

- Block third-party cookies.
- Prefer HTTPS and avoid speculative/background network traffic where practical.
- Do not send omnibox text to remote suggestion services without explicit opt-in.
- Restrict sensitive permissions and require an explicit site prompt.
- Keep profiles for STANDARD, PRIVATE and ANONYMOUS separate.
- Clear ephemeral data for PRIVATE/ANONYMOUS at shutdown.
- Use locally evaluated filter lists; never upload browsing history for classification.
- Strip known tracking query parameters conservatively.
- Standardize fingerprint-exposed values in cohorts; do not randomize per page.

## Anonymous mode

Anonymous mode uses an existing Tor SOCKS endpoint and proxy-side DNS. Startup validates the endpoint and Tor control evidence when configured. Runtime health failure causes new navigations to be denied; there is no direct-network fallback.

## Non-goals

This project does not promise perfect anonymity, protection from a compromised device/browser, or safety when users identify themselves to websites. It is not a replacement for the Tor Browser's mature anonymity research when maximum anonymity is required.
