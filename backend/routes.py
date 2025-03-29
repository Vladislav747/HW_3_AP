from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl, ValidationError
from typing import Dict

from models.models import Link
from utils_new.utils import generate_short_code
from database import get_db

router = APIRouter()

# Создание короткой ссылки
@router.post("/links/shorten")
def create_short_link(payload: Dict, db: Session = Depends(get_db)):
    try:
        if payload['custom_alias'] is not None:
            short_code = payload['custom_alias']

            link = db.query(Link).filter(Link.short_code == short_code).first()

            if link is not None:
                raise HTTPException(
                    status_code=422,
                    detail=f"Duplicate alias '{short_code}' already exists. Please choose a different alias."""
                )

        else:
            short_code = generate_short_code()

        db_link = Link(
            original_url=str(payload['original_url']),
            short_code=short_code,
        )

        db.add(db_link)
        db.commit()
        return {"short_code": short_code}

    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid URL"
        )
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Missing 'original_url' in payload"
        )


# Поиск ссылки по оригинальному URL
@router.get("/links/search")
def search_link_by_url(
        original_url: str,
        db: Session = Depends(get_db)):

    link = db.query(Link).filter(Link.original_url == original_url).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"short_code": link.short_code}


# Удаление короткой ссылки
@router.delete("/links/{short_code}")
def delete_link(short_code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()

    return {"message": f"Link {short_code} deleted"}


@router.put("/links/{short_code}")
def update_link(short_code: str, new_url: HttpUrl, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    link.original_url = str(new_url)  # Сохраняем новый URL
    db.commit()

    return {"message": "Link updated", "short_code": short_code, "new_url": new_url}


@router.get("/links/{short_code}/stats")
def get_link_stats(short_code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"original_url": link.original_url}
