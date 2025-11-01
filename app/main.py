from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import logging
from pathlib import Path

from app.models.schemas import Customer, CreditScoreResponse
from app.services.credit_scorer import CreditScorer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Credit Score API",
    version="1.0.0",
    description="Professional API for credit scoring predictions.",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the scorer
try:
    scorer = CreditScorer('ressource/pipeline', 'ressource/classifier')
    logger.info("Credit scorer initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize credit scorer: {str(e)}")
    raise

# Load the dataset
try:
    data_path = Path('data/dataset_sample.csv')
    if not data_path.exists():
        raise FileNotFoundError("Dataset file not found")
        
    df = pd.read_csv(
        data_path,
        engine='pyarrow',
        encoding='ISO-8859-1'
    )
    logger.info("Dataset loaded successfully")
except Exception as e:
    logger.error(f"Failed to load dataset: {str(e)}")
    raise

@app.post("/predict", 
         response_model=CreditScoreResponse,
         tags=["credit_score"],
         summary="Get credit score prediction",
         response_description="Credit score and advice")
async def get_prediction(client: Customer) -> CreditScoreResponse:
    """
    Get credit score prediction for a customer.

    Args:
        client (Customer): Customer ID

    Returns:
        CreditScoreResponse: Credit score prediction and advice

    Raises:
        HTTPException: If client ID is not found or other errors occur
    """
    try:
        # Validate client ID exists
        if client.id not in df['SK_ID_CURR'].unique():
            raise HTTPException(
                status_code=404,
                detail=f"Client ID {client.id} not found"
            )

        # Get features and prediction
        features = scorer.transform(df, client.dict())
        prob, info_default = scorer.make_prediction(features)

        return CreditScoreResponse(
            credit_score=round(float(prob[0]), 3),
            advice=info_default
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing prediction request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred"
        )