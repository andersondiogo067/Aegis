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
        "HttpsUpgradesEnabled": policy.https_only,
        "BackgroundModeEnabled": False,
        "BrowserNetworkTimeQueriesEnabled": False,
        "DomainReliabilityAllowed": False,
        "MetricsReportingEnabled": False,
        "UrlKeyedAnonymizedDataCollectionEnabled": False,
        "ComponentUpdatesEnabled": True,
        "ChromeVariations": 1,
        "DefaultGeolocationSetting": 3,
        "DefaultMediaStreamSetting": 3,
        "DefaultClipboardSetting": 3,
        "DefaultFileSystemReadGuardSetting": 3,
        "DefaultFileSystemWriteGuardSetting": 3,
        "DefaultNotificationsSetting": 2,
        "DefaultSensorsSetting": 2,
        "DefaultIdleDetectionSetting": 2,
        "DefaultLocalFontsSetting": 2,
        "DefaultSerialGuardSetting": 2,
        "DefaultWebBluetoothGuardSetting": 2,
        "DefaultWebHidGuardSetting": 2,
        "DefaultWebUsbGuardSetting": 2,
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
                "camera": "ask",
                "microphone": "ask",
                "geolocation": "ask",
                "clipboard": "ask",
                "filesystem": "ask",
                "notifications": "block",
                "sensors": "block",
                "idle_detection": "block",
                "local_fonts": "block",
                "bluetooth": "block",
                "usb": "block",
                "serial": "block",
                "hid": "block",
                "midi": "block",
            }
        ),
    )
