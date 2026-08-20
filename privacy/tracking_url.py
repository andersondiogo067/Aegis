"""Conservative removal of well-known click-tracking query parameters."""

from urllib.parse import unquote_plus, urlsplit, urlunsplit

TRACKING_PARAMETERS = frozenset(
    {
        "fbclid",
        "gclid",
        "dclid",
        "msclkid",
        "mc_cid",
        "mc_eid",
        "igshid",
        "vero_conv",
        "vero_id",
    }
)


def _is_tracking_parameter(raw_part: str) -> bool:
    raw_key = raw_part.partition("=")[0]
    key = unquote_plus(raw_key).casefold()
    return key.startswith("utm_") or key in TRACKING_PARAMETERS


def strip_tracking_parameters(url: str) -> str:
    """Strip only known tracking keys while preserving other raw query pieces."""
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.query:
        return url
    kept = [part for part in parsed.query.split("&") if not _is_tracking_parameter(part)]
    if len(kept) == len(parsed.query.split("&")):
        return url
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "&".join(kept), parsed.fragment))
