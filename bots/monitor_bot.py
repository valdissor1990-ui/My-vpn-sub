"""Pre-score cap → skip dead cache → TCP + score."""

from __future__ import annotations

import json
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from bots.dead_cache import is_dead, mark_alive, mark_dead, stats as dead_stats
from bots.score_bot import classify_list, is_vision_tcp, score_line
from config import CONNECT_TIMEOUT, MAX_PING_MS, MAX_WORKERS, PRE_SCORE_CAP


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [monitor] {msg}")


def protocol_of(line: str) -> str | None:
    low = line.strip().lower()
    for p in ("hysteria2", "hy2", "hysteria", "vless", "vmess", "trojan"):
        if low.startswith(f"{p}://"):
            return p
    return None


def extract_host_port(line: str):
    p = protocol_of(line)
    try:
        if p == "vmess":
            import base64

            encoded = line.split("://", 1)[1].split("#")[0]
            pad = 4 - len(encoded) % 4
            if pad != 4:
                encoded += "=" * pad
            data = json.loads(base64.b64decode(encoded).decode("utf-8", errors="ignore"))
            return data.get("add") or data.get("host"), int(data.get("port", 443))
        m = re.search(r"@([^:/?\s]+):(\d+)", line)
        if m:
            return m.group(1), int(m.group(2))
        m2 = re.search(r"://(?:[^@/]+@)?([^:/?\s]+):(\d+)", line)
        if m2:
            return m2.group(1), int(m2.group(2))
    except Exception:
        pass
    return None, None


def tcp_ping(host: str, port: int) -> int:
    if not host or host.startswith(("127.", "0.0.", "192.168.", "10.")):
        return 99999
    try:
        t0 = time.perf_counter()
        with socket.create_connection((host, int(port)), timeout=CONNECT_TIMEOUT):
            return int((time.perf_counter() - t0) * 1000)
    except Exception:
        return 99999


def run_monitor(candidates: list[str]):
    # 1) pre-score без ping → top PRE_SCORE_CAP
    pre = [(score_line(ln, None), ln) for ln in candidates]
    pre.sort(key=lambda x: -x[0])
    if len(pre) > PRE_SCORE_CAP:
        log(f"pre-score cap {len(pre)} → {PRE_SCORE_CAP}")
        pre = pre[:PRE_SCORE_CAP]
    capped = [ln for _, ln in pre]

    # 2) skip dead cache
    to_check = []
    skipped_dead = 0
    for ln in capped:
        host, port = extract_host_port(ln)
        if host and port and is_dead(host, port):
            skipped_dead += 1
            continue
        to_check.append(ln)
    log(f"TCP candidates={len(to_check)} (skipped_dead={skipped_dead}) {dead_stats()}")

    results = []

    def check(line: str):
        host, port = extract_host_port(line)
        if not host or not port:
            return None
        ms = tcp_ping(host, port)
        if ms >= MAX_PING_MS:
            mark_dead(host, port)
            return None
        mark_alive(host, port)
        return {
            "raw": line,
            "host": host,
            "port": port,
            "ping_ms": ms,
            "protocol": protocol_of(line) or "?",
            "score": score_line(line, ms),
            "list_type": classify_list(line),
            "is_vision": is_vision_tcp(line),
        }

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = [pool.submit(check, c) for c in to_check]
        for i, fut in enumerate(as_completed(futs), 1):
            if i % 400 == 0:
                log(f"  {i}/{len(to_check)}")
            try:
                row = fut.result()
                if row:
                    results.append(row)
            except Exception:
                pass

    results.sort(key=lambda r: (-r["score"], r["ping_ms"]))
    log(f"TCP alive={len(results)}")
    return results, {
        "tcp_alive": len(results),
        "checked": len(to_check),
        "pre_score_cap": PRE_SCORE_CAP,
        "skipped_dead": skipped_dead,
        "dead_cache": dead_stats(),
    }
