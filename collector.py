#!/usr/bin/env python3
"""collector → tg → filter → monitor → clash → rotate picker"""

import sys
import traceback

from bots.collector_bot import run_collector
from bots.enrich_bot import run_enrich
from bots.filter_bot import run_filter
from bots.monitor_bot import run_monitor
from bots.notify_bot import notify_status
from bots.picker_bot import run_picker
from bots.protocol_test_bot import run_protocol_test
from bots.telegram_bot import run_telegram_collect


def main() -> int:
    try:
        raw, collect_stats = run_collector()
        tg = run_telegram_collect()
        if tg:
            raw.extend(tg)
            collect_stats["telegram_links"] = len(tg)

        filtered, filter_stats = run_filter(raw)
        run_enrich(filtered, "filtered")

        tcp_alive, monitor_stats = run_monitor(filtered)
        proto_passed, proto_stats = run_protocol_test(tcp_alive)
        status = run_picker(
            proto_passed, collect_stats, filter_stats, monitor_stats, proto_stats
        )
        notify_status(status)
        print("PIPELINE", status.get("pipeline"))
        print("HEALTH", status.get("health"), "source", status.get("pick_source"))
        return 0 if status.get("health") == "ok" else 1
    except Exception:
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
