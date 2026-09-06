"""Clash Meta protocol test. Hy2 via bots.hy2 (Brutal/hop/obfs)."""

from __future__ import annotations

import base64
import gzip
import json
import os
import shutil
import subprocess
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from bots.hy2 import is_hy2, to_clash as hy2_to_clash
from config import (
    MIHOMO_VERSIONS,
    PROTOCOL_TEST_CANDIDATES,
    PROTOCOL_TEST_MAX_PASS,
    PROTOCOL_TEST_TIMEOUT,
    PROTOCOL_TEST_WORKERS,
    PROTOCOL_TEST_WORKERS_HY2,
    TEST_URLS,
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
    for ver in MIHOMO_VERSIONS:
        for suffix in (
            f"mihomo-linux-amd64-{ver}.gz",
            f"mihomo-linux-amd64-compatible-{ver}.gz",
            f"mihomo-linux-amd64-v2-{ver}.gz",
        ):
            url = f"https://github.com/MetaCubeX/mihomo/releases/download/{ver}/{suffix}"
            try:
                log(f"Trying {url}")
                gz_path = cache / "mihomo.gz"
                urllib.request.urlretrieve(url, gz_path)
                with gzip.open(gz_path, "rb") as f_in, open(binary, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                binary.chmod(0o755)
                if binary.stat().st_size > 1000:
                    return str(binary)
            except Exception as e:
                log(f"  fail: {e}")
    return None


def _vless_to_clash(link: str, name: str) -> dict | None:
    try:
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
            "name": name, "type": "vless", "server": host, "port": int(port),
            "uuid": uuid, "network": network, "udp": True,
            "tls": security in ("tls", "reality"),
            "client-fingerprint": q.get("fp") or "chrome",
        }
        sni = q.get("sni") or host
        if security in ("tls", "reality"):
            proxy["servername"] = sni
        if security == "reality":
            if not q.get("pbk"):
                return None
            proxy["reality-opts"] = {"public-key": q["pbk"], "short-id": q.get("sid", "")}
        flow = q.get("flow", "")
        if flow and network == "tcp":
            proxy["flow"] = flow
        if network == "ws":
            proxy["ws-opts"] = {"path": q.get("path", "/"), "headers": {"Host": q.get("host") or sni}}
        elif network == "grpc":
            proxy["grpc-opts"] = {"grpc-service-name": q.get("serviceName") or q.get("path") or ""}
        elif network == "xhttp":
            proxy["network"] = "xhttp"
            proxy["xhttp-opts"] = {"path": q.get("path", "/"), "host": q.get("host") or sni, "mode": q.get("mode") or "auto"}
        return proxy
    except Exception:
        return None


def _vmess_to_clash(link: str, name: str) -> dict | None:
    try:
        if not link.startswith("vmess://"):
            return None
        raw = link[8:].split("#")[0]
        pad = 4 - len(raw) % 4
        if pad != 4:
            raw += "=" * pad
        data = json.loads(base64.b64decode(raw).decode("utf-8", errors="ignore"))
        host = data.get("add") or data.get("host")
        uuid = data.get("id")
        if not host or not uuid:
            return None
        network = data.get("net", "tcp")
        proxy: dict = {
            "name": name, "type": "vmess", "server": host, "port": int(data.get("port", 443)),
            "uuid": uuid, "alterId": int(data.get("aid", 0)), "cipher": data.get("scy") or "auto",
            "network": network, "udp": True, "tls": data.get("tls", "") in ("tls", "reality"),
            "client-fingerprint": data.get("fp") or "chrome",
        }
        if data.get("sni") or data.get("host"):
            proxy["servername"] = data.get("sni") or data.get("host")
        if network == "ws":
            proxy["ws-opts"] = {"path": data.get("path", "/"), "headers": {"Host": data.get("host") or host}}
        elif network == "grpc":
            proxy["grpc-opts"] = {"grpc-service-name": data.get("path", "")}
        return proxy
    except Exception:
        return None


def _trojan_to_clash(link: str, name: str) -> dict | None:
    try:
        if not link.startswith("trojan://"):
            return None
        u = urlparse(link)
        password, host, port = unquote(u.username or ""), u.hostname, u.port or 443
        if not password or not host:
            return None
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        network = q.get("type", "tcp")
        proxy: dict = {
            "name": name, "type": "trojan", "server": host, "port": int(port),
            "password": password, "network": network, "udp": True,
            "sni": q.get("sni") or host, "client-fingerprint": q.get("fp") or "chrome",
            "skip-cert-verify": q.get("allowInsecure", "0") in ("1", "true"),
        }
        if network == "ws":
            proxy["ws-opts"] = {"path": q.get("path", "/"), "headers": {"Host": q.get("host") or q.get("sni") or host}}
        elif network == "grpc":
            proxy["grpc-opts"] = {"grpc-service-name": q.get("serviceName") or ""}
        return proxy
    except Exception:
        return None


def _hy2_to_clash(link: str, name: str) -> dict | None:
    return hy2_to_clash(link, name)


def _link_to_clash(link: str, name: str) -> dict | None:
    if link.startswith("vless://"):
        return _vless_to_clash(link, name)
    if link.startswith("vmess://"):
        return _vmess_to_clash(link, name)
    if link.startswith("trojan://"):
        return _trojan_to_clash(link, name)
    if is_hy2(link):
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
        "proxy-groups": [{"name": "PROXY", "type": "select", "proxies": names or ["DIRECT"]}],
        "rules": ["MATCH,PROXY"],
    }


