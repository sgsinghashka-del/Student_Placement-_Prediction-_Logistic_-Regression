# 🎓 Student Placement Prediction

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/Model-Logistic%20Regression-8B5CF6)](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

An end-to-end machine-learning application that estimates a student's placement probability from academic performance, practical experience, and interview-readiness signals. The project combines a scikit-learn model, a FastAPI inference service, and a Streamlit user interface.

> **Project preview** — the following screenshot is a generated UI preview of the Streamlit application.

![Student Placement Prediction dashboard preview](docs/project-preview.svg)

## ✨ Highlights

- **Probabilistic predictions** with Logistic Regression.
- **Five input signals:** CGPA, aptitude score, technical projects, internships, and mock interview score.
- **FastAPI service** with health, prediction, explainability, and metrics endpoints.
- **Streamlit interface** for interactive predictions.
- **Versioned model artifact** (`model/model_v1.pkl`).
- **Configurable decision threshold** through `PREDICTION_THRESHOLD`.
- **Request logging and latency metrics** for basic observability.

## 🧠 How it works

```text
Student profile → Streamlit UI → FastAPI /predict → Logistic Regression → Placement probability
                                      ├── /explain  (model coefficients)
                                      └── /metrics  (request and latency metrics)
```

The training script creates a reproducible synthetic dataset of 1,000 student profiles, standardizes the features, trains a Logistic Regression pipeline, and saves the trained model as `model/model_v1.pkl`.

## 📊 Input features

| Feature | Description | Example |
| --- | --- | ---: |
| `CGPA` | Academic performance on a 5–10 scale | `8.2` |
| `Aptitude_Score` | Logical and aptitude assessment score | `78` |
| `Technical_Projects` | Number of completed technical projects | `3` |
| `Internships` | Number of internships completed | `1` |
| `Mock_Interview_Score` | Interview-readiness score on a 50–100 scale | `75` |

## 🗂️ Repository structure

```text
.
├── app.py             # Streamlit frontend
├── main.py            # FastAPI backend
├── train_model.py     # Dataset generation and model training
├── requirements.txt   # Python dependencies
├── docs/
│   └── project-preview.svg
└── README.md
```

The `model/` and `logs/` directories are created at runtime when the model is trained and the API receives requests.

## 🚀 Quick start

### 1. Clone and install

```bash
git clone https://github.com/sgsinghashka-del/Student_Placement-_Prediction-_Logistic_-Regression.git
cd Student_Placement-_Prediction-_Logistic_-Regression

python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Train the model

Create the output directory and generate the versioned model artifact:

```bash
mkdir -p model
python train_model.py
```

On Windows PowerShell, use `New-Item -ItemType Directory model -Force` instead of `mkdir -p model`.

### 3. Start the API

In terminal 1:

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

### 4. Start the Streamlit app

In terminal 2:

```bash
streamlit run app.py
```

The browser UI will open at the local Streamlit URL shown in the terminal. Keep the FastAPI server running while making predictions.

## 🔌 API reference

### Health check — `GET /`

```json
{
  "status": "running",
  "model_version": "v1",
  "threshold": 0.6
}
```

### Prediction — `POST /predict`

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "CGPA": 8.2,
    "Aptitude_Score": 78,
    "Technical_Projects": 3,
    "Internships": 1,
    "Mock_Interview_Score": 75
  }'
```

Example response:

```json
{
  "model_version": "v1",
  "placement_probability": 0.72,
  "placed_prediction": 1,
  "threshold_used": 0.6
}
```

### Explainability — `POST /explain`

Returns the standardized Logistic Regression coefficients used as feature-importance signals. The endpoint accepts the same `StudentInput` schema as `/predict`.

### Metrics — `GET /metrics`

Returns the in-process request count, average latency, and active model version. Metrics reset whenever the API process restarts.

## ⚙️ Configuration

The placement decision threshold defaults to `0.6` and can be overridden with an environment variable:

```bash
# macOS/Linux
PREDICTION_THRESHOLD=0.7 uvicorn main:app --reload

# Windows PowerShell
$env:PREDICTION_THRESHOLD = "0.7"
uvicorn main:app --reload
```

## 🛠️ Technology stack

- **Python** — application and model-training language
- **pandas / NumPy** — data generation and preparation
- **scikit-learn** — scaling, pipeline construction, and Logistic Regression
- **FastAPI + Uvicorn** — inference API
- **Streamlit** — interactive frontend
- **Joblib** — model serialization

## ⚠️ Notes and limitations

- The training data is synthetic and is intended for demonstration and learning—not real hiring decisions.
- The API loads `model/model_v1.pkl` during startup, so train the model before launching FastAPI.
- The in-memory metrics are process-local and are not a replacement for production monitoring.
- No authentication, rate limiting, or persistent database is included.

## 🔮 Future improvements

- Replace synthetic data with a validated, privacy-preserving dataset.
- Add automated tests, CI, and model evaluation metrics such as precision, recall, ROC-AUC, and calibration.
- Add model/data versioning and drift monitoring.
- Containerize and deploy the API and UI.
- Add authentication, rate limiting, and persistent observability.

## 📄 License

No license has been specified yet. Add a license before distributing or reusing this project in production.
