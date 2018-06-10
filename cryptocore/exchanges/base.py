import sys
import signal
from functools import wraps

from ..mixins import LoggerMixin, ThreadPoolMixin, CCXTMixin, QuotesMixin

class ExchangeClientBase(CCXTMixin, QuotesMixin, ThreadPoolMixin, LoggerMixin):
    """
    Base Exchange Client
    """

    def __init__(self, exchange, num_workers=4, ccxt_options=None):
        LoggerMixin.__init__(self, logger_name=exchange)
        ThreadPoolMixin.__init__(self, num_workers=num_workers)
        CCXTMixin.__init__(self, exchange, ccxt_options=ccxt_options)
        QuotesMixin.__init__(self)

        for method in self.__inherited_ccxt_methods__:
            setattr(self, method, self.wrap_async(getattr(self, method)))


    def _signal_exit(self, *args, **kwargs):
        self.logger.info("Exit command received")
        self.stop()
        sys.exit()


    def start(self):
        self.logger.debug("Assigned exit signals")
        signal.signal(signal.SIGINT, self._signal_exit)
        signal.signal(signal.SIGTERM, self._signal_exit)

        self.logger.info("Exchange Client starting")
        
 
    def stop(self):
        """
        Any cleanup necessary for resources
        """
        self.logger.info("Exchange Client stopping")
