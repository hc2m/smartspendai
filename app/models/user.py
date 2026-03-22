from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP, DateTime
from app.database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key = True, index=True)
    username = Column(String,unique=True,nullable=False)
    email = Column(String, unique= True, index= True, nullable=False)
    password = Column(String, nullable=True)
    provider = Column(String, default="local")
    picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    failed_attempts = Column(Integer, default=0)
    lock_until = Column(TIMESTAMP,nullable=True)

    reset_otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)

    otp_verified = Column(Boolean, default=False)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(TIMESTAMP, nullable=True)
