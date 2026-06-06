from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

from generate_lung import generate_lung_image

app = FastAPI()

# ✅ Enable CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
model = joblib.load("damage_model.joblib")

class UserData(BaseModel):
    age: int
    years_smoking: int
    cigarettes_per_day: int
    exercise: int = 0
    pollution: int = 0


def explain(score):
    if score < 25:
        return "Lungs appear mostly healthy with minimal structural damage."
    elif score < 50:
        return "Mild lung tissue inflammation and early signs of damage detected."
    elif score < 75:
        return "Moderate lung damage with scarring and impaired air exchange."
    else:
        return "Severe lung destruction with high risk of respiratory failure."


def medical_report(score, data):

    return f"""
==============================
       LUNG HEALTH REPORT
==============================

Patient Information:
Age: {data.age}
Smoking Years: {data.years_smoking}
Cigarettes/Day: {data.cigarettes_per_day}
Exercise Hours/Week: {data.exercise}
Pollution Level: {data.pollution}/10

Predicted Lung Damage:
{round(score,2)} %

Clinical Findings:
{explain(score)}

Recommendations:
• Quit smoking immediately
• Exercise regularly
• Avoid polluted areas
• Consult lung specialist

Disclaimer:
AI simulation – not medical diagnosis
==============================
"""


@app.post("/predict")
def predict(data: UserData):

    X = [[
        data.age,
        data.years_smoking,
        data.cigarettes_per_day,
        data.exercise,
        data.pollution
    ]]

    score = float(model.predict(X)[0])

    # Generate lung images
    generate_lung_image(score)

    explanation = explain(score)
    report = medical_report(score, data)

    return {
        "damage_score": round(score, 2),
        "explanation": explanation,
        "report": report
    }
