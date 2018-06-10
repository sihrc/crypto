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
     - get_between_quote_data(tickers, before=None, after=None)
     - load_latest_quote_data(tickers, previous_n=1)
     - load_between_quote_data(tickers, before=None, after=None)
     - list_tickers()
     - save_quotes_data(quote_info(s))

    inputs:
     - before, after: timestamp seconds since epoch
     - ticker(s): list of ticker string, single ticker, or None - for all tickers
     - previous_n: int - number of latest entries
    """

    def __init__(self, exchange):
        self.exchange = exchange

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

    def _validate_quotes(self, quote_infos):
        quote_infos = self._ensure_list(quote_infos)

        for quote_info in quote_infos:
            QuoteContract.validate(quote_info)
    
    def save_quotes_data(self, quote_infos):
        self._validate_quotes(quote_infos)

    @staticmethod
    def _ensure_list(items):
        if not isinstance(items, Sequence):
            return [items]
        return items

