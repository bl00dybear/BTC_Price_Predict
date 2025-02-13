import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from model_config import SCALER_PATH

def load_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['Timestamp'])
    df.sort_values(by='Timestamp', inplace=True)
    return df


def preprocess_data(df,interval,date, window_size=20, h=1):
    scaler = MinMaxScaler()
    feature_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'MA_5', 'MA_10', 'RSI', 'MACD', 'MACD_signal',
                       'MACD_hist']
    scaled_features = scaler.fit_transform(df[feature_columns])

    df['target'] = (df['Close'].shift(-h) / df['Close'] - 1) >= 0.01
    df['target'] = df['target'].astype(int)

    x, y = [], []
    for i in range(len(scaled_features) - window_size - h):
        x.append(scaled_features[i:i + window_size])
        y.append(df['target'].iloc[i + window_size])

    scaler_path = SCALER_PATH + interval+'_'+date+'_'+str(window_size)+'wsize.pkl'

    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)

    return np.array(x), np.array(y), scaler


def split_data(X, y, test_size=0.2):
    return train_test_split(X, y, test_size=test_size, shuffle=False)