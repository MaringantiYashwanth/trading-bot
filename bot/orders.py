import logging
from typing import Any

from .client import BinanceClient

LOGGER = logging.getLogger(__name__)


class Orders:
    def __init__(self, client: BinanceClient) -> None:
        self.client = client

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict[str, Any] | None:
        LOGGER.info(
            "Order request type=MARKET symbol=%s side=%s quantity=%s",
            symbol,
            side,
            quantity,
        )
        response = self.client.place_market_order(symbol=symbol, side=side, quantity=quantity)
        LOGGER.info("Order response type=MARKET response=%s", response)
        return response

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
    ) -> dict[str, Any] | None:
        LOGGER.info(
            "Order request type=LIMIT symbol=%s side=%s quantity=%s price=%s",
            symbol,
            side,
            quantity,
            price,
        )
        response = self.client.place_limit_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
        )
        LOGGER.info("Order response type=LIMIT response=%s", response)
        return response
