import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

rows = 5000

age = np.random.randint(18,80,rows)
years_smoking = np.random.randint(0,50,rows)
cigarettes_per_day = np.random.randint(0,40,rows)
exercise = np.random.randint(0,10,rows)
pollution = np.random.randint(1,10,rows)

damage = (
    years_smoking * 1.6 +
    cigarettes_per_day * 1.3 +
    age * 0.4 +
    pollution * 2 -
    exercise * 1.5 +
    np.random.normal(0,5,rows)
)

damage = np.clip(damage,0,100)

df = pd.DataFrame({
    "age":age,
    "years_smoking":years_smoking,
    "cigarettes_per_day":cigarettes_per_day,
    "exercise":exercise,
    "pollution":pollution,
    "damage":damage
})

X = df.drop("damage",axis=1)
y = df["damage"]

model = RandomForestRegressor(n_estimators=200)
model.fit(X,y)

joblib.dump(model,"damage_model.joblib")

print("Model retrained successfully!")
