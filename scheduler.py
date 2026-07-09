import time
from market import get_market_data
from strategy import check_signal
from telegram_bot import send_signal

last_signals = {}
last_signal_time = {}

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
                    f"🚨 НОВЫЙ СИГНАЛ\n\n"
                    f"💱 {pair}\n"
                    f"📈 Направление: {signal}\n"
                    f"⏱ Таймфрейм: M1\n"
                    f"⌛ Экспирация: 1 минута"
                )

                print(pair, signal)

        time.sleep(60)
