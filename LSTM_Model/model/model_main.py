# from LSTM_Model.config import CSV_PATH
from preprocess_data import *
from build_model import *
from train_model import *
from evaluate_model import *
from predict import *

CSV_PATH = '/home/sebi/BTC_Price_Predict/LSTM_Model/dataset/bitcoin_binance_30min_1_1_2018.csv'


df = load_data(CSV_PATH)
X, y, scaler = preprocess_data(df)
X_train, X_test, y_train, y_test = split_data(X, y)

model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))
train_model(model, X_train, y_train, X_test, y_test)

accuracy = evaluate_model(model, X_test, y_test)
print(f'Accuracy: {accuracy:.2f}')

probability = predict_probability(model, X_test[-1])
print(f'Probabilitatea creșterii BTC cu 2%: {probability:.2f}')