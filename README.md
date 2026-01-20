# Fraud Detection System — Production-Ready ML for Financial Transactions

**License:** MIT  
**Language:** Python  
**Repo size:** ~500 MB dataset (external)

A production-ready machine learning system for detecting fraudulent financial transactions.
This project combines domain-driven feature engineering with an optimized Logistic Regression model to deliver real-time fraud detection via a FastAPI inference service and an interactive Streamlit UI.

Note: This project has been deployed to AWS EC2 (Docker Compose). See the "AWS EC2 (Docker Compose)" section under Deployment Options for the deployment steps and notes.

---

## Highlights

- Accuracy: **98.85%**
- AUC: **0.9958**
- Precision: **94.39%**
- Recall: **92.90%**
- F1-Score: **0.9364**
- Operational efficiency: **1 fraud detected per 16.8 investigations**
- Estimated annual savings: **$114M+**

---

## Table of Contents

- Overview
- Performance Summary
- Dataset
- System Architecture
- Components
  - Backend (FastAPI)
  - Frontend (Streamlit)
- Model Artifacts
- Local Quickstart (Docker)
- Local Development (Without Docker)
- API Usage Examples
- Deployment Options
  - AWS EC2 (Docker Compose)
- Monitoring & Production Considerations
- Future Enhancements
- Contributing
- License
- Acknowledgments

---

## Overview

This repository contains a full-stack, containerized ML system for fraud detection:

- A FastAPI microservice that loads a trained ML model and preprocessing pipeline (joblib) and exposes a `/predict` endpoint.
- A Streamlit frontend for transaction input and fraud risk visualization.
- Dockerfiles for backend and frontend and a `docker-compose.yml` for one-command orchestration.

Design goals: stateless, cloud-agnostic, production-ready, and training–serving parity via runtime feature engineering.

---

## Performance Summary

| Metric     | Score   |
|------------|---------|
| Accuracy   | 98.85%  |
| AUC        | 0.9958  |
| Precision  | 94.39%  |
| Recall     | 92.90%  |
| F1-Score   | 0.9364  |

Business metrics:
- Fraud detection rate: 92.9%
- False positive rate: ~0.6%
- Operational efficiency: 1 fraud per 16.8 investigations
- Estimated annual savings: $114M+

---

## Dataset

- Size: ~500 MB  
- Download: https://drive.google.com/file/d/1N5gCt0KrnwIrCbAhz3bpxMR96pegHs5n/view

Notes:
- Dataset is excluded from the repository due to size and privacy concerns.
- Do not commit raw or PII-sensitive data.
- Update training scripts with the local dataset path if retraining.

---

## System Architecture

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

- Frontend and backend run in separate containers.
- Communication occurs via REST.
- Backend performs runtime feature engineering to ensure training–serving parity.

---

## Components

### Backend (FastAPI)
Responsibilities:
- Validate incoming transaction payloads
- Apply the same feature engineering used during training
- Generate fraud probability and classification

Tech stack:
- FastAPI, scikit-learn, pandas, numpy, joblib

Example endpoint:
- POST `/predict`

Example response:
```json
{
  "fraud_probability": 0.987,
  "is_fraud": true
}
```

### Frontend (Streamlit)
- Interactive UI for transaction input
- Displays fraud probability and risk status
- Sends requests to the backend `/predict` endpoint

Backend URL configuration:
- `BACKEND_URL=http://<backend-host>:8000`

The frontend is independently containerized and can be deployed to Streamlit Cloud or any container-compatible platform.

---

## Model Artifacts

- Trained model: `fraud_best_model.pkl`
- Preprocessing pipeline: `fraud_scaler.pkl`

Best practice:
- Do not commit large artifacts repeatedly.
- Use S3 / GCS / Azure Blob or release assets for production pipelines.
- Load models from remote storage at container startup where appropriate.

---

## Local Quickstart (Docker)

Prerequisites:
- Docker
- Docker Compose

```bash
git clone https://github.com/meet9614/Fraud-Detection-Model.git
cd Fraud-Detection-Model
docker-compose up --build
```

