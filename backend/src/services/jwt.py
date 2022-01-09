from datetime import datetime, timedelta
from typing import Dict

from jose import jwt
from pydantic import ValidationError

from models.users import User, UserInJWT
from models.jwt import JWT as JWTModel


def create_jwt_token(
    *,
    jwt_content: Dict[str, str],
    secret_key: str,
    expires_delta: timedelta,
    jwt_subject: str,
    jwt_algorithm: str,
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    # print("expire = ", expire)
    to_encode.update(JWTModel(exp=expire, sub=jwt_subject).dict())
    return jwt.encode(to_encode, secret_key, algorithm=jwt_algorithm)


def create_access_token(user: User, config: dict) -> str:
    # print("config = ", config)
    return create_jwt_token(
        jwt_content=UserInJWT(username=user.username).dict(),
        secret_key=config['secret_key'],
        expires_delta=timedelta(seconds=int(
            config['jwt_access_token_expire'])),
        jwt_subject=config['jwt_subject'],
        jwt_algorithm=config['jwt_algorithm'],
    )
