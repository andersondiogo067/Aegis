"""Evidence-driven local Privacy Dashboard rendering."""

from dataclasses import dataclass

from .policy import BrowserMode


@dataclass(frozen=True, slots=True)
class ProtectionEvidence:
    mode: BrowserMode
    trackers_blocked: int | None = None
    cookies_third_party_blocked: bool = False
    fingerprint_verified: bool = False
    https_only: bool = False
    webrtc_protected: bool = False
    tor_verified: bool = False


def _verified(label: str, value: bool, active: str) -> str:
    return f"{label}: {active}" if value else f"{label}: não verificado"


def render_dashboard(evidence: ProtectionEvidence) -> str:
    trackers = (
        str(evidence.trackers_blocked)
        if evidence.trackers_blocked is not None and evidence.trackers_blocked >= 0
        else "não verificado"
    )
    tor = (
        "Tor: conectado (verificado)"
        if evidence.tor_verified
        else "Tor: BLOQUEADO / não verificado"
    )
    rows = [
        f"Trackers bloqueados: {trackers}",
        _verified("Cookies de terceiros", evidence.cookies_third_party_blocked, "bloqueados"),
        _verified("Fingerprint", evidence.fingerprint_verified, "proteção verificada"),
        _verified("HTTPS", evidence.https_only, "modo estrito ativo"),
        _verified("WebRTC", evidence.webrtc_protected, "proteção ativa"),
        tor,
    ]
    cards = "".join(f"<li>{row}</li>" for row in rows)
    anonymous = evidence.mode is BrowserMode.ANONYMOUS
    accent = "#6F42C1" if anonymous else "#22B8A7"
    warning = (
        "<p class='warning'>ANONYMOUS — não se identifique em sites. "
        "Sem garantia de anonimato absoluto.</p>"
        if anonymous
        else ""
    )
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Aegis — Proteções desta página</title>
<style>body{{font:16px system-ui;background:#20242A;color:#eef2f5;max-width:760px;margin:4rem auto;padding:1rem}}
h1{{color:{accent}}}li{{background:#2b3038;margin:.65rem 0;padding:1rem;border-left:4px solid {accent};list-style:none}}
.warning{{border:2px solid {accent};padding:1rem;font-weight:700}}</style></head>
<body><h1>Aegis {evidence.mode.value.upper()}</h1>{warning}<h2>Proteções desta página</h2><ul>{cards}</ul>
<p>Somente evidências verificadas aparecem como ativas.</p></body></html>"""
