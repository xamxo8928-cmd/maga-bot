import time
from market import get_market_data
from strategy import check_signal
from telegram_bot import send_signal

last_signals = {}

def run_scheduler():
    while True:
        print("Проверяю рынок...")

        data = get_market_data()

        for pair, df in data.items():

            signal = check_signal(df)

            if signal is None:
                continue

            if last_signals.get(pair) != signal:

                last_signals[pair] = signal

                send_signal(
                    f"🚨 Сигнал\n\n"
                    f"Пара: {pair}\n"
                    f"Сигнал: {signal}\n"
                    f"Таймфрейм: M1"
                )

                print(pair, signal)

        time.sleep(60)
