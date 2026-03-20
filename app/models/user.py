from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP
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