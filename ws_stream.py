"""
ws_stream.py - Mark price streamer helper.
Provides subscribe_mark_price(symbol, callback) that runs in a thread and calls callback(data)
"""
from websocket import WebSocketApp
import json, time, threading, os

BASE_WS = os.environ.get("BASE_WS", "wss://stream.binancefuture.com/ws/")

def _on_message_factory(cb):
    def _on_message(ws, msg):
        try:
            data = json.loads(msg)
            cb(data)
        except Exception as e:
            print("ws_stream on_message error:", e)
    return _on_message

def subscribe_mark_price(symbol, cb):
    symbol = symbol.lower()
    stream = f"{symbol}@markPrice"
    url = BASE_WS + stream
    def _run():
        while True:
            try:
                ws = WebSocketApp(url, on_message=_on_message_factory(cb), on_error=lambda w,e: print("ws err", e), on_close=lambda w,c,r: print("ws close"), on_open=lambda w: print("ws open"))
                ws.run_forever()
            except Exception as e:
                print("ws_stream crashed:", e)
            time.sleep(2)
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return t