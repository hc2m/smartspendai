from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.dependencies import get_db, get_current_user
from app.services.analytics_service import (
    get_dashboard_data,
    get_category_expense,
    get_monthly_expense
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db),
                      user = Depends(get_current_user)):

    return get_dashboard_data(db, user.id)


@router.get("/category")
def category_data(db: Session = Depends(get_db),
                  user = Depends(get_current_user)):

    return get_category_expense(db, user.id)


@router.get("/monthly")
def monthly_data(db: Session = Depends(get_db),
                 user = Depends(get_current_user)):

    return get_monthly_expense(db, user.id)