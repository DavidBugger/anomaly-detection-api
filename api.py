from fastapi import APIRouter, HTTPException
import requests
from config import Config
from model import predict_anomaly
from log_fetcher import fetch_logs, fetch_sign_in_logs, get_access_token

# Create a class to manage prediction state
class PredictionManager:
    _instance = None
    last_prediction_result = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(PredictionManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_last_prediction(cls, result):
        cls.last_prediction_result = result

    @classmethod
    def get_last_prediction(cls):
        return cls.last_prediction_result

# Create a singleton instance
prediction_manager = PredictionManager()

router = APIRouter()

@router.post("/predict")
async def predict(data: dict):
    try:
        result = predict_anomaly(data)
        # Store the prediction result
        prediction_manager.set_last_prediction(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get-access-token")
async def get_token():
    """API endpoint to fetch an access token."""
    try:
        token = get_access_token()
        return {"access_token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fetch-logs")
async def fetch_sign_in_logs():
    """API endpoint to fetch sign-in logs."""
    try:
        token = get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(Config.GRAPH_API_URL, headers=headers)
        response.raise_for_status()
        return {"logs": response.json().get("value", [])}
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/get_status')
async def get_status():
    """
    Get the status of the last anomaly detection prediction.
    """
    last_prediction_result = prediction_manager.get_last_prediction()
    
    if last_prediction_result is None:
        raise HTTPException(status_code=400, detail="No previous prediction available")
    
    return {
        "is_anomaly": last_prediction_result['is_anomaly'],
        "message": last_prediction_result['message']
    }