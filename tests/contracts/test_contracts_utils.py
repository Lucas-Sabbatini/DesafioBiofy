import pytest
from contract_text import CONTRACT_TEXT
from fastapi import HTTPException
from app.contracts.utils import (
    __parse_and_normalize_json,
    process_contract_with_ai
)


def test_parse_and_normalize_json_with_markdown():
    """Testa o parsing de JSON envolvido em markdown."""
    json_string = "```json\n{\"key\": \"value\"}\n```"
    expected = {"key": "value"}
    assert __parse_and_normalize_json(json_string) == expected


def test_parse_and_normalize_json_plain():
    """Testa o parsing de uma string JSON pura."""
    json_string = "{\"key\": \"value\"}"
    expected = {"key": "value"}
    assert __parse_and_normalize_json(json_string) == expected


def test_parse_and_normalize_json_invalid():
    """Testa o parsing de uma string JSON inválida, esperando uma exceção."""
    json_string = "{\"key\": \"value\""  # JSON malformado
    with pytest.raises(HTTPException) as exc_info:
        __parse_and_normalize_json(json_string)
    assert exc_info.value.status_code == 500
    assert "AI returned a malformed JSON" in exc_info.value.detail

@pytest.mark.asyncio
async def test_process_contract_with_ai_success():
    ai_response = await process_contract_with_ai(CONTRACT_TEXT)

    assert ai_response.get("parties") is not None
    assert ai_response.get("monetary_values") is not None
    assert ai_response.get("main_obligations") is not None
    assert ai_response.get("additional_data") is not None
    assert ai_response.get("termination_clause") is not None
