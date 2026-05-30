from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1 import auth, collections, content, media
from app.db.session import Base, engine, SessionLocal
from app.db import models
from app.core.security import get_password_hash
from app.core.config import settings
from app.core.cache import get_redis_client
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

def _seed_users(db: Session):
    if not settings.SEED_DEFAULT_USERS:
        return

    admin_exists = db.query(models.User).filter(models.User.email == settings.DEFAULT_ADMIN_EMAIL).first()
    if not admin_exists:
        admin_user = models.User(
            email=settings.DEFAULT_ADMIN_EMAIL,
            hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
            role="Admin"
        )
        db.add(admin_user)
        db.commit()
        print(f"Seeded default admin user: {settings.DEFAULT_ADMIN_EMAIL}")

    editor_exists = db.query(models.User).filter(models.User.email == settings.DEFAULT_EDITOR_EMAIL).first()
    if not editor_exists:
        editor_user = models.User(
            email=settings.DEFAULT_EDITOR_EMAIL,
            hashed_password=get_password_hash(settings.DEFAULT_EDITOR_PASSWORD),
            role="Editor"
        )
        db.add(editor_user)
        db.commit()
        print(f"Seeded default editor user: {settings.DEFAULT_EDITOR_EMAIL}")

# FIX 1: Replace deprecated @app.on_event("startup") with modern lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    db: Session = SessionLocal()
    try:
        if settings.AUTO_CREATE_DB:
            Base.metadata.create_all(bind=engine)
        _seed_users(db)
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()
    yield  # App runs while yielded

app = FastAPI(title="Headless CMS Engine API", version="1.0.0", lifespan=lifespan)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(collections.router, prefix="/api/v1/collections", tags=["collections"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(media.router, prefix="/api/v1/media", tags=["media"])

@app.get("/health")
def health_check():
    status = {"status": "ok", "db": "ok", "redis": "disabled"}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        status["db"] = "error"
        status["status"] = "degraded"

    client = get_redis_client()
    if client is not None:
        try:
            client.ping()
            status["redis"] = "ok"
        except Exception:
            status["redis"] = "error"
            status["status"] = "degraded"

    return status
