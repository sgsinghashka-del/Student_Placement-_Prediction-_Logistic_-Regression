# model/train_model.py

import numpy as np
import pandas as pd
import joblib


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# ------------------------------
# Dataset Simulation
# ------------------------------
np.random.seed(42)
n_samples = 1000

data = pd.DataFrame({
    "CGPA": np.random.uniform(5.0, 10.0, n_samples),
    "Aptitude_Score": np.random.randint(40, 100, n_samples),
    "Technical_Projects": np.random.randint(0, 6, n_samples),
    "Internships": np.random.randint(0, 4, n_samples),
    "Mock_Interview_Score": np.random.uniform(50, 100, n_samples),
    "Placed": np.random.choice([0, 1], size=n_samples, p=[0.4, 0.6])
})

X = data.drop(columns=["Placed"])
y = data["Placed"]

X_train, _, y_train, _ = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ------------------------------
# Pipeline
# ------------------------------
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("log_reg", LogisticRegression(
        solver="liblinear",
        C=1.0,
        max_iter=1000
    ))
])

pipeline.fit(X_train, y_train)

# ------------------------------
# Save Versioned Model
# ------------------------------
joblib.dump(pipeline, "model/model_v1.pkl")

print("✅ Model v1 saved successfully")