# Privacy test matrix

`PASS` means the named local test was executed on the current host. `BLOCKED` means a real Chromium binary/native patch is required; a policy/unit test is not represented as browser proof.

| Area | Local evidence | Browser/native E2E |
|---|---|---|
| Native privacy defaults | exact-file `git am --3way`: PASS | Compile/profile behavior: BLOCKED |
| Third-party cookies | Policy JSON unit: PASS | Embedded A/B origin test: BLOCKED |
| Storage/cache/history | Ephemeral profile deletion: PASS | Cookie/IDB/SW/cache population: BLOCKED |
| Session cleanup | Normal profile/Tor cleanup: PASS | Crash scavenging: BLOCKED |
| Canvas/WebGL/Audio/fonts/screen/navigator/timezone | Diagnostic page + cohort specification: PASS | Cross-host renderer cohort: BLOCKED |
| WebRTC | Restrictive command policy: PASS | ICE/STUN packet capture: BLOCKED |
| DNS/proxy | SOCKS remote-hostname live route: PASS | Zero direct DNS/DoH packet capture: BLOCKED |
| Tor | Control+SOCKS unit and official IsTor live check: PASS | Native browser egress gate: BLOCKED |
| Tor fail-closed | Gate unit + stop-Tor live health test: PASS | Mid-navigation browser kill/packet capture: BLOCKED |
| URL tracking | Pure conservative/idempotent behavior: PASS | Navigation-throttle integration: BLOCKED |
| Permissions | M151 policy keys/enums unit: PASS | Prompt/content-setting browser test: BLOCKED |
| Tracker rules | parser/hash/DNR compilation: PASS | Native URLLoader coverage/counter: BLOCKED |
| Unexpected network | strace IPv4 audit harness exercised: PASS | Chromium startup baseline: BLOCKED |

Run all host-capable checks with `scripts/test_all.sh`. Set `AEGIS_LIVE_TOR=1` to include the network-dependent Tor integration test.
