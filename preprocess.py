from joblib import load
import numpy as np

# Load encoders and scaler
encoders = load("label_encoders.joblib")
scaler = load("feature_scaler.joblib")

def preprocess(data):
    categorical_features = ["user_type", "ip_address", "username", "browser", "operating_system"]
    encoded_features = []

    for feature in categorical_features:
        if feature in data and feature in encoders:
            encoder = encoders[feature]
            encoded_features.append(encoder.transform([data[feature]])[0])
        else:
            raise ValueError(f"Missing or invalid feature: {feature}")

    # Scale features
    scaled_features = scaler.transform([encoded_features])
    return scaled_features
