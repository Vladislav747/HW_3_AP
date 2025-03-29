from sqlalchemy import Column, String, DateTime, Integer

from datetime import datetime
from models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
