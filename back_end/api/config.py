"""
Configuration module for the application.
Loads environment variables and provides settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # PostgreSQL settings (primary)
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    # Backward compatibility
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_NAME: Optional[str] = None
    
    # Application settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8222
    DEBUG: bool = True
    
    # Testing
    TEST_DB_NAME: str = "office_db_test"
    RUN_MIGRATIONS_ON_STARTUP: bool = False
    
    # Extra field (for conda environment name, not used by app)
    CONDA_ENV: Optional[str] = None
    
    class Config:
        """Pydantic config."""
        extra = "ignore"  # Ignore extra fields from .env
    
    @property
    def database_url(self) -> str:
        """Get PostgreSQL connection URL."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def test_database_url(self) -> str:
        """Get test database connection URL."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.TEST_DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
