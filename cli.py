import argparse
import logging
import sys
from typing import Any

from bot.client import BinanceClient
from bot.logging_config import LoggingConfig
from bot.orders import Orders
from bot.validators import Validators

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="Order side: BUY or SELL")
    parser.add_argument("--order-type", required=True, help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Limit order price")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print order payload without sending to Binance",
    )
    return parser


def build_dry_run_payload(validated: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "symbol": validated["symbol"],
        "side": validated["side"],
        "type": validated["order_type"],
        "quantity": validated["quantity"],
    }
    if validated["order_type"] == "LIMIT":
        payload["timeInForce"] = "GTC"
        payload["price"] = validated["price"]
    return payload


def main() -> None:
    LoggingConfig.configure()
    args = build_parser().parse_args()
    try:
        validated = Validators.validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValueError as exc:
        LOGGER.error("Input validation failed: %s", exc)
        print(f"Input error: {exc}")
        sys.exit(2)

    if args.dry_run:
        payload = build_dry_run_payload(validated)
        LOGGER.info("Dry-run enabled. payload=%s", payload)
        print({"dry_run": True, "payload": payload})
        return

    client = BinanceClient(use_testnet=True)
    orders = Orders(client=client)

    if validated["order_type"] == "MARKET":
        result = orders.place_market_order(
            validated["symbol"],
            validated["side"],
            validated["quantity"],
        )
    else:
        result = orders.place_limit_order(
            validated["symbol"],
            validated["side"],
            validated["quantity"],
            validated["price"],
        )

    LOGGER.info("CLI order result=%s", result)
    print(result)


if __name__ == "__main__":
    main()
