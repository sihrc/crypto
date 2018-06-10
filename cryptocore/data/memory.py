import time

from collections import defaultdict, deque

from .base import BaseDataClient
from ..config import MAX_PREVIOUS_N_IN_MEMORY

class InMemoryDataClient(BaseDataClient):
    GLOBAL_IN_MEMORY_STORE = {}

    def __init__(self, exchange, previous_n_saved=MAX_PREVIOUS_N_IN_MEMORY):
        BaseDataClient.__init__(self, exchange)
        self._in_memory_store = InMemoryDataClient.GLOBAL_IN_MEMORY_STORE.get(
            exchange, defaultdict(lambda: deque([], maxlen=previous_n_saved))
        )

    def get_latest_quote_data(self, tickers, previous_n=1):
        returned_data = {}
        for ticker in BaseDataClient._ensure_list(tickers):
            returned_data[ticker] = self._in_memory_store[ticker][:previous_n]
        return returned_data

    def get_between_quote_data(self, tickers, before=None, after=None):
        returned_data = {}
        before = before or time.time()
        after = after or 0
                
        for ticker in BaseDataClient._ensure_list(tickers):
            returned_data[ticker] = [
                quote for quote in self._in_memory_store[ticker]
                if quote["timestamp"] < before and quote["timestamp"] > after
            ]
        
        return returned_data

    def load_latest_quote_data(self, tickers, previous_n=1):
        raise NotImplementedError("Loading available for InMemoryDataClient")

    def load_between_quote_data(self, tickers, before=None, after=None):
        raise NotImplementedError("Loading available for InMemoryDataClient")

    def list_tickers(self):
        return list(self._in_memory_store.keys())

    def save_quotes_data(self, quote_infos):
        super().save_quotes_data(quote_infos)

        for quote_info in BaseDataClient._ensure_list(quote_infos):
            self._in_memory_store[quote_info["ticker"]].appendleft(quote_info)

        return quote_infos
