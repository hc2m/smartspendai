from fastapi import APIRouter, Request, Depends, Response
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from jose import jwt
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from app.utils.jwt_handler import create_access_token

import os
from dotenv import load_dotenv

load_dotenv()
IS_PRODUCTION = os.getenv("ENV") == "production"

router = APIRouter()

oauth = OAuth()

oauth.register(
    name="google",
    client_id = os.getenv("GOOGLE_CLIENT_ID"),
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs = {"scope":"openid email profile"}
)

# //smartspend-ai-68ou.onrender.com

# step 1: Redirect user to google
@router.get("/auth/google")
async def login_google(request: Request):
    redirect_uri = "https://api.smartspendai.org/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

# step 2: callback from google
@router.get("/auth/google/callback")
async def auth_google(request: Request, response: Response, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    email = user_info["email"]
    name = user_info["name"]
    picture = user_info["picture"]

    # check user exists
    user = db.query(User).filter(User.email == email).first()

    if not user:
        # ➕ create user
        user = User(
            email = email,
            username = name,
            provider = "google",
            picture = picture
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # create 🔑 jwt using handler 
    access_token = create_access_token({"user_id":user.id, "email": user.email})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="none" if IS_PRODUCTION else "lax",
        max_age=3600,
        domain=".smartspendai.org" if IS_PRODUCTION else None,
        path="/"
    )

    return{
        # "access_token": access_token,
        # "token_type": "brearer",
        "user_info":{
            "email": user.email,
            "name": user.username,
            "picture":user.picture
        }
    }