"""
Опциональный сбор из Telegram-каналов.
Требует secrets: TG_API_ID, TG_API_HASH
Опционально: TG_CHANNELS (через запятую)

Без secrets — no-op (не ломает pipeline).
"""

from __future__ import annotations

import os
import re
from datetime import datetime

from config import TG_CHANNELS_DEFAULT

LINK_RE = re.compile(
    r"((?:vless|vmess|trojan|hysteria2|hy2|hysteria)://[^\s<>\"']+)",
    re.I,
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [tg] {msg}")


def run_telegram_collect() -> list[str]:
    api_id = os.environ.get("TG_API_ID", "").strip()
    api_hash = os.environ.get("TG_API_HASH", "").strip()
    if not api_id or not api_hash:
        log("TG secrets нет — пропуск Telegram-сбора")
        return []

    channels = os.environ.get("TG_CHANNELS", "").strip()
    ch_list = [c.strip() for c in channels.split(",") if c.strip()] or TG_CHANNELS_DEFAULT

    try:
        from telethon.sync import TelegramClient  # type: ignore
    except ImportError:
        log("telethon не установлен — пропуск")
        return []

    links: list[str] = []
    try:
        with TelegramClient("tg_session", int(api_id), api_hash) as client:
            for ch in ch_list:
                try:
                    log(f"Читаю {ch}...")
                    for msg in client.iter_messages(ch, limit=80):
                        text = msg.message or ""
                        links.extend(LINK_RE.findall(text))
                except Exception as e:
                    log(f"  fail {ch}: {e}")
    except Exception as e:
        log(f"TG client error: {e}")
        return []

    log(f"Из TG: {len(links)} ссылок")
    return links
