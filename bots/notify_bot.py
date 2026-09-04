"""Telegram alert при health=empty. Secrets: TG_BOT_TOKEN, TG_CHAT_ID."""

from __future__ import annotations

import os
from datetime import datetime

import requests


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [notify] {msg}")


def notify_status(status: dict) -> None:
    token = os.environ.get("TG_BOT_TOKEN", "").strip()
    chat = os.environ.get("TG_CHAT_ID", "").strip()
    if not token or not chat:
        log("No TG_BOT_TOKEN/TG_CHAT_ID — skip notify")
        return

    health = status.get("health", "?")
    out = status.get("output", {})
    proto = status.get("protocol_test", {})
    mon = status.get("monitor", {})
    col = status.get("collect", {})

    text = (
        f"My-vpn-sub · {health}\n"
        f"sub.txt: {out.get('sub.txt', 0)}\n"
        f"TCP alive: {mon.get('tcp_alive', '?')}\n"
        f"Clash: {proto.get('passed', 0)}/{proto.get('tested', 0)}\n"
        f"TG links: {col.get('telegram_links', 0)}\n"
        f"sources ok/fail: {col.get('sources_ok')}/{col.get('sources_fail')}\n"
    )
    if health == "empty":
        text = "⚠️ EMPTY POOL\n" + text

    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": text},
            timeout=15,
        )
        log(f"notify HTTP {r.status_code}")
    except Exception as e:
        log(f"notify fail: {e}")
