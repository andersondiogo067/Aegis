"""Safe Chromium command construction for Aegis modes."""

from pathlib import Path
from typing import Iterable

from .policy import BrowserMode

FORBIDDEN_FLAGS = frozenset({"--no-sandbox", "--ignore-certificate-errors"})


def build_chromium_command(
    executable: Path,
    mode: BrowserMode,
    profile: Path,
    urls: Iterable[str],
    extra_flags: Iterable[str] = (),
) -> list[str]:
    flags = [str(flag) for flag in extra_flags]
    for flag in flags:
        name = flag.split("=", 1)[0]
        if name in FORBIDDEN_FLAGS:
            raise ValueError(f"forbidden Chromium flag: {name}")

    command = [
        str(executable),
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
    ]
    if mode is not BrowserMode.STANDARD:
        command.append("--incognito")
    command.extend(flags)
    command.extend(str(url) for url in urls)
    return command
