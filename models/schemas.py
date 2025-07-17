from pydantic import BaseModel, HttpUrl
from typing import List, Dict



class AnalysisRequest(BaseModel):
    """
    Defines the structure for the incoming request body.
    Requires a single 'text' field.
    """
    text: str



class Video(BaseModel):
    """
    Defines the structure for a single YouTube video recommendation.
    """
    title: str
    url: HttpUrl 

class AnalysisResponse(BaseModel):
    """
    Defines the structure for the final API response, combining
    analysis results with video recommendations.
    """
    core_emotion: str
    core_keywords: List[str]
    recommendations: Dict[str, List[Video]]
