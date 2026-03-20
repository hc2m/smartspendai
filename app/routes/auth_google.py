from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
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
async def auth_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")

    return {"email": user["email"], "name": user["name"], "picture": user["picture"]}