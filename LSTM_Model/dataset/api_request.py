import requests
import time
import datetime
from config import BINANCE_URL, SYMBOL, INTERVAL, LIMIT, DAYS

def get_binance_data(start_time=None):
    params = {
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'limit': LIMIT
    }
    if start_time:
        params['startTime'] = start_time

    response = requests.get(BINANCE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def fetch_full_binance_data():
    all_data = []
    custom_start_date = datetime.datetime(2018, 1, 1)
    start_time = int(custom_start_date.timestamp() * 1000)
    total_candles = DAYS * 48
    request_count = 0
    request_limit = 12

    while len(all_data) < total_candles:
        data = get_binance_data(start_time)
        if not data:
            break

        all_data.extend(data)
        start_time = data[-1][0] + 1
        request_count += 1

        print(f"Downloaded {len(all_data)} / {total_candles} candles...")

        if request_count % request_limit == 0:
            print("Rate limit reached. Waiting for 60 seconds...")
            # time.sleep(60)
        time.sleep(1)

    return all_data
