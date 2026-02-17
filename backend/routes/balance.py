from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.balance import get_balances
from app.auth import get_current_user

router = APIRouter(prefix="/balances", tags=["Balances"])

@router.get("/analytics/{group_id}")
def balances(
    group_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_balances(group_id, db)
