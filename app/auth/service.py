from datetime import datetime, timedelta
from typing import Optional, Annotated
import jwt
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from .schemas import TokenData, User
from .. import models
from ..config import settings
from .utils import verify_password
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def authenticate_user(
        db: Session, username: str, password: str
) -> Optional[models.User]:
    user = get_user_by_username(db,username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return (
        db
        .query(models.User)
        .filter(models.User.username == username)
        .first()
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
