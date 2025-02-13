from preprocess_data import *
from build_model import *
from train_model import *
from evaluate_model import *
from predict import *
from model_config import CSV_PATH


interval = input("Interval: ")
date = input("Date: ")
window_size = int(input("Window size: "))

dataset_path = CSV_PATH + interval + '_' + date + ".csv"
# print(name)
df = load_data(dataset_path)
# print(df)
# X, y, scaler = preprocess_data(df)
# X_train, X_test, y_train, y_test = split_data(X, y)
#
# model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))
# train_model(model, X_train, y_train, X_test, y_test)
#
# accuracy = evaluate_model(model, X_test, y_test)
# print(f'Accuracy: {accuracy:.2f}')
#
# probability = predict_probability(model, X_test[-1])
# print(X_test[-1])
# print(f'Probabilitatea creșterii BTC cu 2%: {probability:.2f}')