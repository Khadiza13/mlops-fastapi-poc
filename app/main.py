from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import Optional

app = FastAPI(title="Titanic Survival Prediction API")

# Pydantic model for input data
class PredictionInput(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str
    FamilySize: int  # Added to match training script

# Load model
try:
    model = joblib.load('data/model.pkl')
except Exception as e:
    raise Exception(f"Failed to load model: {str(e)}")

@app.post("/predict")
async def predict(input_data: PredictionInput):
    try:
        # Convert input to DataFrame
        data = pd.DataFrame([input_data.dict()])
        
        # Preprocess: Encode Sex and Embarked to match training
        data['Sex'] = data['Sex'].map({'male': 1, 'female': 0})
        data['Embarked'] = data['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})
        
        # Predict
        prediction = model.predict(data)[0]
        probability = model.predict_proba(data)[0].tolist()
        
        return {
            "prediction": int(prediction),
            "probability": probability,
            "interpretation": "Survived" if prediction == 1 else "Did not survive"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Titanic Survival Prediction API. Use POST /predict with Pclass, Sex, Age, SibSp, Parch, Fare, Embarked, FamilySize."}