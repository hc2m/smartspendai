from fastapi import FastAPI
from app.database.database import engine, Base
from app.routes import auth_routes

app = FastAPI(title="SmartSpend AI")

Base.metadata.create_all(bind = engine)

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "SmartSpend Backend Running.."}