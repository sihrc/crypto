import time
import requests
from operator import itemgetter

from binance.websockets import BinanceSocketManager
from binance.client import Client
from twisted.internet import reactor

from .base import ExchangeClientBase
from ..keychain import KeyChain

class BinanceExchangeService(ExchangeClientBase):
    """
    Binance Exchange Services
    (Depends on 3rd party binance websockets library, python-binanc)e
    https://github.com/sammchardy/python-binance
    
    binance_response_mapping:
        ("s", "symbol"),
    ("E", "timestamp"),
        ("h", "high"),
        ("l", "low"),
        ("b", "bid"),
        ("B", "bid_volume"),
        ("a", "ask"),
        ("A", "ask_volume"),
        ("w", "w_av_price"),
        ("o", "open"),
        ("c", "close"),
        ("x", "previous_close"),
        ("p", "change"),
        ("P", "percentage"),
        ("v", "base_volume"),
        ("q", "quote_volume")
    """

    _binance_item_getter,_binance_quote_keys = zip(*[
        ("E", "timestamp"),
        ("h", "high"),
        ("l", "low"),
        ("b", "bid"),
        ("B", "bid_volume"),
        ("a", "ask"),
        ("A", "ask_volume"),
        ("v", "base_volume"),
        ("q", "target_volume"),
        ("o", "open"),
        ("c", "close"),
        ("x", "previous_close"),
        ("p", "change"),
        ("s", "ticker")
    ])

    _binance_item_getter = itemgetter(*_binance_item_getter)


    def __init__(self):
        ExchangeClientBase.__init__(self, "binance")

        symbol_infos = requests.get(
            "https://api.binance.com/api/v1/exchangeInfo"
        ).json()["symbols"]

        self.binance_symbol_mapping = {
            info["symbol"]: (info["baseAsset"], info["quoteAsset"]) for info in symbol_infos
        }

        self.binance_socket_manager = BinanceSocketManager(
            Client(
                KeyChain.get_key("binance"),
                KeyChain.get_secret("binance")
            )
        )


    def process_ticker_response(self, tickers_response):
        self.logger.debug("Received ticker response {}".format(tickers_response), truncate=480)
        
        for ticker_response in tickers_response:
            self.save_quote(dict(zip(
                self._binance_quote_keys,
                self._binance_item_getter(ticker_response)
            )))
        
        self.logger.info("Saved {} tickers".format(len(tickers_response)))


    def get_base_quote(self, ticker):
        return self.binance_symbol_mapping[ticker]


    def start(self):
        super().start()
        self.binance_socket_manager.start_ticker_socket(
            self.process_ticker_response
        )
        self.binance_socket_manager.start()
        
        while True:            
            time.sleep(60)
            

    def stop(self):
        super().stop()
        reactor.stop() # pylint: disable=E1101
        self.binance_socket_manager.close()
