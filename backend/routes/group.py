from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.group import get_groups, create_group
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/")
def fetch_groups(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_groups(db, user)


@router.post("/")
def add_group(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return create_group(payload, db, user)
