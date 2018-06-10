import sys
import signal
from functools import wraps

from ..mixins import LoggerMixin, ThreadPoolMixin, CCXTMixin
from ..data import InMemoryDataClient

class ExchangeClientBase(CCXTMixin, ThreadPoolMixin, LoggerMixin):
    """
    Base Exchange Client
    """

    def __init__(self, exchange, num_workers=4, ccxt_options=None, data_clients=None):
        LoggerMixin.__init__(self, logger_name=exchange)
        ThreadPoolMixin.__init__(self, num_workers=num_workers)
        CCXTMixin.__init__(self, exchange, ccxt_options=ccxt_options)

        for method in self.__inherited_ccxt_methods__:
            setattr(self, method, self.wrap_async(getattr(self, method)))

        self.data_clients = data_clients or [InMemoryDataClient(exchange)]
        self.EXCHANGE_STOPPED = True


    def _signal_exit(self, *args, **kwargs):
        self.stop()
        sys.exit()


    def start(self):
        try:
            self.EXCHANGE_STOPPED = False
            signal.signal(signal.SIGINT, self._signal_exit)
            signal.signal(signal.SIGTERM, self._signal_exit)
            self.logger.debug("Assigned exit signals")
        except ValueError:
            self.logger.warning("Exchange not run in main thread. Signals should have been registered on the main thread")
            pass

        self.logger.info("Exchange Client starting")


    def stop(self):
        """
        Any cleanup necessary for resources
        """
        self.EXCHANGE_STOPPED = True


    def format_quote_name(self, base, target):
        return base.upper() + "/" + target.upper()


    def get_base_target(self, quote):
        return quote.split("/")


    def save_quotes(self, quote_infos):
        for client in self.data_clients:
            client.save_quotes_data(quote_infos)
