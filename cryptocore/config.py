import os

ENVIRONMENT = os.getenv("CRYPTO_ENVIRONMENT", "development")

LOG_PATH = os.getenv("CRYPTO_LOG_PATH", "/var/log/")