import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    AZURE_CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")
    AZURE_CLIENT_SECRET: str = os.getenv("AZURE_CLIENT_SECRET", "")
    AZURE_TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")

    VISION_ENDPOINT: str = os.getenv("VISION_ENDPOINT", "")
    VISION_KEY: str = os.getenv("VISION_KEY", "")

settings = Settings()
    