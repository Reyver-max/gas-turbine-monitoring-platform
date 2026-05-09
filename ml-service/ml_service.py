from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.ensemble import IsolationForest
import numpy as np
import random

app = FastAPI(title="Gas Turbine ML Anomaly Detection Service")


class TurbineReading(BaseModel):
    rpm: int
    compressor_pressure_bar: float
    turbine_temp_c: float
    efficiency: float
    fuel_flow_kg_s: float


def generate_training_data(n=1000):
    data = []

    for _ in range(n):
        rpm = random.randint(13500, 15000)
        pressure = random.uniform(13.0, 16.0)
        temperature = random.uniform(450.0, 550.0)
        efficiency = random.uniform(0.48, 0.55)
        fuel_flow = random.uniform(2.2, 3.0)

        data.append([rpm, pressure, temperature, efficiency, fuel_flow])

    return np.array(data)


training_data = generate_training_data()

model = IsolationForest(
    contamination=0.1,
    random_state=42
)

model.fit(training_data)


@app.get("/health")
def health():
    return {"status": "ml service ok"}


@app.post("/predict")
def predict(reading: TurbineReading):
    features = np.array([[
        reading.rpm,
        reading.compressor_pressure_bar,
        reading.turbine_temp_c,
        reading.efficiency,
        reading.fuel_flow_kg_s
    ]])

    prediction = model.predict(features)[0]
    raw_score = model.decision_function(features)[0]

    anomaly_score = round(float(1 - raw_score), 3)

    if prediction == 1:
        status = "normal"
    else:
        if reading.turbine_temp_c > 750 or reading.efficiency < 0.38:
            status = "critical"
        else:
            status = "warning"

    return {
        "anomaly_score": anomaly_score,
        "status": status
    }
