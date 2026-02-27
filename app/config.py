from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    qdrant_url: str
    collection_name: str
    vector_size: int
    distance: str

    class Config:
        env_file = BASE_DIR / ".env"

settings = Settings()