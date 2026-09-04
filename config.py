# === Источники ===
# Приоритет доноров: TG-агрегаторы на GitHub + RU white + protocol-tested feeds

SOURCES = [
    # --- уже собрано из Telegram (готовые raw) ---
    "https://cdn.jsdelivr.net/gh/soroushmirzaei/telegram-configs-collector@main/protocols/reality",
    "https://cdn.jsdelivr.net/gh/soroushmirzaei/telegram-configs-collector@main/protocols/vless",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/reality",
    "https://cdn.jsdelivr.net/gh/r3zarahimi/tg-v2ray-configs-every2h@main/Config_jo.txt",
    "https://cdn.jsdelivr.net/gh/r3zarahimi/tg-v2ray-configs-every2h@main/Config_jo_Light.txt",
    "https://cdn.jsdelivr.net/gh/mohamadfg-dev/telegram-v2ray-configs-collector@main/category/vless.txt",
    "https://cdn.jsdelivr.net/gh/Mosifree/-FREE2CONFIG@main/Reality",

    # --- RU / white ---
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_VLESS_RUS_mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",

    # --- Hy2 / Endi / FreeProxy ---
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/1.txt",

    # --- сильные агрегаторы ---
    "https://cdn.jsdelivr.net/gh/Au1rxx/free-vpn-subscriptions@main/output/v2ray-base64.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/verified/configs_base64.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/protocols/vless.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/reality.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/best.txt",
    "https://cdn.jsdelivr.net/gh/Alirewa/V2ray-Configs@main/sub1.txt",
    "https://cdn.jsdelivr.net/gh/itsyebekhe/PSG@main/subscriptions/xray/reality.b64",
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_not_ru.txt",
]

# Публичные TG-каналы для web-scrape (t.me/s/NAME — без API)
TG_WEB_CHANNELS = [
    "v2FreeHub",
    "ATLAS_V2VPN",
    "abc_configs",
    "NexoVPN",
    "nexovpn",
]

# лимиты
MAX_SERVERS = 20
MAX_WHITE = 20
MAX_BLACK = 20
CONNECT_TIMEOUT = 3
MAX_PING_MS = 2200
MAX_WORKERS = 40
PROTOCOL_TEST_CANDIDATES = 30
PROTOCOL_TEST_TIMEOUT = 10
PROTOCOL_TEST_MAX_PASS = 20

# Приоритеты протоколов (выше = лучше для DPI/обхода)
# 1) VLESS Reality + XHTTP
# 2) VLESS Reality + TCP + xtls-rprx-vision (XTLS Vision)
# 3) VLESS Reality + gRPC
# 4) Hysteria2
# 5) прочий Reality TCP
SCORE_XHTTP_REALITY = 100
SCORE_VISION_TCP = 90   # flow=xtls-rprx-vision + tcp + reality
SCORE_GRPC_REALITY = 70
SCORE_HY2 = 55
SCORE_REALITY_OTHER = 40
SCORE_CF_SNI = 15
SCORE_RU_SNI = 20       # yandex/vk — полезно под БС
SCORE_FAST_PING = 12

# Штрафы: несовместимые комбинации
PENALTY_VISION_NON_TCP = -50  # vision только с tcp/raw
PENALTY_NO_PBK = -30          # reality без pbk

PREFERRED_SNI = [
    "yandex", "vk.com", "vk.ru", "mail.ru", "storage.yandex",
    "cloudflare", "google", "microsoft", "apple", "deepl", "cdn",
]

REQUIRE_REALITY_FOR_VLESS = True
ALLOW_XHTTP_GRPC = True
ALLOW_REALITY_TCP = True
ALLOW_HYSTERIA2 = True

PROTOCOLS = ["vless", "vmess", "trojan", "hysteria2", "hy2", "hysteria"]
