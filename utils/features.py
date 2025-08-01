import yfinance as yf
import pandas as pd
import ta

def load_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    df = df.dropna()
    return df

def create_features(df):
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()
    # dll...
    return df.dropna()
