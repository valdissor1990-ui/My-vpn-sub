"""Outputs + base64 + clash yaml + history."""

from __future__ import annotations

import base64
import json
from datetime import datetime, timezone
from pathlib import Path

from bots.clash_export import export_clash_yaml
from bots.score_bot import is_vision_tcp
from config import MAX_BLACK, MAX_SERVERS, MAX_VISION, MAX_WHITE


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [picker] {msg}")


def _key(w: dict) -> str:
    return f"{w.get('host')}:{w.get('port')}:{w.get('protocol')}"


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
    b64_path = path.replace(".txt", "_base64.txt")
    with open(b64_path, "w", encoding="utf-8") as f:
        f.write(base64.b64encode("\n".join(lines).encode()).decode())
    log(f"{path}: {len(lines)}")


def run_picker(
    working: list[dict],
    collect_stats: dict,
    filter_stats: dict,
    monitor_stats: dict,
    proto_stats: dict,
) -> dict:
    for w in working:
        if w.get("is_vision") or is_vision_tcp(w["raw"]):
            w["score"] = w.get("score", 0) + 5
            w["is_vision"] = True

    working = sorted(working, key=lambda w: (-w.get("score", 0), w.get("ping_ms", 9999)))
    mix = working[:MAX_SERVERS]
    vision = [w for w in working if w.get("is_vision") or is_vision_tcp(w["raw"])][:MAX_VISION]

    white = [w for w in working if w.get("list_type") == "white"]
    if len(white) < MAX_WHITE:
        have = {_key(w) for w in white}
        for w in working:
            if _key(w) not in have and "reality" in w["raw"].lower():
                white.append(w)
                have.add(_key(w))
            if len(white) >= MAX_WHITE:
                break
    white = white[:MAX_WHITE]
    white_keys = {_key(w) for w in white}
    black = [w for w in working if w.get("list_type") == "black"]
    if len(black) < 5:
        black = [w for w in working if _key(w) not in white_keys]
    black = black[:MAX_BLACK]
    hy2 = [
        w for w in working
        if str(w.get("protocol", "")).startswith("hy") or w["raw"].lower().startswith(("hy2://", "hysteria"))
    ][:MAX_SERVERS]
    reality = [w for w in mix if "reality" in w["raw"].lower()]

    _write("sub.txt", "My VPN · top", [w["raw"] for w in mix], [
        f"# clash={proto_stats.get('passed', 0)}/{proto_stats.get('tested', 0)}",
        "# engine: mihomo",
    ])
    _write("sub_vision.txt", "My VPN · Vision", [w["raw"] for w in vision], ["# XTLS Vision"])
    _write("sub_white.txt", "My VPN · white", [w["raw"] for w in white], ["# white"])
    _write("sub_black.txt", "My VPN · black", [w["raw"] for w in black], ["# black"])
    _write("sub_hy2.txt", "My VPN · hy2", [w["raw"] for w in hy2], ["# hy2"])
    _write("sub_reality.txt", "My VPN · reality", [w["raw"] for w in reality], ["# reality"])

    clash_n = export_clash_yaml(mix, "sub_clash.yaml")
    log(f"sub_clash.yaml: {clash_n}")

    status = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collect": {
            "sources_ok": collect_stats.get("ok"),
            "sources_fail": collect_stats.get("fail"),
            "total_lines": collect_stats.get("total_lines"),
            "telegram_links": collect_stats.get("telegram_links", 0),
        },
        "filter": filter_stats,
        "monitor": monitor_stats,
        "protocol_test": proto_stats,
        "output": {
            "sub.txt": len(mix),
            "sub_vision.txt": len(vision),
            "sub_white.txt": len(white),
            "sub_black.txt": len(black),
            "sub_hy2.txt": len(hy2),
            "sub_reality.txt": len(reality),
            "sub_clash.yaml": clash_n,
        },
        "pipeline": {
            "raw_lines": collect_stats.get("total_lines"),
            "tg_links": collect_stats.get("telegram_links", 0),
            "filtered": filter_stats.get("unique"),
            "tcp_alive": monitor_stats.get("tcp_alive"),
            "clash_passed": proto_stats.get("passed"),
            "clash_tested": proto_stats.get("tested"),
            "exported": len(mix),
        },
        "top_scores": [
            {
                "host": w.get("host"),
                "score": w.get("score"),
                "ping": w.get("ping_ms"),
                "clash_delay": w.get("clash_delay_ms"),
                "vision": w.get("is_vision"),
                "proto_ok": w.get("proto_ok"),
            }
            for w in mix[:8]
        ],
        "health": "ok" if mix else "empty",
        "mirrors": {
            "jsdelivr": "https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt",
            "clash": "https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_clash.yaml",
            "vision": "https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_vision.txt",
        },
    }

    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)

    # history
    hist = Path("history")
    hist.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    (hist / f"status-{stamp}.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # keep last 48 files
    files = sorted(hist.glob("status-*.json"))
    for old in files[:-48]:
        try:
            old.unlink()
        except Exception:
            pass

    return status
