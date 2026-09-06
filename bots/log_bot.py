"""Единый журнал пайплайна: logs/blog.md, errors.jsonl, pipeline.jsonl."""

from __future__ import annotations

import json
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_DIR = Path("logs")
BLOG = LOG_DIR / "blog.md"
ERRORS = LOG_DIR / "errors.jsonl"
PIPELINE = LOG_DIR / "pipeline.jsonl"
LATEST = LOG_DIR / "latest.json"
MAX_BLOG_LINES = 400
MAX_JSONL = 200


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _ensure() -> None:
    LOG_DIR.mkdir(exist_ok=True)


def _trim_jsonl(path: Path, max_lines: int = MAX_JSONL) -> None:
    if not path.exists():
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) > max_lines:
        path.write_text("\n".join(lines[-max_lines:]) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, obj: dict) -> None:
    _ensure()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    _trim_jsonl(path)


def _prepend_blog(block: str) -> None:
    _ensure()
    old = BLOG.read_text(encoding="utf-8") if BLOG.exists() else "# Pipeline log blog\n\n"
    text = block + "\n" + old
    lines = text.splitlines()
    if len(lines) > MAX_BLOG_LINES:
        lines = lines[:MAX_BLOG_LINES]
    BLOG.write_text("\n".join(lines) + "\n", encoding="utf-8")


def info(stage: str, msg: str, **extra: Any) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{stage}] {msg}")
    row = {"ts": _now(), "level": "info", "stage": stage, "msg": msg, **extra}
    _append_jsonl(PIPELINE, row)


def error(stage: str, msg: str, exc: BaseException | None = None, **extra: Any) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{stage}] ERROR {msg}")
    row: dict[str, Any] = {
        "ts": _now(),
        "level": "error",
        "stage": stage,
        "msg": msg,
        **extra,
    }
    if exc is not None:
        row["exception"] = type(exc).__name__
        row["detail"] = str(exc)
        row["traceback"] = traceback.format_exc()
    _append_jsonl(ERRORS, row)
    _append_jsonl(PIPELINE, row)
    _prepend_blog(
        f"## ❌ {_now()} · `{stage}`\n\n"
        f"{msg}\n\n"
        + (f"```\n{row.get('traceback', '')}\n```\n\n" if exc else "")
    )


def snapshot(status: dict, fixes: list[dict] | None = None) -> None:
    """Итог прогона в blog + latest.json."""
    _ensure()
    pipe = status.get("pipeline") or {}
    health = status.get("health", "?")
    icon = "✅" if health == "ok" else "⚠️"
    lines = [
        f"## {icon} {_now()} · health=`{health}` source=`{status.get('pick_source')}`",
        "",
        f"- raw={pipe.get('raw_lines')} tg={pipe.get('tg_links')} filtered={pipe.get('filtered')}",
        f"- tcp_alive={pipe.get('tcp_alive')} clash={pipe.get('clash_passed')}/{pipe.get('clash_tested')}",
        f"- exported={pipe.get('exported')}",
        "",
    ]
    if fixes:
        lines.append("### Auto-fix commands")
        lines.append("")
        for f in fixes:
            lines.append(f"- **{f.get('priority')}** `{f.get('code')}`: {f.get('action')}")
        lines.append("")
    _prepend_blog("\n".join(lines) + "\n")
    LATEST.write_text(
        json.dumps(
            {"ts": _now(), "status": status, "fixes": fixes or []},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
