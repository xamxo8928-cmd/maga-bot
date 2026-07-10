import os
import time
import pandas as pd
from twelvedata import TDClient


API_KEY = os.getenv("TWELVE_API_KEY")

td = TDClient(apikey=API_KEY)


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

            df = (
                td.time_series(
                    symbol=symbol,
                    interval="1min",
                    outputsize=200
                )
                .as_pandas()
            )


            df = df.sort_index()


            df = df.rename(
                columns={
                    "open": "Open",
                    "high": "High",
                    "low": "Low",
                    "close": "Close",
                    "volume": "Volume"
                }
            )


            df = df.astype(float)


            result[pair_name] = df

            last_data[pair_name] = df


            print(
                f"{pair_name}: {len(df)} свечей"
            )


        except Exception as e:

            print(
                f"{pair_name}: ошибка API, беру старые данные"
            )

            if pair_name in last_data:
                result[pair_name] = last_data[pair_name]


        time.sleep(8)


    return result
