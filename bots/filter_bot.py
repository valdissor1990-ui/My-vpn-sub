"""Бот фильтров: протокол, Reality, XHTTP/gRPC, Hysteria2, дедуп."""

from __future__ import annotations

from datetime import datetime

from config import (
    ALLOW_HYSTERIA2,
    PROTOCOLS,
    REQUIRE_REALITY,
    REQUIRE_XHTTP_OR_GRPC,
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [filter] {msg}")


def protocol_of(line: str) -> str | None:
    low = line.strip().lower()
    for p in ("hysteria2", "hy2", "hysteria", "vless", "vmess", "trojan", "ss"):
        if low.startswith(f"{p}://"):
            return p
    return None


def is_hy2(line: str) -> bool:
    p = protocol_of(line)
    return p in ("hysteria2", "hy2", "hysteria")


def is_reality_xhttp_grpc(line: str) -> bool:
    low = line.lower()
    p = protocol_of(line)
    if p not in ("vless", "vmess", "trojan"):
        return False
    if REQUIRE_REALITY and "reality" not in low and "security=reality" not in low:
        return False
    if REQUIRE_XHTTP_OR_GRPC:
        if not any(x in low for x in ("type=xhttp", "xhttp", "type=grpc", "grpc")):
            return False
    return True


def passes(line: str) -> bool:
    line = line.strip()
    if not line or line.startswith("#"):
        return False
    p = protocol_of(line)
    if not p or p not in PROTOCOLS:
        return False
    if is_hy2(line):
        return ALLOW_HYSTERIA2
    return is_reality_xhttp_grpc(line)


def run_filter(raw_lines: list[str]) -> tuple[list[str], list[str], list[str], dict]:
    """
    Возвращает:
      all_passed, only_hy2, only_reality_xhttp_grpc, stats
    """
    seen: set[str] = set()
    all_passed: list[str] = []
    only_hy2: list[str] = []
    only_reality: list[str] = []

    for line in raw_lines:
        if not passes(line):
            continue
        key = line.split("#")[0].strip()
        if key in seen:
            continue
        seen.add(key)
        all_passed.append(line)
        if is_hy2(line):
            only_hy2.append(line)
        elif is_reality_xhttp_grpc(line):
            only_reality.append(line)

    stats = {
        "unique_passed": len(all_passed),
        "hy2": len(only_hy2),
        "reality_xhttp_grpc": len(only_reality),
    }
    log(
        f"Уникальных: {stats['unique_passed']} "
        f"(Hy2={stats['hy2']}, Reality/XHTTP/gRPC={stats['reality_xhttp_grpc']})"
    )
    return all_passed, only_hy2, only_reality, stats
