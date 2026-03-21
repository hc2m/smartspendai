from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.auth_routes import get_db
from app.models.user import User
from app.utils.otp import generate_otp
from app.utils.email import send_otp_email
from app.utils.hash import hash_otp
from app.schemas.auth_schema import ForgotPasswordRequest,VerifyOtpRequest,ResetPasswordRequest

from app.utils.password_hash import hash_password


router = APIRouter()

@router.post("/auth/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if user:
        otp = generate_otp()
        hashed = hash_otp(otp=otp)

        user.reset_otp = hashed
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        db.commit()

        send_otp_email(data.email,otp)

        print("Sending OTP to", data.email)
        print("OTP", otp)  # remove it letter 
    
    return({"message": "If email exists, OTP sent"}) 

@router.post("/auth/verify-otp")
def verify_otp(data:VerifyOtpRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not user.reset_otp:
        return {"error": "Invalid request"}
    
    if datetime.utcnow() > user.otp_expiry:
        return {"error": "OTP expired"}
    
    if hash_otp(data.otp) != user.reset_otp:
        return {"error": "Invalid OTP"}
    
    return {"message": "OTP verified"}

@router.post("/auth/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return {"error": "Invalid request"}
    
    user.password = hash_password(password=data.new_password)

    # Delete OTP after use

    user.reset_otp = None
    user.otp_expiry = None

    db.commit()
    
    return {"message": "Password reset successful"}

