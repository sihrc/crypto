import time
from collections import defaultdict
from itertools import zip_longest

import redis

from ..base import BaseDataClient
from cryptocore.config import DEFAULT_REDIS_CONFIG, REDIS_LATEST_DB

DEFAULT_REDIS_CONFIG["db"] = REDIS_LATEST_DB


def _iterable_batcher(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)


class RedisLatestDataClient(BaseDataClient):

    def __init__(self, exchange, **redis_info):
        BaseDataClient.__init__(self, exchange)

        default_info = dict(DEFAULT_REDIS_CONFIG)
        default_info.update(redis_info or {})

        self.redis_client = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(**default_info)
        )
        self.tickers_list = self.sync_tickers()

    def get_latest_quote_data(self, tickers, previous_n=1):
        if previous_n > 1:
            raise NotImplementedError("Only the latest entry is available for RedisLatestDataClient")

        pipe = self.redis_client.pipeline()
        for ticker in tickers:
            pipe.hgetall(self._format_redis_key(ticker))

        return dict(zip(tickers, pipe.execute()))

    def sync_tickers(self):
        seen = set()
        seen_add = seen.add
        return [
            key for keys in _iterable_batcher(self.redis_client.scan_iter('*'), 500)
            for key in keys if not (key is None or key in seen or seen_add(key))
        ]

    def list_tickers(self):
        return self.tickers_list

    def save_quotes_data(self, quote_infos):
        quote_infos = super().save_quotes_data(quote_infos)

        pipe = self.redis_client.pipeline()
        for quote_info in quote_infos:
            key = self._format_redis_key(quote_info.get("ticker"))
            pipe.hmset(key, quote_info)

        pipe.execute()

    def _format_redis_key(self, ticker):
        return self.exchange + "-" + ticker

    def get_between_quote_data(self, tickers, start=None, end=None):
        raise NotImplementedError(
            "Only the latest entry is available for RedisLatestDataClient")

    def load_latest_quote_data(self, tickers, previous_n=1):
        if previous_n > 1:
            raise NotImplementedError(
                "Only the latest entry is available for RedisLatestDataClient")

    def load_between_quote_data(self, tickers, start=None, end=None):
        raise NotImplementedError(
            "Only the latest entry is available for RedisLatestDataClient")
