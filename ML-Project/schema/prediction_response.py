from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated , Dict
# pydantic model to validate incoming data
class PredictionResponse(BaseModel):
    
    predicted_category: str = Field(..., description="The predicted insurance premium category", example="High")
    confidence: float = Field(..., description="Model's confidence score for the predicted class (range: 0 to 1)",
        example=0.8432)
    class_probabilities: Dict[str, float] = Field(..., 
        description="Probability distribution across all possible classes",
        example={"Low": 0.01, "Medium": 0.15, "High": 0.84}
    )