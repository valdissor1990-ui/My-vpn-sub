# Источники подписок (бесплатные открытые)
SOURCES = [
    # Основные проверенные
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/xray/mix.b64",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/xray/reality.b64",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix_base64",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub_Merge.txt",
    "https://raw.githubusercontent.com/Sarinaesmailzadeh/V2Hub/main/merged_base64",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/ircfspace/tvc/main/sub/mix_base64",
    "https://raw.githubusercontent.com/itsyebekhe/HiN-VPN/main/subscription/normal/mix_base64",

    # Дополнительные свежие источники
    "https://raw.githubusercontent.com/Alirewa/V2ray-Configs/main/sub1.txt",
    "https://raw.githubusercontent.com/Alirewa/V2ray-Configs/main/config.txt",
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/super-sub.txt",
    "https://raw.githubusercontent.com/0xRadikal/Free-v2ray-Configs/main/verified/configs_base64.txt",
    "https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/light.txt",
    "https://raw.githubusercontent.com/morpheusadam/v2ray-config/main/subs/bundles/best.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/all_extracted_configs.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/All_Configs_base64_Sub.txt",
]

# Настройки тестирования и мониторинга
CONNECT_TIMEOUT = 3   # секунд на TCP-подключение
MAX_PING = 1200       # максимальный пинг в ms (строже — только быстрые)
MAX_WORKERS = 40      # параллельных проверок
MAX_SERVERS = 50      # максимум серверов в итоговой подписке (только самые быстрые)
PROTOCOLS = ["vless", "vmess", "trojan", "ss"]
