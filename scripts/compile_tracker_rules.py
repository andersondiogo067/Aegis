#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from privacy.tracker_blocking import compile_dnr_rules, parse_domain_list

parser = argparse.ArgumentParser(description="Compile local hosts/domain list to Chromium DNR rules")
parser.add_argument("--input", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--limit", type=int, default=30000)
args = parser.parse_args()
domains = parse_domain_list(args.input.read_text(errors="strict"))
if len(domains) > args.limit:
    raise SystemExit(f"refusing silent truncation: {len(domains)} domains exceeds limit {args.limit}")
rules = compile_dnr_rules(domains)
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps(rules, indent=2, sort_keys=True) + "\n")
print(f"compiled {len(rules)} third-party block rules: {args.output}")
