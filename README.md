# My VPN Sub · hourly monitor · top-20 alive

Каждый **час** GitHub Actions:

1. **collector** — все открытые подписки (30+ URL, зеркала)
2. **filter** — Hysteria2 **или** Reality+(XHTTP|gRPC)
3. **monitor** — TCP ping host:port, отсев мёртвых
4. **picker** — только рабочие, **≤ 20**, в `sub.txt`

## Подписка

```
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt
```
```
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub.txt
```

Дополнительно:
- `sub_hy2.txt` — живые Hysteria2
- `sub_reality.txt` — живые Reality
- [`status.json`](https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/status.json) — мониторинг

## Важно про «пинг мобильной сети РФ»

GitHub Actions **не может** пинговать из сети Yota.  
Мониторинг = TCP с зарубежных серверов GitHub → отсекает совсем мёртвые IP.  
На белых списках Yota хост может отвечать с GitHub и **не** работать с телефона.

Если после обновления на Yota снова 0 — это ограничение оператора, не ботов.
