import pandas as pd


def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def rsi(series, period=14):

    delta = series.diff()

    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss

    return 100 - (100 / (1 + rs))


def atr(df, period=14):

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    return tr.rolling(period).mean()


def check_signal(df):

    if len(df) < 200:
        return None

    close = df["Close"]

    ema20 = ema(close, 20)
    ema50 = ema(close, 50)
    ema200 = ema(close, 200)

    rsi14 = rsi(close, 14)
    atr14 = atr(df, 14)

    last = len(df) - 1

    # фильтр слабого рынка
    if atr14.iloc[last] < 0.0005:
        return None

    # CALL
    if (
        ema20.iloc[last] > ema50.iloc[last] > ema200.iloc[last]
        and close.iloc[last] > ema20.iloc[last]
        and rsi14.iloc[last] > 60
    ):
        return "CALL"

    # PUT
    if (
        ema20.iloc[last] < ema50.iloc[last] < ema200.iloc[last]
        and close.iloc[last] < ema20.iloc[last]
        and rsi14.iloc[last] < 40
    ):
        return "PUT"

    return None
