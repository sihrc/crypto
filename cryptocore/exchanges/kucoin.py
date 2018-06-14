import sys

import time
import requests
from concurrent.futures import as_completed
from operator import itemgetter

from .base import ExchangeClientBase

class KucoinExchangeService(ExchangeClientBase):
    BASE_URL = "https://api.kucoin.com/v1/open/tick"
    def __init__(self):
        self.symbols = [
            result["symbol"] for result in
            requests.get(KucoinExchangeService.BASE_URL).json()["data"]
        ]

        ExchangeClientBase.__init__(self, "kucoin", num_workers=len(self.symbols))


    def start(self):
        super().start()

        for future in as_completed([
            self.execute_async(self._poll_symbol, symbol)
            for symbol in self.symbols
        ]):
            future.result()
            sys.exit()


    def _poll_symbol(self, symbol):
        """
        "msg": "Operation succeeded.",
        "data": {
            "coinType": "KCS",
            "trading": true,
            "lastDealPrice": 5040,
            "buy": 5000,
            "sell": 5040,
            "coinTypePair": "BTC",
            "sort": 0,
            "feeRate": 0.001,
            "volValue": 308140577,
            "high": 6890,
            "datetime": 1506050394000,
            "vol": 5028739175025,
            "low": 5040,
            "changeRate": -0.2642
        }
        """
        self.logger.info("Started polling for {}".format(symbol))
        while True:
            try:
                symbol_response = requests.get(self.BASE_URL + "?symbol=" + symbol)
                if symbol_response.status_code != 200:
                    self.logger.error(symbol_response.text)
            except requests.exceptions.RequestException:
                self.logger.exception("Kucoin exception occured")
            else:
                symbol_info = symbol_response.json()["data"]
                self.save_quotes({
                    "base": symbol_info["coinType"],
                    "target": symbol_info["coinTypePair"],
                    "timestamp": symbol_info["datetime"]/1000,
                    "high": symbol_info["high"],
                    "low": symbol_info["low"],
                    "bid": symbol_info["buy"],
                    "bid_volume": None,
                    "ask": symbol_info["sell"],
                    "ask_volume": None,
                    "base_volume": None,
                    "target_volume": symbol_info["vol"],
                    "ticker": self.format_quote_name(
                        symbol_info["coinType"],
                        symbol_info["coinTypePair"]
                    )
                })
                self.logger.debug("Successfully saved a quote for {}".format(symbol))

if __name__ == "__main__":
    client = KucoinExchangeService()
    client.start()
