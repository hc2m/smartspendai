# app/schemas/expense_schema.py

from pydantic import BaseModel
from typing import Optional


class ExpenseCreate(BaseModel):
    category: str
    amount: float
    date: Optional[str] = None
    note: Optional[str] = None