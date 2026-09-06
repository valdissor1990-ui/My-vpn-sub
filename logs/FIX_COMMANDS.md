# FIX_COMMANDS — авто-анализ после прогона

Updated: 2026-09-06T14:04:59.102025+00:00

Эти команды бот выставляет после анализа логов. Критичные (P0) чинить в первую очередь.

## [P0] `CLASH_ZERO`

- action: Все delay fail: сменить TEST_URLS / версию mihomo / не резать pool только proto_ok
- auto: `force_tcp_fallback_pick`

## [P1] `MIHOMO_DOWN`

- action: mihomo не стартовал — проверить releases URL и bin/mihomo
- auto: `retry_mihomo_download`

