"""
Протокольный smoke-тест через Xray-core (если бинарник доступен).
Для каждого кандидата: временный socks inbound + outbound из share-link,
затем HTTP GET через socks. Не Hy2 (нужен другой клиент).

Если xray не скачался — пропускаем, оставляем TCP+score.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from config import PROTOCOL_TEST_CANDIDATES, PROTOCOL_TEST_TIMEOUT

XRAY_URL = (
    "https://github.com/XTLS/Xray-core/releases/download/v25.8.3/"
    "Xray-linux-64.zip"
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [proto] {msg}")


def _ensure_xray() -> str | None:
    cache = Path("bin")
    cache.mkdir(exist_ok=True)
    binary = cache / "xray"
    if binary.exists() and os.access(binary, os.X_OK):
        return str(binary)
    try:
        log("Скачиваю Xray-core...")
        zip_path = cache / "xray.zip"
        urllib.request.urlretrieve(XRAY_URL, zip_path)
        import zipfile

        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(cache)
        if binary.exists():
            binary.chmod(0o755)
            return str(binary)
        # иногда имя Xray
        alt = cache / "Xray"
        if alt.exists():
            alt.chmod(0o755)
            return str(alt)
    except Exception as e:
        log(f"Xray download failed: {e}")
    return None


def _vless_to_outbound(link: str) -> dict | None:
    """Грубый парсер vless:// → xray outbound. Не все transport покрыты."""
    try:
        from urllib.parse import parse_qs, unquote, urlparse

        if not link.startswith("vless://"):
            return None
        u = urlparse(link)
        uuid = u.username
        host = u.hostname
        port = u.port or 443
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        security = q.get("security", "none")
        network = q.get("type", "tcp")
        if network == "raw":
            network = "tcp"

        stream: dict = {"network": network}
        if security == "reality":
            stream["security"] = "reality"
            stream["realitySettings"] = {
                "publicKey": q.get("pbk", ""),
                "fingerprint": q.get("fp", "chrome"),
                "serverName": q.get("sni", host),
                "shortId": q.get("sid", ""),
                "spiderX": q.get("spx", "/"),
            }
        elif security == "tls":
            stream["security"] = "tls"
            stream["tlsSettings"] = {"serverName": q.get("sni", host)}

        if network == "ws":
            stream["wsSettings"] = {
                "path": q.get("path", "/"),
                "headers": {"Host": q.get("host", q.get("sni", host))},
            }
        elif network == "grpc":
            stream["grpcSettings"] = {"serviceName": q.get("serviceName", q.get("path", ""))}
        elif network == "xhttp":
            # xray newer: xhttp
            stream["network"] = "xhttp"
            stream["xhttpSettings"] = {
                "path": q.get("path", "/"),
                "host": q.get("host", q.get("sni", "")),
                "mode": q.get("mode", "auto"),
            }

        outbound = {
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": host,
                        "port": int(port),
                        "users": [
                            {
                                "id": uuid,
                                "encryption": q.get("encryption", "none"),
                                "flow": q.get("flow", ""),
                            }
                        ],
                    }
                ]
            },
            "streamSettings": stream,
        }
        return outbound
    except Exception:
        return None


def _test_one(xray_bin: str, link: str, socks_port: int) -> bool:
    outbound = _vless_to_outbound(link)
    if not outbound:
        return False
    conf = {
        "log": {"loglevel": "error"},
        "inbounds": [
            {
                "port": socks_port,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {"udp": False},
            }
        ],
        "outbounds": [outbound, {"protocol": "freedom", "tag": "direct"}],
    }
    proc = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(conf, f)
            conf_path = f.name
        proc = subprocess.Popen(
            [xray_bin, "run", "-c", conf_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1.2)
        # HTTP через socks
        proxy_handler = urllib.request.ProxyHandler(
            {"http": f"socks5h://127.0.0.1:{socks_port}"}
        )
        opener = urllib.request.build_opener(proxy_handler)
        # многие узлы режут произвольные сайты — пробуем generate_204
        req = urllib.request.Request(
            "http://www.gstatic.com/generate_204",
            method="GET",
        )
        with opener.open(req, timeout=PROTOCOL_TEST_TIMEOUT) as resp:
            return resp.status in (204, 200, 301, 302)
    except Exception:
        return False
    finally:
        if proc:
            proc.kill()
            try:
                proc.wait(timeout=3)
            except Exception:
                pass
        try:
            os.unlink(conf_path)
        except Exception:
            pass


def run_protocol_test(candidates: list[dict]) -> tuple[list[dict], dict]:
    """
    candidates: list of {raw, host, port, ping_ms, protocol, score, list_type}
    """
    xray = _ensure_xray()
    stats = {
        "enabled": bool(xray),
        "tested": 0,
        "passed": 0,
        "skipped_non_vless": 0,
    }
    if not xray:
        log("Xray недоступен — protocol test SKIP, используем TCP+score")
        return candidates, stats

    # только vless, top by score
    vless = [c for c in candidates if str(c.get("protocol", "")).startswith("vless") or (c.get("raw") or "").startswith("vless://")]
    vless = sorted(vless, key=lambda c: c.get("score", 0), reverse=True)[:PROTOCOL_TEST_CANDIDATES]
    log(f"Protocol-test {len(vless)} vless через Xray...")

    passed: list[dict] = []
    base_port = 10800
    for i, c in enumerate(vless):
        stats["tested"] += 1
        ok = _test_one(xray, c["raw"], base_port + (i % 20))
        if ok:
            c = dict(c)
            c["proto_ok"] = True
            passed.append(c)
            stats["passed"] += 1
            log(f"  PASS {c.get('host')}:{c.get('port')} score={c.get('score')}")
        if len(passed) >= 25:
            break

    log(f"Protocol passed: {stats['passed']}/{stats['tested']}")
    # если никто не прошёл — fallback на TCP candidates (лучше что-то, чем пусто)
    if not passed:
        log("Никто не прошёл HTTP-over-Xray → fallback TCP ranked")
        return candidates, stats
    return passed, stats
