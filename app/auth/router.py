from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .exceptions import IncorrectUserException
from ..database import get_db
from . import service
from .schemas import Token

router = APIRouter(tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise IncorrectUserException()
    access_token = service.create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}