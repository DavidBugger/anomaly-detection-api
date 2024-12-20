from fastapi import FastAPI
from api import router

app = FastAPI(
    title="Anomaly Detection API",
    description="Detect anomalies in Active Directory logs",
    version="1.0.0"
)

# Include the API routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Anomaly Detection API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
