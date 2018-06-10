import sys
import time
import signal
import importlib
from concurrent.futures import ThreadPoolExecutor, as_completed

from cryptocore.mixins.logger import set_logging_level

EXCHANGES = {
    "binance": ("cryptocore.exchanges.binance", "BinanceExchangeService")
}


def run_exchanges(exchanges):
    """
    Dynamically import the Exchange class to prevent exchange environment contamination.
    """
    thread_pool = ThreadPoolExecutor(max_workers=len(exchanges))

    tasks = []
    exchange_clients = []

    for exchange in exchanges:
        try:
            module, class_ = EXCHANGES[exchange]
        except KeyError:
            raise ValueError("{} is not a supported exchange. Please make sure it is listed in {}.EXCHANGES".format(
                exchange,
                __file__
            ))
        else:
            exchange = getattr(importlib.import_module(module), class_)
            exchange_client = exchange()
            exchange_clients.append(exchange_client)
            tasks.append(thread_pool.submit(exchange_client.start))

    def signal_exit(*args, **kwargs):
        for exchange_client in exchange_clients:
            exchange_client.stop()
        sys.exit()

    signal.signal(signal.SIGINT, signal_exit)
    signal.signal(signal.SIGTERM, signal_exit)

    while all([task.running() for task in tasks]):
        pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("exchanges", nargs="+", help="name of the exchange e.g. binance, kucoin, etc")
    parser.add_argument("--debug", help="turn on debugging logs", action="store_true")

    args = parser.parse_args()

    if args.debug:
        set_logging_level(10)
    else:
        set_logging_level(20)


    run_exchanges(args.exchanges)
