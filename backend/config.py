"""
Configuration management for Diligent-Jarvis
Uses Pydantic for strict typing and validation
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Diligent-Jarvis"
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    PORT: int = 5000
    HOST: str = "0.0.0.0"

    # Pinecone Settings
    PINECONE_API_KEY: str = ""
    PINECONE_INDEX_NAME: str = "jarvis-knowledge"
    PINECONE_CLOUD: str = "aws"
    PINECONE_REGION: str = "us-east-1" 

    # LLM Settings
    MODEL_PATH: str = "models/llama-2-7b-chat.gguf"
    MODEL_TYPE: str = "llama"
    MAX_TOKENS: int = 512
    TEMPERATURE: float = 0.7
    CONTEXT_WINDOW: int = 2048

    # Vector DB Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    TOP_K_RESULTS: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()