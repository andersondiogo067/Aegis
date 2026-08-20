"""Profile lifecycle with strict separation and ephemeral cleanup."""

import shutil
import tempfile
from pathlib import Path
from types import TracebackType

from .policy import BrowserMode


class BrowserProfile:
    def __init__(self, mode: BrowserMode, state_root: Path):
        self.mode = mode
        self.state_root = state_root.expanduser().resolve()
        self.path: Path | None = None
        self._ephemeral_root = self.state_root / "ephemeral"

    def __enter__(self) -> Path:
        self.state_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.mode is BrowserMode.STANDARD:
            path = self.state_root / "profiles" / "standard"
            path.mkdir(mode=0o700, parents=True, exist_ok=True)
        else:
            self._ephemeral_root.mkdir(mode=0o700, parents=True, exist_ok=True)
            path = Path(
                tempfile.mkdtemp(prefix=f"{self.mode.value}-", dir=self._ephemeral_root)
            )
        path.chmod(0o700)
        self.path = path
        return path

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self.mode is BrowserMode.STANDARD or self.path is None:
            return
        path = self.path.resolve()
        if path.parent != self._ephemeral_root.resolve():
            raise RuntimeError(f"refusing to remove profile outside ephemeral root: {path}")
        shutil.rmtree(path, ignore_errors=False)
