from typing import List
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from app import models, database

router = APIRouter()


@router.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=models.PostResponse
)
def create_post(post: models.PostCreate, db: Session = Depends(database.get_db)):
    new_post = database.PostDB(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts", response_model=List[models.PostResponse])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(database.PostDB).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found"
        )
    return posts


@router.get("/posts/{post_id}", response_model=models.PostResponse)
def get_post(post_id: int, db: Session = Depends(database.get_db)):
    post = db.query(database.PostDB).filter(database.PostDB.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(database.get_db)):
    query = db.query(database.PostDB).filter(database.PostDB.id == post_id)
    if query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {post_id} doesn't exist",
        )
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{post_id}", response_model=models.PostResponse)
def update_post(
    post_id: int,
    post_updated: models.PostCreate,
    db: Session = Depends(database.get_db),
):
    post_query = db.query(database.PostDB).filter(database.PostDB.id == post_id)
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
