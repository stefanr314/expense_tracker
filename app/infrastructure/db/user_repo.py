# infrastructure/db/repositories.py
from sqlalchemy.orm import Session

from app.domain.user.entities import User
from app.infrastructure.db.models import UserDBModel


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        db_user = UserDBModel(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            refresh_token=user.refresh_token,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        # map from DB user to entity user
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            full_name=db_user.full_name,
            refresh_token=db_user.refresh_token,
        )

    def save_refresh_token(self, user_id: int, refresh_token: str):
        db_user = self.db.query(UserDBModel).filter(UserDBModel.id == user_id).first()
        if not db_user:
            return None

        db_user.refresh_token = refresh_token
        self.db.commit()
        self.db.refresh(db_user)

    def get_by_email(self, email: str) -> User | None:
        db_user = self.db.query(UserDBModel).filter(UserDBModel.email == email).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            full_name=db_user.full_name,
            refresh_token=db_user.refresh_token,
        )

    def get_by_id(self, id: int) -> User | None:
        db_user = self.db.query(UserDBModel).filter_by(id=id).first()
        if not db_user:
            return None
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            full_name=db_user.full_name,
            refresh_token=db_user.refresh_token,
        )
