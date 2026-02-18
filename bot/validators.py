import re


class Validators:
    _SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,20}$")

    @staticmethod
    def validate_symbol(symbol: str) -> str:
        normalized = symbol.strip().upper()
        if not Validators._SYMBOL_PATTERN.fullmatch(normalized):
            raise ValueError("symbol must be alphanumeric like BTCUSDT")
        return normalized

    @staticmethod
    def validate_side(side: str) -> str:
        normalized = side.strip().upper()
        if normalized not in {"BUY", "SELL"}:
            raise ValueError("side must be BUY or SELL")
        return normalized

    @staticmethod
    def validate_order_type(order_type: str) -> str:
        normalized = order_type.strip().upper()
        if normalized not in {"MARKET", "LIMIT"}:
            raise ValueError("order_type must be MARKET or LIMIT")
        return normalized

    @staticmethod
    def validate_quantity(quantity: float) -> float:
        if quantity <= 0:
            raise ValueError("quantity must be a positive number")
        return quantity

    @staticmethod
    def validate_price(price: float | None, order_type: str) -> float | None:
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("price is required for LIMIT orders")
            if price <= 0:
                raise ValueError("price must be a positive number")
            return price

        if price is not None and price <= 0:
            raise ValueError("price must be a positive number when provided")
        return price

    @staticmethod
    def validate_order_inputs(
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
    ) -> dict[str, str | float | None]:
        validated_order_type = Validators.validate_order_type(order_type)
        return {
            "symbol": Validators.validate_symbol(symbol),
            "side": Validators.validate_side(side),
            "order_type": validated_order_type,
            "quantity": Validators.validate_quantity(quantity),
            "price": Validators.validate_price(price, validated_order_type),
        }
