🚨 Fraud Detection System – Machine Learning for Financial Transactions

A production-ready machine learning system for detecting fraudulent financial transactions with exceptional performance (98.85% accuracy, 99.58% AUC). This project combines advanced feature engineering with optimized logistic regression to deliver real-time fraud detection through a scalable API and interactive user interface.

🏆 Performance Highlights
Metric	Score	Business Impact
Accuracy	98.85%	Outstanding overall performance
AUC Score	0.9958	Near-perfect fraud discrimination
Precision	94.39%	94% of flagged alerts are genuine fraud
Recall	92.90%	Detects ~93% of fraudulent transactions
F1-Score	0.9364	Strong balance for real-world operations
💰 Business Impact

Fraud Detection Rate: 92.9%

False Positive Rate: ~0.6%

Operational Efficiency: 1 fraud detected per 16.8 investigations

Estimated Annual Savings: $114M+

📊 Dataset

Dataset Size: ~500 MB
Download Link:
https://drive.google.com/file/d/1N5gCt0KrnwIrCbAhz3bpxMR96pegHs5n/view?usp=drive_link

🚀 Deployment & Engineering Progress
🐳 Fully Dockerized System (Production-Oriented)

The project has been extended beyond model training into a complete, deployable ML system with a clear separation between backend inference and frontend interaction.

🔧 Backend – FastAPI (ML Inference Service)

Built a FastAPI-based REST API for real-time fraud prediction

Loads trained ML model and preprocessing pipeline using joblib

Performs feature engineering at inference time to ensure training–serving consistency

Exposes /predict endpoint returning fraud probability and classification

Designed for stateless, scalable inference

Fully containerized using Docker

Tech Stack

FastAPI

Scikit-learn

Pandas / NumPy

Joblib

Docker

🖥️ Frontend – Streamlit (Interactive UI)

Developed an interactive Streamlit dashboard for transaction risk scoring

Allows manual entry of transaction details

Sends REST requests to backend API and displays predictions in real time

Uses environment-based configuration for backend URL (cloud-ready design)

Independently containerized for flexible deployment

Tech Stack

Streamlit

Requests

Docker

🧱 System Architecture
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

📦 Docker & Local Orchestration

Separate Dockerfiles for backend and frontend

docker-compose.yml for multi-container local execution

Enables one-command startup of the complete system

Architecture is cloud-provider agnostic (Azure / AWS compatible)

🌐 Deployment Status

Backend implemented as a production-ready containerized API

Frontend prepared for deployment on Streamlit Cloud

System architecture supports:

Azure Container Apps / App Service

AWS ECS / App Runner

Local Docker environments

🔮 Future Enhancements

Real-time model drift detection

Ensemble learning with multiple algorithms

Graph-based fraud network analysis

Automated feature discovery

Multi-currency transaction support

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgments

Financial transaction dataset providers

Machine learning research community

Fraud detection industry best practices

⭐ Star this repository if you find it helpful!
