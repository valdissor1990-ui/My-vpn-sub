"""Бот фильтров: протокол / Reality / XHTTP|gRPC / Hy2 / дедуп."""

from __future__ import annotations

from datetime import datetime

from config import (
    ALLOW_HYSTERIA2,
    PROTOCOLS,
    REQUIRE_REALITY_FOR_VLESS,
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
    return protocol_of(line) in ("hysteria2", "hy2", "hysteria")


def is_reality_fast(line: str) -> bool:
    low = line.lower()
    p = protocol_of(line)
    if p not in ("vless", "vmess", "trojan"):
        return False
    if REQUIRE_REALITY_FOR_VLESS and "reality" not in low:
        return False
    if REQUIRE_XHTTP_OR_GRPC and not any(
        x in low for x in ("type=xhttp", "xhttp", "type=grpc", "grpc")
    ):
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
    return is_reality_fast(line)


def run_filter(raw_lines: list[str]) -> tuple[list[str], dict]:
    seen: set[str] = set()
    out: list[str] = []
    hy2 = 0
    reality = 0

    for line in raw_lines:
        if not passes(line):
            continue
        key = line.split("#")[0].strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(line)
        if is_hy2(line):
            hy2 += 1
        else:
            reality += 1

    stats = {"unique": len(out), "hy2": hy2, "reality_xhttp_grpc": reality}
    log(f"После фильтра: {len(out)} (Hy2={hy2}, Reality={reality})")
    return out, stats
