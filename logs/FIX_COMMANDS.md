# FIX_COMMANDS — авто-анализ после прогона

Updated: 2026-09-06T15:05:00.627912+00:00

Эти команды бот выставляет после анализа логов. Критичные (P0) чинить в первую очередь.

## [P0] `LOW_EXPORT`

- action: Clash ok=1, export=1: soft-fill из TCP top + поднять PROTOCOL_TEST_MAX_PASS
- auto: `soft_fill_and_raise_pass`

## [P2] `CLASH_LOW_RATIO`

- action: pass rate 1/40: расширить кандидатов, снизить score bias на мёртвые free-keys
- auto: `raise_candidates`

