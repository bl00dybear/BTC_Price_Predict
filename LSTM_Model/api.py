import numpy as np
import tensorflow as tf
import pickle
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from fastapi import FastAPI


MODEL_PATH = '/home/sebi/BTC_Price_Predict/LSTM_Model/model/lstm_btc_model_30_2.h5'
SCALER_PATH = '/home/sebi/BTC_Price_Predict/LSTM_Model/model/scaler.pkl'

app = FastAPI()

# Încărcăm modelul antrenat
model = tf.keras.models.load_model(MODEL_PATH)

# Încărcăm scalerul folosit la antrenare (dacă e nevoie)
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

@app.get("/")
def read_root():
    return {"message": "API de predicție BTC activ!"}

@app.post("/predict/")
def predict(data: dict):
    try:
        # Date de intrare
        input_data = np.array(data["features"]).reshape(1, -1, len(data["features"][0]))

        # Facem predicția
        probability = model.predict(input_data)[0][0]

        return {"probability": float(probability)}

    except Exception as e:
        return {"error": str(e)}

# Pornire server FastAPI: uvicorn api:app --host 0.0.0.0 --port 8000
