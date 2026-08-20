#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${CHROMIUM_SRC:-$ROOT/src}"
[[ -d "$SRC/.git" ]] || { echo "error: Chromium checkout not found: $SRC" >&2; exit 2; }
cd "$SRC"
while IFS= read -r patch; do
  [[ -z "$patch" || "$patch" == \#* ]] && continue
  file="$ROOT/patches/$patch"
  [[ -f "$file" ]] || { echo "error: missing patch $file" >&2; exit 2; }
  git am --3way "$file"
done < "$ROOT/patches/series"
