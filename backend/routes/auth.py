from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth import google_auth

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/google")
def google_login(
    payload: dict,
    db: Session = Depends(get_db)
):
    return google_auth(payload, db)
