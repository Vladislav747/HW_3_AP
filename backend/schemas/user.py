from pydantic import BaseModel, Field, EmailStr


class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")


class UserInfoResponse(BaseModel):
    login: str = Field(..., example="john_doe")


class UserCreateResponse(UserInfoResponse):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")


class UserCreateRequest(BaseModel):
    login: str = Field(..., min_length=3, max_length=50, example="john_doe")
    password: str = Field(..., min_length=6, example="strongpassword")


class UserAuthRequest(BaseModel):
    login: str = Field(..., example="john_doe")
    password: str = Field(..., example="strongpassword")


class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Error message")