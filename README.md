# My VPN Sub · full stack

## Подписки
```
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_vision.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_clash.yaml
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/status.json
```

## Что внутри
- collector + **18 TG web** каналов
- filter / score (XHTTP > Vision > gRPC > Hy2)
- TCP + **dead_cache** + pre-score cap
- **mihomo Clash** delay (vless/vmess/trojan/hy2, URL rotate, parallel)
- outputs: txt / base64 / **sub_clash.yaml** / vision/white/black
- **history/status-*.json**
- TG notify (`TG_BOT_TOKEN` + `TG_CHAT_ID`) при любом прогоне; empty → Actions red

## Secrets (опционально)
| Secret | Назначение |
|--------|------------|
| TG_API_ID / TG_API_HASH | Telethon deep scrape |
| TG_CHANNELS | список каналов |
| TG_BOT_TOKEN / TG_CHAT_ID | алерт в Telegram |
