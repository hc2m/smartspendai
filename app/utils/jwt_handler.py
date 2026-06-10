from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"   # remove
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAY = 7

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAY)

    to_encode.update({"exp": expire})

    encoded_refersh_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)

    return encoded_refersh_jwt