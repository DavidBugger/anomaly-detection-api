import numpy as np
from tensorflow.keras.models import load_model
from preprocess import preprocess


# Global variable to store the last prediction result
last_prediction_result = None
# Load the trained model
model = load_model("anomaly_detection_model.h5")


# def predict_anomaly(data):
#     # Preprocess the input data
#     username = data.get('username')
#     preprocessed_data = preprocess(data)
#     # Get the prediction from the model
#     prediction = model.predict(preprocessed_data)
#     # Extract the probability of anomaly
#     probability = float(prediction[0][0])
#     # Determine if it is an anomaly
#     is_anomaly = probability > 0.58  # Compare probability directly
#     # Return the result
#     if is_anomaly:
#         return {'is_anomaly': False, 'username': username, 'message': f'No Anomaly in login activity for {username}'}
#     else:
#         return {'is_anomaly': True, 'username': username, 'message': f'Anomaly  in login activity for {username}'}

def predict_anomaly(data):
    # Ensure all required features are present
    required_features = ['username', 'user_type', 'ip_address', 'operating_system', 'browser']
    for feature in required_features:
        if feature not in data:
            raise ValueError(f"Missing or invalid feature: {feature}")
    
    # Preprocess the input data
    username = data.get('username')
    preprocessed_data = preprocess(data)
    
    # Get the prediction from the model
    prediction = model.predict(preprocessed_data)
    
    # Extract the probability of anomaly
    probability = float(prediction[0][0])
    
    # Determine if it is an anomaly
    is_anomaly = probability <= 0.58  # Corrected comparison
    
    # Create result dictionary
    result = {
        'is_anomaly': is_anomaly, 
        'username': username, 
        'message': f'{"Anomaly" if is_anomaly else "No Anomaly"} in login activity for {username}'
    }
    
    # Store the result globally
    global last_prediction_result
    last_prediction_result = result
    
    return result


