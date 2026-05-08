from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "E-Commerce AI Support"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database Configuration (SQLite for local dev, PostgreSQL for production)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./ecommerce_ai.db"
    )
    SQLALCHEMY_ECHO: bool = False
    
    # Redis Configuration (optional)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_TTL: int = 3600  # 1 hour
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "False").lower() == "true"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.3
    
    # Pinecone Configuration
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX: str = os.getenv("PINECONE_INDEX", "ecommerce-faq")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east1-aws")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://yourdomain.com"
    ]
    
    # Monitoring
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    
    # AI Settings
    ESCALATION_CONFIDENCE_THRESHOLD: float = 0.6
    MAX_CONTEXT_ITEMS: int = 5
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
