#!/usr/bin/env python3
"""collector → tg → filter → monitor → clash → picker → health/logs"""

import sys

from bots import log_bot
from bots.collector_bot import run_collector
from bots.enrich_bot import run_enrich
from bots.filter_bot import run_filter
from bots.health_bot import run_health
from bots.monitor_bot import run_monitor
from bots.notify_bot import notify_status
from bots.picker_bot import run_picker
from bots.protocol_test_bot import run_protocol_test
from bots.telegram_bot import run_telegram_collect


def main() -> int:
    try:
        log_bot.info("main", "pipeline start")
        raw, collect_stats = run_collector()
        log_bot.info("collect", f"lines={collect_stats.get('total_lines')} ok={collect_stats.get('ok')} fail={collect_stats.get('fail')}")

        tg = run_telegram_collect()
        if tg:
            raw.extend(tg)
            collect_stats["telegram_links"] = len(tg)
        log_bot.info("tg", f"links={len(tg)}")

        filtered, filter_stats = run_filter(raw)
        log_bot.info("filter", f"unique={filter_stats.get('unique')}")
        run_enrich(filtered, "filtered")

        tcp_alive, monitor_stats = run_monitor(filtered)
        log_bot.info("monitor", f"tcp_alive={monitor_stats.get('tcp_alive')}")

        proto_passed, proto_stats = run_protocol_test(tcp_alive)
        log_bot.info(
            "clash",
            f"passed={proto_stats.get('passed')}/{proto_stats.get('tested')} enabled={proto_stats.get('enabled')}",
        )

        status = run_picker(
            proto_passed, collect_stats, filter_stats, monitor_stats, proto_stats
        )
        fixes = run_health(status)
        try:
            notify_status(status)
        except Exception as e:
            log_bot.error("notify", "telegram notify failed", e)

        print("PIPELINE", status.get("pipeline"))
        print("HEALTH", status.get("health"), "source", status.get("pick_source"))
        print("FIXES", [f.get("code") for f in fixes])
        return 0 if status.get("health") == "ok" else 1
    except Exception as e:
        log_bot.error("main", "pipeline crash", e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
