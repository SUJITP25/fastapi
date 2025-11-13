from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from config.config import Config
import uuid
import logging

password_context = CryptContext(schemes=["bcrypt"])


def generate_password_hash(password: str) -> str:
    hashed_password = password_context.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def cerate_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data

    payload["jti"] = str(uuid.uuid4())

    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=3600)
    )

    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_dict = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=Config.JWT_ALGORITHM
        )
        return token_dict
    except jwt.PyJWTError as e: 
        logging.exception(e)
        return None
        
        
