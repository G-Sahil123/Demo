from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models import User
from app.schemas import GoogleAuthRequest
from app.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/google")
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    if not payload.email or not payload.googleId:
        raise HTTPException(status_code=400, detail="Invalid Google data")

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        user = User(
            google_id=payload.googleId,
            email=payload.email,
            name=payload.name,
            avatar=payload.avatar
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(
        data={"user_id": user.id},
        expires_delta=timedelta(days=7)
    )

    return {"token": token}
