"""Scoring + vision detection. XHTTP > Vision-TCP > gRPC > Hy2."""

from __future__ import annotations

import re
from urllib.parse import unquote

from config import (
    PENALTY_NO_PBK,
    PENALTY_VISION_NON_TCP,
    PREFERRED_SNI,
    SCORE_CF_SNI,
    SCORE_FAST_PING,
    SCORE_GRPC_REALITY,
    SCORE_HY2,
    SCORE_REALITY_OTHER,
    SCORE_RU_SNI,
    SCORE_VISION_TCP,
    SCORE_XHTTP_REALITY,
)


def _sni(line: str) -> str:
    low = line.lower()
    for key in ("sni=", "host=", "peer="):
        m = re.search(rf"{key}([^&\s#]+)", low)
        if m:
            return unquote(m.group(1))
    return ""


def is_vision_tcp(line: str) -> bool:
    low = line.lower()
    if "xtls-rprx-vision" not in low and "flow=xtls-rprx-vision" not in low:
        return False
    if "reality" not in low:
        return False
    if "xhttp" in low or "type=grpc" in low or "type=ws" in low:
        return False
    return True


def score_line(line: str, ping_ms: int | None = None) -> int:
    low = line.lower()
    s = 0
    is_reality = "reality" in low
    is_xhttp = "xhttp" in low
    is_grpc = "type=grpc" in low
    is_hy2 = low.startswith(("hysteria2://", "hy2://", "hysteria://"))
    vision = is_vision_tcp(line)

    if is_hy2:
        s += SCORE_HY2
    elif is_reality and is_xhttp:
        s += SCORE_XHTTP_REALITY
    elif vision:
        s += SCORE_VISION_TCP
    elif is_reality and is_grpc:
        s += SCORE_GRPC_REALITY
    elif is_reality:
        s += SCORE_REALITY_OTHER

    if ("xtls-rprx-vision" in low) and not vision:
        s += PENALTY_VISION_NON_TCP
    if is_reality and "pbk=" not in low:
        s += PENALTY_NO_PBK

    sni = _sni(line)
    if "cloudflare" in sni or "cloudflare" in low:
        s += SCORE_CF_SNI
    if any(x in sni for x in ("yandex", "vk.com", "vk.ru", "mail.ru")):
        s += SCORE_RU_SNI
    for pref in PREFERRED_SNI:
        if pref in sni:
            s += 8
            break

    if ping_ms is not None:
        if ping_ms < 350:
            s += SCORE_FAST_PING
        elif ping_ms < 700:
            s += SCORE_FAST_PING // 2
    return s


def classify_list(line: str) -> str:
    low = line.lower()
    if any(x in low for x in ("white", "whitelist", "cidr", "[wl]")):
        return "white"
    if any(x in low for x in ("black", "[bl]", "blacklist")):
        return "black"
    if is_vision_tcp(line) or ("reality" in low and "xhttp" in low):
        return "white"
    return "unknown"
