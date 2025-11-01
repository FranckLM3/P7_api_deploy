from pydantic import BaseModel, Field

class Customer(BaseModel):
    """
    Schema for customer data validation.
    """
    id: int = Field(..., description="Customer ID", gt=0)

class CreditScoreResponse(BaseModel):
    """
    Schema for credit score response.
    """
    credit_score: float = Field(..., description="Credit score between 0 and 1")
    advice: str = Field(..., description="Credit score interpretation")
    