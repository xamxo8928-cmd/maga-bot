import time
import yfinance as yf


PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
}

last_data = {}


def get_market_data():

    print("MARKET VERSION YAHOO")

    global last_data

    result = {}

    for pair_name, symbol in PAIRS.items():

        print(f"Загружаю {pair_name}")

        try:

            df = yf.download(
                symbol,
                period="1d",
                interval="1m",
                progress=False,
                auto_adjust=False,
                threads=False
            )

            if df.empty:
                raise Exception("Нет данных")

            try:
                df.columns = df.columns.droplevel(1)
            except Exception:
                pass

            df = df[["Open", "High", "Low", "Close"]].astype(float)

            result[pair_name] = df
            last_data[pair_name] = df

            print(f"{pair_name}: {len(df)} свечей")

        except Exception as e:

            print(f"{pair_name}: ошибка ({e}), беру старые данные")

            if pair_name in last_data:
                result[pair_name] = last_data[pair_name]

        time.sleep(3)

    return result
