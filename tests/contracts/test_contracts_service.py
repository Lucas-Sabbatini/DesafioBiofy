import pytest
from unittest.mock import patch
from fastapi import UploadFile, HTTPException
import io

from app.contracts.service import ContractService
from app.models import Contract


@pytest.fixture
def contract_service(db_session):
    """Fixture para criar uma instância de ContractService com uma sessão de db."""
    return ContractService(db_session)


@pytest.mark.asyncio
@patch('app.contracts.service.extract_text_from_pdf')
@patch('app.contracts.service.process_contract_with_ai')
async def test_upload_and_process_contract(mock_process_ai, contract_service, db_session, mock_user):
    """
    Testa o fluxo completo de upload e processamento de um contrato.
    A chamada à IA é mockada.
    """
    # Configuração do Mock da IA
    ai_response_data = {
        "parties": ["Empresa A", "Empresa B"],
        "monetary_values": ["Valor A", "Valor B"],
        "main_obligations": ["Obrigacao A", "Obrigacao B"],
        "additional_data": {
            "objeto": "Objeto A",
            "vigencia": "Vigência A",
        },
        "termination_clause": "Cláusula de Rescisão A",
    }
    mock_process_ai.return_value = ai_response_data

    # Cria um arquivo em memória para simular o upload
    file_content = b"dummy pdf content %%EOF"
    file = io.BytesIO(file_content)
    upload_file = UploadFile(filename="new_contract.pdf", file=file)

    # Execução
    result = await contract_service.upload_and_process_contract(upload_file)

    # Verificações
    mock_process_ai.assert_called_once()
    assert result.file_name == "new_contract.pdf"
    assert result.contract_data.parties == ["Empresa A", "Empresa B"]
    assert result.contract_data.monetary_values == ["Valor A", "Valor B"]
    assert result.contract_data.main_obligations == ["Obrigacao A", "Obrigacao B"]
    assert result.contract_data.additional_data == { "objeto": "Objeto A", "vigencia": "Vigência A"}
    assert result.contract_data.termination_clause == "Cláusula de Rescisão A"


    # Verifica se foi salvo no banco
    db_contract = db_session.query(Contract).filter(Contract.file_name == "new_contract.pdf").first()
    assert db_contract is not None


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
