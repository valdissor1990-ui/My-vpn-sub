"""Hysteria 2: разбор URI + поля mihomo (Brutal, hop, obfs)."""

from __future__ import annotations

from urllib.parse import parse_qs, unquote, urlparse

from config import (
    HY2_ALPN,
    HY2_APPLY_WINDOWS,
    HY2_DOWN,
    HY2_FINGERPRINT,
    HY2_HOP_INTERVAL,
    HY2_INIT_CONN_WINDOW,
    HY2_INIT_STREAM_WINDOW,
    HY2_MAX_CONN_WINDOW,
    HY2_MAX_STREAM_WINDOW,
    HY2_UP,
)


def is_hy2(link: str) -> bool:
    low = (link or "").lower()
    return low.startswith(("hysteria2://", "hy2://", "hysteria://"))


def parse_hy2(link: str) -> dict | None:
    if not is_hy2(link):
        return None
    try:
        norm = link.replace("hy2://", "hysteria2://", 1).replace("hysteria://", "hysteria2://", 1)
        u = urlparse(norm)
        q = {k.lower(): v[0] for k, v in parse_qs(u.query).items()}
        host = u.hostname
        port = u.port or 443
        password = unquote(u.username or "") or q.get("auth") or q.get("password") or ""
        if not host:
            return None
        ports = q.get("mport") or q.get("ports") or q.get("port-hopping") or ""
        obfs = (q.get("obfs") or "").lower()
        return {
            "host": host,
            "port": int(port),
            "password": password,
            "sni": q.get("sni") or q.get("peer") or host,
            "insecure": q.get("insecure", "0") in ("1", "true", "yes"),
            "obfs": obfs if obfs in ("salamander", "gecko") else ("salamander" if obfs else ""),
            "obfs_password": q.get("obfs-password") or q.get("obfs_password") or "",
            "ports": ports,
            "hop_interval": q.get("hop-interval") or q.get("hopinterval") or str(HY2_HOP_INTERVAL),
            "alpn": q.get("alpn") or "h3",
            "pinSHA256": q.get("pinsha256") or q.get("pinSHA256") or "",
        }
    except Exception:
        return None


def to_clash(link: str, name: str) -> dict | None:
    p = parse_hy2(link)
    if not p:
        return None
    proxy: dict = {
        "name": name,
        "type": "hysteria2",
        "server": p["host"],
        "port": p["port"],
        "password": p["password"],
        "sni": p["sni"],
        "skip-cert-verify": p["insecure"],
        "alpn": HY2_ALPN if not p["alpn"] else [x.strip() for x in p["alpn"].split(",")],
        "fingerprint": HY2_FINGERPRINT,
        # Brutal: без up/down mihomo/клиенты часто падают в BBR
        "up": HY2_UP,
        "down": HY2_DOWN,
    }
    if p["obfs"]:
        proxy["obfs"] = p["obfs"]
        if p["obfs_password"]:
            proxy["obfs-password"] = p["obfs_password"]
    if p["ports"]:
        proxy["ports"] = p["ports"]
        proxy["hop-interval"] = int(str(p["hop_interval"]).split("-")[0]) if str(p["hop_interval"]).split("-")[0].isdigit() else HY2_HOP_INTERVAL
    if p["pinSHA256"]:
        proxy["pin-sha256"] = p["pinSHA256"]
    if HY2_APPLY_WINDOWS:
        proxy["initial-stream-receive-window"] = HY2_INIT_STREAM_WINDOW
        proxy["max-stream-receive-window"] = HY2_MAX_STREAM_WINDOW
        proxy["initial-connection-receive-window"] = HY2_INIT_CONN_WINDOW
        proxy["max-connection-receive-window"] = HY2_MAX_CONN_WINDOW
    return proxy