Access:
- Streamlit UI: http://localhost:8501
- FastAPI docs: http://localhost:8000/docs

---

## Local Development (Without Docker)

Setup:
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

Run backend:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Run frontend:
```bash
export BACKEND_URL=http://localhost:8000
streamlit run frontend/app.py
```

---

## API Usage Example

Example `curl`:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{ "amount": 123.45, "oldbalanceOrg": 1000, "newbalanceOrig": 876.55 }'
```

Refer to `/docs` for the exact request schema.

---

## Deployment Options

Supported / tested:
- AWS EC2 (Docker Compose)
- AWS ECS / App Runner
- Azure Container Apps
- GCP Cloud Run
- Kubernetes

Recommended:
- Store model artifacts in S3 / Blob Storage
- Load models at container startup
- Use environment-based configuration
- Use secrets manager for secrets

### AWS EC2 (Docker Compose) — (added/updated)
This project has been deployed to AWS EC2 using Docker Compose. Below are practical steps and notes that you can follow or adapt.

1. Provision an EC2 instance
   - Suggested instance: t3.medium or larger (adjust for traffic/model size)
   - OS: Amazon Linux 2 / Ubuntu 22.04
   - Security Group inbound rules:
     - TCP 22 (SSH) — restrict to your IP
     - TCP 80 (optional — for reverse proxy / Nginx)
     - TCP 8000 (FastAPI) — restrict to proxy or internal network
     - TCP 8501 (Streamlit) — restrict to proxy or internal network
   - For production, place an ALB / Nginx in front to terminate TLS.

2. Connect and install Docker & Docker Compose (example for Ubuntu)
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

3. Pull repo and start
```bash
git clone https://github.com/meet9614/Fraud-Detection-Model.git
cd Fraud-Detection-Model
# Create or edit .env with the variables below
docker-compose up -d --build
```

4. Example `.env` (place at repo root)
```
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_URL=http://<EC2_PUBLIC_IP_OR_DOMAIN>:8000
MODEL_S3_PATH=s3://your-bucket/path/to/fraud_best_model.pkl
SCALER_S3_PATH=s3://your-bucket/path/to/fraud_scaler.pkl
```
- If using S3, attach an IAM role to the EC2 instance with least-privilege S3 access (recommended) instead of embedding AWS keys.

5. Access
- FastAPI docs: http://<EC2_PUBLIC_IP_OR_DOMAIN>:8000/docs
- Streamlit UI: http://<EC2_PUBLIC_IP_OR_DOMAIN>:8501

6. Production tips
- Use Nginx or ALB to:
  - Terminate TLS (Let's Encrypt)
  - Route traffic and prevent exposing internal ports
- Run docker-compose as a service (systemd) or use container orchestration
- Centralize logs (CloudWatch / ELK) and metrics (Prometheus / Grafana)
- Add health checks and readiness probes for container lifecycle management

If you'd like, I can:
- Add a sample `systemd` unit for running docker-compose on boot
- Add an example Nginx reverse-proxy configuration
- Replace placeholder <EC2_PUBLIC_IP_OR_DOMAIN> with your instance's public DNS in the README

---

## Monitoring & Production Considerations

- Structured logging (JSON) and centralized log collection (CloudWatch / ELK)
- Metrics (Prometheus / Grafana)
- Input schema validation
- Rate limiting and authentication (API keys / JWT / mTLS)
- Model drift detection and data / concept drift monitoring
- Canary deployments for model updates
- Health checks and readiness probes

---

## Future Enhancements

- Automated model drift detection
- Scheduled retraining pipelines (CI/CD for models)
- Ensemble and stacking models
- Graph-based fraud detection
- Multi-currency transaction support
- Role-based access control (RBAC) for APIs

---

## Contributing

- Fork the repository
- Create a feature branch
- Add tests and documentation
- Open a PR with a clear description

Please avoid committing raw/PII-sensitive data or large datasets directly to the repo.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Acknowledgments

- Financial transaction dataset providers
- Machine learning research community
- Fraud detection industry best practices