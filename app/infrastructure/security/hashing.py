from pwdlib import PasswordHash

pwd_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hash.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    return pwd_hash.hash(plain_password)
