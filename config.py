# === Источники ===
SOURCES = [
    "https://cdn.jsdelivr.net/gh/soroushmirzaei/telegram-configs-collector@main/protocols/reality",
    "https://cdn.jsdelivr.net/gh/soroushmirzaei/telegram-configs-collector@main/protocols/vless",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/reality",
    "https://cdn.jsdelivr.net/gh/r3zarahimi/tg-v2ray-configs-every2h@main/Config_jo.txt",
    "https://cdn.jsdelivr.net/gh/r3zarahimi/tg-v2ray-configs-every2h@main/Config_jo_Light.txt",
    "https://cdn.jsdelivr.net/gh/mohamadfg-dev/telegram-v2ray-configs-collector@main/category/vless.txt",
    "https://cdn.jsdelivr.net/gh/Mosifree/-FREE2CONFIG@main/Reality",
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_VLESS_RUS_mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/1.txt",
    "https://cdn.jsdelivr.net/gh/Au1rxx/free-vpn-subscriptions@main/output/v2ray-base64.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/verified/configs_base64.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/protocols/vless.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/reality.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/best.txt",
    "https://cdn.jsdelivr.net/gh/Alirewa/V2ray-Configs@main/sub1.txt",
    "https://cdn.jsdelivr.net/gh/itsyebekhe/PSG@main/subscriptions/xray/reality.b64",
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_not_ru.txt",
]

# TG web scrape (t.me/s/NAME) — расширенный список
TG_WEB_CHANNELS = [
    "v2FreeHub",
    "ATLAS_V2VPN",
    "abc_configs",
    "NexoVPN",
    "nexovpn",
    "ConfigsHUB",
    "v2rayngvpn",
    "freev2rayn",
    "VlessConfig",
    "v2ray_configs",
    "hope_net",
    "ProxyForOpensource",
    "v2rayng_config_free",
    "FreeV2rayy",
    "v2raycollector",
    "CustomV2ray",
    "v2rayngfree",
    "ShadowProxy66",
]

MAX_SERVERS = 20
MAX_WHITE = 20
MAX_BLACK = 20
MAX_VISION = 20

CONNECT_TIMEOUT = 3
MAX_PING_MS = 2200
MAX_WORKERS = 40

# pre-score: не пинговать всё подряд
PRE_SCORE_CAP = 3000

# кэш мёртвых host:port
DEAD_CACHE_FILE = "dead_cache.json"
DEAD_CACHE_HOURS = 12

PROTOCOL_TEST_CANDIDATES = 30
PROTOCOL_TEST_TIMEOUT = 10
PROTOCOL_TEST_MAX_PASS = 20

SCORE_XHTTP_REALITY = 100
SCORE_VISION_TCP = 95
SCORE_GRPC_REALITY = 70
SCORE_HY2 = 55
SCORE_REALITY_OTHER = 40
SCORE_CF_SNI = 15
SCORE_RU_SNI = 20
SCORE_FAST_PING = 12
PENALTY_VISION_NON_TCP = -50
PENALTY_NO_PBK = -30

PREFERRED_SNI = [
    "yandex", "vk.com", "vk.ru", "mail.ru", "storage.yandex",
    "cloudflare", "google", "microsoft", "apple", "deepl", "cdn",
]

REQUIRE_REALITY_FOR_VLESS = True
ALLOW_XHTTP_GRPC = True
ALLOW_REALITY_TCP = True
ALLOW_HYSTERIA2 = True

PROTOCOLS = ["vless", "vmess", "trojan", "hysteria2", "hy2", "hysteria"]
