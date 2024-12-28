from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database, utils

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

    jwt_token = utils.create_access_token({"user_id": user.uid})
    return {"access_token": jwt_token, "token_type": "bearer"}
