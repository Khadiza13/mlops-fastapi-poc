from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import warnings
import sklearn

app = FastAPI(title="Titanic Survival Prediction API")


# Pydantic model for input data
class PredictionInput(BaseModel):
    Pclass: int = Field(ge=1, le=3)  # Class must be 1, 2, or 3
    Sex: str = Field(..., pattern="^(male|female)$")  # Must be "male" or "female"
    Age: float = Field(ge=0)  # Age must be non-negative
    SibSp: int = Field(ge=0)  # Siblings/Spouses aboard must be non-negative
    Parch: int = Field(ge=0)  # Parents/Children aboard must be non-negative
    Fare: float = Field(ge=0)  # Fare must be non-negative
    Embarked: str = Field(..., pattern="^(S|C|Q)$")  # Must be "S", "C", or "Q"
    FamilySize: int = Field(ge=1)  # Family size must be at least 1


# Load model with warning suppression
try:
    # Suppress sklearn version warnings during model loading
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
        model = joblib.load("data/model.pkl")
    print(f"Model loaded successfully with sklearn version {sklearn.__version__}")
except Exception as e:
    raise Exception(f"Failed to load model: {str(e)}")


@app.post("/predict")
async def predict(input_data: PredictionInput):
    try:
        # Convert input to DataFrame
        data = pd.DataFrame([input_data.model_dump()])

        # Preprocess: Encode Sex and Embarked to match training
        data["Sex"] = data["Sex"].map({"male": 1, "female": 0})
        data["Embarked"] = data["Embarked"].map({"S": 0, "C": 1, "Q": 2})

        # Predict with warning suppression
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
            prediction = model.predict(data)[0]
            probability = model.predict_proba(data)[0].tolist()

        return {
            "prediction": int(prediction),
            "probability": probability,
            "interpretation": "Survived" if prediction == 1 else "Did not survive",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Titanic Survival Prediction"}
