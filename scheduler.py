import time
from market import get_market_data
from strategy import check_signal
from telegram_bot import send_signal
from database import save_signal, get_unchecked, update_result

last_signals = {}
last_signal_time = {}

CHECK_DELAY = 60

def check_results(data):

    signals = get_unchecked()

    for signal_id, pair, direction, entry_price in signals:

        if pair not in data:
            continue

        df = data[pair]

        current_price = round(float(df["Close"].iloc[-1]), 5)

        result = "DRAW"

        if direction == "CALL":

            if current_price > entry_price:
                result = "WIN"

            elif current_price < entry_price:
                result = "LOSS"

        if direction == "PUT":

            if current_price < entry_price:
                result = "WIN"

            elif current_price > entry_price:
                result = "LOSS"

        update_result(
            signal_id,
            current_price,
            result
        )

        print(
            pair,
            direction,
            result
        )

def run_scheduler():

    while True:

        print("Проверяю рынок...")

        data = get_market_data()

        # Проверяем старые сигналы
        check_results(data)

        # Ищем новые сигналы
        for pair, df in data.items():

            signal = check_signal(df)

            if signal is None:
                continue

            if last_signals.get(pair) != signal:

                now = time.time()

                if pair in last_signal_time and now - last_signal_time[pair] < 300:
                    continue

                last_signals[pair] = signal
                last_signal_time[pair] = now

                price = round(
                    float(df["Close"].iloc[-1]),
                    5
                )

                save_signal(
                    pair,
                    signal,
                    price
                )

                send_signal(
                    f"🚨 НОВЫЙ СИГНАЛ\n\n"
                    f"💱 {pair}\n"
                    f"📈 Направление: {signal}\n"
                    f"💰 Цена: {price}\n"
                    f"⏱ Таймфрейм: M1\n"
                    f"⌛ Экспирация: 1 минута"
                )

                print(
                    pair,
                    signal
                )

        time.sleep(CHECK_DELAY)
