from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.database.database import Base

class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    user_id = Column(Integer, ForeignKey("users.id"))