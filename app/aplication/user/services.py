from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from app.aplication.user.dto import UserCreate
from app.domain.user.entities import User
from app.infrastructure.db.user_repo import UserRepository
from app.infrastructure.security.hashing import hash_password, verify_password
from app.infrastructure.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, data: UserCreate) -> User:
        hashed = hash_password(data.password)
        user_entity = User(
            id=None,
            username=data.username,
            email=data.email,
            hashed_password=hashed,
            full_name=data.full_name,
        )
        user_mapped = self.repo.save(user_entity)
        return user_mapped

    def login_user(self, data: OAuth2PasswordRequestForm):
        user = self.repo.get_by_email(
            data.username
        )  # OAuth2PasswordRequestForm uses 'username' field for email
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # NOTE sub has to be string
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        if user.id:
            self.repo.save_refresh_token(user_id=user.id, refresh_token=refresh_token)
        return access_token, refresh_token

    def refresh_access_token(self, refresh_token: str):
        try:
            refresh_token_payload = decode_refresh_token(refresh_token)
        except InvalidTokenError as e:
            print("Invalid refresh token provided. Error: ", e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_entity = self.repo.get_by_id(int(refresh_token_payload.get("sub")))
        if not user_entity or not user_entity.refresh_token == refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token validation failed",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # NOTE sub has to be string
        access_token = create_access_token({"sub": str(user_entity.id)})

        return access_token
