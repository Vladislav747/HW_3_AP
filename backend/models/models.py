from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base

from datetime import datetime, timedelta

Base = declarative_base()


class Link(Base):
    __tablename__ = "links"

    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(minutes=5))
    clicks_count = Column(Integer, default=0)
    last_clicked_at = Column(DateTime, nullable=True)
