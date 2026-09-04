#!/usr/bin/env python3
"""
collector → telegram? → filter → enrich → monitor(TCP+score)
  → protocol_test(Xray HTTP) → picker (mix/white/black/hy2 ≤20)
"""

from bots.collector_bot import run_collector
from bots.enrich_bot import run_enrich
from bots.filter_bot import run_filter
from bots.monitor_bot import run_monitor
from bots.picker_bot import run_picker
from bots.protocol_test_bot import run_protocol_test
from bots.telegram_bot import run_telegram_collect


def main() -> None:
    raw, collect_stats = run_collector()
    tg_links = run_telegram_collect()
    if tg_links:
        raw.extend(tg_links)
        collect_stats["telegram_links"] = len(tg_links)

    filtered, filter_stats = run_filter(raw)
    run_enrich(filtered, "filtered")

    tcp_alive, monitor_stats = run_monitor(filtered)
    proto_passed, proto_stats = run_protocol_test(tcp_alive)

    status = run_picker(
        proto_passed, collect_stats, filter_stats, monitor_stats, proto_stats
    )
    print("HEALTH", status.get("health"), status.get("output"))


if __name__ == "__main__":
    main()
