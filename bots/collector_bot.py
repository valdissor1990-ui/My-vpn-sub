"""Сбор со всех SOURCES."""

from __future__ import annotations

import base64
from datetime import datetime

import requests

from config import SOURCES


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [collector] {msg}")


def _decode(content: str) -> list[str]:
    content = content.strip()
    if not content:
        return []
    try:
        decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = [ln.strip() for ln in decoded.splitlines() if ln.strip()]
        if any(
            ln.lower().startswith(("vless://", "vmess://", "trojan://", "hy2://", "hysteria"))
            for ln in lines[:25]
        ):
            return lines
    except Exception:
        pass
    return [ln.strip() for ln in content.splitlines() if ln.strip()]


def run_collector() -> tuple[list[str], dict]:
    all_lines: list[str] = []
    stats = {"ok": 0, "fail": 0, "total_lines": 0, "sources": []}
    log(f"SOURCES={len(SOURCES)}")
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=25)
            if r.status_code != 200:
                stats["fail"] += 1
                stats["sources"].append({"url": url, "error": r.status_code})
                log(f"FAIL {url[:55]} HTTP {r.status_code}")
                continue
            lines = _decode(r.text)
            stats["ok"] += 1
            stats["sources"].append({"url": url, "lines": len(lines)})
            all_lines.extend(lines)
            log(f"OK {url[:55]} → {len(lines)}")
        except Exception as e:
            stats["fail"] += 1
            stats["sources"].append({"url": url, "error": str(e)})
            log(f"FAIL {url[:40]} {e}")
    stats["total_lines"] = len(all_lines)
    log(f"total raw lines={len(all_lines)}")
    return all_lines, stats
