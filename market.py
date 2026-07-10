import os
import time
import requests
import pandas as pd

API_KEY = os.getenv("TWELVE_API_KEY")

PAIRS = {
    "EUR/USD": "EUR/USD",
    "GBP/USD": "GBP/USD",
    "USD/JPY": "USD/JPY",
    "AUD/USD": "AUD/USD",
    "USD/CAD": "USD/CAD",
    "USD/CHF": "USD/CHF",
    "NZD/USD": "NZD/USD",
}

last_data = {}


def get_market_data():

    global last_data

    result = {}

    for pair_name, symbol in PAIRS.items():

        print(f"Загружаю {pair_name}")

        try:

            response = requests.get(
                "https://api.twelvedata.com/time_series",
                params={
                    "symbol": symbol,
                    "interval": "1min",
                    "outputsize": 200,
                    "apikey": API_KEY,
                    "format": "JSON"
                },
                timeout=10
            )

            data = response.json()

            if "values" not in data:
                raise Exception(data)

            df = pd.DataFrame(data["values"])

            df = df.rename(columns={
                "datetime": "Datetime",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close"
            })

            df["Datetime"] = pd.to_datetime(df["Datetime"])
            df = df.set_index("Datetime")
            df = df.sort_index()

            for col in ["Open", "High", "Low", "Close"]:
                df[col] = df[col].astype(float)

            result[pair_name] = df
            last_data[pair_name] = df

            print(f"{pair_name}: {len(df)} свечей")

        except Exception as e:

            print(f"{pair_name}: ошибка API ({e}), беру старые данные")

            if pair_name in last_data:
                result[pair_name] = last_data[pair_name]

        time.sleep(1)

    return result
