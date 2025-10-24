from pydantic import BaseModel

from app.aplication.user.dto import UserBase


class UserPublic(UserBase):
    id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
