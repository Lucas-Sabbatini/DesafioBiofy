# app/schemas.py
import json

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional

# Schemas gerais que podem ser reutilizados
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Base para schemas de usuário
class UserBase(BaseModel):
    username: str

# Schema para criação de usuário (excluindo hash_password)
class UserCreate(UserBase):
    password: str

# Schema para leitura de usuário (excluindo senha)
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True # ou orm_mode = True para Pydantic < v2

# Schemas para Contratos
class ContractBase(BaseModel):
    file_name: str

class ContractUpload(ContractBase):
    # Não precisamos de outros campos aqui, pois serão extraídos pela IA
    pass

class ContractData(BaseModel):
    parties: Optional[List[str]] = Field(default_factory=list)
    monetary_values: Optional[List[str]] = Field(default_factory=list)
    main_obligations: Optional[List[str]] = Field(default_factory=list)
    additional_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
    termination_clause: Optional[str] = None

class ContractResponse(ContractBase):
    id: int
    uploaded_at: datetime
    contract_data: ContractData # Inclui os dados extraídos pela IA

    class Config:
        from_attributes = True
        json_dumps = lambda x: json.dumps(x, indent=2) # Para exibir JSON formatado
        json_loads = json.loads # Para carregar JSON