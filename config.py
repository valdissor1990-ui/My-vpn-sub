# === Источники (бот сбора) ===
# Зеркала: jsDelivr / GitHack / Codeberg / GitLab / GitVerse / Bitbucket

SOURCES = [
    # zieng2 — под белые списки
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    "https://codeberg.org/zieng2/wl/raw/branch/main/vless_universal.txt",
    "https://gitlab.com/zieng2/wl/raw/main/vless_universal.txt",
    "https://gitverse.ru/api/repos/zieng2/wl/raw/branch/master/list_universal.txt",

    # igareck white + mobile
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-SNI-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/WHITE-CIDR-RU-checked.txt",

    # Subzio Hy2 + white
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt",
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/WHITE_LIST_PROXY_COLLECTION.txt",
    "https://raw.githack.com/Subzio/subzio/main/HYSTERIA2.txt",

    # kizyak / Endi
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta7.txt",
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta6.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-black-list.txt",

    # доп. агрегаторы
    "https://cdn.jsdelivr.net/gh/nikita29a/FreeProxyList@main/mirror/1.txt",
    "https://cdn.jsdelivr.net/gh/3inker/v2ray-subscription@main/all_not_ru.txt",
]

# === Фильтры (filter-bot) ===
MAX_MAIN = 50
MAX_HY2 = 30
MAX_REALITY = 40

# Бонус к score, если SNI/host содержит эти подстроки (чаще в «белых» сценариях)
PREFERRED_SNI = [
    "yandex", "vk.com", "vk.ru", "mail.ru", "okcdn", "mycdn",
    "wildberries", "ozon", "avito", "sber", "tinkoff",
    "cloudflare", "google", "microsoft", "apple", "amazon",
    "fastly", "akamai", "edge", "cdn",
]

# Обязательные условия для VLESS/VMess/Trojan
REQUIRE_REALITY = True
REQUIRE_XHTTP_OR_GRPC = True
ALLOW_HYSTERIA2 = True

PROTOCOLS = ["vless", "vmess", "trojan", "hysteria2", "hy2", "hysteria"]
