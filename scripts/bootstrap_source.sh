#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$ROOT/CHROMIUM_VERSION")"
if [[ "$(uname -m)" != "x86_64" ]]; then
  echo "error: release source bootstrap requires native Linux x86_64; current: $(uname -m)" >&2
  exit 2
fi
command -v git >/dev/null || { echo "error: git is required" >&2; exit 2; }
if [[ ! -d "$ROOT/depot_tools/.git" ]]; then
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git "$ROOT/depot_tools"
fi
export PATH="$ROOT/depot_tools:$PATH"
mkdir -p "$ROOT/src"
cd "$ROOT/src"
if [[ ! -d .git ]]; then
  fetch --nohooks chromium
fi
git fetch --tags origin
git checkout --detach "$VERSION"
gclient sync --with_branch_heads --with_tags --no-history
printf '%s
' "$VERSION" > "$ROOT/build/resolved-version.txt"
git rev-parse HEAD > "$ROOT/build/chromium-commit.txt"
