import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Ensure directories exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# Verify and load data
data_path = "data/raw/train.csv"
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit(1)

# Load and preprocess
try:
    df = pd.read_csv(data_path)
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Fill missing values
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# Drop irrelevant columns
df = df.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1)

# Encode categorical variables
le_sex = LabelEncoder()
df["Sex"] = le_sex.fit_transform(df["Sex"])
le_embarked = LabelEncoder()
df["Embarked"] = le_embarked.fit_transform(df["Embarked"])

# Create FamilySize feature (EDA: combine SibSp and Parch)
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

# Drop rows with any remaining missing values
df = df.dropna()

# Save processed data
processed_path = "data/processed/train_processed.csv"
df.to_csv(processed_path, index=False)
print(f"Processed data saved to {processed_path}")

# Features and target
X = df.drop("Survived", axis=1)
y = df["Survived"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.2f}")
print(f"Features used for training: {list(X.columns)}")

# Save model
model_path = "data/model.pkl"
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
