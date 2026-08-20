#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 -m unittest discover -s . -p 'test_*.py' -v
scripts/verify_security_flags.sh
python3 -m json.tool build/policies/standard.json >/dev/null
python3 -m json.tool build/policies/private.json >/dev/null
python3 -m json.tool privacy/extension/manifest.json >/dev/null
python3 -m json.tool privacy/extension/rules.json >/dev/null
if [[ "${AEGIS_LIVE_TOR:-0}" == "1" ]]; then
  python3 tests/privacy/run_tor_integration.py
else
  echo "live Tor test: SKIP (set AEGIS_LIVE_TOR=1)"
fi
echo "Aegis host-capable test suite: PASS"
