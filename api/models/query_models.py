from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., description="The question about a simpro mobile app feature")
    structured: bool = Field(default=False, description="Whether to return a structured response")
    
    class Config:
        schema_extra = {
            "example": {
                "question": "How do I use the mobile audit feature?",
                "structured": True
            }
        }

class FeatureGuide(BaseModel):
    feature_purpose: str = Field(description="Brief explanation of what this feature does")
    how_to_access: str = Field(description="How to find and access this feature in the mobile app")
    key_steps: List[str] = Field(description="Step-by-step instructions (8 steps maximum)")
    usage_tips: List[str] = Field(description="1-3 practical tips for effective use")
    related_features: Optional[List[str]] = Field(default=None, description="Other related features that might be useful")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="The answer to the question")
    structured_guide: Optional[FeatureGuide] = Field(
        default=None, 
        description="Mobile-friendly structured guide to the feature (if requested)"
    )