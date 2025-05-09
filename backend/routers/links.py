from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl, ValidationError
from typing import Dict, List, Union

from datetime import datetime

from database import get_db

from models.links import Link
from models.user import User

from utils_new.utils import generate_short_code, is_valid_url
from security.user import get_current_user
from cache import cache, invalidate_cache

from schemas.links import (
    ShortenLinkRequest,
    ShortenLinkResponse,
    ErrorResponse,
    LinkResponse,
    UpdateLinkRequest,
    LinkExpiredResponse,
    LinkStatsResponse
)

router = APIRouter(
    prefix="/links",
    tags=["links"]
)


@router.post(
    "/shorten",
    response_model=ShortenLinkResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        400: {"model": ErrorResponse, "description": "Bad request"}
    }
)
def create_short_link(
        payload: ShortenLinkRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        is_url_valid = is_valid_url(payload.original_url)
        if is_url_valid is False:
            return JSONResponse(status_code=422, content={"detail": "Invalid URL format - use right template like https://example.com or http://www.aa.com"})
        custom_alias = payload.custom_alias
        if custom_alias is not None:
            short_code = payload.custom_alias

            link = db.query(Link).filter(Link.short_code == short_code).first()

            if link is not None:
                raise HTTPException(
                    status_code=422,
                    detail=f"Duplicate alias '{short_code}' already exists. Please choose a different alias."""
                )

        else:
            short_code = generate_short_code()

        db_link = Link(
            original_url=str(payload.original_url),
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

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown error {str(e)}"
        )


# Поиск ссылки по оригинальному URL
@router.get(
    "/search",
    response_model=ShortenLinkResponse,
    responses={404: {"model": ErrorResponse}}
)
@cache(expire=300, prefix="links")
def search_link_by_url(
        original_url: str,
        db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.original_url == original_url).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"short_code": link.short_code}


# Удаление короткой ссылки
@router.delete("/{short_code}")
async def delete_link(
        short_code: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()

    await invalidate_cache("link", short_code)  # Удаляем кэш конкретной ссылки
    await invalidate_cache("links")  # Удаляем кэш всех ссылок

    return {"message": f"Link {short_code} deleted"}


# Обновить ссылку
@router.put(
    "/{short_code}",
    response_model=LinkResponse,
    responses={
        404: {"model": ErrorResponse},
        410: {"model": ErrorResponse}
    }
)
async def update_link(
        short_code: str,
        payload: UpdateLinkRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(Link.short_code == short_code).first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    # Проверяем, не истекло ли время жизни ссылки
    if link.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Link has expired and cannot be updated")

    link.original_url = str(payload.new_url)
    db.commit()

    await invalidate_cache("link", short_code)  # Удаляем кэш конкретной ссылки
    await invalidate_cache("links")  # Удаляем кэш всех ссылок

    return {"message": "Link updated", "short_code": short_code, "new_url": str(payload.new_url)}


@router.get(
    "/expired",
    response_model=Union[List[LinkExpiredResponse], Dict[str, str]],
)
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
@router.get(
    "/{short_code}/stats",
    response_model=LinkStatsResponse,
    responses={404: {"model": ErrorResponse}}
)
@cache(expire=300, prefix="links")
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