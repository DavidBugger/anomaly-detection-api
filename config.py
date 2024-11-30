import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    TENANT_ID = os.getenv("TENANT_ID")
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    GRAPH_API_URL = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
    MODEL_PATH = "anomaly_detection_model.h5"
    SCALER_PATH = "feature_scaler.joblib"
    ENCODER_PATH = "label_encoders.joblib"
    MS_GRAPH_API_TOKEN = os.getenv("MS_GRAPH_API_TOKEN")
