from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import PostCreate, PostResponse, UserCreate, UserResponse
from .config import get_settings
from .database import engine, Base, get_db, PostDB, UserDB
from .utils import hash

settings = get_settings()

social_app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
)

Base.metadata.create_all(bind=engine)


@social_app.get("/")
def hello():
    return {"message": "Hello World"}
