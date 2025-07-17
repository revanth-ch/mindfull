import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from core.config import settings # Import settings to get the API key
from models.schemas import Video # Import the Pydantic model for type hinting

# --- YouTube Service Initialization ---
try:
    # Initialize the YouTube API client
    youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)
except Exception as e:
    print(f"Failed to initialize YouTube service: {e}")
    youtube = None

# A curated set of keywords to ensure recommendations are relevant and safe.
# This helps filter out unrelated or inappropriate content from search results.
ALLOWED_KEYWORDS = {
    # Core topics
    "focus", "study", "motivation", "discipline", "concentration", "productivity",
    
    # Mental health & emotional regulation
    "mental health", "mindset", "anxiety", "anxious", "calm", "cope", "overcome",
    "depression", "burnout", "nervousness", "stress", "panic", "relax",

    # Self-improvement & habit building
    "addiction", "dopamine", "habit", "routine", "lazy", "laziness", "confidence",
    "self-esteem", "procrastination", "energy", "sleep", "healthy",

    # Support & guidance
    "help", "advice", "support", "improve", "guide", "therapy", "healing", "recover"
}

def search_youtube_sync(query: str, max_results: int) -> list[Video]:
    """
    The synchronous function that performs the actual YouTube API call.
    This will be run in a separate thread to avoid blocking the main async event loop.
    """
    if not youtube:
        return []
        
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            videoCategoryId="27",  # Category for "Education"
            maxResults=max_results,
            safeSearch="strict"
        )
        response = request.execute()

        videos = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            # Filter results to ensure they are relevant
            if any(word in title.lower() for word in ALLOWED_KEYWORDS):
                video_id = item["id"]["videoId"]
                url = f"https://www.youtube.com/watch?v={video_id}"
                videos.append(Video(title=title, url=url))
        return videos
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during YouTube search: {e}")
        return []


async def get_youtube_recommendations(query: str, max_results: int = 3) -> list[Video]:
    """
    Asynchronously gets YouTube video recommendations.
    
    It runs the blocking, synchronous `search_youtube_sync` function in a 
    separate thread pool, allowing the FastAPI event loop to remain unblocked.
    """
    loop = asyncio.get_running_loop()
    videos = await loop.run_in_executor(
        None,  
        search_youtube_sync,
        query,
        max_results
    )
    return videos
