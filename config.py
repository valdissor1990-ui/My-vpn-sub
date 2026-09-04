# Источники — только репозитории, заточенные под РФ / мобильный интернет
# (уже отфильтрованные авторами под DPI/ТСПУ)

SOURCES = [
    # igareck — основной и самый цитируемый проект под РФ (обновляется часто)
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile-2.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_SS%2BAll_RUS.txt",

    # FreeProxyList — Reality / Hysteria2 / TUIC под РФ
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/main/mirror/1.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/main/mirror/2.txt",

    # Другие актуальные RU-ориентированные
    "https://raw.githubusercontent.com/Stintik-123/vpn-configs-russia/main/mobile.txt",
    "https://raw.githubusercontent.com/Maskkost93/kizyak-vpn-4.0/main/kizyakbeta7.txt",
    "https://raw.githubusercontent.com/MrEndi777709/Endi-VPN/main/mrendi-vpn-black-list.txt",
    "https://raw.githubusercontent.com/MrEndi777709/Endi-VPN/main/mrendi-vpn-white-list.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/githubmirror/clean/vless.txt",
]

# Настройки
MAX_SERVERS = 50
# TCP-проверку с GitHub отключаем: она не показывает работу с РФ-мобильного
SKIP_TCP_TEST = True
PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria2", "hy2"]
