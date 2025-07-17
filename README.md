YouTube Recommender API
This project provides a FastAPI backend that analyzes a user's text input to determine their emotional state and key concerns, then recommends relevant YouTube videos to help them.

Features
Emotion Analysis: Uses a transformers model to detect emotions from text.

Keyword Extraction: Uses KeyBERT to find the most relevant keywords.

YouTube Recommendations: Queries the YouTube API for helpful videos based on the analysis.

Asynchronous API: Built with FastAPI for high performance.

Setup & Installation
1. Clone the Repository
git clone <your-repo-url>
cd youtube-recommender

2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

On Windows:

python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install all required packages from the requirements.txt file.

pip install -r requirements.txt

4. Configure Environment Variables
The application requires a YouTube Data API v3 key.

Create a file named .env in the root of the project.

Add your API key to this file:

YOUTUBE_API_KEY="YOUR_ACTUAL_YOUTUBE_API_KEY"

Security Note: The .env file is included in .gitignore to prevent you from accidentally committing your secret API key to version control.

Running the Application
Once the setup is complete, you can run the application using uvicorn, a lightning-fast ASGI server.

uvicorn main:app --reload

main: Refers to the main.py file.

app: Refers to the FastAPI() object created inside main.py.

--reload: This flag makes the server restart automatically after you change the code.

The API will be available at http://127.0.0.1:8000.

Using the API
You can access the interactive API documentation by navigating to http://127.0.0.1:8000/docs in your browser.

From there, you can make requests directly to the /analyze-and-recommend endpoint to test its functionality.