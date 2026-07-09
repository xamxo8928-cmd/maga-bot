import pandas as pd

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss

    return 100 - (100 / (1 + rs))

def check_signal(df_m1, df_m5=None):

    close = df_m1["Close"]

    ema20 = ema(close, 20)
    ema50 = ema(close, 50)
    ema200 = ema(close, 200)

    rsi14 = rsi(close, 14)

    last = len(df_m1) - 1

    trend_ok = True

    if df_m5 is not None:
        close5 = df_m5["Close"]
        ema20_5 = ema(close5, 20)
        ema50_5 = ema(close5, 50)

        trend_ok = ema20_5.iloc[-1] > ema50_5.iloc[-1]

    if (
        ema20.iloc[last] > ema50.iloc[last] > ema200.iloc[last]
        and close.iloc[last] > ema20.iloc[last]
        and rsi14.iloc[last] > 60
        and trend_ok
    ):
        return "CALL"

    trend_ok = True

    if df_m5 is not None:
        trend_ok = ema20_5.iloc[-1] < ema50_5.iloc[-1]

    if (
        ema20.iloc[last] < ema50.iloc[last] < ema200.iloc[last]
        and close.iloc[last] < ema20.iloc[last]
        and rsi14.iloc[last] < 40
        and trend_ok
    ):
        return "PUT"

    return None
