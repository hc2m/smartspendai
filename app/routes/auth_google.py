from fastapi import APIRouter, Request, Depends
from app.routes.auth_routes import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from jose import jwt
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from app.utils.jwt_handler import create_access_token
import os

router = APIRouter()

oauth = OAuth()

oauth.register(
    name="google",
    client_id = os.getenv("GOOGLE_CLIENT_ID"),
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs = {"scope":"openid email profile"}
)

# step 1: Redirect user to google
@router.get("/auth/google")
async def login_google(request: Request):
    redirect_uri = "https://smartspend-ai-68ou.onrender.com/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

# step 2: callback from google
@router.get("/auth/google/callback")
async def auth_google(request: Request, db: Session = Depends(get_db)):
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
    access_token = create_access_token({"sub":user.email})

    return{
        "access_token": access_token,
        "token_type": "brearer",
        "user_info":{
            "email": user.email,
            "name": user.username,
            "picture":user.picture
        }
    }