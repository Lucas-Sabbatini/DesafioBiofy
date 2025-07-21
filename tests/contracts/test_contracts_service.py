import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException

from app.contracts.service import ContractService
from app.models import Contract


@pytest.fixture
def contract_service(db_session):
    """Fixture para criar uma instância de ContractService com uma sessão de db."""
    return ContractService(db_session)


def test_get_contract_by_name_success(contract_service, db_session):
    """Testa a busca de um contrato existente pelo nome."""
    contract = Contract(file_name="my_contract.pdf")
    db_session.add(contract)
    db_session.commit()

    found_contract = contract_service.get_contract_by_name(contract.file_name)
    assert found_contract is not None
    assert found_contract.file_name == "my_contract.pdf"


def test_get_contract_by_name_not_found(contract_service):
    """Testa a busca por um contrato que não existe."""
    with pytest.raises(HTTPException) as exc_info:
        contract_service.get_contract_by_name("non_existent.pdf")
    assert exc_info.value.status_code == 404
    assert "Contract" and  "not found" in exc_info.value.detail
