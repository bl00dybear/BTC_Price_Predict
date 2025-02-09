import pandas as pd
import pandas_ta as ta

def convert_binance_data(data):
    df = pd.DataFrame(data, columns=[
        'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close_time', 'Quote_asset_volume', 'Trades',
        'Taker_base_volume', 'Taker_quote_volume', 'Ignore'
    ])
    df = df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)
    return df

def add_technical_indicators(df):
    df.ta.rsi(length=14, append=True)
    df.ta.sma(length=5, append=True)
    df.ta.sma(length=10, append=True)
    df.ta.macd(fast=12, slow=26, signal=9, append=True)

    df.rename(columns={
        'SMA_5': 'MA_5',
        'SMA_10': 'MA_10',
        'RSI_14': 'RSI',
        'MACD_12_26_9': 'MACD',
        'MACDh_12_26_9': 'MACD_hist',
        'MACDs_12_26_9': 'MACD_signal'
    }, inplace=True)

    return df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'MA_5', 'MA_10', 'RSI', 'MACD', 'MACD_signal', 'MACD_hist']]
