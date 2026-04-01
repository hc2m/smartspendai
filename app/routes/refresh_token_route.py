from fastapi import APIRouter , Response, Cookie, HTTPException
from jose import jwt
from app.utils.jwt_handler import create_access_token

import os
from dotenv import load_dotenv

load_dotenv()

IS_PRODUCTION = os.getenv("ENV") == "production"

SECRET_KEY = "supersecretkey"   # remove
ALGORITHM = "HS256"

router = APIRouter()

@router.post("/auth/refresh")
def refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token: 
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(refresh_token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")

    except:
        raise HTTPException(status_code=401, detail= "Invalid refresh token")
    
    new_access_token = create_access_token({"user_id": user_id, "email": email})

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="none" if IS_PRODUCTION else "lax",
        max_age=900,
        domain=".smartspendai.org" if IS_PRODUCTION else None,
        path="/"
    )

    return {"message": "Access token refreshed"}



