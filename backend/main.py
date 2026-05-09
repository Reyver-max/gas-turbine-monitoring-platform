from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
import requests

app = FastAPI(title="Gas Turbine Telemetry API")

ML_SERVICE_URL = "http://ml-service:9000/predict"


class TurbineReading(BaseModel):
    rpm: int
    compressor_pressure_bar: float
    turbine_temp_c: float
    efficiency: float
    fuel_flow_kg_s: float


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "turbine_db"),
        user=os.getenv("POSTGRES_USER", "turbine_user"),
        password=os.getenv("POSTGRES_PASSWORD", "turbine_pass"),
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/readings")
def create_reading(reading: TurbineReading):

    # Call ML service
    ml_response = requests.post(
        ML_SERVICE_URL,
        json=reading.dict()
    )

    ml_result = ml_response.json()

    anomaly_score = ml_result["anomaly_score"]
    status = ml_result["status"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO turbine_readings (
            rpm,
            compressor_pressure_bar,
            turbine_temp_c,
            efficiency,
            fuel_flow_kg_s,
            anomaly_score,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """,
        (
            reading.rpm,
            reading.compressor_pressure_bar,
            reading.turbine_temp_c,
            reading.efficiency,
            reading.fuel_flow_kg_s,
            anomaly_score,
            status,
        ),
    )

    reading_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "reading saved",
        "id": reading_id,
        "ml_result": ml_result
    }


@app.get("/readings")
def get_readings():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            timestamp,
            rpm,
            compressor_pressure_bar,
            turbine_temp_c,
            efficiency,
            fuel_flow_kg_s,
            anomaly_score,
            status
        FROM turbine_readings
        ORDER BY timestamp DESC
        LIMIT 50;
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "timestamp": row[1],
            "rpm": row[2],
            "compressor_pressure_bar": float(row[3]),
            "turbine_temp_c": float(row[4]),
            "efficiency": float(row[5]),
            "fuel_flow_kg_s": float(row[6]),
            "anomaly_score": float(row[7]) if row[7] is not None else None,
            "status": row[8],
        }
        for row in rows
    ]


@app.get("/stats")
def get_stats():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            COUNT(*) AS total_readings,
            AVG(rpm),
            AVG(turbine_temp_c),
            AVG(efficiency)
        FROM turbine_readings;
        """
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_readings": row[0],
        "avg_rpm": float(row[1]) if row[1] else None,
        "avg_temp": float(row[2]) if row[2] else None,
        "avg_efficiency": float(row[3]) if row[3] else None,
    }
