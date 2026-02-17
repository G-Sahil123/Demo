from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

from app.database import get_db
from app.models import User
from app.schemas import GoogleAuthRequest
from app.auth import create_access_token
from app.config import GOOGLE_CLIENT_ID

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/google")
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        # ✅ 1. VERIFY GOOGLE TOKEN
        idinfo = id_token.verify_oauth2_token(
            payload.credential,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    # ✅ 2. TRUST ONLY GOOGLE DATA
    email = idinfo["email"]
    name = idinfo.get("name")
    google_id = idinfo["sub"]
    avatar = idinfo.get("picture")

    # ✅ 3. USER UPSERT
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            name=name,
            google_id=google_id,
            avatar=avatar
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # ✅ 4. ISSUE JWT
    token = create_access_token(
        data={"user_id": user.id},
        expires_delta=timedelta(days=7)
    )

    return {"token": token}
