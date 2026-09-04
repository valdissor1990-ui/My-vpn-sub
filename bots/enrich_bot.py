"""
Бот обогащения: разбирает ключи, считает протоколы/порты/SNI,
пишет collect_meta.json для мониторинга.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import unquote


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [enrich] {msg}")


def _proto(line: str) -> str:
    low = line.lower()
    for p in ("hysteria2", "hy2", "hysteria", "vless", "vmess", "trojan"):
        if low.startswith(f"{p}://"):
            return p
    return "other"


def _port(line: str) -> str:
    m = re.search(r"@[^:/\s]+:(\d+)", line)
    if m:
        return m.group(1)
    m2 = re.search(r"://(?:[^@/]+@)?[^:/\s]+:(\d+)", line)
    return m2.group(1) if m2 else "?"


def _sni(line: str) -> str:
    low = line.lower()
    for key in ("sni=", "host=", "peer="):
        m = re.search(rf"{key}([^&\s#]+)", low)
        if m:
            return unquote(m.group(1))[:80]
    return ""


def _transport(line: str) -> str:
    low = line.lower()
    if "xhttp" in low:
        return "xhttp"
    if "grpc" in low:
        return "grpc"
    if "type=ws" in low:
        return "ws"
    if "reality" in low:
        return "reality-tcp"
    if low.startswith(("hy2://", "hysteria2://")):
        return "hysteria2"
    return "other"


def run_enrich(lines: list[str], tag: str = "filtered") -> dict:
    protos = Counter(_proto(l) for l in lines)
    ports = Counter(_port(l) for l in lines)
    transports = Counter(_transport(l) for l in lines)
    snis = Counter(_sni(l) for l in lines if _sni(l))

    meta = {
        "tag": tag,
        "count": len(lines),
        "protocols": dict(protos.most_common(15)),
        "ports": dict(ports.most_common(15)),
        "transports": dict(transports.most_common(10)),
        "top_sni": dict(snis.most_common(20)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    path = f"meta_{tag}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    log(f"{path}: {len(lines)} keys, protos={dict(protos)}")
    return meta
