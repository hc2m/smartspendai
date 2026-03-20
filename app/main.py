from fastapi import FastAPI
from app.database.database import engine, Base
from app.routes import auth_routes
from starlette.middleware.sessions import SessionMiddleware
import os


app = FastAPI(title="SmartSpend AI")

app.add_middleware(
    SessionMiddleware,
    secret_key = os.getenv("SESSION_SECRET_KEY")
)

# this is importent after imddleware add then include_router
from app.routes import auth_google
app.include_router(auth_google.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind = engine)

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "SmartSpend Backend Running.."}