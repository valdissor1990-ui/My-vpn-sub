"""Фильтр: Hy2 | Reality+(xhttp|grpc) | Reality+TCP(vision)."""

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


def is_hy2(line: str) -> bool:
    return protocol_of(line) in ("hysteria2", "hy2", "hysteria")


def is_reality(line: str) -> bool:
    low = line.lower()
    return "reality" in low or "security=reality" in low


def is_xhttp_grpc(line: str) -> bool:
    low = line.lower()
    return any(x in low for x in ("type=xhttp", "xhttp", "type=grpc", "grpc"))


def is_reality_tcp(line: str) -> bool:
    low = line.lower()
    if not is_reality(line):
        return False
    # tcp / raw / без явного ws
    if "type=ws" in low or "type=http" in low and "xhttp" not in low:
        return False
    if is_xhttp_grpc(line):
        return False
    return "type=tcp" in low or "type=raw" in low or "flow=xtls-rprx-vision" in low


def passes(line: str) -> bool:
    line = line.strip()
    if not line or line.startswith("#"):
        return False
    p = protocol_of(line)
    if not p or p not in PROTOCOLS:
        return False
    if is_hy2(line):
        return ALLOW_HYSTERIA2
    if REQUIRE_REALITY_FOR_VLESS and not is_reality(line):
        return False
    if ALLOW_XHTTP_GRPC and is_xhttp_grpc(line):
        return True
    if ALLOW_REALITY_TCP and is_reality_tcp(line):
        return True
    return False


def run_filter(raw_lines: list[str]) -> tuple[list[str], dict]:
    seen: set[str] = set()
    out: list[str] = []
    counts = {"hy2": 0, "xhttp_grpc": 0, "reality_tcp": 0}

    for line in raw_lines:
        if not passes(line):
            continue
        key = line.split("#")[0].strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(line)
        if is_hy2(line):
            counts["hy2"] += 1
        elif is_xhttp_grpc(line):
            counts["xhttp_grpc"] += 1
        else:
            counts["reality_tcp"] += 1

    stats = {"unique": len(out), **counts}
    log(f"Фильтр: {len(out)} | {counts}")
    return out, stats
