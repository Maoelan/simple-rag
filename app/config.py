from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    qdrant_url: str
    collection_name: str
    vector_size: int
    distance: str

    class Config:
        env_file = "../.env"

settings = Settings()