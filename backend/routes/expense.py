from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.expense import add_expense, get_expenses
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/")
def create_expense(
    payload: dict,
    db: Session = Depends(get_db)
):
    return add_expense(payload, db)


@router.get("/{group_id}")
def list_expenses(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_expenses(group_id, db)

@router.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).get(expense_id)
    db.delete(expense)
    db.commit()
    return {"success": True}


@router.put("/expenses/{expense_id}")
def update_expense(expense_id: int, payload: dict, db: Session = Depends(get_db)):
    expense = db.query(Expense).get(expense_id)
    expense.description = payload["description"]
    expense.amount = payload["amount"]
    db.commit()
    return {"success": True}
