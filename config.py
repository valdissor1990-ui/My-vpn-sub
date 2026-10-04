# Только zieng2/wl — подписка под обход белых списков (мобильный РФ)
SOURCES = [
    # GitVerse — часто доступнее при ограничениях
    "https://gitverse.ru/api/repos/zieng2/wl/raw/branch/master/list_universal.txt",
    # GitHub raw + jsDelivr
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_universal.txt",
    "https://cdn.jsdelivr.net/gh/zieng2/wl@main/vless_universal.txt",
    # Codeberg зеркало
    "https://codeberg.org/zieng2/wl/raw/branch/main/vless_universal.txt",
    # lite (меньше узлов, иногда свежее)
    "https://raw.githubusercontent.com/zieng2/wl/main/vless_lite.txt",
    "https://gitverse.ru/api/repos/zieng2/wl/raw/branch/master/list_lite.txt",
]

# TG web отключён — только zieng2
TG_WEB_CHANNELS = []

MAX_SERVERS = 20
MAX_WHITE = 20
MAX_BLACK = 10
MAX_VISION = 20

CONNECT_TIMEOUT = 3
MAX_PING_MS = 2200
MAX_WORKERS = 32
PRE_SCORE_CAP = 500  # у zieng2 мало узлов, не раздувать

DEAD_CACHE_FILE = "dead_cache.json"
DEAD_CACHE_HOURS = 6  # список обновляется часто — короткий кэш

PROTOCOL_TEST_CANDIDATES = 60
PROTOCOL_TEST_TIMEOUT = 10
PROTOCOL_TEST_MAX_PASS = 20
PROTOCOL_TEST_WORKERS = 4
PROTOCOL_TEST_WORKERS_HY2 = 2

TEST_URLS = [
    "http://www.gstatic.com/generate_204",
    "http://cp.cloudflare.com/generate_204",
    "http://connectivitycheck.gstatic.com/generate_204",
    "http://www.msftconnecttest.com/connecttest.txt",
]

MIHOMO_VERSIONS = ["v1.19.12", "v1.19.11", "v1.18.10"]

HY2_UP = "20 Mbps"
HY2_DOWN = "80 Mbps"
HY2_HOP_INTERVAL = 30
HY2_ALPN = ["h3"]
HY2_FINGERPRINT = "chrome"
HY2_INIT_STREAM_WINDOW = 8388608
HY2_MAX_STREAM_WINDOW = 8388608
HY2_INIT_CONN_WINDOW = 20971520
HY2_MAX_CONN_WINDOW = 20971520
HY2_APPLY_WINDOWS = False

# Приоритет под БС: Vision-TCP Reality ≈ XHTTP Reality > gRPC > прочее
SCORE_XHTTP_REALITY = 100
SCORE_VISION_TCP = 100
SCORE_GRPC_REALITY = 75
SCORE_HY2 = 40
SCORE_HY2_OBFS = 10
SCORE_HY2_PORTS = 5
SCORE_REALITY_OTHER = 50
SCORE_CF_SNI = 10
SCORE_RU_SNI = 25  # yandex/vk/max — важны для мобильного
SCORE_FAST_PING = 12
PENALTY_VISION_NON_TCP = -50
PENALTY_NO_PBK = -40

PREFERRED_SNI = [
    "yandex", "ya.ru", "vk.com", "vk.ru", "userapi", "max.ru",
    "mail.ru", "x5.ru", "passport.yandex", "360.yandex",
    "cloudflare", "cdn",
]

REQUIRE_REALITY_FOR_VLESS = False  # у zieng2 есть TLS+WS на CDN — не выкидывать всё
ALLOW_XHTTP_GRPC = True
ALLOW_REALITY_TCP = True
ALLOW_HYSTERIA2 = False  # в zieng2 нет hy2

PROTOCOLS = ["vless", "vmess", "trojan"]
