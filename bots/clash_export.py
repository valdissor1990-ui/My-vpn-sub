"""Генерация sub_clash.yaml для Clash Meta / Hiddify."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

# reuse converters from protocol_test
from bots.protocol_test_bot import _link_to_clash


def export_clash_yaml(working: list[dict], path: str = "sub_clash.yaml") -> int:
    proxies = []
    for i, w in enumerate(working):
        p = _link_to_clash(w["raw"], f"node{i}-{w.get('host', 'x')[:20]}")
        if p:
            # human-readable name
            delay = w.get("clash_delay_ms")
            tag = f"{w.get('host')}:{w.get('port')}"
            if delay:
                tag = f"{delay}ms | {tag}"
            if w.get("is_vision"):
                tag = f"VISION | {tag}"
            p["name"] = tag[:64]
            proxies.append(p)

    # unique names
    seen = set()
    uniq = []
    for p in proxies:
        n = p["name"]
        if n in seen:
            p["name"] = n + f"#{len(seen)}"
        seen.add(p["name"])
        uniq.append(p)

    names = [p["name"] for p in uniq]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    conf = {
        "mixed-port": 7890,
        "allow-lan": False,
        "mode": "rule",
        "log-level": "info",
        "proxies": uniq,
        "proxy-groups": [
            {"name": "AUTO", "type": "url-test", "proxies": names or ["DIRECT"], "url": "http://www.gstatic.com/generate_204", "interval": 300},
            {"name": "PROXY", "type": "select", "proxies": ["AUTO"] + names + ["DIRECT"]},
        ],
        "rules": [
            "GEOIP,RU,DIRECT",
            "MATCH,PROXY",
        ],
    }

    # YAML without PyYAML dependency — simple dump
    text = f"# My VPN Sub Clash Meta · {now}\n# nodes: {len(uniq)}\n"
    text += _to_yaml(conf)
    Path(path).write_text(text, encoding="utf-8")
    return len(uniq)


def _to_yaml(obj, indent: int = 0) -> str:
    sp = "  " * indent
    if isinstance(obj, dict):
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{sp}{k}:")
                lines.append(_to_yaml(v, indent + 1))
            else:
                lines.append(f"{sp}{k}: {_scalar(v)}")
        return "\n".join(lines)
    if isinstance(obj, list):
        lines = []
        for item in obj:
            if isinstance(item, dict):
                # first key inline style for proxies
                lines.append(f"{sp}-")
                for k, v in item.items():
                    if isinstance(v, (dict, list)):
                        lines.append(f"{sp}  {k}:")
                        lines.append(_to_yaml(v, indent + 2))
                    else:
                        lines.append(f"{sp}  {k}: {_scalar(v)}")
            else:
                lines.append(f"{sp}- {_scalar(item)}")
        return "\n".join(lines)
    return f"{sp}{_scalar(obj)}"


def _scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if v is None:
        return "null"
    s = str(v)
    if any(c in s for c in ":#{}[],&*?|>!%@`"):
        return json.dumps(s, ensure_ascii=False)
    return s
