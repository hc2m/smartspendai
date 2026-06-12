from fastapi import APIRouter, Depends
from app.utils.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.models.income import Income
from app.models.expense import Expense

from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/transactions")
def get_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incomes = db.query(Income)\
    .filter(Income.user_id == current_user.id)\
    .all()

    expenses = db.query(Expense)\
    .filter(Expense.user_id == current_user.id)\
    .all()

    transactions = []

    for income in incomes:
        transactions.append({
            "id": income.id,
            "type": "income",
            "title": income.source,
            "amount": income.amount,
            "note": income.note,
            "date": income.created_at
        })

    for expense in expenses:
        transactions.append({
            "id": expense.id,
            "type": "expense",
            "title": expense.category,
            "amount": expense.amount,
            "note": expense.note,
            "date": expense.created_at
        })

    transactions.sort(
    key=lambda x: x["date"],
    reverse=True
    )

    return transactions