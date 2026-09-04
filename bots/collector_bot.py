"""Бот сбора: качает все SOURCES, декодирует base64, возвращает сырые строки."""

from __future__ import annotations

import base64
from datetime import datetime

import requests

from config import SOURCES


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [collector] {msg}")


def _decode_body(content: str) -> list[str]:
    content = content.strip()
    if not content:
        return []
    try:
        decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
        lines = [ln.strip() for ln in decoded.splitlines() if ln.strip()]
        if lines and any(
            ln.startswith((
                "vless://",
                "vmess://",
                "trojan://",
                "ss://",
                "hysteria",
                "hy2://",
            ))
            for ln in lines[:20]
        ):
            return lines
    except Exception:
        pass
    return [ln.strip() for ln in content.splitlines() if ln.strip()]


def fetch_one(url: str) -> tuple[str, list[str], str | None]:
    try:
        r = requests.get(url, timeout=25)
        if r.status_code != 200:
            return url, [], f"HTTP {r.status_code}"
        return url, _decode_body(r.text), None
    except Exception as e:
        return url, [], str(e)


def run_collector() -> tuple[list[str], dict]:
    """Возвращает все строки + статистику по источникам."""
    log(f"Источников: {len(SOURCES)}")
    all_lines: list[str] = []
    stats: dict = {"sources": [], "ok": 0, "fail": 0, "total_lines": 0}

    for url in SOURCES:
        u, lines, err = fetch_one(url)
        short = u[:70]
        if err:
            log(f"FAIL {short} → {err}")
            stats["fail"] += 1
            stats["sources"].append({"url": u, "lines": 0, "error": err})
        else:
            log(f"OK   {short} → {len(lines)}")
            stats["ok"] += 1
            stats["sources"].append({"url": u, "lines": len(lines), "error": None})
            all_lines.extend(lines)

    stats["total_lines"] = len(all_lines)
    log(f"Собрано строк: {len(all_lines)} (ok={stats['ok']} fail={stats['fail']})")
    return all_lines, stats
