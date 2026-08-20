"""Declarative privacy policy shared by launch tooling and tests."""

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class BrowserMode(str, Enum):
    STANDARD = "standard"
    PRIVATE = "private"
    ANONYMOUS = "anonymous"


@dataclass(frozen=True, slots=True)
class PrivacyPolicy:
    mode: BrowserMode
    block_third_party_cookies: bool
    https_only: bool
    search_suggestions: bool
    network_prediction: bool
    site_isolation: bool
    sandbox: bool
    tls_validation: bool
    ephemeral_profile: bool
    separate_profile: bool
    clear_on_exit: bool
    permissions: Mapping[str, str]


def chromium_managed_policy(policy: PrivacyPolicy) -> dict[str, object]:
    """Translate audited Aegis defaults to supported Chromium enterprise policy keys.

    Security services are intentionally not disabled here. In particular, there is no
    policy that weakens Safe Browsing, updates, TLS, Site Isolation, or sandboxing.
    """
    managed: dict[str, object] = {
        "BlockThirdPartyCookies": policy.block_third_party_cookies,
        "SearchSuggestEnabled": policy.search_suggestions,
        "NetworkPredictionOptions": 0 if policy.network_prediction else 2,
        "HttpsOnlyMode": "force_enabled" if policy.https_only else "allowed",
        "BackgroundModeEnabled": False,
        "MetricsReportingEnabled": False,
    }
    if policy.clear_on_exit:
        managed["ClearBrowsingDataOnExitList"] = [
            "browsing_history",
            "download_history",
            "cookies_and_other_site_data",
            "cached_images_and_files",
        ]
    return managed


def policy_for(mode: BrowserMode) -> PrivacyPolicy:
    """Return security-preserving defaults for a browser mode."""
    return PrivacyPolicy(
        mode=mode,
        block_third_party_cookies=True,
        https_only=True,
        search_suggestions=False,
        network_prediction=False,
        site_isolation=True,
        sandbox=True,
        tls_validation=True,
        ephemeral_profile=mode is not BrowserMode.STANDARD,
        separate_profile=True,
        clear_on_exit=mode is not BrowserMode.STANDARD,
        permissions=MappingProxyType(
            {
                name: "ask"
                for name in (
                    "camera",
                    "microphone",
                    "geolocation",
                    "notifications",
                    "clipboard",
                    "bluetooth",
                    "usb",
                    "serial",
                    "midi",
                    "filesystem",
                )
            }
        ),
    )
