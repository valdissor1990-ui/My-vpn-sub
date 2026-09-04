# Yota / белые списки — только white-list источники
# Обычные black-list подписки на жёстком БС почти не работают

SOURCES = [
    # igareck — белые списки (CIDR / Reality под мобильный БС)
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-SNI-RU-all.txt",

    # Endi — только обход (white)
    "https://raw.githubusercontent.com/MrEndi777709/Endi-VPN/main/mrendi-vpn-white-list.txt",

    # Запас: mobile black (иногда при ослаблении БС)
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt",
]

MAX_SERVERS = 50
SKIP_TCP_TEST = True
PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria2", "hy2"]
