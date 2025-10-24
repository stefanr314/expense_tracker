from typing import Annotated, cast

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.aplication.user.dto import TokenData
from app.domain.user.entities import User
from app.infrastructure.db.dependencies import get_user_repo
from app.infrastructure.db.user_repo import UserRepository
from app.infrastructure.security.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# DI Producer as auth protection route, FastAPI takes care of exception routing
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_payload = decode_access_token(token)
        user_id = user_payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        user_id = cast(str, user_id)
        token_data = TokenData(id=user_id)
    except InvalidTokenError as e:
        print("Token decoding failed:", e)
        raise credentials_exception
    user = repo.get_by_id(id=int(token_data.id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
