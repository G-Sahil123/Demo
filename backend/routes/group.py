from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.group import get_groups, create_group
from app.auth import get_current_user

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("/")
def fetch_groups(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_groups(db, user)


@router.post("/")
def add_group(
    payload: dict,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_group(payload, db, user)
