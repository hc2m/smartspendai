from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.income import Income
from app.schemas.income_schema import IncomeCreate
from app.utils.dependencies import get_current_user
from app.database.database import get_db

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


# ==============================
# ADD INCOME
# ==============================

@router.post("/")
def add_income(
    data: IncomeCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    # validation
    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )

    income = Income(
        source=data.source,
        amount=data.amount,
        created_at=data.date,
        note=data.note,
        user_id=user.id
    )

    db.add(income)
    db.commit()
    db.refresh(income)

    return {
        "success": True,
        "message": "Income added successfully",
        "data": {
            "id": income.id,
            "source": income.source,
            "amount": income.amount,
            "date": income.created_at,
            "note": income.note
        }
    }


# ==============================
# GET ALL INCOME
# ==============================

@router.get("/")
def get_income(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):

    incomes = (
        db.query(Income)
        .filter(Income.user_id == user.id)
        .order_by(Income.id.desc())
        .all()
    )

    return {
        "success": True,
        "count": len(incomes),
        "data": incomes
    }