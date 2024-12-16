from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import numpy as np
import tensorflow as tf
import uvicorn

app = FastAPI(title="Extreme Weather Management System",
             description="API for weather risk assessment and prediction")

# Load the trained model (placeholder)
model = None

class WeatherData(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float
    pressure: float
    location: dict

class RiskAssessment(BaseModel):
    risk_level: str
    confidence: float
    recommendations: list
    timestamp: datetime

def load_model():
    """Load the trained model"""
    global model
    try:
        model = tf.keras.models.load_model('models/weather_risk_model.h5')
    except:
        print("Warning: Model not found. Using dummy predictions.")

def preprocess_data(data: WeatherData):
    """Preprocess weather data for model input"""
    return np.array([[
        data.temperature,
        data.humidity,
        data.wind_speed,
        data.precipitation,
        data.pressure
    ]])

def get_risk_level(prediction: float) -> str:
    """Convert model prediction to risk level"""
    if prediction < 0.3:
        return "Low"
    elif prediction < 0.7:
        return "Medium"
    else:
        return "High"

def get_recommendations(risk_level: str) -> list:
    """Get recommendations based on risk level"""
    recommendations = {
        "Low": ["Monitor weather conditions", "No immediate action required"],
        "Medium": ["Alert local authorities", "Prepare emergency resources"],
        "High": ["Evacuate risk areas", "Deploy emergency response teams", "Activate crisis protocols"]
    }
    return recommendations.get(risk_level, [])

@app.get("/")
async def root():
    return {"message": "Welcome to Extreme Weather Management System API"}

@app.post("/predict", response_model=RiskAssessment)
async def predict_risk(data: WeatherData):
    try:
        # Preprocess input data
        processed_data = preprocess_data(data)
        
        # Make prediction (dummy prediction if model not loaded)
        if model is None:
            prediction = np.random.random()
        else:
            prediction = model.predict(processed_data)[0][0]
        
        # Get risk level and recommendations
        risk_level = get_risk_level(prediction)
        recommendations = get_recommendations(risk_level)
        
        return RiskAssessment(
            risk_level=risk_level,
            confidence=float(prediction),
            recommendations=recommendations,
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    load_model()
    uvicorn.run(app, host="0.0.0.0", port=8000)
