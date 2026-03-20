from fastapi import FastAPI
from app.database.database import engine, Base
from app.routes import auth_routes, auth_google
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(title="SmartSpend AI")
app.include_router(auth_google.router)
app.add_middleware(
    SessionMiddleware,
    secret_key = os.getenv("SESSION_SECRET_KEY")
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind = engine)

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "SmartSpend Backend Running.."}