# Источники подписок
# Упор: российский мобильный интернет (DPI/ТСПУ), YouTube без рекламы, доступ к ИИ
# Приоритет: VLESS + Reality и конфиги, заточенные под РФ

SOURCES = [
    # --- Специализированные под РФ / мобильный интернет ---
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt",
    "https://raw.githubusercontent.com/kort0881/vpn-vless-configs-russia/main/githubmirror/clean/vless.txt",

    # --- Reality / mix, хорошо заходят с мобильного ---
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/xray/reality.b64",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/xray/mix.b64",
    "https://raw.githubusercontent.com/itsyebekhe/HiN-VPN/main/subscription/normal/mix_base64",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix_base64",

    # --- Дополнительные качественные источники ---
    "https://raw.githubusercontent.com/Alirewa/V2ray-Configs/main/sub1.txt",
    "https://raw.githubusercontent.com/0xRadikal/Free-v2ray-Configs/main/verified/configs_base64.txt",
    "https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/best.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/super-sub.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub_Merge.txt",
]

# Настройки под мобильный интернет РФ
CONNECT_TIMEOUT = 3   # секунд на TCP-проверку
MAX_PING = 1000       # только относительно быстрые (важно для YouTube/ИИ)
MAX_WORKERS = 40      # параллельных проверок
MAX_SERVERS = 50      # топ-50 самых быстрых живых
PROTOCOLS = ["vless", "vmess", "trojan", "ss"]  # vless (особенно Reality) в приоритете при сортировке
