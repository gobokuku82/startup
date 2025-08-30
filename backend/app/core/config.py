"""
Application configuration
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Application
    APP_NAME: str = Field(default="StartupManager")
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    VERSION: str = Field(default="0.1.0")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-here-change-in-production")
    JWT_SECRET_KEY: str = Field(default="your-jwt-secret-key-here")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./data/sqlite/startup.db")
    DATABASE_ECHO: bool = Field(default=False)
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # OpenAI
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview")
    
    # LangSmith (Optional)
    LANGCHAIN_TRACING_V2: bool = Field(default=False)
    LANGCHAIN_API_KEY: Optional[str] = Field(default=None)
    LANGCHAIN_PROJECT: str = Field(default="startup-manager")
    
    # ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = Field(default="./data/chroma")
    CHROMA_COLLECTION_NAME: str = Field(default="policies")
    
    # Storage
    STORAGE_PATH: str = Field(default="./data/storage")
    MAX_FILE_SIZE_MB: int = Field(default=10)
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"]
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="./logs/app.log")
    
    # LangGraph
    LANGGRAPH_CHECKPOINT_DIR: str = Field(default="./data/checkpoints")
    LANGGRAPH_CACHE_TTL: int = Field(default=3600)  # 1 hour
    LANGGRAPH_MAX_RECURSION: int = Field(default=25)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()