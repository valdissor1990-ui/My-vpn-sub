"""Анализ status/logs → urgent fix commands для следующего прогона / оператора."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bots import log_bot

FIX_JSON = Path("logs/fix_commands.json")
FIX_MD = Path("logs/FIX_COMMANDS.md")


def analyze(status: dict) -> list[dict[str, Any]]:
    fixes: list[dict[str, Any]] = []
    pipe = status.get("pipeline") or {}
    mon = status.get("monitor") or {}
    proto = status.get("protocol_test") or {}
    col = status.get("collect") or {}
    out = status.get("output") or {}

    exported = int(out.get("sub.txt") or pipe.get("exported") or 0)
    clash_p = int(proto.get("passed") or 0)
    clash_t = int(proto.get("tested") or 0)
    tcp = int(mon.get("tcp_alive") or pipe.get("tcp_alive") or 0)
    sources_fail = int(col.get("sources_fail") or 0)
    sources_ok = int(col.get("sources_ok") or 0)

    if status.get("health") == "empty" or exported == 0:
        fixes.append({
            "priority": "P0",
            "code": "EMPTY_POOL",
            "action": "Увеличить PROTOCOL_TEST_CANDIDATES; временно soft-fill TCP; проверить mihomo download",
            "auto": "soft_fill_tcp",
        })

    if exported < 5 and clash_p > 0:
        fixes.append({
            "priority": "P0",
            "code": "LOW_EXPORT",
            "action": f"Clash ok={clash_p}, export={exported}: soft-fill из TCP top + поднять PROTOCOL_TEST_MAX_PASS",
            "auto": "soft_fill_and_raise_pass",
        })

    if clash_t > 0 and clash_p == 0:
        fixes.append({
            "priority": "P0",
            "code": "CLASH_ZERO",
            "action": "Все delay fail: сменить TEST_URLS / версию mihomo / не резать pool только proto_ok",
            "auto": "force_tcp_fallback_pick",
        })

    if not proto.get("enabled") or proto.get("fallback_tcp"):
        fixes.append({
            "priority": "P1",
            "code": "MIHOMO_DOWN",
            "action": "mihomo не стартовал — проверить releases URL и bin/mihomo",
            "auto": "retry_mihomo_download",
        })

    if sources_fail > sources_ok and sources_ok < 5:
        fixes.append({
            "priority": "P1",
            "code": "SOURCES_DEAD",
            "action": f"sources_ok={sources_ok} fail={sources_fail}: обновить SOURCES зеркала jsDelivr",
            "auto": "prefer_jsdelivr",
        })

    if tcp < 20:
        fixes.append({
            "priority": "P1",
            "code": "TCP_LOW",
            "action": f"tcp_alive={tcp}: ослабить pre_score / dead_cache hours",
            "auto": "clear_stale_dead_cache",
        })

    if clash_t >= 20 and clash_p > 0 and (clash_p / max(clash_t, 1)) < 0.05:
        fixes.append({
            "priority": "P2",
            "code": "CLASH_LOW_RATIO",
            "action": f"pass rate {clash_p}/{clash_t}: расширить кандидатов, снизить score bias на мёртвые free-keys",
            "auto": "raise_candidates",
        })

    # errors.jsonl last entries
    err_path = Path("logs/errors.jsonl")
    if err_path.exists():
        try:
            last = err_path.read_text(encoding="utf-8").strip().splitlines()[-5:]
            for ln in last:
                try:
                    e = json.loads(ln)
                    fixes.append({
                        "priority": "P1",
                        "code": f"LOG_ERR_{e.get('stage', '?')}",
                        "action": e.get("msg", "see errors.jsonl"),
                        "auto": "review_traceback",
                    })
                except Exception:
                    pass
        except Exception:
            pass

    # dedup by code
    seen = set()
    uniq = []
    for f in fixes:
        if f["code"] in seen:
            continue
        seen.add(f["code"])
        uniq.append(f)
    return uniq


def apply_auto_hints(fixes: list[dict]) -> dict:
    """
    Не правит config.py на лету в CI без commit-цикла,
    но пишет machine-readable hints для следующего запуска / ручного фикса.
    """
    hints = {
        "soft_fill_tcp": any(f.get("auto") == "soft_fill_tcp" or f.get("auto") == "soft_fill_and_raise_pass" for f in fixes),
        "force_tcp_fallback_pick": any(f.get("auto") == "force_tcp_fallback_pick" for f in fixes),
        "raise_candidates": any(f.get("auto") == "raise_candidates" for f in fixes),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fixes": fixes,
    }
    Path("logs").mkdir(exist_ok=True)
    FIX_JSON.write_text(json.dumps(hints, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# FIX_COMMANDS — авто-анализ после прогона",
        "",
        f"Updated: {hints['generated_at']}",
        "",
        "Эти команды бот выставляет после анализа логов. Критичные (P0) чинить в первую очередь.",
        "",
    ]
    if not fixes:
        md.append("_Проблем не найдено._")
    for f in fixes:
        md.append(f"## [{f['priority']}] `{f['code']}`")
        md.append("")
        md.append(f"- action: {f['action']}")
        md.append(f"- auto: `{f.get('auto')}`")
        md.append("")
    FIX_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    log_bot.info("health", f"fixes={len(fixes)}", codes=[f["code"] for f in fixes])
    return hints


def run_health(status: dict) -> list[dict]:
    fixes = analyze(status)
    apply_auto_hints(fixes)
    log_bot.snapshot(status, fixes)
    return fixes
