import numpy as np
from tensorflow.keras.models import load_model
from preprocess import preprocess

# Load the trained model
model = load_model("anomaly_detection_model.h5")

def predict_anomaly(data):
    preprocessed_data = preprocess(data)
    prediction = model.predict(preprocessed_data)
    is_anomaly = bool(prediction[0][0] > 0.5)
    probability = float(prediction[0][0])
    return {
        "is_anomaly": is_anomaly,
        "probability": probability,
        "message": "Anomaly detection result"
    }
