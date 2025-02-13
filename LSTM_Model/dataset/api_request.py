import requests
from datetime import datetime
import re

from dataset_config import BINANCE_URL, SYMBOL, DAYS,LIMIT,MINUTES_PER_DAY

def get_binance_data(interval_,start_time=None):
    # print(interval_)
    params = {
        'symbol': SYMBOL,
        'interval': interval_,
        'limit': LIMIT,
        'startTime': start_time
    }
    if start_time:
        params['startTime'] = start_time

    response = requests.get(BINANCE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def extract_date_parts(date_str):
    try:
        day, month, year = date_str.split('_')
        return int(day), int(month), int(year)
    except ValueError:
        raise ValueError("Formatul stringului trebuie sa fie 'z_m_y', cu separatorul '_'")


def extract_minutes_from_string(input_str):
    match = re.match(r"(\d+)([mhd])", input_str)
    if match:
        value, unit = int(match.group(1)), match.group(2)
        if unit == 'm':
            return value
        elif unit == 'h':
            return value * 60
        elif unit == 'd':
            return value * 1440
    raise ValueError("Stringul trebuie sa contina un numar urmat de 'm', 'h' sau 'd'.")


def days_difference(date_str,custom_start_date):
    try:
        day, month, year = extract_date_parts(date_str)
        today_date = datetime.today()
        difference = today_date - custom_start_date
        return difference.days
    except ValueError as e:
        return str(e)



def fetch_full_binance_data(date_str, interval_str):
    all_data = []
    day, month, year = extract_date_parts(date_str)
    custom_start_date = datetime(int(year), int(month), int(day))
    start_time = int(custom_start_date.timestamp() * 1000)
    interval = extract_minutes_from_string(interval_str)
    total_candles = days_difference(date_str,custom_start_date) * (MINUTES_PER_DAY // interval)
    request_count = 0
    # request_limit = 12
    print(start_time)


    # !!!!!!!!!!!!!!!!!!trebuie sa compun api ul binance

    while len(all_data) < total_candles:
        data = get_binance_data(interval_str,start_time)
        if not data:
            break

        all_data.extend(data)
        start_time = data[-1][0] + 1
        request_count += 1

        print(f"Downloaded {len(all_data)} / {total_candles} candles...")

        # if request_count % request_limit == 0:
        #     print("Rate limit reached. Waiting for 60 seconds...")
            # time.sleep(60)
        # time.sleep(1)

    return all_data
