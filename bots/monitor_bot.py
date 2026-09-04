"""
Бот мониторинга работоспособности.
TCP connect host:port с раннера GitHub Actions (не из сети Yota).

Важно: «alive» здесь ≠ гарантия работы на мобильном БС в РФ.
Это отсев мёртвых IP/портов. Финальная проверка — только с твоей SIM.
"""

from __future__ import annotations

import json
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.parse import unquote

from config import CONNECT_TIMEOUT, MAX_PING_MS, MAX_SERVERS, MAX_WORKERS, PREFERRED_SNI


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [monitor] {msg}")


def protocol_of(line: str) -> str | None:
    low = line.strip().lower()
    for p in ("hysteria2", "hy2", "hysteria", "vless", "vmess", "trojan"):
        if low.startswith(f"{p}://"):
            return p
    return None


def extract_host_port(line: str) -> tuple[str | None, int | None]:
    p = protocol_of(line)
    if not p:
        return None, None
    try:
        if p == "vmess":
            import base64

            encoded = line.split("://", 1)[1].split("#")[0]
            pad = 4 - len(encoded) % 4
            if pad != 4:
                encoded += "=" * pad
            data = json.loads(base64.b64decode(encoded).decode("utf-8", errors="ignore"))
            host = data.get("add") or data.get("host")
            port = int(data.get("port", 443))
            return host, port

        # vless/trojan/hy2: user@host:port
        m = re.search(r"@([^:/?\s]+):(\d+)", line)
        if m:
            return m.group(1), int(m.group(2))
        # hy2 sometimes host:port without @
        m2 = re.search(r"://(?:[^@/]+@)?([^:/?\s]+):(\d+)", line)
        if m2:
            return m2.group(1), int(m2.group(2))
    except Exception:
        pass
    return None, None


def tcp_ping(host: str, port: int) -> int:
    """Возвращает RTT мс или 99999 при ошибке."""
    if not host or host in ("0.0.0.0", "127.0.0.1", "localhost"):
        return 99999
    if host.startswith("192.168.") or host.startswith("10."):
        return 99999
    try:
        start = time.perf_counter()
        with socket.create_connection((host, port), timeout=CONNECT_TIMEOUT):
            return int((time.perf_counter() - start) * 1000)
    except Exception:
        return 99999


def score_line(line: str, ping_ms: int) -> tuple:
    low = line.lower()
    s = 0
    if low.startswith(("hysteria2://", "hy2://")):
        s += 50
    if "xhttp" in low:
        s += 30
    if "grpc" in low:
        s += 20
    if "reality" in low:
        s += 15
    for pref in PREFERRED_SNI:
        if pref in low:
            s += 10
            break
    return (-s, ping_ms)  # выше score, ниже ping


def run_monitor(candidates: list[str]) -> tuple[list[dict], dict]:
    log(f"TCP-проверка {len(candidates)} кандидатов (timeout={CONNECT_TIMEOUT}s)...")
    log("NOTE: проверка с GitHub runner, НЕ с мобильной сети РФ")

    results: list[dict] = []

    def check(line: str) -> dict | None:
        host, port = extract_host_port(line)
        if not host or not port:
            return None
        ms = tcp_ping(host, port)
        if ms >= MAX_PING_MS:
            return None
        return {
            "raw": line,
            "host": host,
            "port": port,
            "ping_ms": ms,
            "protocol": protocol_of(line) or "?",
        }

    alive = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = {pool.submit(check, c): c for c in candidates}
        done = 0
        for fut in as_completed(futs):
            done += 1
            if done % 200 == 0 or done == len(candidates):
                log(f"  проверено {done}/{len(candidates)}")
            try:
                row = fut.result()
                if row:
                    results.append(row)
                    alive += 1
            except Exception:
                pass

    results.sort(key=lambda r: score_line(r["raw"], r["ping_ms"]))
    top = results[:MAX_SERVERS]

    stats = {
        "checked": len(candidates),
        "tcp_alive": alive,
        "exported": len(top),
        "max_servers": MAX_SERVERS,
        "max_ping_ms": MAX_PING_MS,
        "runner_note": "TCP from GitHub Actions (not RU mobile/Yota)",
        "top_pings": [{"host": r["host"], "port": r["port"], "ms": r["ping_ms"], "proto": r["protocol"]} for r in top[:10]],
    }
    log(f"Живых TCP: {alive} → в подписку: {len(top)} (max {MAX_SERVERS})")
    return top, stats
