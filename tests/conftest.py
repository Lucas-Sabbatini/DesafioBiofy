import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from typing import Generator

# Importações do seu projeto
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.auth.utils import get_password_hash
from app.auth.service import create_access_token

# URL do banco de dados de teste (SQLite em memória)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Cria a engine do SQLAlchemy para o banco de teste
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Cria uma sessão de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas no banco de dados em memória
Base.metadata.create_all(bind=engine)

def override_get_db():
    """
    Função para sobrescrever a dependência get_db do FastAPI.
    Isso garante que os endpoints da API usem o banco de dados de teste em memória.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Aplica a sobrescrita da dependência na aplicação FastAPI
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Fixture do Pytest para fornecer uma sessão de banco de dados limpa para cada teste.
    Limpa as tabelas após cada teste para garantir isolamento.
    """
    # Cria as tabelas antes de cada teste
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Remove todas as tabelas após cada teste
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Fixture do Pytest para fornecer um TestClient para a aplicação.
    É executado uma vez por módulo de teste.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def test_user(db_session):
    """
    Fixture para criar um usuário de teste no banco de dados.
    """
    user = User(
        username="testuser",
        hashed_password=get_password_hash("testpassword")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_token(test_user):
    """
    Fixture para gerar um token de autenticação para o usuário de teste.
    """
    return create_access_token(data={"sub": test_user.username})
