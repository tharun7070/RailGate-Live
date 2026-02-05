import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./railgate.db"
    
    # Railway API
    RAIL_API_KEY: Optional[str] = None
    RAIL_API_BASE_URL: str = "https://indianrailapi.com/api/v2"
    
    # Demo Mode
    DEMO_MODE: bool = True
    
    # Server
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # Redis (optional)
    USE_REDIS: bool = False
    REDIS_URL: Optional[str] = None
    
    # Prediction Parameters
    BUFFER_MINUTES: float = 2.5  # Gate closes before train arrives
    AVG_CLOSE_DURATION: float = 8.0  # Average closure duration in minutes
    TRAIN_SPEED_KM_MIN: float = 0.8  # ~48 km/h average
    PREDICTION_WINDOW_MINUTES: int = 40  # How far ahead to predict
    CLOSING_SOON_THRESHOLD_MINUTES: int = 7  # "Closing soon" window
    
    # Scheduler
    AUTO_REFRESH_INTERVAL_SECONDS: int = 90  # Background update frequency
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
