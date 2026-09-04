# My VPN Sub · score + protocol test + white/black

Пайплайн каждый час:

1. **collector** — открытые подписки (доноры Au1rxx, 0xRadikal, igareck, …)
2. **telegram** — опционально (`TG_API_ID` + `TG_API_HASH` secrets)
3. **filter** — Reality / XHTTP|gRPC|TCP / Hy2
4. **monitor** — TCP + **scoring** (Reality +25, CF +20, XHTTP, …)
5. **protocol_test** — HTTP через **Xray-core** (vless), fallback на TCP
6. **picker** — ≤20 в каждую выгрузку

## Подписки

| Файл | Назначение |
|------|------------|
| `sub.txt` | top scored (+ proto-ok если прошли) |
| `sub_white.txt` | white-ish |
| `sub_black.txt` | black-ish |
| `sub_hy2.txt` | Hysteria2 |
| `sub_reality.txt` | Reality из mix |

```
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_white.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/status.json
```

## Telegram (опционально)

Settings → Secrets → Actions:
- `TG_API_ID`
- `TG_API_HASH`
- `TG_CHANNELS` (например `@channel1,@channel2`)

Без secrets TG-бот просто пропускается.

## Важно

Протокольный тест идёт с GitHub runner, **не с Yota**.  
`proto_ok` снижает «пинг есть / коннекта нет», но не гарантирует мобильный БС.
