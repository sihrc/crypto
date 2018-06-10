import asyncio
import json

import websockets

from .base import ExchangeClientBase


class WebsocketExchangeBase(ExchangeClientBase):
    def __init__(self, exchange, uri, num_workers=4, ccxt_options=None):
        ExchangeClientBase.__init__(
            self,
            exchange,
            num_workers=num_workers,
            ccxt_options=ccxt_options
        )

        self.websocket_uri = uri

    @asyncio.coroutine
    def _websocket_start_listening(self):
        self.logger.info(
            "Connecting to websocket at {}".format(self.websocket_uri))
        self.connection = yield from websockets.connect(self.websocket_uri)
        self.logger.info(
            "Connection established at {}".format(self.websocket_uri))

        for message in self.websocket_subscribe_list():
            self.logger.info(
                "Sending websocket subscription {}".format(message))
            yield from self.connection.send(json.dumps(message))

        self.logger.info("Websocket listening")

        while True:
            try:
                message = yield from asyncio.wait_for(self.connection.recv(), timeout=5)
                self.logger.debug("Received message {}".format(message))
                message = self.websocket_format_message(message)
            except asyncio.TimeoutError:
                try:
                    self.logger.info("Issuing websocket ping")
                    pong_waiter = yield from self.connection.ping()
                    yield from asyncio.wait_for(pong_waiter, timeout=10)
                    self.logger.info("Websocket pong received")
                except asyncio.TimeoutError:
                    self.logger.warning(
                        "Experienced websocket timeout on receive.")
                    asyncio.get_event_loop().stop()
                    break
            else:
                self.websocket_handle_result(message)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._websocket_start_listening())
        loop.run_forever()

    def websocket_handle_result(self, message):
        raise NotImplementedError()

    def websocket_format_message(self, message):
        return json.loads(message)

    def websocket_subscribe_list(self):
        raise NotImplementedError()
