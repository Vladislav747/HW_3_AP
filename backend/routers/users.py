from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models.user import User
from typing import Dict
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from utils_new.utils import generate_access_token


router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/auth")
def auth(payload: Dict, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.login == payload['login']).first()

    if current_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Such login '{payload['login']}' not found"
        )

    if current_user.password == payload['password']:
        return {"access_token": current_user.access_token}

    raise HTTPException(
        status_code=403,
        detail="Invalid credentials"
    )


@router.post("/create")
def auth(payload: Dict, db: Session = Depends(get_db)):
    if db.query(User).filter(User.login == payload['login']).first():
        raise HTTPException(status_code=400, detail="Login already registered")

    access_token = generate_access_token()

    new_user = User(
        login=str(payload['login']),
        password=str(payload['password']),
        access_token=str(access_token),
        expires_at=str(datetime.utcnow() + timedelta(hours=1))
    )

    db.add(new_user)
    db.commit()
    return {"login": payload['login'], "access_token": access_token}


@router.get("/user_info/{username}")
def auth(payload: Dict, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.login == payload['login']).first()

    return {"login": current_user.login, "password": current_user.password}
