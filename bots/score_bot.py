"""Приоритеты: XHTTP-Reality > Vision-TCP > gRPC-Reality > Hy2. XTLS-aware."""

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


def score_line(line: str, ping_ms: int | None = None) -> int:
    low = line.lower()
    s = 0

    is_reality = "reality" in low or "security=reality" in low
    is_xhttp = "xhttp" in low or "type=xhttp" in low
    is_grpc = "type=grpc" in low or "network=grpc" in low
    is_tcp = "type=tcp" in low or "type=raw" in low or (
        is_reality and "type=" not in low and not is_xhttp and not is_grpc
    )
    is_vision = "xtls-rprx-vision" in low or "flow=xtls-rprx-vision" in low
    is_hy2 = low.startswith(("hysteria2://", "hy2://", "hysteria://"))

    # --- protocol priority ---
    if is_hy2:
        s += SCORE_HY2
    elif is_reality and is_xhttp:
        s += SCORE_XHTTP_REALITY
    elif is_reality and is_vision and is_tcp:
        # XTLS Vision: маскировка TLS под чужой сайт + flow vision
        s += SCORE_VISION_TCP
    elif is_reality and is_grpc:
        s += SCORE_GRPC_REALITY
    elif is_reality:
        s += SCORE_REALITY_OTHER

    # штрафы
    if is_vision and not is_tcp:
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
    if any(x in low for x in ("white", "whitelist", "cidr", "[wl]", "*cidr")):
        return "white"
    if any(x in low for x in ("black", "[bl]", "blacklist")):
        return "black"
    # Vision/XHTTP reality чаще для жёстких сетей → soft white
    if "reality" in low and ("xhttp" in low or "xtls-rprx-vision" in low):
        return "white"
    return "unknown"
