from pydantic_settings import BaseSettings
import os
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Headless CMS Engine"

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Postgres
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "cmsuser")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "cmspassword")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "cms_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    USE_SQLITE: bool = os.getenv("USE_SQLITE", "True") == "True"
    SQLITE_DB: str = "cms.db"
    
    @property
    def DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            return f"sqlite:///{self.SQLITE_DB}"
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "False") == "True"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-jwt-override-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MIN_PASSWORD_LENGTH: int = int(os.getenv("MIN_PASSWORD_LENGTH", "8"))
    ALLOW_PUBLIC_REGISTRATION: bool = os.getenv("ALLOW_PUBLIC_REGISTRATION", "False") == "True"

    DEFAULT_ADMIN_EMAIL: str = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@example.com")
    DEFAULT_ADMIN_PASSWORD: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "adminpass")
    DEFAULT_EDITOR_EMAIL: str = os.getenv("DEFAULT_EDITOR_EMAIL", "editor@example.com")
    DEFAULT_EDITOR_PASSWORD: str = os.getenv("DEFAULT_EDITOR_PASSWORD", "editorpass")
    SEED_DEFAULT_USERS: bool = os.getenv("SEED_DEFAULT_USERS", "True") == "True"

    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    
    # Uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")

    AUTO_CREATE_DB: bool = os.getenv("AUTO_CREATE_DB", "False") == "True"
    
    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
