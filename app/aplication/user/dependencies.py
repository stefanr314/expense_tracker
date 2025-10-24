from typing import Annotated

from fastapi import Depends

from app.aplication.user.services import UserService
from app.infrastructure.db.dependencies import get_user_repo
from app.infrastructure.db.user_repo import UserRepository


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)
