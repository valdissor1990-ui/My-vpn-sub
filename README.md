# My VPN Sub

## Подписки

| Файл | Содержимое |
|------|------------|
| **sub.txt** | top-20 (XHTTP > Vision > gRPC > Hy2) |
| **sub_vision.txt** | только Reality + TCP + XTLS Vision |
| sub_white / black / hy2 / reality | срезы |
| `*_base64.txt` | то же в base64 |

```
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_vision.txt
https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_base64.txt
https://raw.githack.com/valdissor1990-ui/My-vpn-sub/main/sub.txt
```

## Оптимизации
- **pre-score cap** 3000 до TCP
- **dead_cache.json** — мёртвые host:port на 12 ч
- TG web: 18 публичных каналов `t.me/s/...`

## Приоритет
1. Reality + XHTTP  
2. Reality + TCP + `xtls-rprx-vision`  
3. Reality + gRPC  
4. Hysteria2  
