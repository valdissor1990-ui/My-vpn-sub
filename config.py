# Yota / белые списки
# Только зеркала (raw.githubusercontent часто режется)
# В итоговый sub попадают только Reality + (XHTTP или gRPC)

SOURCES = [
    # --- jsDelivr ---
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-SNI-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/BLACK_VLESS_RUS_mobile.txt",

    # --- GitHack ---
    "https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githack.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githack.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt",

    # --- Codeberg ---
    "https://codeberg.org/igareck/vpn-configs-for-russia/raw/branch/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://codeberg.org/igareck/vpn-configs-for-russia/raw/branch/main/WHITE-CIDR-RU-checked.txt",

    # --- Bitbucket ---
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/WHITE-CIDR-RU-checked.txt",

    # --- Endi white (jsDelivr) ---
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
]

MAX_SERVERS = 50
# Строгий фильтр: только Reality + (xhttp ИЛИ grpc)
REQUIRE_REALITY = True
REQUIRE_XHTTP_OR_GRPC = True
PROTOCOLS = ["vless", "vmess", "trojan"]
