"""Xray HTTP-over-socks test. Fixes: flow only on tcp, conf_path safety, ranking."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from config import (
    PROTOCOL_TEST_CANDIDATES,
    PROTOCOL_TEST_MAX_PASS,
    PROTOCOL_TEST_TIMEOUT,
)

XRAY_URL = (
    "https://github.com/XTLS/Xray-core/releases/download/v25.8.3/Xray-linux-64.zip"
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [proto] {msg}")


def _ensure_xray() -> str | None:
    cache = Path("bin")
    cache.mkdir(exist_ok=True)
    for name in ("xray", "Xray"):
        p = cache / name
        if p.exists() and os.access(p, os.X_OK):
            return str(p)
    try:
        log("Downloading Xray-core...")
        zip_path = cache / "xray.zip"
        urllib.request.urlretrieve(XRAY_URL, zip_path)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(cache)
        for name in ("xray", "Xray"):
            p = cache / name
            if p.exists():
                p.chmod(0o755)
                return str(p)
    except Exception as e:
        log(f"Xray download failed: {e}")
    return None


def _vless_to_outbound(link: str) -> dict | None:
    try:
        if not link.startswith("vless://"):
            return None
        u = urlparse(link)
        uuid, host, port = u.username, u.hostname, u.port or 443
        if not uuid or not host:
            return None
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        security = q.get("security", "none")
        network = q.get("type", "tcp")
        if network == "raw":
            network = "tcp"

        flow = q.get("flow", "")
        # XTLS Vision valid mainly with TCP(+reality), not xhttp/grpc/ws
        if network != "tcp":
            flow = ""

        stream: dict = {"network": network}
        if security == "reality":
            pbk = q.get("pbk", "")
            if not pbk:
                return None
            stream["security"] = "reality"
            stream["realitySettings"] = {
                "publicKey": pbk,
                "fingerprint": q.get("fp") or "chrome",
                "serverName": q.get("sni") or host,
                "shortId": q.get("sid", ""),
                "spiderX": q.get("spx", "/"),
            }
        elif security == "tls":
            stream["security"] = "tls"
            stream["tlsSettings"] = {
                "serverName": q.get("sni") or host,
                "fingerprint": q.get("fp") or "chrome",
            }

        if network == "ws":
            stream["wsSettings"] = {
                "path": q.get("path", "/"),
                "headers": {"Host": q.get("host") or q.get("sni") or host},
            }
        elif network == "grpc":
            stream["grpcSettings"] = {
                "serviceName": q.get("serviceName") or q.get("path") or ""
            }
        elif network == "xhttp":
            stream["network"] = "xhttp"
            stream["xhttpSettings"] = {
                "path": q.get("path", "/"),
                "host": q.get("host") or q.get("sni") or "",
                "mode": q.get("mode") or "auto",
            }

        user = {"id": uuid, "encryption": q.get("encryption", "none")}
        if flow:
            user["flow"] = flow

        return {
            "protocol": "vless",
            "settings": {
                "vnext": [
                    {
                        "address": host,
                        "port": int(port),
                        "users": [user],
                    }
                ]
            },
            "streamSettings": stream,
        }
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
        "outbounds": [outbound],
    }
    conf_path = None
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
        time.sleep(1.0)
        if proc.poll() is not None:
            return False
        proxy_handler = urllib.request.ProxyHandler(
            {"http": f"socks5h://127.0.0.1:{socks_port}"}
        )
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request("http://www.gstatic.com/generate_204")
        with opener.open(req, timeout=PROTOCOL_TEST_TIMEOUT) as resp:
            return resp.status in (204, 200, 301, 302)
    except Exception:
        return False
    finally:
        if proc and proc.poll() is None:
            proc.kill()
            try:
                proc.wait(timeout=2)
            except Exception:
                pass
        if conf_path:
            try:
                os.unlink(conf_path)
            except Exception:
                pass


def run_protocol_test(candidates: list[dict]) -> tuple[list[dict], dict]:
    stats = {"enabled": False, "tested": 0, "passed": 0, "fallback_tcp": False}
    xray = _ensure_xray()
    if not xray:
        log("Xray missing → TCP fallback")
        stats["fallback_tcp"] = True
        return candidates, stats
    stats["enabled"] = True

    vless = [
        c
        for c in candidates
        if (c.get("raw") or "").startswith("vless://")
    ]
    vless.sort(key=lambda c: c.get("score", 0), reverse=True)
    vless = vless[:PROTOCOL_TEST_CANDIDATES]
    log(f"Xray-test {len(vless)} vless...")

    passed: list[dict] = []
    for i, c in enumerate(vless):
        stats["tested"] += 1
        if _test_one(xray, c["raw"], 11000 + (i % 25)):
            row = dict(c)
            row["proto_ok"] = True
            row["score"] = row.get("score", 0) + 50  # bonus за реальный HTTP
            passed.append(row)
            stats["passed"] += 1
            log(f"  PASS {c.get('host')} score={row['score']}")
        if len(passed) >= PROTOCOL_TEST_MAX_PASS:
            break

    log(f"proto {stats['passed']}/{stats['tested']}")
    if not passed:
        stats["fallback_tcp"] = True
        return candidates, stats
    passed.sort(key=lambda c: (-c.get("score", 0), c.get("ping_ms", 9999)))
    return passed, stats
