"""
Шифрование секретов (Fernet/AES).

Что это даёт:
  - хранить личные URI/URL в private/*.enc без открытого текста в git
  - расшифровка только при SUB_ENCRYPT_KEY (локально или GitHub Secret)

Чего это НЕ даёт:
  - публичная sub.txt, где ключи «не видны», но VPN у всех работает
  - клиент v2rayNG/Hiddify всё равно получит открытый конфиг после расшифровки у себя

Использование:
  export SUB_ENCRYPT_KEY='пароль-или-фраза'
  python -m bots.encrypt_bot encrypt private/my_nodes.txt
  python -m bots.encrypt_bot decrypt private/my_nodes.txt.enc
  python -m bots.encrypt_bot seal-url 'https://example.com/sub/TOKEN'
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import sys
from pathlib import Path

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    Fernet = None  # type: ignore
    InvalidToken = Exception  # type: ignore

PRIVATE_DIR = Path("private")
VAULT_URLS = PRIVATE_DIR / "source_urls.enc"


def _derive_key(secret: str) -> bytes:
    """Стабильный Fernet-ключ из парольной фразы."""
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


def _fernet(secret: str | None = None) -> "Fernet":
    if Fernet is None:
        raise RuntimeError("Установи cryptography: pip install cryptography")
    secret = (secret or os.environ.get("SUB_ENCRYPT_KEY", "")).strip()
    if not secret:
        raise RuntimeError("Нужен SUB_ENCRYPT_KEY (env) или --key")
    return Fernet(_derive_key(secret))


def encrypt_bytes(data: bytes, secret: str | None = None) -> bytes:
    return _fernet(secret).encrypt(data)


def decrypt_bytes(token: bytes, secret: str | None = None) -> bytes:
    try:
        return _fernet(secret).decrypt(token)
    except InvalidToken as e:
        raise RuntimeError("Неверный SUB_ENCRYPT_KEY или повреждённый файл") from e


def encrypt_file(path: Path, secret: str | None = None) -> Path:
    raw = path.read_bytes()
    out = path.with_suffix(path.suffix + ".enc") if path.suffix != ".enc" else path
    if path.suffix != ".enc":
        out = Path(str(path) + ".enc")
    out.write_bytes(encrypt_bytes(raw, secret))
    return out


def decrypt_file(path: Path, secret: str | None = None, dest: Path | None = None) -> Path:
    data = decrypt_bytes(path.read_bytes(), secret)
    if dest is None:
        dest = Path(str(path).removesuffix(".enc"))
        if dest == path:
            dest = path.with_suffix(".dec")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest


def seal_text(text: str, secret: str | None = None) -> str:
    return encrypt_bytes(text.encode("utf-8"), secret).decode("ascii")


def open_text(token: str, secret: str | None = None) -> str:
    return decrypt_bytes(token.encode("ascii"), secret).decode("utf-8")


def load_private_urls(secret: str | None = None) -> list[str]:
    """Читает private/source_urls.enc → список URL (по одному в строке)."""
    if not VAULT_URLS.exists():
        return []
    try:
        text = decrypt_bytes(VAULT_URLS.read_bytes(), secret).decode("utf-8")
    except Exception as e:
        print(f"[encrypt] vault skip: {e}")
        return []
    urls = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def load_private_lines(secret: str | None = None) -> list[str]:
    """Все private/*.txt.enc → расшифрованные share-link строки (не коммитятся)."""
    if not PRIVATE_DIR.exists():
        return []
    lines: list[str] = []
    for enc in sorted(PRIVATE_DIR.glob("*.enc")):
        if enc.name == VAULT_URLS.name:
            continue
        try:
            text = decrypt_bytes(enc.read_bytes(), secret).decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[encrypt] skip {enc.name}: {e}")
            continue
        for ln in text.splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#") and "://" in ln:
                lines.append(ln)
    return lines


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="My-vpn-sub encrypt vault")
    p.add_argument("cmd", choices=["encrypt", "decrypt", "seal-url", "seal-file", "check"])
    p.add_argument("target", nargs="?", help="file path or URL")
    p.add_argument("--key", default=None, help="override SUB_ENCRYPT_KEY")
    args = p.parse_args(argv)

    if args.cmd == "check":
        key = (args.key or os.environ.get("SUB_ENCRYPT_KEY") or "").strip()
        print("cryptography", "ok" if Fernet else "MISSING")
        print("SUB_ENCRYPT_KEY", "set" if key else "empty")
        print("vault", VAULT_URLS.exists())
        return 0

    if args.cmd == "seal-url":
        if not args.target:
            print("нужен URL")
            return 1
        PRIVATE_DIR.mkdir(exist_ok=True)
        existing = ""
        if VAULT_URLS.exists():
            try:
                existing = decrypt_bytes(VAULT_URLS.read_bytes(), args.key).decode() + "\n"
            except Exception:
                existing = ""
        blob = existing + args.target.strip() + "\n"
        VAULT_URLS.write_bytes(encrypt_bytes(blob.encode(), args.key))
        print(f"sealed → {VAULT_URLS}")
        return 0

    if not args.target:
        print("нужен путь к файлу")
        return 1
    path = Path(args.target)

    if args.cmd in ("encrypt", "seal-file"):
        out = encrypt_file(path, args.key)
        print(f"encrypted → {out}")
        print("Исходник с открытыми ключами лучше удалить и не коммитить.")
        return 0

    if args.cmd == "decrypt":
        out = decrypt_file(path, args.key)
        print(f"decrypted → {out} (не коммить этот файл)")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
