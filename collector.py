#!/usr/bin/env python3
"""White-list + Hysteria2 сборка с зеркал."""

import base64
from datetime import datetime, timezone

import requests
from config import (
    SOURCES,
    MAX_SERVERS,
    PROTOCOLS,
    ALLOW_HYSTERIA2,
    REQUIRE_REALITY_FOR_VLESS,
    REQUIRE_XHTTP_OR_GRPC_FOR_VLESS,
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_source(url: str) -> list[str]:
    try:
        r = requests.get(url, timeout=25)
        if r.status_code != 200:
            log(f"  HTTP {r.status_code}: {url[:55]}")
            return []
        content = r.text.strip()
        if not content:
            return []
        try:
            decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
            return [ln.strip() for ln in decoded.splitlines() if ln.strip()]
        except Exception:
            return [ln.strip() for ln in content.splitlines() if ln.strip()]
    except Exception as e:
        log(f"  err: {e}")
        return []


def protocol_of(line: str) -> str | None:
    line = line.strip().lower()
    for p in ("hysteria2", "hy2", "hysteria", "vless", "vmess", "trojan"):
        if line.startswith(f"{p}://"):
            return p
    return None


def passes(line: str) -> bool:
    p = protocol_of(line)
    if not p:
        return False
    low = line.lower()

    if p in ("hysteria2", "hy2", "hysteria"):
        return ALLOW_HYSTERIA2

    # vless/vmess/trojan: Reality + xhttp/grpc
    if REQUIRE_REALITY_FOR_VLESS:
        if "security=reality" not in low and "reality" not in low:
            return False
    if REQUIRE_XHTTP_OR_GRPC_FOR_VLESS:
        if not any(x in low for x in ("type=xhttp", "xhttp", "type=grpc", "grpc")):
            return False
    return True


def score(line: str) -> int:
    low = line.lower()
    s = 0
    if low.startswith("hysteria2://") or low.startswith("hy2://"):
        s += 80
    if "xhttp" in low:
        s += 50
    if "grpc" in low:
        s += 40
    if "reality" in low:
        s += 30
    if "cidr" in low or "white" in low:
        s += 15
    return s


def main() -> None:
    log("Сбор WL + Hysteria2")
    all_lines: list[str] = []
    for url in SOURCES:
        log(f"  {url[:60]}...")
        lines = download_source(url)
        log(f"    → {len(lines)}")
        all_lines.extend(lines)

    seen: set[str] = set()
    configs: list[str] = []
    for line in all_lines:
        if not passes(line):
            continue
        key = line.split("#")[0].strip()
        if key in seen:
            continue
        seen.add(key)
        configs.append(line)

    log(f"После фильтра: {len(configs)}")
    configs.sort(key=score, reverse=True)
    final = configs[:MAX_SERVERS]

    hy = sum(1 for c in final if c.lower().startswith(("hysteria2://", "hy2://", "hysteria://")))
    xv = len(final) - hy
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    header = [
        "#profile-title: base64:" + base64.b64encode("My VPN · WL + Hy2".encode()).decode(),
        "#profile-update-interval: 2",
        "#subscription-userinfo: upload=0; download=0; total=1073741824000000; expire=2546249531",
        f"# Generated: {now}",
        f"# Servers: {len(final)} | Reality/XHTTP/gRPC: {xv} | Hysteria2: {hy}",
        "# Sources: zieng2, igareck, Subzio, kizyak, Endi (mirrors)",
        "# https://github.com/valdissor1990-ui/My-vpn-sub",
    ]

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(header + final) + "\n")
    log(f"sub.txt: {len(final)}")


if __name__ == "__main__":
    main()
