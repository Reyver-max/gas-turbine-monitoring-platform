CREATE TABLE IF NOT EXISTS turbine_readings (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rpm INTEGER NOT NULL,
    compressor_pressure_bar NUMERIC(6,2) NOT NULL,
    turbine_temp_c NUMERIC(6,2) NOT NULL,
    efficiency NUMERIC(5,3) NOT NULL,
    fuel_flow_kg_s NUMERIC(6,3) NOT NULL,
    anomaly_score NUMERIC(5,3),
    status VARCHAR(20) DEFAULT 'normal'
);
