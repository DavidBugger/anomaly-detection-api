from fastapi import APIRouter, HTTPException
import requests
from config import Config
from model import predict_anomaly
from log_fetcher import fetch_logs, fetch_sign_in_logs, get_access_token

router = APIRouter()

@router.post("/predict")
async def predict(data: dict):
    try:
        result = predict_anomaly(data)
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
    

