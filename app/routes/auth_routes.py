from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.password_hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

import time
from datetime import datetime, timedelta

# Brout force 

login_attempts = {}

MAX_ATTEMPTS = 5
BLOCK_TIME = 60   # sec

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter((User.email == user.email.lower()) | (User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail=f"User already exists please login with{existing_user.provider}")
    
    # fix later if not user.password return HTTPExpectation error (password must be filled)

    hashed = hash_password(user.password)

    new_user = User(username= user.username, email = user.email, password = hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}

@router.post("/login")
def login(user: UserLogin, db:Session = Depends(get_db)):

    email = user.email.lower()
    current_time = time.time()

    # Initialize tracking
    if email not in login_attempts:
        login_attempts[email] = {"count":0, "last_attempt": current_time}

    attempt = login_attempts[email]

    # Block if too many attempts
    if attempt["count"] >= MAX_ATTEMPTS:
        if current_time - attempt["last_attempt"] < BLOCK_TIME:
            raise HTTPException(status_code=429, detail=f"Too manny attempts. Try later ")
        else:
            # Reset after block time
            attempt["count"] = 0


    db_user = db.query(User).filter(User.email == user.email.lower()).first()

    if db_user.lock_until and db_user.lock_until > datetime.utcnow():
        raise HTTPException(status_code=403, detail="Account locked. Try later")

    if not db_user or not verify_password(user.password, db_user.password):
        if db_user:
            db_user.failed_attempts += 1

            if  db_user.failed_attempts >= MAX_ATTEMPTS:
                db_user.lock_until = datetime.utcnow() + timedelta(minutes= 5)
            
            db.commit()

        raise HTTPException(status_code= 400, detail="Invalid credentials")
    
    # Reset on success
    login_attempts[email] = {"count":0, "last_attempt": current_time}
    db_user.failed_attempts = 0
    db_user.lock_until = None
    db.commit()

    
    token = create_access_token({"user_id": db_user.id,"email": db_user.email})

    return {"access_token": token, "token_type": "bearer"}