#!/usr/bin/env python3
"""
Агрегатор рабочих VPN/прокси конфигов (VLESS / VMess / Trojan / Shadowsocks).
Скачивает публичные подписки, проверяет TCP-доступность серверов
и сохраняет только живые конфиги, отсортированные по пингу.
"""

import base64
import json
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import requests
from config import (
    SOURCES,
    MAX_WORKERS,
    MAX_PING,
    MAX_SERVERS,
    PROTOCOLS,
    CONNECT_TIMEOUT,
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_source(url: str) -> list[str]:
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            log(f"  HTTP {response.status_code}: {url[:60]}")
            return []

        content = response.text.strip()
        if not content:
            return []

        # Пробуем base64, иначе берём как plain text
        try:
            decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
            return [line.strip() for line in decoded.splitlines() if line.strip()]
        except Exception:
            return [line.strip() for line in content.splitlines() if line.strip()]

    except Exception as e:
        log(f"  Ошибка {url[:50]}: {e}")
        return []


def parse_config(line: str) -> dict | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    for protocol in ("vless", "vmess", "trojan", "ss", "hysteria", "hysteria2"):
        if line.startswith(f"{protocol}://"):
            name = line.split("#", 1)[-1] if "#" in line else "Unknown"
            # Убираем URL-encoded символы в имени для читаемости
            try:
                from urllib.parse import unquote
                name = unquote(name)
            except Exception:
                pass
            return {
                "protocol": protocol,
                "raw": line,
                "name": name[:80],
            }
    return None


def extract_host_port(line: str, protocol: str) -> tuple[str | None, int | None]:
    try:
        if protocol == "vmess":
            encoded = line.removeprefix("vmess://")
            # Добавляем padding если нужно
            padding = 4 - len(encoded) % 4
            if padding != 4:
                encoded += "=" * padding
            data = json.loads(base64.b64decode(encoded).decode("utf-8"))
            host = data.get("add") or data.get("host")
            port = int(data.get("port", 443))
            return host, port
        else:
            # vless://uuid@host:port?...  или trojan://pass@host:port?...  или ss://...
            match = re.search(r"@([^:/?\s]+):(\d+)", line)
            if match:
                return match.group(1), int(match.group(2))
    except Exception:
        pass
    return None, None


def test_connection(config: dict) -> tuple[str | None, int]:
    """TCP-проверка доступности сервера (без root)."""
    try:
        host, port = extract_host_port(config["raw"], config["protocol"])
        if not host or not port:
            return None, 9999

        # Отбрасываем локальные и явно мусорные адреса
        if host in ("0.0.0.0", "127.0.0.1", "localhost") or host.startswith("192.168."):
            return None, 9999

        start = time.perf_counter()
        with socket.create_connection((host, port), timeout=CONNECT_TIMEOUT):
            elapsed_ms = int((time.perf_counter() - start) * 1000)
        return host, elapsed_ms
    except Exception:
        return None, 9999


def main() -> None:
    log("Запуск агрегатора VPN-подписок")

    # 1. Скачиваем все источники
    all_lines: list[str] = []
    for url in SOURCES:
        log(f"Скачивание: {url[:55]}...")
        lines = download_source(url)
        log(f"  → {len(lines)} строк")
        all_lines.extend(lines)

    log(f"Всего скачано строк: {len(all_lines)}")

    # 2. Парсим и убираем точные дубликаты
    seen_raw: set[str] = set()
    parsed: list[dict] = []
    for line in all_lines:
        config = parse_config(line)
        if not config or config["protocol"] not in PROTOCOLS:
            continue
        if config["raw"] in seen_raw:
            continue
        seen_raw.add(config["raw"])
        parsed.append(config)

    log(f"Уникальных конфигов: {len(parsed)}")
    log(f"Тестирование TCP ({MAX_WORKERS} потоков)...")

    # 3. Параллельная проверка
    working: list[dict] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(test_connection, c): c for c in parsed}
        for i, future in enumerate(as_completed(futures), 1):
            if i % 200 == 0 or i == len(parsed):
                log(f"  Проверено {i}/{len(parsed)}")
            try:
                host, ms = future.result()
                if host and ms < MAX_PING:
                    config = futures[future]
                    config["host"] = host
                    config["ping"] = ms
                    working.append(config)
            except Exception:
                pass

    log(f"Живых серверов: {len(working)}")

    # 4. Дедупликация по host:port (оставляем самый быстрый)
    best_by_endpoint: dict[str, dict] = {}
    for c in working:
        key = f"{c['host']}:{extract_host_port(c['raw'], c['protocol'])[1]}"
        if key not in best_by_endpoint or c["ping"] < best_by_endpoint[key]["ping"]:
            best_by_endpoint[key] = c

    unique = list(best_by_endpoint.values())
    unique.sort(key=lambda x: x["ping"])

    # 5. Ограничиваем количество (оптимизация размера sub.txt)
    final = unique[:MAX_SERVERS]
    log(f"После дедупликации и лимита: {len(final)} серверов")

    # 6. Формируем подписку
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = [
        "#profile-title: base64:" + base64.b64encode("My VPN Sub".encode()).decode(),
        "#profile-update-interval: 4",
        "#subscription-userinfo: upload=0; download=0; total=1073741824000000; expire=2546249531",
        f"# Generated: {now}",
        f"# Working servers: {len(final)} (max ping {MAX_PING}ms)",
        f"# Source: https://github.com/valdissor1990-ui/My-vpn-sub",
    ]

    content = "\n".join(header + [c["raw"] for c in final]) + "\n"

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(content)

    log("Сохранено: sub.txt")
    log("Топ-5 самых быстрых:")
    for i, c in enumerate(final[:5], 1):
        log(f"  {i}. [{c['ping']:4d}ms] {c['name'][:55]}")


if __name__ == "__main__":
    main()
