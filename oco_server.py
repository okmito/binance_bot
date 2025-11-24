"""
oco_server.py - Simple stateful OCO manager.
Stores OCO pairs in oco_state.json and listens to user data stream for ORDER_TRADE_UPDATE events.
When one order fills, cancels the linked order via REST.

Usage:
  python oco_server.py

Requires BINANCE_API_KEY / BINANCE_API_SECRET in env or config.json
"""
import os, json, time, threading, requests
from websocket import WebSocketApp

STATE_FILE = "oco_state.json"
BASE_WS = os.environ.get("BASE_WS", "wss://stream.binancefuture.com/ws/")
BASE_URL = os.environ.get("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

def load_config(path="config.json"):
    if os.path.exists(path):
        return json.load(open(path))
    return {}

class OCOState:
    def __init__(self, path=STATE_FILE):
        self.path = path
        self._lock = threading.Lock()
        self._data = {"pairs": []}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                self._data = json.load(open(self.path))
            except:
                self._data = {"pairs": []}

    def add_pair(self, symbol, limit_order_id, stop_order_id):
        with self._lock:
            self._data["pairs"].append({"symbol": symbol, "limit": int(limit_order_id), "stop": int(stop_order_id), "created": int(time.time())})
            self._save()

    def find_pair_by_order(self, orderId):
        with self._lock:
            for p in self._data["pairs"]:
                if p["limit"] == int(orderId) or p["stop"] == int(orderId):
                    return p
        return None

    def remove_pair(self, pair):
        with self._lock:
            self._data["pairs"] = [p for p in self._data["pairs"] if not (p["limit"]==pair["limit"] and p["stop"]==pair["stop"])]
            self._save()

    def _save(self):
        json.dump(self._data, open(self.path, "w"), indent=2)

class OCOManager:
    def __init__(self, api_key, api_secret, cfg):
        self.api_key = api_key
        self.api_secret = api_secret
        self.cfg = cfg
        self.state = OCOState()
        self.listen_key = None
        self.ws = None

    def _headers(self):
        return {"X-MBX-APIKEY": self.api_key}

    def fetch_listen_key(self):
        base = self.cfg.get("base_url") or os.environ.get("BINANCE_BASE_URL") or "https://testnet.binancefuture.com"
        url = f"{base.rstrip('/')}/fapi/v1/listenKey"

        r = requests.post(url, headers=self._headers(), timeout=10)
        r.raise_for_status()

        self.listen_key = r.json().get("listenKey")
        print("[OCO] listenKey:", self.listen_key)
        return self.listen_key


    def cancel_order(self, symbol, orderId):
        url = f"{self.cfg.get('base_url','https://testnet.binancefuture.com')}/fapi/v1/order"
        params = {"symbol": symbol, "orderId": orderId}
        r = requests.delete(url, params=params, headers=self._headers(), timeout=10)
        try:
            print("[OCO] cancel response:", r.json())
        except:
            print("[OCO] cancel raw:", r.text)

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if isinstance(data, dict) and data.get("e") == "ORDER_TRADE_UPDATE":
                o = data.get("o", {})
                status = o.get("X")
                orderId = o.get("i")
                symbol = o.get("s")
                print("[OCO] Order update:", orderId, status, symbol)
                pair = self.state.find_pair_by_order(orderId)
                if pair:
                    other = pair["limit"] if int(orderId) != pair["limit"] else pair["stop"]
                    print("[OCO] Cancelling other order:", other)
                    try:
                        self.cancel_order(pair["symbol"], other)
                    except Exception as e:
                        print("[OCO] Cancel failed:", e)
                    self.state.remove_pair(pair)
        except Exception as e:
            print("[OCO] ws parse error:", e)

    def on_open(self, ws):
        print("[OCO] WS opened")

    def run(self):
        self.fetch_listen_key()
        url = (os.environ.get("BASE_WS") or BASE_WS) + self.listen_key
        print("[OCO] connecting to", url)
        self.ws = WebSocketApp(url, on_message=self.on_message, on_open=self.on_open)
        self.ws.run_forever()

if __name__ == "__main__":
    cfg = load_config()
    api_key = cfg.get("api_key") or os.environ.get("BINANCE_API_KEY")
    api_secret = cfg.get("api_secret") or os.environ.get("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise SystemExit("API keys required in config.json or env")
    mgr = OCOManager(api_key, api_secret, cfg)
    mgr.run()