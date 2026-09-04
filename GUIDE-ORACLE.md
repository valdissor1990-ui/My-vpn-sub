# Вариант 1: Oracle Cloud Always Free (свой сервер за 0 ₽/мес)

Это самый надёжный бесплатный путь для Yota + YouTube + ИИ.

## Что получишь
- Виртуальная машина навсегда (Always Free)
- На ней — Amnezia или VLESS Reality
- Свой ключ, не чужие сгоревшие подписки

## Шаги

### 1. Регистрация
1. Открой https://www.oracle.com/cloud/free/
2. Sign up / Start for free
3. Регион лучше: **Frankfurt (EU)** или **Amsterdam** (ближе к РФ)
4. Потребуется карта (холд ~1 USD, потом можно отвязать)
5. Подтверди email и телефон

### 2. Создать VM (Compute Instance)
1. Меню → Compute → Instances → Create instance
2. Name: vpn
3. Image: **Ubuntu 22.04** или 24.04
4. Shape: **VM.Standard.A1.Flex** (Ampere ARM) — Always Free
   - OCPU: 2, Memory: 12 GB (в рамках free tier)
5. Networking: создать VCN по умолчанию
6. SSH keys: сгенерировать или вставить свой публичный ключ
7. Create

Если A1 недоступен в регионе — попробуй другой регион EU или AMD micro (меньше ресурсов).

### 3. Открыть порты
Networking → Virtual Cloud Networks → Subnet → Security List → Ingress:
- TCP 443
- TCP 22 (SSH)
- UDP 443 (если будет Hysteria2/AmneziaWG)

### 4. Подключиться по SSH
```bash
ssh -i твой_ключ ubuntu@ПУБЛИЧНЫЙ_IP
```

### 5. Поставить VPN (проще через Amnezia)
На **телефоне**:
1. Установи приложение **AmneziaVPN** (сайт amnezia.org)
2. «Самостоятельный сервер» / Self-hosted
3. Введи IP, пользователя `ubuntu`, SSH-ключ
4. Amnezia сама поставит протокол (AmneziaWG / Reality)
5. Подключайся своим ключом

Альтернатива без Amnezia — 3x-ui:
```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```
Дальше в панели создай inbound VLESS + Reality, порт 443.

### 6. Если Yota всё ещё режет IP Oracle
Тогда нужен «белый» первый хоп (сложно без второго сервера) или комбинация с WARP (вариант 3).
Часто Oracle Frankfurt/Amsterdam на Yota всё же проходит вне самого жёсткого БС.

## Важно
- Не нарушай ToS Oracle (не рассылай спам, не открывай открытый прокси на весь мир)
- Только личное использование
- Сохрани SSH-ключ и бэкап конфига
