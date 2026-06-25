import streamlit as st
import requests

# -----------------------------
# Config
# -----------------------------
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Student Placement Predictor",
    page_icon="🎓",
    layout="centered"
)

# -----------------------------
# UI Header
# -----------------------------
st.title("🎓 Student Placement Prediction")
st.markdown("Predict placement probability using ML model")

st.divider()

# -----------------------------
# Input Form
# -----------------------------
with st.form("prediction_form"):
    cgpa = st.slider("CGPA", 5.0, 10.0, 7.5, 0.1)
    aptitude = st.slider("Aptitude Score", 40, 100, 70)
    projects = st.number_input("Technical Projects", 0, 10, 2)
    internships = st.number_input("Internships", 0, 5, 1)
    mock_score = st.slider("Mock Interview Score", 50.0, 100.0, 75.0)

    submit = st.form_submit_button("Predict")

# -----------------------------
# Prediction Call
# -----------------------------
if submit:
    payload = {
        "CGPA": cgpa,
        "Aptitude_Score": aptitude,
        "Technical_Projects": projects,
        "Internships": internships,
        "Mock_Interview_Score": mock_score
    }

    with st.spinner("Predicting..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()

        st.success("Prediction Successful")

        st.metric(
            label="Placement Probability",
            value=f"{result['placement_probability'] * 100:.1f}%"
        )

        if result["placed_prediction"] == 1:
            st.success("✅ Likely to be Placed")
        else:
            st.error("❌ Unlikely to be Placed")

        st.caption(f"Model Version: {result['model_version']}")
    else:
        st.error("API Error – Is FastAPI running?")