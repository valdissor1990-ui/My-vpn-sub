# Yota БС — максимум white-list источников с зеркал
# Reality+XHTTP/gRPC ИЛИ Hysteria2 (UDP иногда проходит иначе)

SOURCES = [
    # --- zieng2/wl (специально под белые списки) ---
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    "https://codeberg.org/zieng2/wl/raw/branch/main/vless_universal.txt",
    "https://gitlab.com/zieng2/wl/raw/main/vless_universal.txt",
    "https://gitverse.ru/api/repos/zieng2/wl/raw/branch/master/list_universal.txt",

    # --- igareck white ---
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-checked.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-CIDR-RU-all.txt",
    "https://cdn.jsdelivr.net/gh/igareck/vpn-configs-for-russia@main/WHITE-SNI-RU-all.txt",
    "https://raw.githack.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://bitbucket.org/igareck/vpn-configs-for-russia/raw/main/Vless-Reality-White-Lists-Rus-Mobile.txt",

    # --- Subzio (Hysteria2 + white collection) ---
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/HYSTERIA2.txt",
    "https://cdn.jsdelivr.net/gh/Subzio/subzio@main/WHITE_LIST_PROXY_COLLECTION.txt",
    "https://raw.githack.com/Subzio/subzio/main/HYSTERIA2.txt",

    # --- kizyak white/mobile ---
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta7.txt",
    "https://cdn.jsdelivr.net/gh/Maskkost93/kizyak-vpn-4.0@main/kizyakbeta6.txt",

    # --- Endi white ---
    "https://cdn.jsdelivr.net/gh/MrEndi777709/Endi-VPN@main/mrendi-vpn-white-list.txt",
]

MAX_SERVERS = 60
# Reality+(xhttp|grpc) ИЛИ hysteria2/hy2
ALLOW_HYSTERIA2 = True
REQUIRE_REALITY_FOR_VLESS = True
REQUIRE_XHTTP_OR_GRPC_FOR_VLESS = True
PROTOCOLS = ["vless", "vmess", "trojan", "hysteria2", "hy2", "hysteria"]
