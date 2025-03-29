from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl, ValidationError
from typing import Dict

from database import get_db

from models.links import Link
from utils_new.utils import generate_short_code, is_valid_url
from datetime import datetime


router = APIRouter(
    prefix="/links",
    tags=["links"]
)


@router.post("/shorten")
def create_short_link(payload: Dict, db: Session = Depends(get_db)):
    try:
        is_url_valid = is_valid_url(payload['original_url'])
        if is_url_valid is False:
            return JSONResponse(status_code=422, content={"detail": "Invalid URL format - use right template like https://example.com or http://www.aa.com"})
        custom_alias = payload.get('custom_alias')
        if custom_alias is not None:
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
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Missing key: {str(e)} in payload"
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown error {str(e)}"
        )


# Поиск ссылки по оригинальному URL
@router.get("/search")
def search_link_by_url(
        original_url: str,
        db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.original_url == original_url).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"short_code": link.short_code}


# Удаление короткой ссылки
@router.delete("/{short_code}")
def delete_link(short_code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()

    return {"message": f"Link {short_code} deleted"}


# Обновить ссылку
@router.put("/{short_code}")
def update_link(short_code: str, new_url: Dict, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    # Проверяем, не истекло ли время жизни ссылки
    if link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link has expired and cannot be updated")

    link.original_url = str(new_url)
    db.commit()

    return {"message": "Link updated", "short_code": short_code, "new_url": new_url}


@router.get("/expired")
def get_expired_links(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    expired_links = db.query(Link).filter(Link.expires_at < now).all()

    if not expired_links:
        return {"message": "No expired links found"}

    return [
        {
            "short_code": link.short_code,
            "original_url": link.original_url,
            "created_at": link.created_at,
            "expires_at": link.expires_at,
            "clicks": link.clicks_count,
            "last_clicked_at": link.last_clicked_at,
        }
        for link in expired_links
    ]


# Получить статистику по ссылке
@router.get("/{short_code}/stats")
def get_link_stats(short_code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return {
        "original_url": link.original_url,
        "created_at": link.created_at,
        "expires_at": link.expires_at,
        "clicks_count": link.clicks_count,
        "last_clicked_at": link.last_clicked_at
    }


@router.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    # Проверяем, не истекло ли время жизни ссылки
    if link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link has expired")

    link.clicks_count += 1
    link.last_clicked_at = datetime.utcnow()
    db.commit()

    return RedirectResponse(url=link.original_url, status_code=302)