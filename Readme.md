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
