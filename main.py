import sys
import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 


try:
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    
    from models.schemas import AnalysisRequest, AnalysisResponse, Video
    from services.analysis import analyze_text
    from services.youtube import get_youtube_recommendations

except ImportError as e:
    
    print("---" * 20)
    print("FATAL: A module could not be imported. This is a common Python path issue.")
    print(f"Original Error: {e}")
    print("\nTroubleshooting Steps:")
    print(f"1. Make sure you are running the command from the correct directory:")
    print(f"   -> Your current directory: {os.getcwd()}")
    print(f"   -> It should be: {current_dir}")
    print("2. Ensure all required packages are installed by running:")
    print("   -> pip install -r requirements.txt")
    print("3. Check for typos in your directory or file names.")
    print("---" * 20)
    sys.exit(1)

app = FastAPI(
    title="Mental Wellness YouTube Recommender",
    description="Analyzes text to understand user's emotional state and recommends helpful YouTube videos.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.post("/analyze-and-recommend", response_model=AnalysisResponse)
async def analyze_and_recommend_videos(request: AnalysisRequest):
    """
    This endpoint performs two main tasks:
    1.  Analyzes the input text to extract a core emotion and keywords.
    2.  Fetches relevant YouTube videos based on the analysis.
    """
    try:

        primary_emotion, core_keywords = analyze_text(request.text)

        
        search_topics = core_keywords if core_keywords else [primary_emotion]
        
        
        tasks = []
        for topic in search_topics:
            
            query = f"how to overcome {topic} for students"
            tasks.append(get_youtube_recommendations(query, max_results=3))
        
        
        results_per_topic = await asyncio.gather(*tasks)

        
        recommendations = {
            topic: videos for topic, videos in zip(search_topics, results_per_topic)
        }

        return AnalysisResponse(
            core_emotion=primary_emotion,
            core_keywords=core_keywords,
            recommendations=recommendations
        )
        
    except Exception as e:
        
        print(f"An error occurred in the main endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal server error occurred. Please try again later."
        )

@app.get("/", include_in_schema=False)
async def root():
    """
    Redirects the root URL to the interactive API documentation.
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")
