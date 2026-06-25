from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import logging
import time
import os
from datetime import datetime

# =============================
# Environment Configuration
# =============================
MODEL_VERSION = "v1"
THRESHOLD = float(os.getenv("PREDICTION_THRESHOLD", 0.6))

# =============================
# Logging Configuration
# =============================
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/api.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =============================
# Load Model
# =============================
model = joblib.load("model/model_v1.pkl")

# =============================
# FastAPI App
# =============================
app = FastAPI(
    title="Student Placement Prediction API",
    description="Production-grade ML API using Logistic Regression",
    version=MODEL_VERSION
)

# =============================
# Metrics
# =============================
REQUEST_COUNT = 0
TOTAL_LATENCY = 0.0

# =============================
# Request Schema
# =============================
class StudentInput(BaseModel):
    CGPA: float
    Aptitude_Score: int
    Technical_Projects: int
    Internships: int
    Mock_Interview_Score: float

# =============================
# Health Check
# =============================
@app.get("/")
def health_check():
    return {
        "status": "running",
        "model_version": MODEL_VERSION,
        "threshold": THRESHOLD
    }

# =============================
# Prediction Endpoint
# =============================
@app.post("/predict")
def predict(data: StudentInput):
    global REQUEST_COUNT, TOTAL_LATENCY

    start_time = time.time()
    REQUEST_COUNT += 1

    features = [[
        data.CGPA,
        data.Aptitude_Score,
        data.Technical_Projects,
        data.Internships,
        data.Mock_Interview_Score
    ]]

    probability = model.predict_proba(features)[0][1]
    prediction = int(probability >= THRESHOLD)

    latency = time.time() - start_time
    TOTAL_LATENCY += latency

    logging.info(
        f"INPUT={data.dict()} | PROB={probability:.3f} | "
        f"PRED={prediction} | LATENCY={latency:.4f}s"
    )

    return {
        "model_version": MODEL_VERSION,
        "placement_probability": round(probability, 3),
        "placed_prediction": prediction,
        "threshold_used": THRESHOLD
    }

# =============================
# Explainability Endpoint
# =============================
@app.post("/explain")
def explain(data: StudentInput):
    coefficients = model.named_steps["log_reg"].coef_[0]

    return {
        "model_version": MODEL_VERSION,
        "feature_importance": {
            "CGPA": round(coefficients[0], 3),
            "Aptitude_Score": round(coefficients[1], 3),
            "Technical_Projects": round(coefficients[2], 3),
            "Internships": round(coefficients[3], 3),
            "Mock_Interview_Score": round(coefficients[4], 3)
        }
    }

# =============================
# Metrics Endpoint
# =============================
@app.get("/metrics")
def metrics():
    avg_latency = TOTAL_LATENCY / REQUEST_COUNT if REQUEST_COUNT else 0

    return {
        "total_requests": REQUEST_COUNT,
        "average_latency_seconds": round(avg_latency, 4),
        "model_version": MODEL_VERSION
    }