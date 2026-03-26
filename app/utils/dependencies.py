from fastapi import Depends, HTTPException, Cookie
# from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app.routes.auth_routes import get_db
from app.models.user import User

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):

    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")
        # print(payload)
        # print("user_id = ",user_id)
        # print(email)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter((User.id == user_id) & (User.email == email)).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user