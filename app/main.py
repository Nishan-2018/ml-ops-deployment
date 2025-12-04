from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from typing import List

app = FastAPI(title="Iris Model API", description="A simple API to serve an Iris classification model.", version="1.0.0")

# Load model
MODEL_PATH = "model.joblib"
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        # In a real scenario, we might want to fail or train on startup.
        # For this demo, we'll just log a warning or handle it in the predict endpoint.
        print(f"Warning: Model file {MODEL_PATH} not found. Please run train.py first.")

class IrisInput(BaseModel):
    features: List[float]

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: IrisInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(data.features) != 4:
        raise HTTPException(status_code=400, detail="Expected 4 features")

    prediction = model.predict([data.features])
    return {"class": int(prediction[0])}
