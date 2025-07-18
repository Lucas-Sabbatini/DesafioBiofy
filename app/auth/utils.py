from jwt import InvalidTokenError
from passlib.context import CryptContext
from app.auth.exceptions import CredentialsException
from app.auth.schemas import TokenData
from app.config import settings
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def decode_token(token:str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise CredentialsException()
    except InvalidTokenError:
        raise CredentialsException()

    return TokenData(username=username)

def encode_token(to_encode : dict) -> str:
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )