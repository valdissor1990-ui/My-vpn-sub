# === Источники: расширенный сбор ===
SOURCES = [
    # RU / white-list
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    "https://codeberg.org/zieng2/wl/raw/branch/main/vless_universal.txt",
    "https://gitlab.com/zieng2/wl/raw/main/vless_universal.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-SNI-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_VLESS_RUS_mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_SS%2BAll_RUS.txt",
    "https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/WHITE-CIDR-RU-checked.txt",

    # Hysteria2 / white
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt",
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/WHITE_LIST_PROXY_COLLECTION.txt",
    "https://raw.githack.com/Subzio/subzio/main/HYSTERIA2.txt",

    # kizyak / Endi / FreeProxy
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta7.txt",
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta6.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-black-list.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-all.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/1.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/2.txt",
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/3.txt",

    # крупные агрегаторы
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_not_ru.txt",
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_ru.txt",
    "https://cdn.jsdelivr.net/gh/Epodonios/v2ray-configs@main/All_Configs_base64_Sub.txt",
    "https://cdn.jsdelivr.net/gh/barry-far/V2ray-Configs@main/Sub_Merge.txt",
    "https://cdn.jsdelivr.net/gh/mahdibland/V2RayAggregator@main/sub/sub_merge_base64.txt",
    "https://cdn.jsdelivr.net/gh/peasoft/NoMoreWalls@main/list_raw.txt",
    "https://cdn.jsdelivr.net/gh/mfuu/v2ray@main/v2ray",
    "https://cdn.jsdelivr.net/gh/Pawdroid/Free-servers@main/sub",
    "https://cdn.jsdelivr.net/gh/aiboboxx/v2rayfree@main/v2",
    "https://cdn.jsdelivr.net/gh/freefq/free@main/v2",

    # новые открытые
    "https://cdn.jsdelivr.net/gh/Alirewa/V2ray-Configs@main/sub1.txt",
    "https://cdn.jsdelivr.net/gh/Alirewa/V2ray-Configs@main/sub2.txt",
    "https://cdn.jsdelivr.net/gh/Alirewa/V2ray-Configs@main/config.txt",
    "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/v2ray/super-sub.txt",
    "https://cdn.jsdelivr.net/gh/MatinGhanbari/v2ray-configs@main/subscriptions/filtered/subs/vless.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/verified/configs_base64.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/protocols/vless.txt",
    "https://cdn.jsdelivr.net/gh/0xRadikal/Free-v2ray-Configs@main/all/configs_base64.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/best.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/reality.txt",
    "https://cdn.jsdelivr.net/gh/morpheusadam/v2ray-config@main/subs/bundles/lite.txt",
    "https://cdn.jsdelivr.net/gh/Au1rxx/free-vpn-subscriptions@main/output/v2ray-base64.txt",
    "https://cdn.jsdelivr.net/gh/hamedcode/port-based-v2ray-configs@main/split/vless-443.txt",
    "https://cdn.jsdelivr.net/gh/itsyebekhe/PSG@main/subscriptions/xray/reality.b64",
    "https://cdn.jsdelivr.net/gh/itsyebekhe/PSG@main/subscriptions/xray/mix.b64",
    "https://cdn.jsdelivr.net/gh/yebekhe/TelegramV2rayCollector@main/sub/mix_base64",
]

# лимиты
MAX_SERVERS = 20
CONNECT_TIMEOUT = 3
MAX_PING_MS = 2500
MAX_WORKERS = 50

# фильтры: шире, т.к. пинг есть а коннект нет — пробуем и TCP Reality
REQUIRE_REALITY_FOR_VLESS = True
ALLOW_XHTTP_GRPC = True
ALLOW_REALITY_TCP = True   # type=tcp + reality + vision
ALLOW_HYSTERIA2 = True

PREFERRED_SNI = [
    "yandex", "vk.com", "vk.ru", "mail.ru", "okcdn", "mycdn",
    "wildberries", "ozon", "cloudflare", "google", "microsoft",
    "apple", "amazon", "cdn", "fastly", "tesla", "paypal",
]

PROTOCOLS = ["vless", "vmess", "trojan", "hysteria2", "hy2", "hysteria"]
