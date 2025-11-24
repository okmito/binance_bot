Simplified Binance Futures Trading Suite
===============================================

What's included:
- bot.py, cli.py, repl.py (from earlier)
- monitor.py     : auto-fetch & renew listenKey, connect to user stream
- oco_server.py  : stateful OCO manager (persistent oco_state.json)
- ws_stream.py   : mark price websocket helper
- dashboard/     : Flask + Socket.IO demo (forwards mark price & place dry-run orders)
- strategy.py    : signal generator example
- tests/         : pytest tests
- requirements.txt

Quick start
-----------

1) Create virtualenv and install:
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt

2) Configure API keys:
   Copy config_example.json -> config.json and add your testnet api_key and api_secret,
   or export environment variables:
     export BINANCE_API_KEY="..."
     export BINANCE_API_SECRET="..."

3) Run tests:
   pytest -v

4) Start monitor (auto listenKey + renew):
   python monitor.py

5) Start OCO server (in another terminal):
   python oco_server.py

6) Start dashboard (in another terminal):
   python dashboard/app.py
   Open http://localhost:5000

7) Use CLI / REPL:
   python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --dry-run
   python repl.py

Notes
-----
- Use TESTNET keys only.
- If web sockets fail, adjust BASE_WS env var to the correct host for testnet.