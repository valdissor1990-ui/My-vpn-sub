"""Выгрузка: mix / white / black / hy2, ≤20, status.json."""

from __future__ import annotations

import base64
import json
from datetime import datetime, timezone

from config import MAX_BLACK, MAX_SERVERS, MAX_WHITE


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [picker] {msg}")


def _write(path: str, title: str, lines: list[str], extra: list[str]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    t = base64.b64encode(title.encode()).decode()
    header = [
        f"#profile-title: base64:{t}",
        "#profile-update-interval: 1",
        f"# Generated: {now}",
        f"# Count: {len(lines)}",
        *extra,
        "# https://github.com/valdissor1990-ui/My-vpn-sub",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(header + lines) + "\n")
    log(f"{path}: {len(lines)}")


def run_picker(
    working: list[dict],
    collect_stats: dict,
    filter_stats: dict,
    monitor_stats: dict,
    proto_stats: dict,
) -> dict:
    # working already ranked; may be protocol-passed or TCP fallback
    mix = working[:MAX_SERVERS]
    white = [w for w in working if w.get("list_type") == "white"][:MAX_WHITE]
    if len(white) < 5:
        # добор высокоскоренными reality
        extra = [w for w in working if w not in white and "reality" in w["raw"].lower()]
        white = (white + extra)[:MAX_WHITE]
    black = [w for w in working if w.get("list_type") == "black"][:MAX_BLACK]
    if len(black) < 5:
        black = [w for w in working if w not in white][:MAX_BLACK]
    hy2 = [
        w
        for w in working
        if str(w.get("protocol", "")).startswith("hy")
        or w["raw"].lower().startswith(("hy2://", "hysteria"))
    ][:MAX_SERVERS]

    _write(
        "sub.txt",
        "My VPN · top scored",
        [w["raw"] for w in mix],
        [
            f"# proto_ok_run={proto_stats.get('passed', 0)}/{proto_stats.get('tested', 0)}",
            "# scoring+TCP (+ optional Xray HTTP)",
        ],
    )
    _write("sub_white.txt", "My VPN · white", [w["raw"] for w in white], ["# white-ish"])
    _write("sub_black.txt", "My VPN · black", [w["raw"] for w in black], ["# black-ish"])
    _write("sub_hy2.txt", "My VPN · hy2", [w["raw"] for w in hy2], ["# hysteria2"])
    reality = [w for w in mix if "reality" in w["raw"].lower()]
    _write("sub_reality.txt", "My VPN · reality", [w["raw"] for w in reality], ["# reality"])

    status = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collect": collect_stats,
        "filter": filter_stats,
        "monitor": monitor_stats,
        "protocol_test": proto_stats,
        "output": {
            "sub.txt": len(mix),
            "sub_white.txt": len(white),
            "sub_black.txt": len(black),
            "sub_hy2.txt": len(hy2),
            "sub_reality.txt": len(reality),
        },
        "top_scores": [
            {"host": w.get("host"), "score": w.get("score"), "ping": w.get("ping_ms"), "proto_ok": w.get("proto_ok")}
            for w in mix[:10]
        ],
        "health": "ok" if mix else "empty",
        "warning": "Protocol test on GH runner ≠ Yota mobile",
    }
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    log("status.json written")
    return status
