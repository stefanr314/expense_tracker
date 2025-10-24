import os
from datetime import datetime, timedelta, timezone

import dotenv
import jwt

dotenv.load_dotenv()

jwt_secret = os.getenv("SECRET_KEY", "secret")
jwt_algo = os.getenv("ALGORITHM", "HS256")
jwt_expire_time = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
jwt_refresh_secret = os.getenv("SECRET_REFRESH_KEY")
jwt_expire_refresh = float(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "1"))


def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    to_encode = {**data}
    if expires:
        expire = datetime.now(timezone.utc) + expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_expire_time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret, algorithm=jwt_algo)

    return encoded_jwt


def create_refresh_token(data: dict, expires: timedelta | None = None) -> str:
    to_encode = {**data}
    if expires:
        expire = datetime.now(timezone.utc) + expires
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=jwt_expire_refresh)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, jwt_refresh_secret, algorithm=jwt_algo)
    return encode_jwt


def decode_access_token(token: str):

    return jwt.decode(token, jwt_secret, algorithms=[jwt_algo])


def decode_refresh_token(token: str):
    return jwt.decode(token, jwt_refresh_secret, algorithms=[jwt_algo])
