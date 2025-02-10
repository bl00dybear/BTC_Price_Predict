import requests
from LSTM_Model.config import SYMBOL, INTERVAL, BINANCE_URL


def get_live_candle(start_time=None):
    params = {
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'limit': 1
    }

    response = requests.get(BINANCE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def aaa():
    data = get_live_candle()
