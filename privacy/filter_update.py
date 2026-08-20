"""Verified local filter-list installation."""

import hashlib
import os
import tempfile
from pathlib import Path


def install_verified_filter(payload: bytes, expected_sha256: str, target: Path) -> None:
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected_sha256.casefold():
        raise ValueError(f"filter list SHA-256 mismatch: expected {expected_sha256}, got {actual}")
    target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.")
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(0o644)
        temporary.replace(target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
