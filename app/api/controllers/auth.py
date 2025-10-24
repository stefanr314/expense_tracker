from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.aplication.user.dependencies import get_user_service
from app.aplication.user.dto import UserCreate
from app.aplication.user.response import TokenResponse, UserPublic
from app.aplication.user.services import UserService
from app.domain.user.entities import User
from app.infrastructure.security.dependencies import get_current_user

ServiceInstance = Annotated[UserService, Depends(get_user_service)]

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserPublic)
def register_user_route(data: UserCreate, service: ServiceInstance):
    user_entity = service.register_user(data=data)
    # FastAPI does automatic conversion to response model
    return UserPublic.model_validate(user_entity.__dict__)


@router.post("/login", response_model=TokenResponse)
def login_user_route(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: ServiceInstance,
    response: Response,
):
    access_token, refresh_token = service.login_user(data)

    # NOTE set the max_age with env sometime, set just for local testing currently
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/auth/refresh",  # send only to this endpoint
    )

    print("Login successful, access token generated." + access_token)
    return {"access_token": access_token}


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(
    refresh_token: Annotated[str | None, Cookie()], service: ServiceInstance
):
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Token not provided correctly.")
    access_token = service.refresh_access_token(refresh_token=refresh_token)
    return {"access_token": access_token}


@router.get("/me", response_model=UserPublic)
def get_me_route(current_user: Annotated[User, Depends(get_current_user)]):
    # DTO mapping, with dunder types
    return UserPublic.model_validate(current_user.__dict__)
