from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str