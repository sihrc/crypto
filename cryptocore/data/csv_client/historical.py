from collections import defaultdict

from ..base import BaseDataClient, QuoteContract


class CSVHistoricalDataClient(BaseDataClient):
    """
    Data Directory Structure
    data/
        year_day(365)/
            hour(24)/
                <ticker>_year_day_hour.csv
                    :fields - QuoteContract fields
    """
    def __init__(self, exchange):
        BaseDataClient.__init__(self, exchange)

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
