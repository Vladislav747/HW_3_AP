from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from models.user import User
from typing import Dict
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from utils_new.utils import generate_access_token
from schemas.user import (
    TokenResponse,
    UserCreateResponse,
    UserCreateRequest,
    UserAuthRequest,
    ErrorResponse
)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post(
    "/auth",
    response_model=TokenResponse,
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        403: {"model": ErrorResponse, "description": "Invalid credentials"}
    }
)
def auth(payload: UserAuthRequest, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.login == payload.login).first()
    duration_minutes_access_token = 5

    if current_user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Such login '{payload.login}' not found"
        )

    if current_user.password == payload.password:
        new_access_token = generate_access_token()
        current_user.access_token = new_access_token
        current_user.expires_at = str(datetime.utcnow() + timedelta(minutes=duration_minutes_access_token))
        db.commit()
        return {"access_token": new_access_token}

    raise HTTPException(
        status_code=403,
        detail="Invalid credentials"
    )


@router.post(
    "/create",
    response_model=UserCreateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Login already registered"}
    }
)
def auth(payload: UserCreateRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.login == payload.login).first():
        raise HTTPException(status_code=400, detail="Login already registered")

    access_token = generate_access_token()

    duration_minutes_access_token = 5

    new_user = User(
        login=str(payload.login),
        password=str(payload.password),
        access_token=str(access_token),
        expires_at=str(datetime.utcnow() + timedelta(minutes=duration_minutes_access_token))
    )

    db.add(new_user)
    db.commit()
    return {"login": payload.login, "access_token": access_token}


@router.get("/user_info/{username}")
def auth(payload: Dict, db: Session = Depends(get_db)):
    current_user = db.query(User).filter(User.login == payload['login']).first()

    return {"login": current_user.login, "password": current_user.password}
