from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.participant import (
    add_participant,
    get_participants_by_group
)
from app.core.auth import get_current_user

router = APIRouter(
    prefix="/participants",
    tags=["Participants"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/{group_id}")
def create_participant(
    group_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):
    return add_participant(group_id, payload, db)


@router.get("/{group_id}")
def list_participants(
    group_id: int,
    db: Session = Depends(get_db)
):
    return get_participants_by_group(group_id, db)
