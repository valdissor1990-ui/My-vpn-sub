#!/usr/bin/env python3
"""
collector → enrich(raw) → filter → enrich(filtered) → monitor → picker
Пинг ≠ полный VPN: TCP живой, а Reality handshake может падать.
"""

from bots.collector_bot import run_collector
from bots.enrich_bot import run_enrich
from bots.filter_bot import run_filter
from bots.monitor_bot import run_monitor
from bots.picker_bot import run_picker


def main() -> None:
    raw, collect_stats = run_collector()
    run_enrich(raw, tag="raw")

    filtered, filter_stats = run_filter(raw)
    run_enrich(filtered, tag="filtered")

    working, monitor_stats = run_monitor(filtered)
    status = run_picker(working, collect_stats, filter_stats, monitor_stats)
    print(
        "DONE health=",
        status.get("health"),
        "exported=",
        status["output"]["sub.txt"],
        "| note: TCP alive may still fail VLESS handshake on Yota",
    )


if __name__ == "__main__":
    main()
