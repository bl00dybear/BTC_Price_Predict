import numpy as np
import tensorflow as tf
import pickle
from fastapi import FastAPI
from live_request import get_live_data
from api_config import MODEL_PATH, SCALER_PATH

app = FastAPI()

model = tf.keras.models.load_model(MODEL_PATH)
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

@app.get("/")
def read_root():
    return {"message": "API de predicție BTC activ!"}

@app.post("/predict/")
def predict():
    # print("A")
    live_data = get_live_data()
    if live_data is None or len(live_data) < 20:
        return {"error": "Nu s-au putut obține suficiente date live de la Binance."}


    input_sequence = np.array([
        [
            entry[0],  # Open
            entry[1],  # High
            entry[2],  # Low
            entry[3],  # Close
            entry[4],  # Volume
            entry[5],  # MA_5
            entry[6],  # MA_10
            entry[7],  # RSI
            entry[8],  # MACD
            entry[9],  # MACD_signal
            entry[10]  # MACD_hist
        ]
        for entry in live_data[-20:]
    ])
    try:
        input_data_scaled = scaler.transform(input_sequence)
        input_data_scaled = input_data_scaled.reshape(1, 20, input_data_scaled.shape[1])  # LSTM format

        probability = model.predict(input_data_scaled)[0][0]
        return {"probability": float(probability)}

    except Exception as e:
        return {"error": str(e)}
