from fastapi import FastAPI
from app.database.database import engine, Base
from app.routes import auth_routes
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI(title="SmartSpend AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://smartspendai.org",
        "https://www.smartspendai.org"

    ],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    SessionMiddleware,
    secret_key = os.getenv("SESSION_SECRET_KEY")
)

# this is importent after imddleware add then include_router
from app.routes import auth_google,auth,income_routes,expense_routes
app.include_router(auth_google.router)
app.include_router(auth.router)
app.include_router(income_routes.router)
app.include_router(expense_routes.router)


@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind = engine)
        print("Database connected")
    except Exception as e:
        print("Database connection faild:", e)

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "SmartSpend Backend Running.."}