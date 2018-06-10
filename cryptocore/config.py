import os

ENVIRONMENT = os.getenv("CRYPTO_ENVIRONMENT", "development")

LOG_PATH = os.getenv("CRYPTO_LOG_PATH", "/var/log/")

# In Memory Data Client
MAX_PREVIOUS_N_IN_MEMORY = int(os.getenv("MAX_PREVIOUS_N_IN_MEMORY", 10))
