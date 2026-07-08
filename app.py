from flask import Flask, request
import requests
import os
from market import get_market_data

app = Flask(__name__)

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

    # TradingView отправляет текст
    message = data.get("message", "No signal")

    send_telegram(message)

    return "ok", 200
@app.route("/prices")
def prices():
    return get_market_data()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
