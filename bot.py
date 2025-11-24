"""
bot.py - Minimal BasicBot used by the dashboard.

This implementation provides a simple `BasicBot` class with a `create_order`
method. When `dry_run=True` it returns a simulated order response so the
dashboard can function without requiring full Binance REST signing logic.

If you want real trading, extend this class to implement authenticated
requests with proper HMAC signing and error handling.
"""
import time
import random
from typing import Optional, Dict, Any


class BasicBot:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, base_url: Optional[str] = None, dry_run: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.dry_run = bool(dry_run)

    def create_order(self, symbol: str, side: str, type_: str = "MARKET", quantity: Optional[str] = None, price: Optional[str] = None, stopPrice: Optional[str] = None) -> Dict[str, Any]:
        """Create an order.

        - If `dry_run` is True, returns a simulated order dict (no network calls).
        - If `dry_run` is False, raises NotImplementedError to avoid accidental live orders.
        """
        if self.dry_run:
            # Simulate an order response similar to Binance's REST API minimal fields
            order_id = random.randint(10000000, 99999999)
            resp = {
                "symbol": symbol,
                "orderId": order_id,
                "clientOrderId": f"dry-{int(time.time())}-{random.randint(0,999)}",
                "transactTime": int(time.time() * 1000),
                "price": str(price) if price is not None else "0",
                "origQty": str(quantity) if quantity is not None else "0",
                "executedQty": "0",
                "status": "NEW",
                "type": type_,
                "side": side,
                "note": "dry_run simulated response",
            }
            return resp

        # For safety, do not perform live orders by default
        raise NotImplementedError("BasicBot.create_order called with dry_run=False: implement live order logic before enabling real trading")
