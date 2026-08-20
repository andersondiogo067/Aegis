"""Local tracker-domain list parsing and Chromium DNR rule compilation."""

import ipaddress
import re
from collections.abc import Iterable

_DOMAIN = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_RESOURCE_TYPES = [
    "script",
    "image",
    "xmlhttprequest",
    "sub_frame",
    "ping",
    "media",
    "font",
    "websocket",
]


def parse_domain_list(source: str) -> list[str]:
    domains: set[str] = set()
    for raw_line in source.splitlines():
        line = raw_line.partition("#")[0].strip().casefold()
        if not line:
            continue
        fields = line.split()
        candidate = fields[-1].rstrip(".")
        if candidate == "localhost" or not _DOMAIN.fullmatch(candidate):
            continue
        try:
            ipaddress.ip_address(candidate)
        except ValueError:
            domains.add(candidate)
    return sorted(domains)


def compile_dnr_rules(domains: Iterable[str]) -> list[dict[str, object]]:
    return [
        {
            "id": index,
            "priority": 1,
            "action": {"type": "block"},
            "condition": {
                "urlFilter": f"||{domain}^",
                "domainType": "thirdParty",
                "resourceTypes": list(_RESOURCE_TYPES),
            },
        }
        for index, domain in enumerate(sorted(set(domains)), start=1)
    ]
