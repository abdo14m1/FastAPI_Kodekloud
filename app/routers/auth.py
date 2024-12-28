from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database
from app import utils

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: models.UserLogin, db: Session = Depends(database.get_db)):
    user = (
        db.query(database.UserDB)
        .filter(database.UserDB.email == user_credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )
    # TODO: Create a token for verified users
    return {"token"}
