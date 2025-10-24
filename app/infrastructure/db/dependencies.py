from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.user_repo import UserRepository

from .database import SessionLocal


# Provider of db connection, used only by repo
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repo(db: Annotated[Session, Depends(get_db)]):
    return UserRepository(db=db)
