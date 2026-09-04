# My VPN Sub · усиленный сбор + TCP monitor

Каждый час:
1. **collector** — 50+ открытых подписок (зеркала)
2. **enrich** — статистика протоколов/портов/SNI → `meta_*.json`
3. **filter** — Hy2 | Reality+XHTTP/gRPC | Reality+TCP
4. **monitor** — TCP ping, только живые
5. **picker** — **≤ 20** в `sub.txt`

## Подписка

```
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt
```

Статус: `status.json` · мета: `meta_raw.json`, `meta_filtered.json`

## Пинг есть, подключения нет

Это ожидаемо:
- **TCP ping** = порт открыт с GitHub
- **Подключение VPN** = ещё Reality/Hy2 handshake + политика Yota

Мы на пути: сначала появляются «живые» порты, дальше нужен ключ, который проходит handshake с твоей сети. Обновляй подписку каждый час и перебирай серверы вручную.
