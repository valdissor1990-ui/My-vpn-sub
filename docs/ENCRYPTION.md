# Шифрование ключей

## Жёсткий предел

| Сценарий | Возможно |
|----------|----------|
| В git не видно открытых ключей | Да — `private/*.enc` + `SUB_ENCRYPT_KEY` |
| Публичная подписка работает у всех, а ключи «спрятаны» | **Нет** |
| Клиент VPN без UUID/pbk/host | **Нет** |

Приложение на телефоне **всегда** должно получить открытый конфиг. Иначе не к чему подключаться.

## Схема в этом репо

```
private/nodes.txt.enc     ← можно коммитить (шифротекст)
SUB_ENCRYPT_KEY           ← только у тебя / в GitHub Secret
public sub.txt            ← только публичные free-источники пайплайна
```

Платные подписки в публичный `SOURCES` / `sub.txt` не добавляются.

## Команды

```bash
pip install -r requirements.txt
export SUB_ENCRYPT_KEY='...'

python -m bots.encrypt_bot check
python -m bots.encrypt_bot encrypt path/to/secrets.txt
python -m bots.encrypt_bot decrypt path/to/secrets.txt.enc
python -m bots.encrypt_bot seal-url 'https://my-private-sub-url'
```
