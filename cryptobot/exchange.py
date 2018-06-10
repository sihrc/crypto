import importlib

from cryptocore.mixins.logger import set_logging_level

EXCHANGES = {
    "binance": ("cryptocore.exchanges.binance", "BinanceExchangeService")
}


def run_exchange(exchange):
    """
    Dynamically import the Exchange class to prevent exchange environment contamination.
    """
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
        exchange_client.start()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("exchange", help="name of the exchange e.g. binance, kucoin, etc")
    parser.add_argument("--debug", help="turn on debugging logs", action="store_true")

    args = parser.parse_args()

    if args.debug:
        set_logging_level(10)
    else:
        set_logging_level(20)
    

    run_exchange(args.exchange)
