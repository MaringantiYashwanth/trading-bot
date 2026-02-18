import logging
import os
from typing import Any

import dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

dotenv.load_dotenv()

LOGGER = logging.getLogger(__name__)
FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"


class BinanceClient:
    # Purpose: bridge between the bot and Binance API for futures order placement.
    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        use_testnet: bool = True,
    ) -> None:
        api_key = api_key or os.getenv("BINANCE_API_KEY")
        api_secret = api_secret or os.getenv("BINANCE_API_SECRET")

        self.client = Client(api_key=api_key, api_secret=api_secret)
        if use_testnet:
            self.client.FUTURES_URL = FUTURES_TESTNET_URL
        LOGGER.info("Binance client initialized. testnet=%s", use_testnet)

    @staticmethod
    def _validate_side(side: str) -> str:
        upper = side.upper()
        if upper not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")
        return upper

    @staticmethod
    def _parse_order_response(order: dict[str, Any]) -> dict[str, Any]:
        return {
            "order_id": order.get("orderId"),
            "symbol": order.get("symbol"),
            "side": order.get("side"),
            "type": order.get("type"),
            "status": order.get("status"),
            "origQty": order.get("origQty"),
            "executedQty": order.get("executedQty"),
            "avgPrice": order.get("avgPrice"),
        }

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict[str, Any] | None:
        try:
            payload = {
                "symbol": symbol.upper(),
                "side": self._validate_side(side),
                "type": "MARKET",
                "quantity": quantity,
            }
            LOGGER.info("Placing market order payload=%s", payload)
            order = self.client.futures_create_order(**payload)
            parsed = self._parse_order_response(order)
            LOGGER.info("Market order success response=%s", parsed)
            return parsed
        except (BinanceAPIException, BinanceOrderException) as exc:
            LOGGER.error("Binance order error: %s", exc)
            return None
        except Exception as exc:
            LOGGER.exception("Unexpected market order error: %s", exc)
            return None

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        price: float,
        time_in_force: str = "GTC",
    ) -> dict[str, Any] | None:
        try:
            payload = {
                "symbol": symbol.upper(),
                "side": self._validate_side(side),
                "type": "LIMIT",
                "timeInForce": time_in_force,
                "quantity": quantity,
                "price": price,
            }
            LOGGER.info("Placing limit order payload=%s", payload)
            order = self.client.futures_create_order(**payload)
            parsed = self._parse_order_response(order)
            LOGGER.info("Limit order success response=%s", parsed)
            return parsed
        except (BinanceAPIException, BinanceOrderException) as exc:
            LOGGER.error("Binance order error: %s", exc)
            return None
        except Exception as exc:
            LOGGER.exception("Limit order unexpected: %s", exc)
            return None

    def get_server_time(self) -> dict[str, Any]:
        return self.client.get_server_time()
