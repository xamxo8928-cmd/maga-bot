import yfinance as yf

pairs = {
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "AUDUSD": "AUDUSD=X",
    "USDCAD": "CAD=X"
}

def get_prices():
    prices = {}

    for name, ticker in pairs.items():
        try:
            data = yf.download(ticker, period="1d", interval="1m", progress=False)

            if not data.empty:
                prices[name] = float(data["Close"].iloc[-1])

        except Exception as e:
            print(f"Ошибка {name}: {e}")

    return prices
