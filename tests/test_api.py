import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Titanic Survival Prediction"}


def test_predict_valid():
    """Test /predict with valid Titanic passenger data."""
    payload = {
        "Pclass": 3,
        "Sex": "male",
        "Age": 22.0,
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S",
        "FamilySize": 2,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert result["prediction"] in [0, 1]
    assert "probability" in result
    assert len(result["probability"]) == 2
    assert sum(result["probability"]) == pytest.approx(1.0, 0.01)
    assert "interpretation" in result
    assert result["interpretation"] in ["Survived", "Did not survive"]


def test_predict_valid_female():
    """Test /predict with likely survivor (female, first class)."""
    payload = {
        "Pclass": 1,
        "Sex": "female",
        "Age": 28.0,
        "SibSp": 1,
        "Parch": 1,
        "Fare": 82.17,
        "Embarked": "C",
        "FamilySize": 3,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert "probability" in result
    assert "interpretation" in result


def test_predict_invalid_input():
    """Test /predict with invalid data (negative Age)."""
    payload = {
        "Pclass": 3,
        "Sex": "male",
        "Age": -5.0,  # Invalid age
        "SibSp": 1,
        "Parch": 0,
        "Fare": 7.25,
        "Embarked": "S",
        "FamilySize": 2,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation)
