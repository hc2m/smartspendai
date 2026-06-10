from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.schemas.expense_schema import ExpenseCreate
from app.utils.dependencies import get_current_user
from app.database.database import get_db

router = APIRouter(
    prefix="/expense",
    tags=["Expense"]
)


# ==============================
# ADD EXPENSE
# ==============================

@router.post("/")
def add_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid amount"
        )

    expense = Expense(
        category=data.category,
        amount=data.amount,
        date=data.date,
        note=data.note,
        user_id=user.id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return {
        "message": "Expense added",
        "data": {
            "id": expense.id,
            "category": expense.category,
            "amount": expense.amount,
            "date": expense.date,
            "note": expense.note
        }
    }


# ==============================
# GET ALL EXPENSES
# ==============================

@router.get("/")
def get_expenses(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    expenses = db.query(Expense).filter(
        Expense.user_id == user.id
    ).all()

    return {
        "data": expenses
    }