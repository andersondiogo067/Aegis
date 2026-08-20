#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from privacy.filter_update import install_verified_filter

parser = argparse.ArgumentParser(description="Download a pinned filter list and verify SHA-256 before install")
parser.add_argument("--source", default="stevenblack-unified-hosts")
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
sources = json.loads((ROOT / "privacy/lists/sources.json").read_text())
metadata = sources[args.source]
request = Request(metadata["url"], headers={"User-Agent": "Aegis-Browser-filter-updater/1"})
with urlopen(request, timeout=60) as response:
    payload = response.read(10_000_001)
if len(payload) > 10_000_000:
    raise SystemExit("filter list exceeds 10 MB safety limit")
install_verified_filter(payload, metadata["sha256"], args.output)
print(f"installed {args.source}: {args.output} ({len(payload)} bytes)")
