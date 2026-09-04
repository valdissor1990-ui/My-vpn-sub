# Источники — репозитории под РФ / мобильный интернет

SOURCES = [
    # igareck (основной под РФ)
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_SS%2BAll_RUS.txt",

    # FreeProxyList
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/main/mirror/1.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/main/mirror/2.txt",

    # Другие
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/main/kizyakbeta7.txt",
    "https://raw.githubusercontent.com/MrEndi777709/Endi-VPN/main/mrendi-vpn-black-list.txt",
    "https://raw.githubusercontent.com/MrEndi777709/Endi-VPN/main/mrendi-vpn-white-list.txt",
]

MAX_SERVERS = 50
SKIP_TCP_TEST = True
PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria2", "hy2"]
