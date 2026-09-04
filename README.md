# My VPN Sub — audit build

## Приоритет протоколов (scoring)
1. **VLESS Reality + XHTTP**
2. **VLESS Reality + TCP + XTLS Vision** (`flow=xtls-rprx-vision`)
3. **VLESS Reality + gRPC**
4. **Hysteria2**
5. Прочий Reality TCP

XTLS Vision: `flow` применяется **только** с `type=tcp` (в protocol-test flow сбрасывается для xhttp/grpc).

## Пайплайн
collector → **TG web scrape** (`t.me/s/...`) → filter → TCP+score → Xray HTTP test → ≤20 outs

## Подписки
```
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_white.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/status.json
```

TG-каналы (web): v2FreeHub, ATLAS_V2VPN, abc_configs, NexoVPN  
+ raw с GitHub-коллекторов, которые уже парсят Telegram.
