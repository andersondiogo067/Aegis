"""Serialization of Chromium managed policy files."""

import json
import os
import tempfile
from pathlib import Path

from .policy import BrowserMode, chromium_managed_policy, policy_for


def write_managed_policy(target: Path, mode: BrowserMode) -> None:
    target = target.expanduser()
    target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
    payload = json.dumps(
        chromium_managed_policy(policy_for(mode)),
        indent=2,
        sort_keys=True,
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        dir=target.parent, prefix=f".{target.name}.", text=True
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(0o644)
        temporary.replace(target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
