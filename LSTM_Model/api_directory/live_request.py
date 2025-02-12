import requests
import pandas as pd
import pandas_ta as ta
from api_config import SYMBOL, INTERVAL, BINANCE_URL, WINDOW_SIZE


def get_live_candles():
    params = {
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'limit': WINDOW_SIZE + 40
    }

    try:
        response = requests.get(BINANCE_URL, params=params)
        response.raise_for_status()

        kline_data = response.json()

        df = pd.DataFrame(kline_data, columns=[
            'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close_time', 'Quote_asset_volume', 'Trades',
            'Taker_base_volume', 'Taker_quote_volume', 'Ignore'
        ])
        df = df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
        df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
        print(df)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching live candle data: {e}")
        return None


def add_technical_indicators(df):
    df = df.copy()

    df.ta.sma(length=5, append=True)
    df.ta.sma(length=10, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.macd(fast=12, slow=26, signal=9, append=True)

    df.rename(columns={
        'SMA_5': 'MA_5',
        'SMA_10': 'MA_10',
        'RSI_14': 'RSI',
        'MACD_12_26_9': 'MACD',
        'MACDh_12_26_9': 'MACD_hist',
        'MACDs_12_26_9': 'MACD_signal'
    }, inplace=True)

    return df


def get_live_data():
    df = get_live_candles()
    if df is None or len(df) < WINDOW_SIZE + 40:
        print("Not enough live data retrieved.")
        return None

    df = add_technical_indicators(df)
    df.dropna(inplace=True)

    if len(df) < WINDOW_SIZE:
        print("Not enough valid data points after computing indicators.")
        return None

    return df[['Open', 'High', 'Low', 'Close', 'Volume', 'MA_5', 'MA_10', 'RSI', 'MACD', 'MACD_signal', 'MACD_hist']].tail(WINDOW_SIZE).to_numpy()
