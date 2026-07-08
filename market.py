import yfinance as yf

PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
    "USD/CHF": "CHF=X",
    "NZD/USD": "NZDUSD=X"
}

def get_market_data():
    result = {}

    for pair_name, ticker in PAIRS.items():
        print(f"Загружаю {pair_name} ({ticker})")

        try:
            df = yf.download(
                ticker,
                period="2d",
                interval="1m",
                progress=False,
                auto_adjust=False
            )

            if df.empty:
                print(f"Нет данных для {pair_name}")
                continue

            df = df.dropna()

            if hasattr(df.columns, "levels"):
                df.columns = [c[0] for c in df.columns]

            result[pair_name] = df.tail(250)

            print(f"{pair_name} загружено: {len(df.tail(250))} свечей")

        except Exception as e:
            print(f"Ошибка {pair_name}: {e}")

    return result
