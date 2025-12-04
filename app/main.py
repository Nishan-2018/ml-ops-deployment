from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from typing import List

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        print(f"Warning: Model file {MODEL_PATH} not found. Please run train.py first.")
    yield

app = FastAPI(title="Iris Model API", description="A simple API to serve an Iris classification model.", version="1.0.0", lifespan=lifespan)

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
