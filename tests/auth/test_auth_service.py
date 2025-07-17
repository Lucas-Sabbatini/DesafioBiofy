import pytest
import jwt
from fastapi import HTTPException
from app.auth.service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_user_by_username
)
from app.config import settings

def test_authenticate_user_success(db_session, test_user):
    """Testa a autenticação bem-sucedida de um usuário."""
    authenticated_user = authenticate_user(db_session, "testuser", "testpassword")
    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"


def test_authenticate_user_failure(db_session, test_user):
    """Testa a falha na autenticação com senha incorreta."""
    authenticated_user = authenticate_user(db_session, "testuser", "wrongpassword")
    assert authenticated_user is None


def test_get_user_by_username(db_session, test_user):
    """Testa a busca de um usuário pelo nome de usuário."""
    user = get_user_by_username(db_session, "testuser")
    assert user is not None
    assert user.id == test_user.id


def test_create_access_token():
    """Testa a criação de um token de acesso JWT."""
    token_data = {"sub": "testuser"}
    token = create_access_token(data=token_data)

    decoded_token = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded_token["sub"] == "testuser"
    assert "exp" in decoded_token

@pytest.mark.asyncio
async def test_get_current_user_success(db_session, test_user, auth_token):
    """Testa a obtenção do usuário atual a partir de um token válido."""
    current_user = await get_current_user(auth_token, db_session)
    assert current_user is not None
    assert current_user.username == test_user.username

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(db_session):
    """Testa a falha ao tentar obter um usuário com um token inválido."""
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalidtoken", db_session,)
    assert exc_info.value.status_code == 401
