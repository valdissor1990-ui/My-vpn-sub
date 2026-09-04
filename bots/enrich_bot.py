"""Мета по набору ключей."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone


def run_enrich(lines: list[str], tag: str = "filtered") -> dict:
    protos = Counter()
    for ln in lines:
        low = ln.lower()
        for p in ("hysteria2", "hy2", "vless", "vmess", "trojan", "hysteria"):
            if low.startswith(f"{p}://"):
                protos[p] += 1
                break
    meta = {
        "tag": tag,
        "count": len(lines),
        "protocols": dict(protos),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(f"meta_{tag}.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return meta
