# My VPN Sub

## Протокольный тест
**Clash Meta (mihomo)** — один процесс, проверка через API:
`GET /proxies/{name}/delay?url=http://www.gstatic.com/generate_204`

Поддержка: **VLESS Reality** (tcp / vision / xhttp / grpc) + **Hysteria2**.

## Подписки

| Файл | Содержимое |
|------|------------|
| **sub.txt** | top-20 после Clash-delay |
| **sub_vision.txt** | Reality + TCP + XTLS Vision |
| `*_base64.txt` | base64 |

```
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_vision.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/status.json
```

## Пайплайн
collector → TG web → filter → pre-score/TCP/dead-cache → **mihomo delay** → picker ≤20

## Приоритет
1. Reality + XHTTP  
2. Reality + TCP + Vision  
3. Reality + gRPC  
4. Hysteria2  

Оптимизации: pre-score cap 3000, dead_cache 12h, 18 TG-каналов.
