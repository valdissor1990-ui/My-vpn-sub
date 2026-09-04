# === SOURCES (доноры + RU/WL) ===
SOURCES = [
    # RU / white
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    "https://codeberg.org/zieng2/wl/raw/branch/main/vless_universal.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-SNI-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_VLESS_RUS_mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_SS%2BAll_RUS.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",

    # PypsCFG-style / donors
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt",
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/WHITE_LIST_PROXY_COLLECTION.txt",
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta7.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-black-list.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/1.txt",

    # strong aggregators (protocol-tested upstream)
    "https://cdn.jsdelivr.net/gh/Au1rxx/free-vpn-subscriptions@main/output/v2ray-base64.txt",
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_not_ru.txt",
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_ru.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/verified/configs_base64.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/protocols/vless.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/best.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/reality.txt",
    "https://cdn.jsdelivr.net/gh/Alirewa/V2ray-Configs@main/sub1.txt",
    "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/v2ray/super-sub.txt",
    "https://cdn.jsdelivr.net/gh/itsyebekhe/PSG@main/subscriptions/xray/reality.b64",
    "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/All_Configs_base64_Sub.txt",
    "https://cdn.jsdelivr.net/gh/barry-far/V2ray-Configs@main/Sub_Merge.txt",
]

# URL hints → white/black label for source
WHITE_SOURCE_HINTS = ["white", "whitelist", "cidr", "wl", "WHITE"]
BLACK_SOURCE_HINTS = ["black", "BLACK", "all_not_ru", "mobile"]

# limits
MAX_SERVERS = 20
MAX_WHITE = 20
MAX_BLACK = 20
CONNECT_TIMEOUT = 3
MAX_PING_MS = 2500
MAX_WORKERS = 40
PROTOCOL_TEST_CANDIDATES = 40  # после TCP берём top-N на xray-проб
PROTOCOL_TEST_TIMEOUT = 12

# scoring weights (config-sub-platform / SmartSub style)
SCORE_HY2 = 40
SCORE_REALITY = 25
SCORE_XHTTP = 20
SCORE_GRPC = 15
SCORE_VISION = 10
SCORE_CF_SNI = 20
SCORE_PREFERRED_SNI = 12
SCORE_TCP_FAST = 15  # ping < 400ms

PREFERRED_SNI = [
    "yandex", "vk.com", "vk.ru", "mail.ru", "okcdn", "cloudflare",
    "google", "microsoft", "apple", "amazon", "tesla", "cdn",
]

# filters
REQUIRE_REALITY_FOR_VLESS = True
ALLOW_XHTTP_GRPC = True
ALLOW_REALITY_TCP = True
ALLOW_HYSTERIA2 = True

PROTOCOLS = ["vless", "vmess", "trojan", "hysteria2", "hy2", "hysteria"]

# Telegram (optional secrets: TG_API_ID, TG_API_HASH, TG_CHANNELS)
TG_CHANNELS_DEFAULT = [
    # публичные примеры — работают только при наличии API secrets
    "@v2ray_configs",
    "@freev2rayn",
]
