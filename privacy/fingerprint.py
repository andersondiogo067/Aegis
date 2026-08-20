"""Central fingerprint cohort definition consumed by downstream patches."""

from dataclasses import dataclass

from .policy import BrowserMode


@dataclass(frozen=True, slots=True)
class FingerprintProfile:
    canvas: str
    webgl: str
    audio_context: str
    font_cohort: str
    screen: tuple[int, int]
    device_pixel_ratio: float
    hardware_concurrency: int
    device_memory_gib: int
    platform: str
    user_agent_strategy: str
    languages: tuple[str, ...]
    timezone: str
    per_site_randomization: bool


_COMMON_COHORT = FingerprintProfile(
    canvas="standardize",
    webgl="standardize",
    audio_context="standardize",
    font_cohort="aegis-common-v1",
    screen=(1920, 1080),
    device_pixel_ratio=1.0,
    hardware_concurrency=4,
    device_memory_gib=8,
    platform="Linux x86_64",
    user_agent_strategy="pinned-to-chromium-major",
    languages=("en-US", "en"),
    timezone="UTC",
    per_site_randomization=False,
)


def fingerprint_profile(mode: BrowserMode) -> FingerprintProfile:
    """Return a deterministic shared cohort; the site is intentionally not an input."""
    del mode
    return _COMMON_COHORT
