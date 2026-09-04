"""TG web scrape + optional Telethon."""

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
            timeout=18,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MyVpnSub/1.1)"},
        )
        if r.status_code != 200:
            return []
        found = [_clean(m) for m in LINK_RE.findall(r.text)]
        return [x for x in found if len(x) > 30]
    except Exception:
        return []


def run_telegram_collect() -> list[str]:
    links: list[str] = []
    log(f"TG web: {len(TG_WEB_CHANNELS)} channels")
    for ch in TG_WEB_CHANNELS:
        got = scrape_tme_s(ch)
        if got:
            log(f"  @{ch} → {len(got)}")
            links.extend(got)

    api_id = os.environ.get("TG_API_ID", "").strip()
    api_hash = os.environ.get("TG_API_HASH", "").strip()
    if api_id and api_hash:
        try:
            from telethon.sync import TelegramClient  # type: ignore

            channels = os.environ.get("TG_CHANNELS", "").strip()
            ch_list = [c.strip() for c in channels.split(",") if c.strip()] or [
                f"@{c}" for c in TG_WEB_CHANNELS[:8]
            ]
            with TelegramClient("tg_session", int(api_id), api_hash) as client:
                for ch in ch_list:
                    try:
                        for msg in client.iter_messages(ch, limit=40):
                            text = msg.message or ""
                            links.extend(_clean(m) for m in LINK_RE.findall(text))
                    except Exception as e:
                        log(f"  api {ch}: {e}")
        except Exception as e:
            log(f"Telethon: {e}")

    seen, out = set(), []
    for ln in links:
        k = ln.split("#")[0]
        if k not in seen:
            seen.add(k)
            out.append(ln)
    log(f"TG unique={len(out)}")
    return out
