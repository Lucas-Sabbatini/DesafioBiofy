from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from .exceptions import CredentialsException, InactiveUserException
from .. import models
from ..config import settings
from .utils import verify_password, decode_token, encode_token
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def authenticate_user(
        db: Session, username: str, password: str
) -> Optional[models.User]:
    user = get_user_by_username(db,username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(username : str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    data = {"sub": username, "exp": expire}

    return encode_token(data)


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return (
        db
        .query(models.User)
        .filter(models.User.username == username)
        .first()
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    token_data = decode_token(token)

    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise CredentialsException()
    if user.is_active is not True:
        raise InactiveUserException()

    return user
