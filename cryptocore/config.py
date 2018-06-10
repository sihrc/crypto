import os

ENVIRONMENT = os.getenv("CRYPTO_ENVIRONMENT", "development")

LOG_PATH = os.getenv("CRYPTO_LOG_PATH", "/var/log/")

# In Memory Data Client
MAX_PREVIOUS_N_IN_MEMORY = int(os.getenv("MAX_PREVIOUS_N_IN_MEMORY", 10))

# Redis Data Client
REDIS_HOST = os.getenv("REDIS_HOST", "crypto-redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "5379"))
REDIS_HISTORICAL_DB = int(os.getenv("REDIS_HISTORICAL_DB", "1"))
REDIS_LATEST_DB = int(os.getenv("REDIS_LATEST_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "redispassword")

DEFAULT_REDIS_CONFIG = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "password": REDIS_PASSWORD
}