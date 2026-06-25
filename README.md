**🎓 Student Placement Prediction System (ML + FastAPI)**
**📌 Project Overview**

This project is an end-to-end Machine Learning system that predicts the probability of a student getting placed based on academic and skill-based features.

The focus of this project is production-ready ML system design, not just model accuracy.
It demonstrates how an ML model can be trained, versioned, served via API, monitored, and consumed by a UI.

**🎯 Problem Statement**

Educational institutions and training programs often need data-driven insights to assess student placement readiness.

This system predicts placement likelihood using:

Academic performance
Aptitude scores
Practical exposure
Interview readiness

**🧠 Model Details**
Algorithm: Logistic Regression
Why Logistic Regression?
Interpretable coefficients
Probabilistic output
Fast inference
Suitable for binary classification
Target Variable: Placed (1 = Placed, 0 = Not Placed)

**📊 Input Features**
Feature	Description
CGPA	Academic performance
Aptitude_Score	Logical & aptitude test score
Technical_Projects	Number of technical projects
Internships	Internship experience
Mock_Interview_Score	Interview readiness score

**🏗️ System Architecture**
User
 ↓
Streamlit UI
 ↓
FastAPI Backend
 ├── /predict
 ├── /metrics
 ├── /explain
 ↓
Logistic Regression Model (versioned)
 ↓
Logs & Metrics

**⚙️ Tech Stack**
Python
Scikit-learn – ML modeling
FastAPI – Backend API
Streamlit – UI
Joblib – Model persistence
Logging – Request & latency tracking

**📁 Project Structure**
Student_Placement_Logistic_ML/
│
├── app/
│   └── main.py              # FastAPI backend
│
├── model/
│   └── train_model.py       # Model training script
│   └── model_v1.pkl         # Versioned model
│
├── ui/
│   └── streamlit_app.py     # Frontend UI
│
├── logs/
│   └── api.log              # Request logs
│
├── requirements.txt
└── README.md

**🚀 API Endpoints**
🔹 Health Check
GET /

Response:

{
  "status": "running",
  "model_version": "v1",
  "threshold": 0.6
}

**🔹 Prediction**
POST /predict

Request:

{
  "CGPA": 8.2,
  "Aptitude_Score": 78,
  "Technical_Projects": 3,
  "Internships": 1,
  "Mock_Interview_Score": 75
}

Response:

{
  "model_version": "v1",
  "placement_probability": 0.72,
  "placed_prediction": 1,
  "threshold_used": 0.6
}


**🔹 Explainability**
POST /explain

Returns feature importance based on model coefficients.

**🔹 Metrics**
GET /metrics

Tracks:

Total requests
Average latency
Model version

**🧪 How to Run Locally**
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Train model
python model/train_model.py
3️⃣ Run backend
uvicorn app.main:app --reload
4️⃣ Run UI
streamlit run ui/streamlit_app.py

**🔧 Configuration**

Prediction threshold is configurable via the environment variable:

set PREDICTION_THRESHOLD=0.6   # Windows

**📈 Key Engineering Highlights**

✔ End-to-end ML system
✔ Model versioning
✔ Configurable decision threshold
✔ Request logging
✔ Performance metrics
✔ Explainability endpoint
✔ UI consuming backend API

**🧠 Interview Talking Points**

Designed a production-ready ML inference service
Focused on system reliability, observability, and interpretability
Deployment-ready architecture (Docker/cloud can be added)

**🔮 Future Enhancements**
Dockerization
Cloud deployment (AWS / Render)
Authentication & rate limiting
Model retraining automation
Drift monitoring
