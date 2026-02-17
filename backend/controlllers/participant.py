from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Participant, Group
from app.schemas import ParticipantCreate

router = APIRouter(prefix="/participants", tags=["Participants"])

@router.get("/{group_id}")
def get_participants(group_id: int, db: Session = Depends(get_db)):
    return db.query(Participant)\
        .filter(Participant.group_id == group_id)\
        .all()


@router.post("/{group_id}")
def add_participant(
    group_id: int,
    payload: ParticipantCreate,
    db: Session = Depends(get_db)
):
    participant = Participant(group_id=group_id, name=payload.name)
    db.add(participant)

    group = db.query(Group).filter(Group.id == group_id).first()
    group.participants.append(participant)

    db.commit()
    return participant
