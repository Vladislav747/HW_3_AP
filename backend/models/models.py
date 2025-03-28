from sqlalchemy import Column, String

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LinkCreate(Base):
    __tablename__ = "links"

    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
