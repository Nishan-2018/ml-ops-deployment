from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from typing import List
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load model
MODEL_PATH = "model.joblib"
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        print(f"Warning: Model file {MODEL_PATH} not found. Please run train.py first.")
    yield

app = FastAPI(title="House Price Predictor API", description="API to predict house prices based on key features.", version="1.0.0", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('app/static/index.html')

class HouseInput(BaseModel):
    med_inc: float
    house_age: float
    ave_rooms: float
    population: float

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: HouseInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Prepare features in the correct order: ['MedInc', 'HouseAge', 'AveRooms', 'Population']
    features = [[data.med_inc, data.house_age, data.ave_rooms, data.population]]
    
    prediction = model.predict(features)
    
    # The target in California Housing is in units of 100,000.
    # So we multiply by 100,000 to get the actual price.
    predicted_price = prediction[0] * 100000
    
    return {"price": round(predicted_price, 2)}
