#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
unsafe='--no-sandbox|--ignore-certificate-errors|use_sandbox[[:space:]]*=[[:space:]]*false|site_isolation.*false'
scan=("$ROOT/build" "$ROOT/scripts" "$ROOT/privacy")
if grep -RInE --exclude='verify_security_flags.sh' --exclude='launcher.py' -e "$unsafe" "${scan[@]}"; then
  echo "error: forbidden security-disabling option found" >&2
  exit 1
fi
grep -qE '^use_sandbox[[:space:]]*=[[:space:]]*true$' "$ROOT/build/args.gn" || {
  echo "error: build/args.gn must explicitly preserve sandbox" >&2; exit 1;
}
echo "security flag verification: PASS"
