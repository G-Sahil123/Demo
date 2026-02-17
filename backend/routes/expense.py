from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.expense import add_expense, get_expenses
from app.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/")
def create_expense(
    payload: dict,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return add_expense(payload, db)


@router.get("/{group_id}")
def list_expenses(
    group_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_expenses(group_id, db)
