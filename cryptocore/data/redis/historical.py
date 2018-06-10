from collections import defaultdict

import redis

from ..base import BaseDataClient
from cryptocore.config import DEFAULT_REDIS_CONFIG, REDIS_HISTORICAL_DB

DEFAULT_REDIS_CONFIG["db"] = REDIS_HISTORICAL_DB

class RedisHistoricalDataClient(BaseDataClient):

    def __init__(self, exchange, **redis_info):
        BaseDataClient.__init__(self, exchange)

        default_info = dict(DEFAULT_REDIS_CONFIG)
        default_info.update(redis_info or {})

        self.redis_pool = redis.ConnectionPool(**default_info)

    def _get_redis_connection(self):
        return redis.StrictRedis(connection_pool=self.redis_pool)

    def get_latest_quote_data(self, tickers, previous_n=1):
        raise NotImplementedError()

    def get_between_quote_data(self, tickers, before=None, after=None):
        raise NotImplementedError()

    def load_latest_quote_data(self, tickers, previous_n=1):
        raise NotImplementedError()

    def load_between_quote_data(self, tickers, before=None, after=None):
        raise NotImplementedError()

    def list_tickers(self):
        raise NotImplementedError()

    def save_quotes_data(self, quote_infos):
        raise NotImplementedError()
