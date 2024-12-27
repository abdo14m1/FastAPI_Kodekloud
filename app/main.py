from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import PostCreate, PostResponse, UserCreate, UserResponse
from .config import get_settings
from .database import engine, Base
from .routers import posts, users

# Settings
settings = get_settings()

# FastAPI app and routers
social_app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
)
social_app.include_router(posts.router)
social_app.include_router(users.router)

# Database
Base.metadata.create_all(bind=engine)


@social_app.get("/")
def hello():
    return {"message": "Hello World"}
