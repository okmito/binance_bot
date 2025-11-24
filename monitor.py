"""
monitor.py - Auto-fetch and auto-renew listenKey; connects to user data stream and forwards ORDER_TRADE_UPDATE events.
Requires: BINANCE_API_KEY and BINANCE_API_SECRET in env or config.json
"""
import os
import time
import threading
import requests
import json
from websocket import WebSocketApp

BASE_URL = os.environ.get("BINANCE_BASE_URL", "https://testnet.binancefuture.com")
BASE_WS = os.environ.get("BASE_WS", "wss://stream.binancefuture.com/ws/")

LISTEN_RENEW_INTERVAL = 60 * 25  # renew every 25 minutes (listenKey valid 30m)
RECONNECT_DELAY = 5

def load_config(path="config.json"):
    if os.path.exists(path):
        return json.load(open(path))
    return {}

class ListenKeyManager:
    def __init__(self, api_key, api_secret, base_url=BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")

        self.listen_key = None
        self._stop = False
        self._lock = threading.Lock()

    def fetch_listen_key(self):
        url = f"{self.base_url}/fapi/v1/listenKey"
        headers = {"X-MBX-APIKEY": self.api_key}
        r = requests.post(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        self.listen_key = data.get("listenKey")
        print("[Monitor] Obtained listenKey:", self.listen_key)
        return self.listen_key

    def renew_listen_key(self):
        if not self.listen_key:
            return False
        url = f"{self.base_url}/fapi/v1/listenKey"
        headers = {"X-MBX-APIKEY": self.api_key}
        r = requests.put(url, headers=headers, json={"listenKey": self.listen_key}, timeout=10)
        if r.status_code == 200:
            print("[Monitor] Renewed listenKey")
            return True
        else:
            print("[Monitor] Failed to renew listenKey:", r.text)
            return False

    def start_autorenew(self):
        def _loop():
            while not self._stop:
                time.sleep(LISTEN_RENEW_INTERVAL)
                try:
                    self.renew_listen_key()
                except Exception as e:
                    print("[Monitor] Error renewing listenKey:", e)
        t = threading.Thread(target=_loop, daemon=True)
        t.start()

    def stop(self):
        self._stop = True

class UserStreamClient:
    def __init__(self, listen_manager):
        self.lm = listen_manager
        self.ws = None
        self._stop = False

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            print("[Monitor] WS message:", data)
        except Exception as e:
            print("[Monitor] Failed to parse message:", e)

    def _on_error(self, ws, error):
        print("[Monitor] WS error:", error)

    def _on_close(self, ws, code, reason):
        print("[Monitor] WS closed", code, reason)

    def _on_open(self, ws):
        print("[Monitor] WS opened")

    def run(self):
        while not self._stop:
            try:
                if not self.lm.listen_key:
                    self.lm.fetch_listen_key()
                url = (os.environ.get("BASE_WS") or BASE_WS) + self.lm.listen_key
                print(f"[Monitor] Connecting to {url} ...")
                self.ws = WebSocketApp(url, on_message=self._on_message, on_error=self._on_error, on_close=self._on_close, on_open=self._on_open)
                self.lm.start_autorenew()
                self.ws.run_forever()
            except Exception as e:
                print("[Monitor] Connection failed:", e)
            print(f"[Monitor] Reconnecting in {RECONNECT_DELAY}s ...")
            time.sleep(RECONNECT_DELAY)

    def stop(self):
        self._stop = True
        if self.ws:
            try:
                self.ws.close()
            except:
                pass

def main():
    cfg = load_config()
    api_key = cfg.get("api_key") or os.environ.get("BINANCE_API_KEY")
    api_secret = cfg.get("api_secret") or os.environ.get("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise SystemExit("API key/secret required in config.json or env variables")
    lm = ListenKeyManager(api_key, api_secret, base_url=cfg.get("base_url"))
    client = UserStreamClient(lm)
    try:
        client.run()
    except KeyboardInterrupt:
        client.stop()
        lm.stop()

if __name__ == "__main__":
    main()