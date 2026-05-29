from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1 import auth, collections, content, media
from app.db.session import Base, engine, SessionLocal
from app.db import models
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Headless CMS Engine API", version="1.0.0")

@app.on_event("startup")
def seed_users():
    db: Session = SessionLocal()
    try:
        admin_exists = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if not admin_exists:
            admin_user = models.User(
                email="admin@example.com",
                hashed_password=get_password_hash("adminpass"),
                role="Admin"
            )
            db.add(admin_user)
            db.commit()
            print("Seeded default admin user: admin@example.com / adminpass")

        editor_exists = db.query(models.User).filter(models.User.email == "editor@example.com").first()
        if not editor_exists:
            editor_user = models.User(
                email="editor@example.com",
                hashed_password=get_password_hash("editorpass"),
                role="Editor"
            )
            db.add(editor_user)
            db.commit()
            print("Seeded default editor user: editor@example.com / editorpass")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(collections.router, prefix="/api/v1/collections", tags=["collections"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(media.router, prefix="/api/v1/media", tags=["media"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
