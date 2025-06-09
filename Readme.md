# MLOps FastAPI PoC – Titanic Dataset

### 📌 Overview

A proof-of-concept machine learning deployment using FastAPI, scikit-learn, and the Titanic dataset and also deploy to self hosted runner through CI/CD pipeline.

### 🧪 Dataset & EDA

- Dataset: [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic/data)
- EDA adapted from: [Data Science Solutions](https://www.kaggle.com/code/startupsci/titanic-data-science-solutions)

### 🛠 How to Run

```bash
# Install deps
pip install -r requirements.txt

# Train model
python train/train.py

# Run API
uvicorn app.main:app --reload
```
### ✅ Data Validation

- **Tool**: [Great Expectations](https://greatexpectations.io/)
- **Validation Script**: `src/validate_data.py` checks:
  - Existence of columns (`Age`, `Sex`, `Embarked`, `Survived`).
  - Value ranges (e.g., `Age` between 0 and 100).
  - Valid sets (e.g., `Embarked` in `["S", "C", "Q"]`, `Survived` in `[0, 1]`).
  - Non-null values for `Sex`.
- **Test Script**: `tests/test_data_quality.py` automates validation tests.
- **Run Validation**:
  ```bash
  python src/validate_data.py