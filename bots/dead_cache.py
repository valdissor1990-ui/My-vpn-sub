"""Кэш мёртвых host:port на DEAD_CACHE_HOURS часов."""

from __future__ import annotations

import json
import time
from pathlib import Path

from config import DEAD_CACHE_FILE, DEAD_CACHE_HOURS


def _load() -> dict:
    p = Path(DEAD_CACHE_FILE)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save(data: dict) -> None:
    Path(DEAD_CACHE_FILE).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def is_dead(host: str, port: int) -> bool:
    data = _load()
    key = f"{host}:{port}"
    ts = data.get(key)
    if not ts:
        return False
    if time.time() - float(ts) > DEAD_CACHE_HOURS * 3600:
        return False
    return True


def mark_dead(host: str, port: int) -> None:
    data = _load()
    data[f"{host}:{port}"] = time.time()
    # prune old
    cutoff = time.time() - DEAD_CACHE_HOURS * 3600 * 2
    data = {k: v for k, v in data.items() if float(v) >= cutoff}
    _save(data)


def mark_alive(host: str, port: int) -> None:
    data = _load()
    key = f"{host}:{port}"
    if key in data:
        del data[key]
        _save(data)


def stats() -> dict:
    data = _load()
    now = time.time()
    active = sum(1 for v in data.values() if now - float(v) <= DEAD_CACHE_HOURS * 3600)
    return {"entries": len(data), "active_dead": active, "hours": DEAD_CACHE_HOURS}
