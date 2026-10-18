# FIX_COMMANDS — авто-анализ после прогона

Updated: 2026-10-18T22:00:39.935814+00:00

Эти команды бот выставляет после анализа логов. Критичные (P0) чинить в первую очередь.

## [P0] `CLASH_ZERO`

- action: Все delay fail: сменить TEST_URLS / версию mihomo / не резать pool только proto_ok
- auto: `force_tcp_fallback_pick`

## [P1] `MIHOMO_DOWN`

- action: mihomo не стартовал — проверить releases URL и bin/mihomo
- auto: `retry_mihomo_download`

## [P1] `TCP_LOW`

- action: tcp_alive=17: ослабить pre_score / dead_cache hours
- auto: `clear_stale_dead_cache`

