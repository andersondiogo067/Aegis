#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(tr -d '[:space:]' < "$ROOT/CHROMIUM_VERSION")"
WORKDIR="${AEGIS_X64_WORKDIR:-$ROOT/build/work/x64-checkout}"
SRC="$WORKDIR/src"
OUT="$SRC/out/Aegis"
MIN_DISK_KB=$((200 * 1024 * 1024))
MIN_RAM_KB=$((16 * 1024 * 1024))
SKIP_SYSTEM_DEPS=0
START_BUILD=0

usage() {
  cat <<'EOF'
Usage: scripts/setup-x64-builder.sh [--skip-system-deps] [--build]

Prepares a fresh native Linux x86-64 builder for the pinned Aegis Chromium
checkout. By default it installs dependencies, syncs Chromium, applies the
ordered patches, generates out/Aegis and performs a Ninja dry-run only.

  --skip-system-deps  Do not invoke apt or Chromium install-build-deps.sh.
  --build             Start the real `autoninja ... chrome` build after setup.
EOF
}

while (($#)); do
  case "$1" in
    --skip-system-deps) SKIP_SYSTEM_DEPS=1 ;;
    --build) START_BUILD=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

fail() {
  echo "error: $*" >&2
  exit 2
}

[[ "$(uname -s)" == "Linux" ]] || fail "builder must run Linux"
[[ "$(uname -m)" == "x86_64" ]] || fail "builder must be native x86_64; current: $(uname -m)"
[[ -f "$ROOT/CHROMIUM_VERSION" ]] || fail "missing CHROMIUM_VERSION"
[[ -f "$ROOT/patches/series" ]] || fail "missing patches/series"

available_kb="$(df --output=avail -k "$ROOT" | tail -n 1 | tr -d '[:space:]')"
mem_kb="$(awk '/^MemTotal:/ {print $2}' /proc/meminfo)"
[[ "$available_kb" =~ ^[0-9]+$ ]] || fail "could not determine free disk space"
[[ "$mem_kb" =~ ^[0-9]+$ ]] || fail "could not determine RAM"
((available_kb >= MIN_DISK_KB)) || fail "at least 200 GiB free is required; found $((available_kb / 1024 / 1024)) GiB"
((mem_kb >= MIN_RAM_KB)) || fail "at least 16 GiB RAM is required; found $((mem_kb / 1024 / 1024)) GiB"

mapfile -t PATCHES < <(sed -e 's/[[:space:]]*$//' -e '/^[[:space:]]*#/d' -e '/^[[:space:]]*$/d' "$ROOT/patches/series")
((${#PATCHES[@]} == 3)) || fail "expected exactly 3 migration patches; found ${#PATCHES[@]}"
for patch in "${PATCHES[@]}"; do
  [[ -f "$ROOT/patches/$patch" ]] || fail "missing patch: patches/$patch"
done

if ((SKIP_SYSTEM_DEPS == 0)); then
  command -v apt-get >/dev/null || fail "this setup currently supports Debian/Ubuntu apt builders"
  if ((EUID == 0)); then
    APT=(apt-get)
  else
    command -v sudo >/dev/null || fail "sudo is required to install system dependencies"
    APT=(sudo apt-get)
  fi
  "${APT[@]}" update
  "${APT[@]}" install -y \
    build-essential ca-certificates clang curl file git lld lsb-release \
    pkg-config python3 python3-venv rsync sudo unzip xz-utils
fi

if [[ ! -d "$ROOT/depot_tools/.git" ]]; then
  git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git "$ROOT/depot_tools"
else
  git -C "$ROOT/depot_tools" pull --ff-only
fi
export PATH="$ROOT/depot_tools:$PATH"
for command_name in fetch gclient gn autoninja; do
  command -v "$command_name" >/dev/null || fail "$command_name is unavailable after depot_tools setup"
done
gclient metrics --disable >/dev/null 2>&1 || true

"$ROOT/scripts/test_all.sh"
"$ROOT/scripts/verify_security_flags.sh"

mkdir -p "$WORKDIR"
if [[ ! -d "$SRC/.git" ]]; then
  if [[ -n "$(find "$WORKDIR" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
    fail "checkout workdir is not empty and has no src Git checkout: $WORKDIR"
  fi
  (
    cd "$WORKDIR"
    fetch --nohooks chromium
  )
fi

if [[ -e "$ROOT/src" || -L "$ROOT/src" ]]; then
  [[ "$(readlink -f "$ROOT/src")" == "$(readlink -f "$SRC")" ]] || \
    fail "$ROOT/src already exists and does not point to $SRC"
else
  ln -s "$SRC" "$ROOT/src"
fi

(
  cd "$SRC"
  git fetch --tags origin
  git checkout --detach "$VERSION"
)
(
  cd "$WORKDIR"
  gclient sync --with_branch_heads --with_tags --no-history
)

if ((SKIP_SYSTEM_DEPS == 0)); then
  "$SRC/build/install-build-deps.sh" --no-prompt
fi
(
  cd "$WORKDIR"
  gclient runhooks
)

[[ -z "$(git -C "$SRC" status --porcelain --untracked-files=no)" ]] || \
  fail "Chromium tracked files changed before applying Aegis patches"
CHROMIUM_SRC="$SRC" "$ROOT/scripts/apply_patches.sh"

printf '%s\n' "$VERSION" > "$ROOT/build/resolved-version.txt"
git -C "$SRC" rev-parse HEAD > "$ROOT/build/chromium-patched-commit.txt"
"$ROOT/scripts/verify_security_flags.sh"

GN_ARGS="$(tr '\n' ' ' < "$ROOT/build/args.gn")"
gn gen "$OUT" --args="$GN_ARGS"
autoninja -C "$OUT" -n chrome

cat <<EOF
Aegis x86-64 builder preparation: PASS
Chromium version: $VERSION
Chromium source:  $SRC
Build output:     $OUT
Patches applied:  ${#PATCHES[@]}

The build graph is generated and the Ninja dry-run passed.
Start the first real build with:
  autoninja -C "$OUT" chrome
EOF

if ((START_BUILD == 1)); then
  autoninja -C "$OUT" chrome
fi
