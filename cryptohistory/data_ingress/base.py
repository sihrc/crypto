import os
from cryptocore.mixins import LoggerMixin

CRYPTO_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

class DataIngressClient(LoggerMixin):  
    def __init__(self, exchange):
        self.exchange = exchange

    def save(self):
        raise NotImplementedError()

    def load(self):
        raise NotImplementedError()
