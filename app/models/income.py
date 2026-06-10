from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey,String,Text
from datetime import datetime
from app.database.database import Base

class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String(100))
    amount = Column(Float)

    created_at = Column(String(50))

    note = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id"))




