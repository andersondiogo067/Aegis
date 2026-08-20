"""Parse process-level network traces into auditable destinations."""

import re

_IPV4_CONNECT = re.compile(
    r"connect\([^\n]*sa_family=AF_INET,\s*sin_port=htons\((\d+)\),\s*"
    r'sin_addr=inet_addr\("([0-9.]+)"\)'
)


def parse_strace_destinations(trace: str) -> list[dict[str, object]]:
    destinations = {
        (address, int(port))
        for port, address in _IPV4_CONNECT.findall(trace)
    }
    return [
        {"family": "ipv4", "address": address, "port": port}
        for address, port in sorted(destinations)
    ]
