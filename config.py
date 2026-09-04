# Источники подписок
SOURCES = [
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/xray/mix.b64",
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/subscriptions/xray/reality.b64",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix_base64",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub_Merge.txt",
    "https://raw.githubusercontent.com/Sarinaesmailzadeh/V2Hub/main/merged_base64",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_base64_Sub.txt",
    "https://raw.githubusercontent.com/ircfspace/tvc/main/sub/mix_base64",
    "https://raw.githubusercontent.com/itsyebekhe/HiN-VPN/main/subscription/normal/mix_base64",
]

# Настройки тестирования
CONNECT_TIMEOUT = 3   # секунд на TCP-подключение
MAX_PING = 1500       # максимальный пинг в ms
MAX_WORKERS = 30      # параллельных проверок
MAX_SERVERS = 400     # максимум серверов в итоговой подписке (чтобы sub.txt не раздувался)
PROTOCOLS = ["vless", "vmess", "trojan", "ss"]
