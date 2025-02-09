from api_request import fetch_full_binance_data
from data_processing import convert_binance_data, add_technical_indicators
from save_data import save_to_csv

def create_dataset():
    raw_data = fetch_full_binance_data()
    if not raw_data:
        print("Error fetching data.")
        return

    df = convert_binance_data(raw_data)
    df = add_technical_indicators(df)
    save_to_csv(df, "bitcoin_binance_30min_180days.csv")

if __name__ == "__main__":
    create_dataset()
