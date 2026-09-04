#!/usr/bin/env python3
"""Сборка white-list конфигов под Yota / мобильный БС."""

import base64
from datetime import datetime, timezone

import requests
from config import SOURCES, MAX_SERVERS, PROTOCOLS


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_source(url: str) -> list[str]:
    try:
        r = requests.get(url, timeout=20)
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
        log(f"  Ошибка: {e}")
        return []


def is_config(line: str) -> bool:
    line = line.strip()
    if not line or line.startswith("#"):
        return False
    for p in PROTOCOLS:
        if line.startswith(f"{p}://") or line.startswith("hy2://"):
            return True
    return False


def score(line: str) -> int:
    s = 0
    low = line.lower()
    if "security=reality" in low:
        s += 100
    if "type=xhttp" in low or "type=grpc" in low:
        s += 50
    if "cidr" in low or "white" in low or "whitelist" in low:
        s += 30
    if "flow=xtls-rprx-vision" in low:
        s += 20
    if line.startswith("vless://"):
        s += 10
    if line.startswith("hysteria2://") or line.startswith("hy2://"):
        s += 25
    return s


def main() -> None:
    log("Сбор WHITE-LIST источников (Yota / БС)")
    all_lines: list[str] = []
    for url in SOURCES:
        log(f"  {url[:60]}...")
        lines = download_source(url)
        log(f"    → {len(lines)} строк")
        all_lines.extend(lines)

    seen: set[str] = set()
    configs: list[str] = []
    for line in all_lines:
        if not is_config(line):
            continue
        key = line.split("#")[0].strip()
        if key in seen:
            continue
        seen.add(key)
        configs.append(line)

    log(f"Уникальных: {len(configs)}")
    configs.sort(key=score, reverse=True)
    final = configs[:MAX_SERVERS]
    reality = sum(1 for c in final if "reality" in c.lower())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    header = [
        "#profile-title: base64:" + base64.b64encode("My VPN · Yota WhiteList".encode()).decode(),
        "#profile-update-interval: 2",
        "#subscription-userinfo: upload=0; download=0; total=1073741824000000; expire=2546249531",
        f"# Generated: {now}",
        f"# Servers: {len(final)} | Reality: {reality}",
        "# Mode: WHITE-LIST for Yota mobile",
        "# https://github.com/valdissor1990-ui/My-vpn-sub",
    ]

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(header + final) + "\n")
    log(f"sub.txt: {len(final)} серверов")


if __name__ == "__main__":
    main()
