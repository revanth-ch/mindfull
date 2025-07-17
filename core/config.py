import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Pydantic model to manage application settings and environment variables.
    It automatically reads variables from the environment.
    """
    YOUTUBE_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
