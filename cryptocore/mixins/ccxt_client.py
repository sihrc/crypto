import time
from functools import wraps
from collections import defaultdict

import cfscrape
import ccxt
from ccxt.base.errors import DDoSProtection

from ..keychain import KeyChain


__DDOS_LAST_RAISED__ = defaultdict(int) # in seconds since epoch
__DDOS_WAIT_TIMES__ = defaultdict(lambda: 60) # in seconds

def _ccxt_client_stub_method_(self, *args, **kwargs):
    raise NotImplementedError("Just a stub method")
    
class CCXTMixin(object):
    """
    Default symbol pair: 
        BASE / QUOTE
    """
    __inherited_ccxt_methods__ = [
        "loadMarkets",
        "fetchBalance",
        "fetchMarkets",
        "createOrder",
        "fetchCurrencies",
        "cancelOrder",
        "fetchTicker",
        "fetchOrder",
        "fetchTickers",
        "fetchOrders",
        "fetchOrderBook",
        "fetchOpenOrders",
        "fetchOHLCV",
        "fetchClosedOrders",
        "fetchTrades",
        "fetchMyTrades",
        "withdraw",
        "deposit"                                     
    ]

    def __init__(self, exchange, ccxt_options=None):
        options = self._ccxt_parse_options_(exchange, ccxt_options)
        self.__ccxt_exchange__ = exchange
        self.ccxt_client = getattr(ccxt, exchange)(options)
        
        for method in self.__inherited_ccxt_methods__:
            ccxt_method = getattr(self.ccxt_client, method, None)
            if ccxt_method is not None:
                setattr(self, method, CCXTMixin.ddos_protected_run(ccxt_method))


    @staticmethod
    def ddos_protected_run(func):
        @wraps(func)
        def wrapped(cls, *args, _ddos_wait=True, **kwargs):
            time_to_wait = __DDOS_WAIT_TIMES__[cls.exchange] - (time.time() - __DDOS_LAST_RAISED__[cls.exchange])
            if time_to_wait > 0 and _ddos_wait:
                time.sleep(time_to_wait)

            try:
                return func(*args, **kwargs)
            except DDoSProtection:
                __DDOS_LAST_RAISED__[cls.exchange] = time.time()
                raise
        
        return wrapped


    @classmethod
    def _ccxt_parse_options_(cls, exchange, ccxt_options):
        if ccxt_options is None:
            ccxt_options = {}
        
        ccxt_options["exchangeKey"] = ccxt_options.get("exchangeKey", KeyChain.get_key(exchange))
        ccxt_options["secret"] = ccxt_options.get("secret", KeyChain.get_secret(exchange))
        ccxt_options["timeout"] = 20000
        ccxt_options["session"] = cfscrape.create_scraper()
    
        return ccxt_options

    # Inherited functions
    loadMarkets = \
    fetchBalance = \
    fetchMarkets = \
    createOrder = \
    fetchCurrencies = \
    cancelOrder = \
    fetchTicker = \
    fetchOrder = \
    fetchTickers = \
    fetchOrders = \
    fetchOrderBook = \
    fetchOpenOrders = \
    fetchOHLCV = \
    fetchClosedOrders = \
    fetchTrades = \
    fetchMyTrades = \
    withdraw = \
    deposit = _ccxt_client_stub_method_
