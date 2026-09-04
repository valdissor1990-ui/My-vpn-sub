# My VPN Sub · боты сбора / фильтра / подбора

Автоматика на GitHub Actions каждые **2 часа**:

1. **collector_bot** — качает ключи с зеркал (jsDelivr, GitHack, Codeberg, GitLab, GitVerse, Bitbucket)
2. **filter_bot** — только Hysteria2 **или** Reality + (XHTTP|gRPC), дедуп
3. **picker_bot** — ranking (SNI/транспорт), режет top-N, пишет 3 подписки + `status.json`

---

## Подписки

| Файл | Содержимое | Ссылка (jsDelivr) |
|------|------------|-------------------|
| **sub.txt** | микс Hy2 + Reality | https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub.txt |
| **sub_hy2.txt** | только Hysteria2 | https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_hy2.txt |
| **sub_reality.txt** | Reality XHTTP/gRPC | https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/sub_reality.txt |

GitHub raw:
```
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub.txt
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub_hy2.txt
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub_reality.txt
```

Статус последнего прогона: [`status.json`](https://cdn.jsdelivr.net/gh/valdissor1990-ui/My-vpn-sub@main/status.json)

---

## Прямые источники (если наша сборка пустая)

```
https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt
https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt
https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt
```

На Yota с БС: сначала **sub_hy2.txt**, потом **sub_reality.txt**, перебор вручную.

---

## Важно

Боты улучшают **отбор и обновление** ключей с GitHub.  
Они **не могут** заставить Yota пропустить уже заблокированные публичные серверы.  
Если все три подписки мертвы на твоей сети — лимит публичных ключей, не ботов.
