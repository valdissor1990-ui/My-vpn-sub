#!/usr/bin/env python3
import base64
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests
from config import SOURCES, PING_TIMEOUT, MAX_WORKERS, MAX_PING, PROTOCOLS
from ping3 import ping


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


def extract_host(line, protocol):
    try:
        if protocol == 'vmess':
            encoded = line.replace('vmess://', '')
            decoded = base64.b64decode(encoded + '==').decode('utf-8')
            data = json.loads(decoded)
            return data.get('add') or data.get('address')
        else:
            match = re.search(r'@([^:/?]+)', line)
            if match:
                return match.group(1)
    except:
        pass
    return None


def test_ping(config):
    try:
        host = extract_host(config['raw'], config['protocol'])
        if not host or host.startswith('0.0.0.0') or host.startswith('127.0.0.1'):
            return None, 9999
        ping_time = ping(host, timeout=PING_TIMEOUT, unit='ms')
        if ping_time is None:
            return None, 9999
        return host, int(ping_time)
    except:
        return None, 9999


def main():
    log("Запуск агрегатора")
    
    all_configs = []
    for url in SOURCES:
        log(f"Скачивание: {url[:50]}...")
        configs = download_source(url)
        all_configs.extend(configs)
    
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
        futures = {executor.submit(test_ping, c): c for c in parsed}
        for i, future in enumerate(as_completed(futures), 1):
            if i % 50 == 0:
                log(f"  Проверено {i}/{len(parsed)}")
            try:
                host, ping_ms = future.result()
                config = futures[future]
                if host and ping_ms < MAX_PING:
                    config['host'] = host
                    config['ping'] = ping_ms
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
    
    for config in working:
        output_lines.append(config['raw'])
    
    output = '\n'.join(output_lines)
    
    with open('sub.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    
    log("Подписка сохранена: sub.txt")
    log("Топ-5 самых быстрых:")
    for i, config in enumerate(working[:5], 1):
        log(f"  {i}. {config['name'][:50]} - {config['ping']}ms")


if __name__ == "__main__":
    main()
