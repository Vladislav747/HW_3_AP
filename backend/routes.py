from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl, ValidationError
from datetime import datetime
from typing import Dict

from models.models import LinkCreate
from utils_new.utils import generate_short_code
from database import get_db

router = APIRouter()


# Модель для хранения информации о ссылке
class Link(BaseModel):
    original_url: HttpUrl
    short_code: str


# Хранение данных в памяти (в реальном приложении используйте базу данных)
links_db: Dict[str, Link] = {}


# Создание короткой ссылки
@router.post("/links/shorten")
def create_short_link(payload: Dict, db: Session = Depends(get_db)):
    try:
        short_code = generate_short_code()
        link_for_local = Link(
            original_url=HttpUrl(payload['original_url']),
            short_code=short_code,
        )
        links_db[short_code] = link_for_local
        db_link = LinkCreate(
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
def search_link_by_url(original_url: HttpUrl = Query(..., description="Original URL to search for")):
    for link in links_db.values():
        if link.original_url == original_url:
            return {"short_code": link.short_code}
    raise HTTPException(status_code=404, detail="Link not found")


# Перенаправление по короткой ссылке
@router.get("/links/{short_code}")
def redirect_to_original(short_code: str):
    if short_code not in links_db:
        raise HTTPException(status_code=404, detail="Link not found")

    link = links_db[short_code]
    if link.expires_at and link.expires_at < datetime.now():
        raise HTTPException(status_code=410, detail="Link has expired")

    link.clicks += 1
    link.last_clicked_at = datetime.now()
    return {"redirect_to": link.original_url}


# Удаление короткой ссылки
@router.delete("/links/{short_code}")
def delete_link(short_code: str):
    if short_code not in links_db:
        raise HTTPException(status_code=404, detail="Link not found")

    del links_db[short_code]
    return {"message": f"Link {short_code} deleted"}


# Обновление URL для короткой ссылки
@router.put("/links/{short_code}")
def update_link(short_code: str, new_url: HttpUrl):
    if short_code not in links_db:
        raise HTTPException(status_code=404, detail="Link not found")

    link = links_db[short_code]
    link.original_url = new_url
    return {"message": "Link updated", "short_code": short_code, "new_url": new_url}


# Получение статистики по короткой ссылке
@router.get("/links/{short_code}/stats")
def get_link_stats(short_code: str):
    print(links_db.items())
    if short_code not in links_db:
        raise HTTPException(status_code=404, detail="Link not found")

    link = links_db[short_code]
    return {
        "original_url": link.original_url,
    }
