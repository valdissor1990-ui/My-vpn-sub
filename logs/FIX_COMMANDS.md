# FIX_COMMANDS — авто-анализ после прогона

Updated: 2026-10-19T15:57:28.881251+00:00

Эти команды бот выставляет после анализа логов. Критичные (P0) чинить в первую очередь.

## [P0] `LOW_EXPORT`

- action: Clash ok=2, export=1: soft-fill из TCP top + поднять PROTOCOL_TEST_MAX_PASS
- auto: `soft_fill_and_raise_pass`

## [P1] `TCP_LOW`

- action: tcp_alive=11: ослабить pre_score / dead_cache hours
- auto: `clear_stale_dead_cache`

