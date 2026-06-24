from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.income import Income
from app.models.expense import Expense

def get_dashboard_data(db: Session, user_id: int):

    total_income = db.query(func.sum(Income.amount))\
        .filter(Income.user_id == user_id).scalar() or 0

    total_expense = db.query(func.sum(Expense.amount))\
        .filter(Expense.user_id == user_id).scalar() or 0

    savings = total_income - total_expense

    if total_income > 0:
        savings_percent = (savings / total_income) * 100
    else:
        savings_percent = 0

    recent_expenses = db.query(Expense)\
    .filter(Expense.user_id == user_id)\
    .all()

    recent_income = db.query(Income)\
    .filter(Income.user_id == user_id)\
    .all()

    transactions = []

    for e in recent_expenses:
        transactions.append({
            "type": "expense",
            "title": e.category,
            "amount": e.amount,
            "created_at": e.created_at
        })

    for i in recent_income:
        transactions.append({
            "type": "income",
            "title": i.source,
            "amount": i.amount,
            "created_at": i.created_at
        })

    transactions.sort(
    key=lambda x: x["created_at"],
    reverse=True
    )

    # last_transactions = transactions[:5]

    return {
        "totalIncome": total_income,
        "totalExpense": total_expense,
        "savings": savings,
        "totalBalance": total_income - total_expense,
        # "last_transactions": last_transactions
    }


def get_category_expense(db: Session, user_id: int):

    data = db.query(
        Expense.category,
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id
    ).group_by(
        Expense.category
    ).all()

    return data

def get_monthly_expense(db: Session, user_id: int):

    data = db.query(
        func.extract('month', Expense.created_at).label("month"),
        func.sum(Expense.amount).label("total")
    ).filter(
        Expense.user_id == user_id
    ).group_by(
        func.extract('month', Expense.created_at)
    ).order_by(
        func.extract('month', Expense.created_at)
    ).all()

    return [
        {
            "month": int(month),
            "amount": float(total)
        }
        for month, total in data
    ]