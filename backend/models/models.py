from sqlalchemy import Column, String
from database import Base


class LinkCreate(Base):
    __tablename__ = "links"

    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
