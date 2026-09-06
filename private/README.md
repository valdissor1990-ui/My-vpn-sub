# Private vault (шифрованные секреты)

Сюда кладутся **только** `.enc` файлы. Открытые ключи и `.dec` — **в git не попадают** (см. `.gitignore`).

## Зачем
Хранить личные URL подписок / свои `vless://` в зашифрованном виде.

## Как пользоваться

```bash
# 1) Придумай фразу-пароль (одна и та же всегда)
export SUB_ENCRYPT_KEY='твоя-длинная-секретная-фраза'

# 2) Зашифровать список личных узлов
echo 'vless://...@my-server:443?...' > /tmp/nodes.txt
python -m bots.encrypt_bot encrypt /tmp/nodes.txt
mv /tmp/nodes.txt.enc private/nodes.txt.enc
rm /tmp/nodes.txt

# 3) Или запечатать URL личной подписки (не коммить открытый URL)
python -m bots.encrypt_bot seal-url 'https://example.com/sub/ONLY_FOR_YOU'

# 4) В GitHub → Settings → Secrets → Actions
#    Name: SUB_ENCRYPT_KEY
#    Value: та же фраза
```

## Важно
- Публичный `sub.txt` **не** получает расшифрованные платные ключи автоматически — это сделано специально.
- Чтобы пользоваться личным vault, расшифровывай **локально** или держи репозиторий **Private**.
- Base64 ≠ шифрование. Здесь Fernet (AES).
