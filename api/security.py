# TODO: add actual hashing

from secrets import token_hex


def hash_password(password: str) -> str:
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password


def create_access_token(*args, **kwargs):
    return token_hex(32)
