from collections.abc import Sequence

from ..contracts import DictContract
from ..errors import NotPopulatedYet

QuoteContract = DictContract(
    required_keys=[
        "base",
        "target",
        "timestamp",
        "high",
        "low",
        "bid",
        "bid_volume",
        "ask",
        "ask_volume",
        "base_volume",
        "target_volume",
        "ticker"
    ],
    optional_keys=[
        "open",
        "close",
        "previous_close",
        "change"
    ]
)

class BaseDataClient(object):
    """
    Interface for Data Client Exchanges

    methods:
     - get_latest_quote_data (tickers, previous_n=1)
     - get_between_quote_data(tickers, start=None, end=None)
     - load_latest_quote_data(tickers, previous_n=1)
     - load_between_quote_data(tickers, start=None, end=None)
     - list_tickers()
     - save_quotes_data(quote_info(s))

    inputs:
     - start, end: timestamp seconds since epoch
     - ticker(s): list of ticker string, single ticker, or None - for all tickers
     - previous_n: int - number of latest entries
    """

    def __init__(self, exchange):
        self.exchange = exchange

    def get_latest_quote_data(self, tickers, previous_n=1):
        raise NotImplementedError()

    def get_between_quote_data(self, tickers, start=None, end=None):
        raise NotImplementedError()

    def load_latest_quote_data(self, tickers, previous_n=1):
        raise NotImplementedError()

    def load_between_quote_data(self, tickers, start=None, end=None):
        raise NotImplementedError()

    def list_tickers(self):
        raise NotImplementedError()

    def _filter_valid_quotes(self, quote_infos):
        return [
            quote_info for quote_info in self._ensure_list(quote_infos)
            if self._validate_quote(quote_info)
        ]

    def _validate_quote(self, quote_info):
        """
        Return True or False for valid or invalid
        """
        return QuoteContract.validate(quote_info)

    def save_quotes_data(self, quote_infos):
        return self._filter_valid_quotes(quote_infos)

    @staticmethod
    def _ensure_list(items):
        if not isinstance(items, Sequence):
            return [items]
        return items

