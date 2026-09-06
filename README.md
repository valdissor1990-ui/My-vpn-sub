# My VPN Sub

Автосбор Reality / Vision / XHTTP / Hy2 + Clash (mihomo) delay + ротация.

## Подписки
```
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub.txt
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub_vision.txt
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub_clash.yaml
```

## Логи и авто-фикс
| Файл | Назначение |
|------|------------|
| [logs/blog.md](logs/blog.md) | хроника прогонов |
| [logs/errors.jsonl](logs/errors.jsonl) | ошибки |
| [logs/pipeline.jsonl](logs/pipeline.jsonl) | этапы |
| [logs/FIX_COMMANDS.md](logs/FIX_COMMANDS.md) | срочные команды боту |
| [logs/latest.json](logs/latest.json) | последний status+fixes |
| [status.json](status.json) | метрики |

Каждый час: collect → filter → TCP → Clash → picker (soft-fill) → **health analyze** → commit logs.

## Пайплайн
1. Источники + TG web
2. Фильтр Reality/Hy2
3. TCP + dead_cache
4. mihomo delay
5. Ротация `sub.txt` (last_export только для mix)
6. Soft-fill если Clash дал < 8 узлов
7. Лог-блог + FIX_COMMANDS
