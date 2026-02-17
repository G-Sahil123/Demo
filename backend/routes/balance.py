from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.balance import get_balances
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/balances",
    tags=["Balances"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/analytics/{group_id}")
def balances(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_balances(group_id, db)
