"""
dashboard/app.py - Flask dashboard that forwards mark price to connected clients via Socket.IO.
"""
import os, json, threading, time
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from bot import BasicBot
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import ws_stream

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "dev"
socketio = SocketIO(app, cors_allowed_origins="*")

cfg = {}
cfg_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
if os.path.exists(cfg_path):
    cfg = json.load(open(cfg_path))
bot = BasicBot(api_key=cfg.get("api_key"), api_secret=cfg.get("api_secret"), base_url=cfg.get("base_url"), dry_run=True)

def mark_callback(data):
    try:
        # markPrice stream format includes 's' (symbol) and 'p' or 'markPrice'
        symbol = data.get("s")
        price = data.get("p") or data.get("markPrice")
        socketio.emit("mark_price", {"symbol": symbol, "price": price})
    except Exception as e:
        print("mark_callback error:", e)

def start_mark_stream(symbol="BTCUSDT"):
    ws_stream.subscribe_mark_price(symbol, mark_callback)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.json
    try:
        resp = bot.create_order(symbol=data.get("symbol"), side=data.get("side"), type_=data.get("type_"), quantity=data.get("quantity"), price=data.get("price"), stopPrice=data.get("stopPrice"))
        return jsonify(resp)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@socketio.on("connect")
def handle_connect():
    emit("connected", {"ok": True})

if __name__ == "__main__":
    t = threading.Thread(target=start_mark_stream, args=("BTCUSDT",), daemon=True)
    t.start()
    socketio.run(app, host="0.0.0.0", port=5000)