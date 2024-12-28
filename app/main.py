from fastapi import FastAPI
from .config import get_settings
from .database import engine, Base
from .routers import posts, users, auth

# Settings
settings = get_settings()

# FastAPI app and routers
social_app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
)
social_app.include_router(posts.router)
social_app.include_router(users.router)
social_app.include_router(auth.router)
# Database
Base.metadata.create_all(bind=engine)


@social_app.get("/")
def hello():
    return {"message": "Hello World"}
