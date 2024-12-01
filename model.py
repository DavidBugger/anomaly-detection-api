import numpy as np
from tensorflow.keras.models import load_model
from preprocess import preprocess

# Load the trained model
model = load_model("anomaly_detection_model.h5")


def predict_anomaly(data):
    # Preprocess the input data
    username = data.get('username')
    preprocessed_data = preprocess(data)
    # Get the prediction from the model
    prediction = model.predict(preprocessed_data)
    # Extract the probability of anomaly
    probability = float(prediction[0][0])
    # Determine if it is an anomaly
    is_anomaly = probability > 0.58  # Compare probability directly
    # Return the result
    if is_anomaly:
        return {'is_anomaly': False, 'username': username, 'message': f'NoAnomaly in login activity for {username}'}
    else:
        return {'is_anomaly': True, 'username': username, 'message': f'Anomaly  in login activity for {username}'}

