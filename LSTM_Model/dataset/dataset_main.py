from api_request import fetch_full_binance_data
from data_processing import convert_binance_data, add_technical_indicators
from save_data import save_to_csv

def create_dataset(interval_str, date_str):
    # print(f"datasets/bitcoin_binance_{timestamp_}_{date_}.csv")
    raw_data = fetch_full_binance_data(date_str, interval_str)
    if not raw_data:
        print("Error fetching data.")
        return

    df = convert_binance_data(raw_data)
    df = add_technical_indicators(df)
    save_to_csv(df, f"datasets/bitcoin_binance_{interval_str}_{date_str}.csv")

if __name__ == "__main__":

    timestamp = input("Interval: ")
    date = input("Date: ")
    print(timestamp, date)
    create_dataset(timestamp, date)

