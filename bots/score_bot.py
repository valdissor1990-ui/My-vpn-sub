"""Scoring: Reality +25, CF +20, XHTTP, gRPC, Hy2, SNI, ping."""

from __future__ import annotations

import re
from urllib.parse import unquote

from config import (
    PREFERRED_SNI,
    SCORE_CF_SNI,
    SCORE_GRPC,
    SCORE_HY2,
    SCORE_PREFERRED_SNI,
    SCORE_REALITY,
    SCORE_TCP_FAST,
    SCORE_VISION,
    SCORE_XHTTP,
)


def _sni(line: str) -> str:
    low = line.lower()
    for key in ("sni=", "host=", "peer="):
        m = re.search(rf"{key}([^&\s#]+)", low)
        if m:
            return unquote(m.group(1))
    return ""


def score_line(line: str, ping_ms: int | None = None) -> int:
    low = line.lower()
    s = 0
    if low.startswith(("hysteria2://", "hy2://", "hysteria://")):
        s += SCORE_HY2
    if "reality" in low:
        s += SCORE_REALITY
    if "xhttp" in low:
        s += SCORE_XHTTP
    if "grpc" in low:
        s += SCORE_GRPC
    if "vision" in low or "xtls-rprx" in low:
        s += SCORE_VISION
    sni = _sni(line)
    if "cloudflare" in sni or "cloudflare" in low:
        s += SCORE_CF_SNI
    for pref in PREFERRED_SNI:
        if pref in sni or pref in low:
            s += SCORE_PREFERRED_SNI
            break
    if ping_ms is not None and ping_ms < 400:
        s += SCORE_TCP_FAST
    elif ping_ms is not None and ping_ms < 800:
        s += SCORE_TCP_FAST // 2
    return s


def classify_list(line: str, source_url: str = "") -> str:
    """white | black | unknown"""
    blob = (line + " " + source_url).lower()
    if any(h.lower() in blob for h in ("white", "whitelist", "cidr", "*cidr", "[wl]")):
        return "white"
    if any(h.lower() in blob for h in ("black", "[bl]", "blacklist")):
        return "black"
    # Reality+xhttp/grpc чаще для обхода — помечаем neutral→prefer white bucket secondary
    return "unknown"
