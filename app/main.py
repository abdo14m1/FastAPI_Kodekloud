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


@social_app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse
)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = PostDB(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@social_app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostDB).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found"
        )
    return posts


@social_app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    return post


@social_app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    query = db.query(PostDB).filter(PostDB.id == post_id)
    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@social_app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_updated: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(PostDB).filter(PostDB.id == post_id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    post_query.update(post_updated.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post


@social_app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserDB(**user.model_dump())
    if db.query(UserDB).filter(UserDB.email == new_user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    hashed_password = hash(new_user.password)
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    return new_user
