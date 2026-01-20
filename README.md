# Fraud Detection System — Production-Ready ML for Financial Transactions

[![Repo Size](https://img.shields.io/github/repo-size/meet9614/Fraud-Detection-Model)](https://github.com/meet9614/Fraud-Detection-Model)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)](#)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B)](#)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](#)
[![AWS](https://img.shields.io/badge/AWS-EC2-orange)](#)

A **production-ready machine learning system** for detecting fraudulent financial transactions.  
This project combines **domain-driven feature engineering** with an **optimized Logistic Regression model** to deliver **real-time fraud detection** via a **FastAPI inference service** and an **interactive Streamlit UI**.

The system is **containerized, cloud-agnostic, and MLOps-ready**, with stateless APIs and production-focused deployment.

## 🚀 Deployment Status (Live)

### 🔹 What I built & deployed
- FastAPI-based machine learning inference backend
- Streamlit interactive frontend for transaction input and risk visualization
- Fully Dockerized backend and frontend architecture
- Deployed on **AWS EC2 (Ubuntu 24.04, t3.micro)**
- Model and scaler correctly loaded inside containers at runtime

### 🔹 Live Endpoints

**FastAPI Swagger (Backend)**  
https://lnkd.in/gpM7CjgQ

**Streamlit UI (Frontend)**  
http://52.66.236.66:8501

Highlights
- Highly accurate model: 98.85% accuracy
- Excellent discrimination: AUC = 0.9958
- Precision: 94.39% — Most flagged alerts are true frauds
- Recall: 92.90% — Detects ~93% of fraudulent transactions
- Operational efficiency: ~1 fraud detected per 16.8 investigations
- Estimated annual savings: $114M+

Table of contents
- [Overview](#overview)
- [Performance Summary](#performance-summary)
- [Dataset](#dataset)
- [Architecture](#architecture)
- [Components](#components)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (Streamlit)](#frontend-streamlit)
  - [Model artifacts](#model-artifacts)
- [Local quickstart (Docker)](#local-quickstart-docker)
- [Local development (without Docker)](#local-development-without-docker)
- [API usage examples](#api-usage-examples)
- [Deployment options](#deployment-options)
- [Future enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
This repository contains a full-stack, containerized ML system for fraud detection:
- A FastAPI microservice that loads a trained model + preprocessing pipeline (joblib) and exposes a `/predict` endpoint for real-time inference.
- A Streamlit frontend for manual transaction input and visualization of risk scores.
- Dockerfiles for backend and frontend and a `docker-compose.yml` for one-command local orchestration.
The system is designed to be stateless, cloud-agnostic, and production-ready.

## Performance summary
| Metric    | Score   | Business impact |
|-----------|--------:|-----------------|
| Accuracy  | 98.85%  | Outstanding overall performance |
| AUC Score | 0.9958  | Near-perfect fraud discrimination |
| Precision | 94.39%  | ~94% of flagged alerts are genuine fraud |
| Recall    | 92.90%  | Detects ~93% of fraudulent transactions |
| F1-Score  | 0.9364  | Strong operational balance |

Business metrics:
- Fraud Detection Rate (Recall): 92.9%
- False Positive Rate: ~0.6%
- Operational efficiency: 1 fraud detected per 16.8 investigations
- Estimated annual savings: $114M+

## Dataset
Dataset size: ~500 MB  
Download (Google Drive): https://drive.google.com/file/d/1N5gCt0KrnwIrCbAhz3bpxMR96pegHs5n/view?usp=drive_link

Notes:
- The dataset is not included in the repo due to size and privacy concerns. After downloading, place it in the path expected by training scripts or point training to its location.
- Do not commit raw PII-sensitive data to the repository.

## Architecture
User (Browser)  
   │  
   ▼
Streamlit Frontend (UI)  
   │  REST API  
   ▼
FastAPI Backend (ML Inference)  
   │  
   ▼
Fraud Probability + Classification

- Frontend and backend run in separate containers; communication occurs over REST.
- Backend performs runtime feature engineering to keep training–serving parity.

## Components

### Backend (FastAPI)
- FastAPI-based inference service providing `/predict`.
- Loads:
  - trained logistic regression model (joblib)
  - preprocessing pipeline (scalers, encoders, engineered feature transforms)
- Responsibilities:
  - Validate and transform incoming transaction payloads
  - Apply same feature engineering as training
  - Return fraud probability and classification
- Typical tech: FastAPI, scikit-learn, pandas, numpy, joblib
- Example endpoint: POST /predict -> { "fraud_probability": 0.987, "is_fraud": true }

### Frontend (Streamlit)
- Interactive dashboard for entering transaction details and visualizing risk.
- Sends requests to the backend `/predict` endpoint.
- Configurable backend URL via environment variable, e.g. `BACKEND_URL=http://localhost:8000`
- Independently containerized so it can be deployed to Streamlit Cloud or run locally.

### Model artifacts
- Trained model: `models/fraud_model.joblib` (logistic regression)
- Preprocessing pipeline: `models/pipeline.joblib`
- If you retrain, commit only small metadata/config files; large artifacts should be stored in an artifact registry (S3, GCS, or release assets).

## Local quickstart (Docker)
Prerequisites: Docker and docker-compose installed.

1. Clone the repo
   git clone https://github.com/meet9614/Fraud-Detection-Model.git
   cd Fraud-Detection-Model

2. Build and run both services
   docker-compose up --build

3. Open:
   - Streamlit UI: http://localhost:8501
   - Backend API docs (Swagger/OpenAPI): http://localhost:8000/docs

Notes:
- docker-compose defines separate services for `backend` and `frontend`. Environment variables in `.env` (if present) configure endpoints and ports.

## Local development (without Docker)
Prereqs: Python 3.8+, pip, virtualenv.

1. Create virtual env
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows

2. Install requirements
   pip install -r requirements.txt

3. Run backend
   # Adjust path/module name if backend app is in a subdir (e.g. backend/main.py)
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

4. Run frontend
   # Adjust to your frontend entrypoint (e.g. frontend/app.py)
   export BACKEND_URL=http://localhost:8000
   streamlit run app.py

## API usage examples

Request
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{\
    "transaction_amount": 123.45,\
    "transaction_time": "2025-12-01T13:22:00Z",\
    "merchant_id": "M123",\
    "card_country": "US",\
    "device_id": "D456",\
    "customer_history": {...}\
  }'

Response (example)
{\
  "fraud_probability": 0.8723,\
  "is_fraud": true,\
  "threshold": 0.5,\
  "explainability": {\
    "top_features": [\
      {"feature": "tx_amount_norm", "impact": 0.25},\
      {"feature": "velocity_score", "impact": 0.18}\
    ]\
  }\
}

Notes:
- Exact request fields depend on the deployed model pipeline. Check the backend docs (`/docs`) for the concrete schema.
- The backend returns probability and boolean classification based on a configurable threshold.

## Deployment options
- Container-native: deploy backend and frontend containers to Azure Container Apps, AWS ECS / App Runner, GCP Cloud Run, or Kubernetes.
- Streamlit frontend can be deployed separately to Streamlit Cloud or any static app host that supports containers.
- Use an artifact store for model files (S3, GCS, Azure Blob) and load them at container startup for easier CI/CD.

## Monitoring & Production considerations
- Add logging and structured metrics (Prometheus, Grafana)
- Implement model drift detection and performance monitoring
- Use feature hashing or strict schema validation to guard against broken inputs
- Implement rate limiting and authentication for the inference endpoint in production
- Consider a canary deployment strategy for model updates

## Future enhancements
- Real-time model drift detection and automatic retraining triggers
- Ensemble models and stacking for improved robustness
- Graph-based fraud network analysis (transactions graph)
- Automated feature discovery / AutoML
- Multi-currency and cross-border transaction support

## Contributing
Contributions are welcome. Suggested workflow:
1. Fork the repository
2. Create a feature branch
3. Add tests and update docs
4. Open a PR describing the change

Please follow the repository's coding style and include unit/integration tests for new functionality.

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Financial transaction dataset providers
- Machine learning research community
- Fraud detection industry best practices

---
