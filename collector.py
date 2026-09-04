#!/usr/bin/env python3
"""White-list сборка: только Reality + XHTTP/gRPC, источники с зеркал."""

import base64
from datetime import datetime, timezone

import requests
from config import (
    SOURCES,
    MAX_SERVERS,
    PROTOCOLS,
    REQUIRE_REALITY,
    REQUIRE_XHTTP_OR_GRPC,
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_source(url: str) -> list[str]:
    try:
        r = requests.get(url, timeout=25)
        if r.status_code != 200:
            log(f"  HTTP {r.status_code}: {url[:60]}")
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
        log(f"  Ошибка {url[:40]}: {e}")
        return []


def is_config(line: str) -> bool:
    line = line.strip()
    if not line or line.startswith("#"):
        return False
    return any(line.startswith(f"{p}://") for p in PROTOCOLS)


def passes_strict_filter(line: str) -> bool:
    low = line.lower()
    if REQUIRE_REALITY and "security=reality" not in low and "reality" not in low:
        return False
    if REQUIRE_XHTTP_OR_GRPC:
        if "type=xhttp" not in low and "type=grpc" not in low and "network=grpc" not in low:
            # также xhttp иногда как packet-up / mode=
            if "xhttp" not in low and "grpc" not in low:
                return False
    return True


def score(line: str) -> int:
    s = 0
    low = line.lower()
    if "type=xhttp" in low or "xhttp" in low:
        s += 50
    if "type=grpc" in low or "grpc" in low:
        s += 40
    if "flow=xtls-rprx-vision" in low:
        s += 15
    if "cidr" in low or "white" in low:
        s += 20
    return s


def main() -> None:
    log("Сбор зеркал → фильтр Reality + XHTTP/gRPC")
    all_lines: list[str] = []
    for url in SOURCES:
        log(f"  {url[:65]}...")
        lines = download_source(url)
        log(f"    → {len(lines)}")
        all_lines.extend(lines)

    seen: set[str] = set()
    configs: list[str] = []
    for line in all_lines:
        if not is_config(line):
            continue
        if not passes_strict_filter(line):
            continue
        key = line.split("#")[0].strip()
        if key in seen:
            continue
        seen.add(key)
        configs.append(line)

    log(f"После фильтра Reality+XHTTP/gRPC: {len(configs)}")
    configs.sort(key=score, reverse=True)
    final = configs[:MAX_SERVERS]

    xhttp_n = sum(1 for c in final if "xhttp" in c.lower())
    grpc_n = sum(1 for c in final if "grpc" in c.lower())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    header = [
        "#profile-title: base64:" + base64.b64encode("My VPN · Reality XHTTP/gRPC".encode()).decode(),
        "#profile-update-interval: 2",
        "#subscription-userinfo: upload=0; download=0; total=1073741824000000; expire=2546249531",
        f"# Generated: {now}",
        f"# Servers: {len(final)} | XHTTP: {xhttp_n} | gRPC: {grpc_n}",
        "# Filter: Reality + (XHTTP or gRPC) only",
        "# Mirrors: jsDelivr, GitHack, Codeberg, Bitbucket",
        "# https://github.com/valdissor1990-ui/My-vpn-sub",
    ]

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(header + final) + "\n")
    log(f"sub.txt: {len(final)} (XHTTP={xhttp_n}, gRPC={grpc_n})")


if __name__ == "__main__":
    main()
