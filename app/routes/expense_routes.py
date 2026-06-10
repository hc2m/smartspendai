from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense_schema import ExpenseCreate
from app.utils.dependencies import get_current_user
from app.database.database import get_db

router = APIRouter(prefix="/expense", tags=["Expense"])

@router.post("/add")
def add_expense(data: ExpenseCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):

    if data.amount <= 0:
        return {"error": "Invalid amount"}
    
    expense = Expense(
        amount = data.amount,
        category = data.category,
        description = data.description,
        user_id = user.id
    )

    db.add(expense)
    db.commit()

    return {"message": "Expense added"}

