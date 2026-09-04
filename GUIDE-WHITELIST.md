# Вариант 2: White-list подписки (под белые списки Yota)

## Зачем
При БС оператор пускает в основном «разрешённые» сети.  
White-list конфиги пытаются идти через IP/подсети, которые чаще в этих списках (CDN, «белые» диапазоны).

## Что сделать в клиенте (Hiddify / v2rayNG)

1. Удали или отключи старые обычные (black) подписки.
2. Добавь **только** эти URL:

**Основная (телефон):**
```
https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt
```

**Запасная:**
```
https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt
```

**CIDR проверенные:**
```
https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt
```

**Наша сборка (white-first):**
```
https://raw.githubusercontent.com/valdissor1990-ui/My-vpn-sub/main/sub.txt
```

3. Обнови подписки.
4. Сортировка по пингу — но на БС «не пингуется» ≠ всегда мёртвый: пробуй подключить 15–20 разных серверов вручную.
5. Приоритет: в названии Reality, gRPC, XHTTP, CIDR, White.

## Если GitHub raw не открывается
У igareck в README есть зеркала: Bitbucket, Codeberg, GitLab, GitHack.  
Скопируй raw с зеркала для тех же имён файлов.

## Ожидания
На жёстком БС Yota срабатывает не всегда. Это лотерея, но шанс выше, чем у обычных black-подписок.
