from pydantic import BaseModel
from typing import Optional


class IncomeCreate(BaseModel):
    source: str
    amount: float
    date: str
    note: Optional[str] = ""