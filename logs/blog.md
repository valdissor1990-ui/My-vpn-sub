## ✅ 2026-09-06 16:05:09 UTC · health=`ok` source=`clash_soft_fill`

- raw=27667 tg=439 filtered=17780
- tcp_alive=1192 clash=2/40
- exported=1

### Auto-fix commands

- **P0** `LOW_EXPORT`: Clash ok=2, export=1: soft-fill из TCP top + поднять PROTOCOL_TEST_MAX_PASS


## ✅ 2026-09-06 15:05:00 UTC · health=`ok` source=`clash_soft_fill`

- raw=27191 tg=425 filtered=17879
- tcp_alive=1165 clash=1/40
- exported=1

### Auto-fix commands

- **P0** `LOW_EXPORT`: Clash ok=1, export=1: soft-fill из TCP top + поднять PROTOCOL_TEST_MAX_PASS
- **P2** `CLASH_LOW_RATIO`: pass rate 1/40: расширить кандидатов, снизить score bias на мёртвые free-keys


## ✅ 2026-09-06 14:04:59 UTC · health=`ok` source=`tcp_fallback`

- raw=27602 tg=419 filtered=17730
- tcp_alive=1182 clash=0/40
- exported=20

### Auto-fix commands

- **P0** `CLASH_ZERO`: Все delay fail: сменить TEST_URLS / версию mihomo / не резать pool только proto_ok
- **P1** `MIHOMO_DOWN`: mihomo не стартовал — проверить releases URL и bin/mihomo


## ✅ 2026-09-06 13:14:17 UTC · health=`ok` source=`clash_soft_fill`

- raw=27719 tg=414 filtered=17774
- tcp_alive=1201 clash=2/40
- exported=1

### Auto-fix commands

- **P0** `LOW_EXPORT`: Clash ok=2, export=1: soft-fill из TCP top + поднять PROTOCOL_TEST_MAX_PASS


## ✅ 2026-09-06 13:04:47 UTC · health=`ok` source=`tcp_fallback`

- raw=27247 tg=414 filtered=17843
- tcp_alive=1169 clash=0/40
- exported=20

### Auto-fix commands

- **P0** `CLASH_ZERO`: Все delay fail: сменить TEST_URLS / версию mihomo / не резать pool только proto_ok
- **P1** `MIHOMO_DOWN`: mihomo не стартовал — проверить releases URL и bin/mihomo


## ✅ 2026-09-06 12:55:12 UTC · health=`ok` source=`tcp_fallback`

- raw=27698 tg=420 filtered=17765
- tcp_alive=1203 clash=0/40
- exported=20

### Auto-fix commands

- **P0** `CLASH_ZERO`: Все delay fail: сменить TEST_URLS / версию mihomo / не резать pool только proto_ok
- **P1** `MIHOMO_DOWN`: mihomo не стартовал — проверить releases URL и bin/mihomo


# Pipeline log blog

Сюда каждый hourly-прогон дописывает итог и ошибки.
Авто-команды: [FIX_COMMANDS.md](./FIX_COMMANDS.md)

---
