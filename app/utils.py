import subprocess
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

# Passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# OAuth Tokens
JWT_KEY = subprocess.run(
    ["openssl", "rand", "-hex", "32"], capture_output=True, text=True, check=False
).stdout
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(token_data: dict):
    to_encode = token_data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"iat": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt
