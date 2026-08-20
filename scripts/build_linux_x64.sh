#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[[ "$(uname -s)" == "Linux" && "$(uname -m)" == "x86_64" ]] || {
  echo "error: release build requires native Linux x86_64" >&2; exit 2;
}
export PATH="$ROOT/depot_tools:$PATH"
for cmd in gn autoninja; do command -v "$cmd" >/dev/null || { echo "error: $cmd missing" >&2; exit 2; }; done
"$ROOT/scripts/verify_security_flags.sh"
ARGS="$(tr '
' ' ' < "$ROOT/build/args.gn")"
gn gen "$ROOT/src/out/Aegis" --args="$ARGS"
autoninja -C "$ROOT/src/out/Aegis" chrome
