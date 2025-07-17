import pytest
from unittest.mock import MagicMock, patch
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
    assert "IA retornou um JSON incorreto" in exc_info.value.detail

