from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class ShortenLinkRequest(BaseModel):
    original_url: str = Field(..., example="https://example.com")
    custom_alias: Optional[str] = Field(None, min_length=3, max_length=32, example="my-link")


class ShortenLinkResponse(BaseModel):
    short_code: str = Field(..., example="abc123")


class LinkResponse(BaseModel):
    short_code: str = Field(..., example="abc123")
    new_url: str = Field(..., example="https://example.com")


class UpdateLinkRequest(BaseModel):
    new_url: str = Field(..., example="https://new-example.com")


class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Error message")


class LinkExpiredResponse(BaseModel):
    short_code: str = Field(
        ...,
        example="abc123",
        description="Короткий код ссылки"
    )
    original_url: str = Field(
        ...,
        example="https://example.com",
        description="Оригинальный URL"
    )
    created_at: datetime = Field(
        ...,
        example="2023-01-01T00:00:00Z",
        description="Дата создания ссылки"
    )
    expires_at: datetime = Field(
        ...,
        example="2023-02-01T00:00:00Z",
        description="Дата истечения срока действия"
    )
    clicks: int = Field(
        ...,
        example=42,
        description="Количество переходов по ссылке"
    )
    last_clicked_at:  Optional[datetime] = Field(
        ...,
        example="2023-02-01T00:00:00Z",
        description="Дата истечения срока действия"
    )


class LinkStatsResponse(BaseModel):
    original_url: str = Field(
        ...,
        example="https://example.com",
        description="Оригинальный URL"
    )
    created_at: datetime = Field(
        ...,
        example="2023-01-01T00:00:00Z",
        description="Дата создания ссылки"
    )
    expires_at: datetime = Field(
        ...,
        example="2023-02-01T00:00:00Z",
        description="Дата истечения срока действия"
    )
    clicks_count: int = Field(
        ...,
        example=42,
        description="Количество переходов по ссылке"
    )
    last_clicked_at:  Optional[datetime] = Field(
        ...,
        example="2023-02-01T00:00:00Z",
        description="Дата истечения срока действия"
    )