"""
1) Web-scrape публичных каналов t.me/s/NAME (без API)
2) Опционально Telethon при TG_API_ID/HASH
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from html import unescape

import requests

from config import TG_WEB_CHANNELS

LINK_RE = re.compile(
    r"((?:vless|vmess|trojan|hysteria2|hy2)://[^\s<>\"'\u003c]+)",
    re.I,
)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [tg] {msg}")


def _clean(link: str) -> str:
    link = unescape(link).strip().rstrip(")"]}>\"'")
    # обрезать HTML entities хвосты
    if "#" in link:
        base, frag = link.split("#", 1)
        frag = re.sub(r"<.*", "", frag)
        link = base + "#" + frag
    return link


def scrape_tme_s(channel: str) -> list[str]:
    url = f"https://t.me/s/{channel.lstrip('@')}"
    try:
        r = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MyVpnSub/1.0)"},
        )
        if r.status_code != 200:
            log(f"  web {channel} HTTP {r.status_code}")
            return []
        found = [_clean(m) for m in LINK_RE.findall(r.text)]
        # фильтр мусора
        found = [x for x in found if len(x) > 30 and "://" in x]
        log(f"  web @{channel} → {len(found)}")
        return found
    except Exception as e:
        log(f"  web @{channel} err {e}")
        return []


def run_telegram_collect() -> list[str]:
    links: list[str] = []

    # --- публичный web preview ---
    log(f"TG web scrape: {len(TG_WEB_CHANNELS)} channels")
    for ch in TG_WEB_CHANNELS:
        links.extend(scrape_tme_s(ch))

    # --- optional Telethon ---
    api_id = os.environ.get("TG_API_ID", "").strip()
    api_hash = os.environ.get("TG_API_HASH", "").strip()
    if api_id and api_hash:
        try:
            from telethon.sync import TelegramClient  # type: ignore

            channels = os.environ.get("TG_CHANNELS", "").strip()
            ch_list = [c.strip() for c in channels.split(",") if c.strip()] or [
                f"@{c}" for c in TG_WEB_CHANNELS
            ]
            with TelegramClient("tg_session", int(api_id), api_hash) as client:
                for ch in ch_list:
                    try:
                        for msg in client.iter_messages(ch, limit=60):
                            text = msg.message or ""
                            links.extend(_clean(m) for m in LINK_RE.findall(text))
                    except Exception as e:
                        log(f"  api {ch}: {e}")
        except Exception as e:
            log(f"Telethon skip: {e}")
    else:
        log("No TG API secrets — web-only")

    # unique
    seen = set()
    out = []
    for ln in links:
        key = ln.split("#")[0]
        if key not in seen:
            seen.add(key)
            out.append(ln)
    log(f"TG total unique: {len(out)}")
    return out
