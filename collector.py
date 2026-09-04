#!/usr/bin/env python3
"""
Оркестратор (каждый час):
  collector → filter → monitor(TCP) → picker(≤20 working)
"""

from bots.collector_bot import run_collector
from bots.filter_bot import run_filter
from bots.monitor_bot import run_monitor
from bots.picker_bot import run_picker


def main() -> None:
    raw, collect_stats = run_collector()
    filtered, filter_stats = run_filter(raw)
    working, monitor_stats = run_monitor(filtered)
    status = run_picker(working, collect_stats, filter_stats, monitor_stats)
    print("STATUS:", status.get("health"), "exported", status["output"]["sub.txt"])


if __name__ == "__main__":
    main()
