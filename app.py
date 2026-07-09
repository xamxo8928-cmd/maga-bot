from flask import Flask, request
import requests
import os

from threading import Thread

from cache import market_cache
from strategy import check_signal
from telegram_bot import send_signal
from scheduler import run_scheduler
from database import init_db

app = Flask(__name__)

init_db()

thread = Thread(target=run_scheduler)
thread.daemon = True
thread.start()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    requests.post(url, data=payload)


@app.route("/")
def home():
    return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if not data:
        return "no data", 400

    message = data.get("message", "No signal")

    send_telegram(message)

    return "ok", 200


@app.route("/signal")
def signal():

    result = {}

    for pair, df in market_cache.items():

        sig = check_signal(df)

        result[pair] = sig if sig else "WAIT"

    return result


@app.route("/prices")
def prices():

    result = {}

    for pair, df in market_cache.items():

        result[pair] = {
            "close": round(float(df["Close"].iloc[-1]), 5),
            "candles": len(df)
        }

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
