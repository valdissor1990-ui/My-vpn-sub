"""Бот подбора: ranking по SNI/транспорту, нарезка top-N, запись файлов."""

from __future__ import annotations

import base64
import json
import re
from datetime import datetime, timezone
from urllib.parse import unquote

from config import MAX_HY2, MAX_MAIN, MAX_REALITY, PREFERRED_SNI


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [picker] {msg}")


def _extract_sni(line: str) -> str:
    low = line.lower()
    for key in ("sni=", "host=", "peer=", "servername="):
        m = re.search(rf"{key}([^&\s#]+)", low)
        if m:
            return unquote(m.group(1))
    return ""


def score(line: str) -> int:
    low = line.lower()
    s = 0
    if low.startswith(("hysteria2://", "hy2://")):
        s += 100
    if "xhttp" in low:
        s += 60
    if "grpc" in low:
        s += 45
    if "reality" in low:
        s += 30
    if "vision" in low:
        s += 10
    sni = _extract_sni(line)
    for pref in PREFERRED_SNI:
        if pref in sni or pref in low:
            s += 25
            break
    if any(x in low for x in ("white", "cidr", "wl")):
        s += 15
    return s


def rank(lines: list[str]) -> list[str]:
    return sorted(lines, key=score, reverse=True)


def _header(title: str, extra: list[str]) -> list[str]:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return [
        "#profile-title: base64:" + base64.b64encode(title.encode()).decode(),
        "#profile-update-interval: 2",
        "#subscription-userinfo: upload=0; download=0; total=1073741824000000; expire=2546249531",
        f"# Generated: {now}",
        *extra,
        "# bots: collector → filter → picker",
        "# https://github.com/valdissor1990-ui/My-vpn-sub",
    ]


def write_sub(path: str, title: str, lines: list[str], meta: list[str]) -> None:
    body = _header(title, meta) + lines
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(body) + "\n")
    log(f"Записан {path}: {len(lines)} ключей")


def run_picker(
    all_passed: list[str],
    only_hy2: list[str],
    only_reality: list[str],
    collect_stats: dict,
    filter_stats: dict,
) -> dict:
    main = rank(all_passed)[:MAX_MAIN]
    hy2 = rank(only_hy2)[:MAX_HY2]
    reality = rank(only_reality)[:MAX_REALITY]

    write_sub(
        "sub.txt",
        "My VPN · WL+Hy2",
        main,
        [
            f"# Servers: {len(main)}",
            "# Mix: Hysteria2 + Reality/XHTTP/gRPC (ranked)",
        ],
    )
    write_sub(
        "sub_hy2.txt",
        "My VPN · Hysteria2 only",
        hy2,
        [f"# Hysteria2 only: {len(hy2)}"],
    )
    write_sub(
        "sub_reality.txt",
        "My VPN · Reality XHTTP/gRPC",
        reality,
        [f"# Reality+XHTTP/gRPC only: {len(reality)}"],
    )

    status = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collect": collect_stats,
        "filter": filter_stats,
        "output": {
            "sub.txt": len(main),
            "sub_hy2.txt": len(hy2),
            "sub_reality.txt": len(reality),
        },
    }
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)
    log("status.json обновлён")
    return status
