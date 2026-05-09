# Industrial Gas Turbine Telemetry & Anomaly Detection Platform

## Overview

This project is a Dockerized industrial telemetry and monitoring platform designed to simulate gas turbine operational monitoring in a modern Industry 4.0 environment.

The system generates synthetic turbine telemetry data, stores it in PostgreSQL, analyzes operational anomalies using machine learning, and visualizes live telemetry through Grafana dashboards.

The project combines DevOps, monitoring, backend engineering, machine learning, and industrial telemetry concepts into a single multi-service platform.

---

<img width="1920" height="956" alt="Screenshot 2026-05-09 at 8 46 40" src="https://github.com/user-attachments/assets/7233ab43-d402-4ae8-83ea-3b63bd8816eb" />


## Features

- Real-time synthetic gas turbine telemetry generation
- FastAPI backend for telemetry ingestion
- PostgreSQL telemetry database
- ML-based anomaly detection using Isolation Forest
- Grafana operational monitoring dashboards
- Dockerized microservice architecture
- GitHub Actions CI pipeline
- Industrial-style predictive maintenance simulation

---

## Architecture

Main system flow:

Simulator → FastAPI Backend → ML Service → PostgreSQL → Grafana Dashboard

The entire platform is orchestrated using Docker Compose.


<img width="1536" height="1024" alt="ChatGPT Image May 9, 2026, 05_18_59 PM" src="https://github.com/user-attachments/assets/c893d2c2-031b-4b63-b159-4f26c70c2f6d" />




| Arrow                | Label              |
| -------------------- | ------------------ |
| Simulator → Backend  | Telemetry JSON     |
| Backend → ML Service | Prediction Request |
| ML Service → Backend | Anomaly Score      |
| Backend → PostgreSQL | Store Telemetry    |
| Grafana → PostgreSQL | SQL Queries        |

---

## Technology Stack

### Backend
- FastAPI
- Python

### Database
- PostgreSQL

### Monitoring
- Grafana

### Machine Learning
- Scikit-learn
- Isolation Forest

### DevOps
- Docker
- Docker Compose
- GitHub Actions CI

---

## Microservices

### Simulator Service
Generates synthetic gas turbine telemetry including:
- RPM
- Turbine temperature
- Compressor pressure
- Fuel flow
- Thermal efficiency

The simulator also injects abnormal operating conditions to emulate industrial anomalies.

---

### Backend API Service
Receives telemetry data and:
- communicates with the ML service
- stores telemetry into PostgreSQL
- exposes REST API endpoints

Main endpoints:
- `/health`
- `/readings`
- `/stats`

---

### ML Anomaly Detection Service
Uses an Isolation Forest model to detect abnormal turbine operating conditions.

The service returns:
- anomaly score
- operational status:
  - normal
  - warning
  - critical

This simulates predictive maintenance and condition monitoring workflows commonly used in industrial environments.

---

### Grafana Monitoring
Grafana dashboards visualize:
- turbine RPM
- turbine temperature
- efficiency
- fuel flow
- anomaly score
- warning events
- critical events

---

## CI/CD

The project includes a GitHub Actions CI pipeline that:
- validates Docker Compose configuration
- builds all Docker services automatically

---

## How to Run

### Clone repository

```bash
git clone https://github.com/Reyver-max/gas-turbine-monitoring-platform.git
cd gas-turbine-monitoring-platform
```

### Start services

```bash
docker compose up --build
```

---

## Service Ports

| Service | Port |
|---|---|
| Backend API | 8000 |
| ML Service | 9000 |
| Grafana | 3000 |
| PostgreSQL | 5433 |

---

## Grafana Login

Username:
```text
admin
```

Password:
```text
admin
```

---

## Example Telemetry Reading

```json
{
  "rpm": 14900,
  "compressor_pressure_bar": 15.5,
  "turbine_temp_c": 880,
  "efficiency": 0.34,
  "fuel_flow_kg_s": 2.9,
  "anomaly_score": 1.037,
  "status": "critical"
}
```

---

## Future Improvements

Potential future upgrades:
- MQTT telemetry ingestion
- Kubernetes deployment
- Prometheus metrics
- Alert notifications
- Persistent Grafana volumes
- Time-series database integration
- Real sensor integration
- Advanced predictive maintenance forecasting

---

## Screenshots

### Grafana Dashboard

(Add screenshot here)

### GitHub Actions CI

(Add screenshot here)

### Architecture Diagram

(Add architecture diagram here)

---

## Author

Reyver Serna

GitHub:
https://github.com/Reyver-max
