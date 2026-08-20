#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from privacy.network_audit import parse_strace_destinations

parser = argparse.ArgumentParser(description="Audit process network destinations with strace")
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("command", nargs=argparse.REMAINDER)
args = parser.parse_args()
command = args.command[1:] if args.command[:1] == ["--"] else args.command
if not command:
    raise SystemExit("error: command required after --")
with tempfile.NamedTemporaryFile(prefix="aegis-net-", suffix=".strace", delete=False) as trace_file:
    trace_path = Path(trace_file.name)
try:
    result = subprocess.run(
        ["strace", "-f", "-qq", "-s", "256", "-e", "trace=network", "-o", str(trace_path), *command]
    )
    trace = trace_path.read_text(errors="replace")
    report = {
        "command": command,
        "exit_code": result.returncode,
        "destinations": parse_strace_destinations(trace),
        "limitations": "process-level IPv4 connect() audit; review packet capture for UDP, DNS and complete release evidence",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(args.output)
    raise SystemExit(result.returncode)
finally:
    trace_path.unlink(missing_ok=True)
