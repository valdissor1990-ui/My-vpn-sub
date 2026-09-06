"""Выгрузка: только рабочие + ротация каждый час."""

from __future__ import annotations

import base64
import json
from datetime import datetime, timezone
from pathlib import Path

from bots.clash_export import export_clash_yaml
from bots.score_bot import is_vision_tcp
from config import MAX_BLACK, MAX_SERVERS, MAX_VISION, MAX_WHITE

LAST_FILE = "last_export.json"


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [picker] {msg}")


def _key(w: dict) -> str:
    return f"{w.get('host')}:{w.get('port')}"


def _load_last() -> set[str]:
    p = Path(LAST_FILE)
    if not p.exists():
        return set()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return set(data.get("keys") or [])
    except Exception:
        return set()


def _save_last(keys: list[str]) -> None:
    Path(LAST_FILE).write_text(
        json.dumps({"keys": keys, "at": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )


def _dedup(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for w in items:
        k = _key(w)
        if k in seen:
            continue
        seen.add(k)
        out.append(w)
    return out


def _rotate(pool: list[dict], n: int) -> list[dict]:
    """Новые рабочие сначала, потом следующий срез пула (чтоб список не стоял)."""
    pool = _dedup(pool)
    last = _load_last()
    fresh = [w for w in pool if _key(w) not in last]
    stale = [w for w in pool if _key(w) in last]
    hour = datetime.now(timezone.utc).hour
    # сдвиг, чтоб даже при том же пуле набор менялся
    if stale:
        off = (hour * 3) % max(len(stale), 1)
        stale = stale[off:] + stale[:off]
    picked = (fresh + stale)[:n]
    _save_last([_key(w) for w in picked])
    log(f"rotate pool={len(pool)} fresh={len(fresh)} picked={len(picked)} last={len(last)}")
    return picked


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
        if w.get("is_vision") or is_vision_tcp(w.get("raw", "")):
            w["score"] = w.get("score", 0) + 5
            w["is_vision"] = True

    working = sorted(working, key=lambda w: (-w.get("score", 0), w.get("ping_ms", 9999)))

    proto_ok = [w for w in working if w.get("proto_ok")]
    # если Clash проверил узлы — в sub.txt ТОЛЬКО proto_ok
    if proto_stats.get("passed", 0) > 0 and proto_ok:
        pool = proto_ok
        source = "clash_http"
    else:
        pool = working
        source = "tcp_fallback"

    mix = _rotate(pool, MAX_SERVERS)
    vision = _rotate(
        [w for w in pool if w.get("is_vision") or is_vision_tcp(w.get("raw", ""))],
        MAX_VISION,
    )
    white = _rotate([w for w in pool if w.get("list_type") == "white"] or pool, MAX_WHITE)
    black = _rotate([w for w in pool if w.get("list_type") != "white"], MAX_BLACK)
    hy2 = _rotate(
        [
            w
            for w in pool
            if str(w.get("protocol", "")).startswith("hy")
            or w.get("raw", "").lower().startswith(("hy2://", "hysteria"))
        ],
        MAX_SERVERS,
    )
    reality = [w for w in mix if "reality" in w.get("raw", "").lower()]

    _write(
        "sub.txt",
        "My VPN · live",
        [w["raw"] for w in mix],
        [
            f"# source={source}",
            f"# clash={proto_stats.get('passed', 0)}/{proto_stats.get('tested', 0)}",
            "# rotated each run; only checked nodes",
        ],
    )
    _write("sub_vision.txt", "My VPN · Vision", [w["raw"] for w in vision], ["# XTLS Vision"])
    _write("sub_white.txt", "My VPN · white", [w["raw"] for w in white], ["# white"])
    _write("sub_black.txt", "My VPN · black", [w["raw"] for w in black], ["# black"])
    _write("sub_hy2.txt", "My VPN · hy2", [w["raw"] for w in hy2], ["# hy2"])
    _write("sub_reality.txt", "My VPN · reality", [w["raw"] for w in reality], ["# reality"])

    clash_n = export_clash_yaml(mix, "sub_clash.yaml")

    status = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pick_source": source,
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
            "pick_source": source,
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
            "raw": "https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub.txt",
        },
    }
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)

    hist = Path("history")
    hist.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    (hist / f"status-{stamp}.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    files = sorted(hist.glob("status-*.json"))
    for old in files[:-48]:
        try:
            old.unlink()
        except Exception:
            pass
    return status
