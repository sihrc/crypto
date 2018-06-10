"""
Quotes handling

base - base currency
quote - target currency
timestamp - time in seconds
"""
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

class QuotesMixin(object):
    """
    Mixin for handling quotes
    """
    def __init__(self):
        self._quote_data = {}
    

    def save_quote(self, quote):
        # Resolve ticker & base & target
        ticker = quote.get("ticker")
        
        if ticker is not None:
            quote["base"], quote["target"] = self.get_base_quote(ticker)

        quote["ticker"] = self.format_ticker_name(quote["base"], quote["target"])
        
        QuoteContract.validate(quote)
        self._quote_data[ticker] = quote

    
    def get_quote(self, base, quote):
        ticker = self.format_ticker_name(base, quote)

        if ticker not in self._quote_data:
            raise NotPopulatedYet(ticker)

        return self._quote_data[ticker]


    def format_ticker_name(self, base, target):
        return base.upper() + "/" + target.upper()


    def get_base_quote(self, ticker):
        return ticker.split("/")


    def get_all_quotes(self):
        return self._quote_data
