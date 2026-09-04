"""Бот выгрузки: только рабочие (после monitor), ≤20, status.json."""

from __future__ import annotations

import base64
import json
from datetime import datetime, timezone


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [picker] {msg}")


def run_picker(
    working: list[dict],
    collect_stats: dict,
    filter_stats: dict,
    monitor_stats: dict,
) -> dict:
    now = datetime.now(timezone.utc)
    lines = [w["raw"] for w in working]

    hy2_n = sum(1 for w in working if (w.get("protocol") or "").startswith("hy"))
    title = base64.b64encode("My VPN · top-20 alive".encode()).decode()

    header = [
        f"#profile-title: base64:{title}",
        "#profile-update-interval: 1",
        "#subscription-userinfo: upload=0; download=0; total=1073741824000000; expire=2546249531",
        f"# Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
        f"# Working TCP: {len(lines)} (max 20)",
        f"# Hy2-ish: {hy2_n}",
        "# Monitor: GitHub runner TCP (not Yota mobile)",
        "# bots: collector → filter → monitor → picker",
        "# https://github.com/valdissor1990-ui/My-vpn-sub",
    ]

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(header + lines) + "\n")
    log(f"sub.txt ← {len(lines)} рабочих")

    # отдельные выгрузки
    hy2_lines = [w["raw"] for w in working if (w.get("protocol") or "") in ("hysteria2", "hy2", "hysteria")]
    reality_lines = [w["raw"] for w in working if w not in [x for x in working if (x.get("protocol") or "") in ("hysteria2", "hy2", "hysteria")]]
    # simpler split:
    hy2_lines = [w["raw"] for w in working if str(w.get("protocol", "")).startswith("hy")]
    reality_lines = [w["raw"] for w in working if not str(w.get("protocol", "")).startswith("hy")]

    def write_named(path: str, title_s: str, body: list[str]) -> None:
        t = base64.b64encode(title_s.encode()).decode()
        h = [
            f"#profile-title: base64:{t}",
            "#profile-update-interval: 1",
            f"# Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
            f"# Count: {len(body)}",
            "# https://github.com/valdissor1990-ui/My-vpn-sub",
        ]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(h + body) + "\n")
        log(f"{path} ← {len(body)}")

    write_named("sub_hy2.txt", "My VPN · Hy2 alive", hy2_lines)
    write_named("sub_reality.txt", "My VPN · Reality alive", reality_lines)

    status = {
        "generated_at": now.isoformat(),
        "interval": "hourly",
        "max_servers": 20,
        "collect": {
            "sources_ok": collect_stats.get("ok"),
            "sources_fail": collect_stats.get("fail"),
            "total_lines": collect_stats.get("total_lines"),
        },
        "filter": filter_stats,
        "monitor": monitor_stats,
        "output": {
            "sub.txt": len(lines),
            "sub_hy2.txt": len(hy2_lines),
            "sub_reality.txt": len(reality_lines),
        },
        "health": "ok" if lines else "empty",
        "warning": "TCP check runs outside Russia; Yota whitelist may still block these hosts",
    }

    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    log("status.json обновлён")
    return status
