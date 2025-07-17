from app.models import Contract
import json

def test_contract_create_from_ai_success():
    """
    Testa a criação de uma instância de Contract a partir de um dicionário bem-sucedido da IA.
    """
    ai_data = {
        "parties": ["Empresa A", "Empresa B"],
        "monetary_values": ["Valor A", "Valor B"],
        "main_obligations": ["Obrigacao A", "Obrigacao B"],
        "additional_data":  {
            "objeto": "Objeto A",
            "vigencia": "Vigência A",
        },
        "termination_clause": "Cláusula de Rescisão A",
    }

    contract = Contract.create_from_ai("Contrato Principal", ai_data )

    assert contract.file_name == "Contrato Principal"
    assert json.loads(contract.parties) ==  ["Empresa A", "Empresa B"]
    assert json.loads(contract.monetary_values) == ["Valor A", "Valor B"]
    assert json.loads(contract.main_obligations) == ["Obrigacao A", "Obrigacao B"]
    assert json.loads(contract.additional_data) == {"objeto": "Objeto A", "vigencia": "Vigência A"}
    assert contract.termination_clause == "Cláusula de Rescisão A"


def test_contract_create_from_ai_missing_keys():
    """
    Testa a criação de uma instância de Contract quando algumas chaves estão faltando
    no dicionário da IA, esperando valores padrão (None).
    """
    ai_data = {
        "parties": ["Empresa A", "Empresa B"],
        "monetary_values": ["Valor A", "Valor B"],
        "main_obligations": ["Obrigacao A", "Obrigacao B"],
    }

    contract = Contract.create_from_ai("Contrato Principal", ai_data)

    assert contract.file_name == "Contrato Principal"
    assert json.loads(contract.parties) == ["Empresa A", "Empresa B"]
    assert json.loads(contract.monetary_values) == ["Valor A", "Valor B"]
    assert json.loads(contract.main_obligations) == ["Obrigacao A", "Obrigacao B"]
    assert json.loads(contract.additional_data) is None
    assert contract.termination_clause is None
