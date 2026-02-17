from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Group
from app.auth import get_current_user
from app.schemas import GroupCreate

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("/")
def get_groups(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(Group).filter(Group.owner_id == user.id).all()


@router.post("/")
def create_group(
    payload: GroupCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    group = Group(name=payload.name, owner_id=user.id)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group
