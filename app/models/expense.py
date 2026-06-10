from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from datetime import datetime
from app.database.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())

    user_id = Column(Integer, ForeignKey("users.id"))