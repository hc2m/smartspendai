from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.income import Income
from app.schemas.income_schema import IncomeCreate
from app.utils.dependencies import get_db, get_current_user

router = APIRouter(prefix="/income", tags=["Income"])

@router.post("/add")
def add_income(data: IncomeCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):

    if data.amount <= 0:
        return {"error": "Invalid amout"}

    income = Income(
        amount = data.amount,
        user_id = user.id
    )

    db.add(income)
    db.commit()

    return {"message": "Income added"}

