from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import Model, MODEL_VERSION
from schema.prediction_response import PredictionResponse
from pydantic import BaseModel
import pandas as pd
app = FastAPI()

 
@app.get("/health")
def health():
    return JSONResponse(status_code=200, content={
        "status":"ok",
        "message": "The API is healthy!",
        "model_loaded": True,
        "model_version": MODEL_VERSION,
        }) 

@app.get("/")
def home():
    return JSONResponse(status_code=200, content={"status":"ok","message": "Welcome to the Insurance Premium Prediction API!"}) 

@app.post('/predict', response_model = PredictionResponse)
def predict_premium(data: UserInput):
    model = Model()
    prediction = model.predict(data)
    return JSONResponse(status_code=200, content={'response': prediction})
