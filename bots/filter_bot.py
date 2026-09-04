"""Фильтр: Reality / Vision-TCP / XHTTP / gRPC / Hy2."""

from __future__ import annotations

from datetime import datetime

from config import (
    ALLOW_HYSTERIA2,
    ALLOW_REALITY_TCP,
    ALLOW_XHTTP_GRPC,
    PROTOCOLS,
    REQUIRE_REALITY_FOR_VLESS,
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [filter] {msg}")


def protocol_of(line: str) -> str | None:
    low = line.strip().lower()
    for p in ("hysteria2", "hy2", "hysteria", "vless", "vmess", "trojan"):
        if low.startswith(f"{p}://"):
            return p
    return None


def passes(line: str) -> bool:
    line = line.strip()
    if not line or line.startswith("#"):
        return False
    p = protocol_of(line)
    if not p or p not in PROTOCOLS:
        return False
    low = line.lower()

    if p in ("hysteria2", "hy2", "hysteria"):
        return ALLOW_HYSTERIA2

    if REQUIRE_REALITY_FOR_VLESS and p == "vless" and "reality" not in low:
        return False

    if "reality" not in low and p == "vless":
        return False

    # reality without public key is useless
    if "reality" in low and "pbk=" not in low:
        return False

    if ALLOW_XHTTP_GRPC and ("xhttp" in low or "grpc" in low):
        return True
    if ALLOW_REALITY_TCP:
        return True
    return False


def run_filter(raw_lines: list[str]) -> tuple[list[str], dict]:
    seen: set[str] = set()
    out: list[str] = []
    for line in raw_lines:
        if not passes(line):
            continue
        key = line.split("#")[0].strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(line)
    stats = {"unique": len(out)}
    log(f"filtered unique={len(out)}")
    return out, stats
