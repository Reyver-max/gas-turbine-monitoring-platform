import random
import time
import requests


BACKEND_URL = "http://backend:8000/readings"


def generate_reading():
    # normal operating ranges
    rpm = random.randint(13500, 15000)
    pressure = round(random.uniform(13.0, 16.0), 2)
    temperature = round(random.uniform(450.0, 550.0), 2)
    efficiency = round(random.uniform(0.48, 0.55), 3)
    fuel_flow = round(random.uniform(2.2, 3.0), 3)

    # occasional anomalies
    if random.random() < 0.1:
        temperature = round(random.uniform(700.0, 900.0), 2)
        efficiency = round(random.uniform(0.30, 0.42), 3)

    return {
        "rpm": rpm,
        "compressor_pressure_bar": pressure,
        "turbine_temp_c": temperature,
        "efficiency": efficiency,
        "fuel_flow_kg_s": fuel_flow
    }


while True:
    reading = generate_reading()

    try:
        response = requests.post(BACKEND_URL, json=reading)

        print("Sent:", reading)
        print("Response:", response.json())

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
