from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Headless CMS Engine"
    
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
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-jwt-override-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    
    class Config:
        env_file = ".env"

settings = Settings()
