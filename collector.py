#!/usr/bin/env python3
import base64
import json
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests
from config import SOURCES, MAX_WORKERS, MAX_PING, PROTOCOLS


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_source(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content = response.text.strip()
            try:
                decoded = base64.b64decode(content).decode('utf-8')
                return decoded.split('\n')
            except:
                return content.split('\n')
    except Exception as e:
        log(f"Ошибка {url}: {e}")
    return []


def parse_config(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    for protocol in ['vless', 'vmess', 'trojan', 'ss', 'hysteria', 'hysteria2']:
        if line.startswith(f"{protocol}://"):
            return {
                "protocol": protocol,
                "raw": line,
                "name": line.split('#')[-1] if '#' in line else "Unknown"
            }
    return None


def extract_host_port(line, protocol):
    try:
        if protocol == 'vmess':
            encoded = line.replace('vmess://', '')
            decoded = base64.b64decode(encoded + '==').decode('utf-8')
            data = json.loads(decoded)
            return data.get('add'), int(data.get('port', 443))
        else:
            match = re.search(r'@([^:/?]+):(\d+)', line)
            if match:
                return match.group(1), int(match.group(2))
    except:
        pass
    return None, None


def test_connection(config):
    """Проверить TCP-подключение к серверу (работает без прав root)"""
    try:
        host, port = extract_host_port(config['raw'], config['protocol'])
        if not host or not port:
            return None, 9999
        if host.startswith('0.0.0.0') or host.startswith('127.0.0.1'):
            return None, 9999
        start = time.time()
        sock = socket.create_connection((host, port), timeout=3)
        elapsed = (time.time() - start) * 1000
        sock.close()
        return host, int(elapsed)
    except:
        return None, 9999


def main():
    log("Запуск агрегатора")

    all_configs = []
    for url in SOURCES:
        log(f"Скачивание: {url[:50]}...")
        all_configs.extend(download_source(url))

    log(f"Скачано: {len(all_configs)}")

    parsed = []
    for line in all_configs:
        config = parse_config(line)
        if config and config['protocol'] in PROTOCOLS:
            parsed.append(config)

    log(f"Распознано: {len(parsed)}")
    log(f"Тестирование {len(parsed)} серверов...")

    working = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(test_connection, c): c for c in parsed}
        for i, future in enumerate(as_completed(futures), 1):
            if i % 100 == 0:
                log(f"  Проверено {i}/{len(parsed)}")
            try:
                host, ms = future.result()
                config = futures[future]
                if host and ms < MAX_PING:
                    config['host'] = host
                    config['ping'] = ms
                    working.append(config)
            except:
                pass

    log(f"Рабочих: {len(working)}")
    working.sort(key=lambda x: x['ping'])

    output_lines = [
        "#profile-title: base64:" + base64.b64encode("My VPN Sub".encode()).decode(),
        "#profile-update-interval: 1",
        "#subscription-userinfo: upload=0; download=0; total=1073741824000000; expire=2546249531",
        f"# Generated: {datetime.now().isoformat()}",
        f"# Working servers: {len(working)}",
    ]
    output_lines += [c['raw'] for c in working]

    with open('sub.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    log("Сохранено: sub.txt")
    log("Топ-5 самых быстрых:")
    for i, c in enumerate(working[:5], 1):
        log(f"  {i}. {c['name'][:50]} - {c['ping']}ms")


if __name__ == "__main__":
    main()
