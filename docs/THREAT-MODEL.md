# Threat model

## Intended protection

- Third-party trackers, pixels, invasive analytics and behavioral advertising.
- Cross-site correlation through cookies, cache, URL parameters and common fingerprint surfaces.
- Accidental IP/DNS exposure, especially WebRTC and DNS bypass in Anonymous mode.
- Local profile correlation among STANDARD, PRIVATE and ANONYMOUS.
- Passive local-network/ISP observation of destinations when Tor is active (subject to Tor's model).

## Adversaries and limits

Aegis does not guarantee anonymity. It cannot fully defeat:

- A compromised OS, malicious extension, browser zero-day, or physical attacker.
- Global traffic-correlation adversaries observing both Tor entry and exit traffic.
- Identification caused by logging in, disclosing identity, downloads opened externally, or unsafe user behavior.
- Sophisticated fingerprinting before all native patches are applied and validated.
- A malicious Tor exit reading non-HTTPS traffic; HTTPS preference and TLS validation remain essential.

## Preserved security boundaries

- Chromium sandbox
- Site Isolation
- TLS and certificate validation
- multiprocess separation
- upstream security updates
- safe browsing/update functions unless a specific replacement and risk review exists

`--no-sandbox` and `--ignore-certificate-errors` are forbidden in normal launch/build scripts.
