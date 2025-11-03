# Credit Score API

FastAPI REST API for credit scoring predictions deployed on Google Cloud Run.

## Overview

Production-ready API that provides credit risk predictions using a LightGBM model with preprocessing pipeline. Returns probability of payment difficulties for loan applicants.

**Live API:** https://credit-score-api-572900860091.europe-west1.run.app

## Features

- RESTful API with FastAPI
- Unified sklearn pipeline (preprocessing + model)
- Automatic input validation
- CORS enabled for dashboard integration
- Deployed on Google Cloud Run (serverless)

## API Endpoint

### POST /predict

**Request:**
```json
{
  "id": 162473
}
```

**Response:**
```json
{
  "credit_score": 0.215,
  "advice": "No payment difficulties"
}
```

**Status Codes:**
- 200: Success
- 404: Client ID not found
- 500: Internal server error

## Project Structure

```
P7_api_deploy/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/              # Pydantic schemas
│   ├── services/            # Business logic (CreditScorer)
│   └── api/                 # API routes
├── ressource/
│   └── pipeline.joblib      # Unified sklearn pipeline (5.2 MB)
├── data/
│   └── dataset_sample.csv   # Sample client data
├── Dockerfile               # Container configuration
└── requirements.txt         # Python dependencies

```

## Local Development

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
# Start development server
uvicorn app.main:app --reload --port 8001

# Test the API
curl -X POST "http://127.0.0.1:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{"id": 162473}'
```

## Deployment

### Deploy to Cloud Run

```bash
# Deploy from source
gcloud run deploy credit-score-api \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated

# Test deployed API
curl -X POST "https://credit-score-api-572900860091.europe-west1.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"id": 162473}'
```

## Model Pipeline

The API uses a unified sklearn pipeline that includes:
1. **Preprocessing**: Imputation, scaling, encoding
2. **Feature Selection**: SelectFromModel with LightGBM
3. **Classification**: LightGBM with optimized hyperparameters

**Decision Threshold:** 0.47 (optimized for G-mean)

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **ML**: scikit-learn 1.6.1, LightGBM 4.6.0
- **Server**: Uvicorn
- **Deployment**: Google Cloud Run
- **Container**: Docker

## Related Projects

- **ML Training**: [P7_Implementez_modele_scoring](../P7_Implementez_modele_scoring) - Model training and pipeline creation
- **Dashboard**: [P7_dashboard_deploy](../P7_dashboard_deploy) - Streamlit dashboard consuming this API

## API Documentation

Interactive documentation available at:
- **Swagger UI**: https://credit-score-api-572900860091.europe-west1.run.app/docs
- **ReDoc**: https://credit-score-api-572900860091.europe-west1.run.app/redoc

## License

OpenClassrooms project - Educational purposes

---

*Last update: November 2025*
