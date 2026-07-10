import time

from market import get_market_data
from strategy import check_signal
from telegram_bot import send_signal
from database import (
    save_signal,
    get_unchecked,
    update_result
)
from cache import save_cache


last_signals = {}
last_signal_time = {}

CHECK_DELAY = 60
SIGNAL_COOLDOWN = 300


def check_results(data):

    signals = get_unchecked()

    for signal_id, pair, direction, entry_price in signals:

        if pair not in data:
            continue

        df = data[pair]

        current_price = round(
            float(df["Close"].iloc[-1]),
            5
        )

        result = "DRAW"


        if direction == "CALL":

            if current_price > entry_price:
                result = "WIN"

            elif current_price < entry_price:
                result = "LOSS"


        elif direction == "PUT":

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
            f"RESULT -> {pair} {direction} {result}"
        )



def run_scheduler():

    print("🚀 Scheduler запущен")


    while True:

        try:

            print("Проверяю рынок...")


            data = get_market_data()


            if not data:

                print("Нет данных рынка")
                time.sleep(CHECK_DELAY)
                continue


            # сохраняем свежие свечи
            save_cache(data)


            # проверяем старые сделки
            check_results(data)



            for pair, df in data.items():


                signal = check_signal(df)


                print(
                    f"{pair} -> {signal}"
                )


                if signal is None:
                    continue



                # защита от одинаковых сигналов
                if last_signals.get(pair) == signal:

                    continue



                now = time.time()


                if (
                    pair in last_signal_time
                    and now - last_signal_time[pair] < SIGNAL_COOLDOWN
                ):

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



                message = (
                    f"🚨 НОВЫЙ СИГНАЛ\n\n"
                    f"💱 {pair}\n"
                    f"📈 {signal}\n"
                    f"💰 Цена: {price}\n"
                    f"⏱ Таймфрейм: M1\n"
                    f"⌛ Экспирация: 1 минута"
                )


                send_signal(message)


                print(
                    f"SEND -> {pair} {signal}"
                )



        except Exception as e:

            print(
                f"Ошибка scheduler: {e}"
            )



        time.sleep(CHECK_DELAY)
