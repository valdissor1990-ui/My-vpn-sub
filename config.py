# === Источники (collector) ===
SOURCES = [
    # --- white-list / RU mobile ---
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    "https://codeberg.org/zieng2/wl/raw/branch/main/vless_universal.txt",
    "https://gitlab.com/zieng2/wl/raw/main/vless_universal.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-SNI-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",

    # --- Hysteria2 / white collections ---
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt",
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/WHITE_LIST_PROXY_COLLECTION.txt",
    "https://raw.githack.com/Subzio/subzio/main/HYSTERIA2.txt",

    # --- kizyak / Endi / FreeProxy ---
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta7.txt",
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta6.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-black-list.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/1.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/2.txt",

    # --- +10 открытых подписок ---
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_not_ru.txt",
    "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/All_Configs_base64_Sub.txt",
    "https://cdn.jsdelivr.net/gh/barry-far/V2ray-Configs@main/Sub_Merge.txt",
    "https://cdn.jsdelivr.net/gh/mahdibland/V2RayAggregator@main/sub/sub_merge_base64.txt",
    "https://cdn.jsdelivr.net/gh/peasoft/NoMoreWalls@main/list_raw.txt",
    "https://cdn.jsdelivr.net/gh/mfuu/v2ray@main/v2ray",
    "https://cdn.jsdelivr.net/gh/Pawdroid/Free-servers@main/sub",
    "https://cdn.jsdelivr.net/gh/aiboboxx/v2rayfree@main/v2",
    "https://cdn.jsdelivr.net/gh/freefq/free@main/v2",
    "https://cdn.jsdelivr.net/gh/learnhard-cn/free_proxy_ss@main/free",
]

# === Лимиты / мониторинг ===
MAX_SERVERS = 20          # только рабочие, не больше 20
CONNECT_TIMEOUT = 3       # сек TCP
MAX_PING_MS = 2000        # отсечка медленных
MAX_WORKERS = 40          # параллельных TCP-проверок

# Фильтры протокола
REQUIRE_REALITY_FOR_VLESS = True
REQUIRE_XHTTP_OR_GRPC = True
ALLOW_HYSTERIA2 = True

PREFERRED_SNI = [
    "yandex", "vk.com", "vk.ru", "mail.ru", "okcdn", "mycdn",
    "wildberries", "ozon", "cloudflare", "google", "microsoft",
    "apple", "amazon", "cdn", "fastly",
]

PROTOCOLS = ["vless", "vmess", "trojan", "hysteria2", "hy2", "hysteria"]
