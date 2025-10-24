from dataclasses import dataclass


@dataclass
class User:
    id: int | None
    email: str
    username: str
    hashed_password: str
    full_name: str
    refresh_token: str | None = None
