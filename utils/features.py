import pandas as pd
import ta

def create_features(df):
    df = df.copy()

    # Pastikan kolom 'Close' ada dan bertipe Series
    if "Close" not in df.columns:
        raise ValueError("Data harus memiliki kolom 'Close'")

    # Indikator teknikal
    close = df["Close"]

    df["RSI"] = ta.momentum.RSIIndicator(close=close).rsi()
    df["SMA_20"] = ta.trend.SMAIndicator(close=close, window=20).sma_indicator()
    df["EMA_20"] = ta.trend.EMAIndicator(close=close, window=20).ema_indicator()
    df["MACD"] = ta.trend.MACD(close=close).macd()

    # Buang baris awal yang kosong karena rolling window
    df.dropna(inplace=True)

    return df
