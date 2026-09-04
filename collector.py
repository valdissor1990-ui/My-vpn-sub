#!/usr/bin/env python3
"""
Оркестратор ботов:
  1) collector_bot — сбор с зеркал
  2) filter_bot    — Reality/XHTTP/gRPC + Hysteria2, дедуп
  3) picker_bot    — ranking, top-N, несколько подписок + status.json
"""

from bots.collector_bot import run_collector
from bots.filter_bot import run_filter
from bots.picker_bot import run_picker


def main() -> None:
    raw, collect_stats = run_collector()
    all_passed, only_hy2, only_reality, filter_stats = run_filter(raw)
    run_picker(all_passed, only_hy2, only_reality, collect_stats, filter_stats)
    print("OK: bots finished")


if __name__ == "__main__":
    main()
