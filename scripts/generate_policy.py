#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from privacy.policy import BrowserMode
from privacy.policy_io import write_managed_policy

parser = argparse.ArgumentParser(description="Generate audited Aegis Chromium managed policy JSON")
parser.add_argument("--mode", choices=["standard", "private"], required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
write_managed_policy(args.output, BrowserMode(args.mode))
print(args.output)