def _api_delay(name: str, timeout_ms: int, test_url: str) -> int | None:
    qname = urllib.request.quote(name, safe="")
    url = (
        f"http://{API_HOST}:{API_PORT}/proxies/{qname}/delay"
        f"?url={urllib.request.quote(test_url, safe='')}&timeout={timeout_ms}"
    )
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {API_SECRET}"})
    try:
        with urllib.request.urlopen(req, timeout=(timeout_ms / 1000) + 4) as resp:
            data = json.loads(resp.read().decode())
            delay = data.get("delay")
            if isinstance(delay, int) and delay > 0:
                return delay
    except Exception:
        return None
    return None


def _delay_with_rotate(name: str, timeout_ms: int):
    for test_url in TEST_URLS:
        d = _api_delay(name, timeout_ms, test_url)
        if d is not None:
            return d, test_url
    return None, None


def run_protocol_test(candidates: list[dict]):
    stats = {
        "engine": "mihomo",
        "enabled": False,
        "tested": 0,
        "passed": 0,
        "fallback_tcp": False,
        "test_urls": TEST_URLS,
        "workers": PROTOCOL_TEST_WORKERS,
        "workers_hy2": PROTOCOL_TEST_WORKERS_HY2,
    }
    mihomo = _ensure_mihomo()
    if not mihomo:
        stats["fallback_tcp"] = True
        return candidates, stats

    ranked = sorted(candidates, key=lambda c: c.get("score", 0), reverse=True)[:PROTOCOL_TEST_CANDIDATES]
    proxies, index = [], []
    for i, c in enumerate(ranked):
        name = f"n{i}"
        proxy = _link_to_clash(c["raw"], name)
        if not proxy:
            continue
        proxies.append(proxy)
        index.append({**c, "_name": name, "_hy2": is_hy2(c["raw"])})

    if not proxies:
        stats["fallback_tcp"] = True
        return candidates, stats

    conf_json = Path("bin") / "clash-test.json"
    conf_json.parent.mkdir(exist_ok=True)
    conf_json.write_text(json.dumps(_build_config(proxies)), encoding="utf-8")

    has_hy2 = any(c["_hy2"] for c in index)
    workers = PROTOCOL_TEST_WORKERS_HY2 if has_hy2 else PROTOCOL_TEST_WORKERS
    stats["workers_used"] = workers
    stats["enabled"] = True
    log(f"mihomo proxies={len(proxies)} workers={workers} hy2={has_hy2}")

    proc = subprocess.Popen([mihomo, "-f", str(conf_json)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    passed = []
    try:
        ready = False
        for _ in range(30):
            time.sleep(0.35)
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
                    break
        if not ready:
            stats["fallback_tcp"] = True
            return candidates, stats

        timeout_ms = int(PROTOCOL_TEST_TIMEOUT * 1000)

        def job(c):
            return (*(_delay_with_rotate(c["_name"], timeout_ms)), c)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = [pool.submit(job, c) for c in index]
            for fut in as_completed(futs):
                stats["tested"] += 1
                try:
                    delay, used_url, c = fut.result()
                except Exception:
                    continue
                if delay is None:
                    continue
                row = {k: v for k, v in c.items() if not k.startswith("_")}
                row["proto_ok"] = True
                row["clash_delay_ms"] = delay
                row["test_url"] = used_url
                row["score"] = row.get("score", 0) + 60
                passed.append(row)
                stats["passed"] += 1
                log(f"  PASS {row.get('host')} {delay}ms")
                if len(passed) >= PROTOCOL_TEST_MAX_PASS:
                    break
    finally:
        proc.kill()
        try:
            proc.wait(timeout=3)
        except Exception:
            pass

    log(f"Clash {stats['passed']}/{stats['tested']}")
    if not passed:
        stats["fallback_tcp"] = True
        return candidates, stats
    passed.sort(key=lambda c: (-c.get("score", 0), c.get("clash_delay_ms", 9999)))
    return passed, stats
