import os


class KeyChain(object):
    EXCHANGE_KEY_FORMAT = "{exchange}_exchange_key"
    SECRET_FORMAT = "{exchange}_exchange_secret"

    @classmethod
    def get_credentials(cls, exchange):
        return {
            "exchangeKey": cls.get_key(exchange),
            "secret": cls.get_secret(exchange)
        }

    @classmethod
    def get_key(cls, exchange):
        return getattr(cls, exchange, os.getenv(cls.EXCHANGE_KEY_FORMAT.format(exchange=exchange).upper()))

    @classmethod
    def get_secret(cls, exchange):
        return getattr(cls, exchange, os.getenv(cls.SECRET_FORMAT.format(exchange=exchange).upper()))
