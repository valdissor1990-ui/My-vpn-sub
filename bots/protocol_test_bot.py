"""
Протокольный тест через Clash Meta (mihomo):
1) Конвертация share-link → proxy dict
2) Один процесс mihomo
3) GET /proxies/{name}/delay — реальный HTTP через узел
"""

from __future__ import annotations

import gzip
import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from config import (
    PROTOCOL_TEST_CANDIDATES,
    PROTOCOL_TEST_MAX_PASS,
    PROTOCOL_TEST_TIMEOUT,
)

# Clash Meta / mihomo
MIHOMO_VERSION = "v1.19.11"
MIHOMO_URL = (
    f"https://github.com/MetaCubeX/mihomo/releases/download/{MIHOMO_VERSION}/"
    f"mihomo-linux-amd64-{MIHOMO_VERSION}.gz"
)

API_HOST = "127.0.0.1"
API_PORT = 19090
MIXED_PORT = 17890
API_SECRET = "myvpnsub"


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [clash] {msg}")


def _ensure_mihomo() -> str | None:
    cache = Path("bin")
    cache.mkdir(exist_ok=True)
    binary = cache / "mihomo"
    if binary.exists() and os.access(binary, os.X_OK):
        return str(binary)
    try:
        log(f"Downloading mihomo {MIHOMO_VERSION}...")
        gz_path = cache / "mihomo.gz"
        urllib.request.urlretrieve(MIHOMO_URL, gz_path)
        with gzip.open(gz_path, "rb") as f_in:
            with open(binary, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        binary.chmod(0o755)
        return str(binary)
    except Exception as e:
        log(f"mihomo download failed: {e}")
        # fallback plain name variants
        alt_url = (
            f"https://github.com/MetaCubeX/mihomo/releases/download/{MIHOMO_VERSION}/"
            f"mihomo-linux-amd64-compatible-{MIHOMO_VERSION}.gz"
        )
        try:
            urllib.request.urlretrieve(alt_url, cache / "mihomo.gz")
            with gzip.open(cache / "mihomo.gz", "rb") as f_in:
                with open(binary, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            binary.chmod(0o755)
            return str(binary)
        except Exception as e2:
            log(f"mihomo alt failed: {e2}")
    return None


def _vless_to_clash(link: str, name: str) -> dict | None:
    """vless:// → Clash Meta proxy object."""
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

        proxy: dict = {
            "name": name,
            "type": "vless",
            "server": host,
            "port": int(port),
            "uuid": uuid,
            "network": network,
            "udp": True,
            "tls": security in ("tls", "reality"),
            "client-fingerprint": q.get("fp") or "chrome",
        }

        sni = q.get("sni") or host
        if security in ("tls", "reality"):
            proxy["servername"] = sni

        if security == "reality":
            pbk = q.get("pbk", "")
            if not pbk:
                return None
            proxy["reality-opts"] = {
                "public-key": pbk,
                "short-id": q.get("sid", ""),
            }

        flow = q.get("flow", "")
        # Vision only with tcp
        if flow and network == "tcp":
            proxy["flow"] = flow

        if network == "ws":
            proxy["ws-opts"] = {
                "path": q.get("path", "/"),
                "headers": {"Host": q.get("host") or sni},
            }
        elif network == "grpc":
            proxy["grpc-opts"] = {
                "grpc-service-name": q.get("serviceName") or q.get("path") or ""
            }
        elif network == "xhttp":
            # mihomo: network xhttp / httpupgrade variants
            proxy["network"] = "xhttp"
            proxy["xhttp-opts"] = {
                "path": q.get("path", "/"),
                "host": q.get("host") or sni,
                "mode": q.get("mode") or "auto",
            }

        return proxy
    except Exception:
        return None


def _hy2_to_clash(link: str, name: str) -> dict | None:
    try:
        low = link.lower()
        if not (low.startswith("hysteria2://") or low.startswith("hy2://")):
            return None
        u = urlparse(link.replace("hy2://", "hysteria2://", 1))
        password = unquote(u.username or "")
        host, port = u.hostname, u.port or 443
        if not host:
            return None
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        proxy = {
            "name": name,
            "type": "hysteria2",
            "server": host,
            "port": int(port),
            "password": password or q.get("auth", ""),
            "sni": q.get("sni") or host,
            "skip-cert-verify": q.get("insecure", "0") in ("1", "true", "yes"),
        }
        if q.get("obfs"):
            proxy["obfs"] = q.get("obfs")
            proxy["obfs-password"] = q.get("obfs-password", "")
        return proxy
    except Exception:
        return None


def _link_to_clash(link: str, name: str) -> dict | None:
    if link.startswith("vless://"):
        return _vless_to_clash(link, name)
    if link.lower().startswith(("hysteria2://", "hy2://")):
        return _hy2_to_clash(link, name)
    return None


def _build_config(proxies: list[dict]) -> dict:
    names = [p["name"] for p in proxies]
    return {
        "mixed-port": MIXED_PORT,
        "allow-lan": False,
        "mode": "global",
        "log-level": "error",
        "external-controller": f"{API_HOST}:{API_PORT}",
        "secret": API_SECRET,
        "proxies": proxies,
        "proxy-groups": [
            {
                "name": "PROXY",
                "type": "select",
                "proxies": names or ["DIRECT"],
            }
        ],
        "rules": ["MATCH,PROXY"],
    }


def _api_delay(name: str, timeout_ms: int) -> int | None:
    """Returns delay ms or None if failed."""
    url = (
        f"http://{API_HOST}:{API_PORT}/proxies/{urllib.request.quote(name, safe='')}"
        f"/delay?url=http://www.gstatic.com/generate_204&timeout={timeout_ms}"
    )
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {API_SECRET}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=(timeout_ms / 1000) + 3) as resp:
            data = json.loads(resp.read().decode())
            delay = data.get("delay")
            if isinstance(delay, int) and delay > 0:
                return delay
    except Exception:
        return None
    return None


def run_protocol_test(candidates: list[dict]) -> tuple[list[dict], dict]:
    stats = {
        "engine": "mihomo",
        "enabled": False,
        "tested": 0,
        "passed": 0,
        "fallback_tcp": False,
    }

    mihomo = _ensure_mihomo()
    if not mihomo:
        log("mihomo unavailable → TCP fallback")
        stats["fallback_tcp"] = True
        return candidates, stats

    # top by score
    ranked = sorted(candidates, key=lambda c: c.get("score", 0), reverse=True)
    ranked = ranked[:PROTOCOL_TEST_CANDIDATES]

    proxies = []
    index: list[dict] = []  # map name → candidate
    for i, c in enumerate(ranked):
        name = f"n{i}"
        proxy = _link_to_clash(c["raw"], name)
        if not proxy:
            continue
        proxies.append(proxy)
        index.append({**c, "_name": name})

    if not proxies:
        log("no clash-convertible proxies → TCP fallback")
        stats["fallback_tcp"] = True
        return candidates, stats

    conf = _build_config(proxies)
    conf_path = Path("bin") / "clash-test.yaml"
    conf_path.parent.mkdir(exist_ok=True)
    # write as JSON (mihomo accepts json)
    conf_json = Path("bin") / "clash-test.json"
    conf_json.write_text(json.dumps(conf), encoding="utf-8")

    stats["enabled"] = True
    log(f"Starting mihomo with {len(proxies)} proxies...")
    proc = subprocess.Popen(
        [mihomo, "-f", str(conf_json)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    passed: list[dict] = []
    try:
        # wait API up
        ready = False
        for _ in range(25):
            time.sleep(0.4)
            try:
                req = urllib.request.Request(
                    f"http://{API_HOST}:{API_PORT}/version",
                    headers={"Authorization": f"Bearer {API_SECRET}"},
                )
                with urllib.request.urlopen(req, timeout=2) as r:
                    if r.status == 200:
                        ready = True
                        break
            except Exception:
                if proc.poll() is not None:
                    log("mihomo exited early")
                    break
        if not ready:
            log("API not ready → TCP fallback")
            stats["fallback_tcp"] = True
            return candidates, stats

        timeout_ms = int(PROTOCOL_TEST_TIMEOUT * 1000)
        for c in index:
            stats["tested"] += 1
            name = c["_name"]
            delay = _api_delay(name, timeout_ms)
            if delay is not None:
                row = {k: v for k, v in c.items() if not k.startswith("_")}
                row["proto_ok"] = True
                row["clash_delay_ms"] = delay
                row["score"] = row.get("score", 0) + 60
                passed.append(row)
                stats["passed"] += 1
                log(f"  PASS {row.get('host')} delay={delay}ms score={row['score']}")
            if len(passed) >= PROTOCOL_TEST_MAX_PASS:
                break
    finally:
        proc.kill()
        try:
            proc.wait(timeout=3)
        except Exception:
            pass

    log(f"Clash passed {stats['passed']}/{stats['tested']}")
    if not passed:
        stats["fallback_tcp"] = True
        return candidates, stats

    passed.sort(key=lambda c: (-c.get("score", 0), c.get("clash_delay_ms", 9999)))
    return passed, stats
