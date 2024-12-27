from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import models, database, utils


router = APIRouter()


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=models.UserResponse
)
def create_user(user: models.UserCreate, db: Session = Depends(database.get_db)):
    new_user = database.UserDB(**user.model_dump())
    if (
        db.query(database.UserDB)
        .filter(database.UserDB.email == new_user.email)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    hashed_password = utils.hash_password(new_user.password)
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    return new_user


@router.get("/users/{id}", response_model=models.UserResponse)
def get_user(uid: int, db: Session = Depends(database.get_db)):
    user = db.query(database.UserDB).filter(database.UserDB.uid == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} doesn't exist",
        )
    return user
