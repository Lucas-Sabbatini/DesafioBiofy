from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..models import Contract
import json

class ContractBase(BaseModel):
    file_name: str

class ContractUpload(ContractBase):
    pass

class ContractData(BaseModel):
    parties: List[str]                   = Field(default_factory=list)
    monetary_values: List[str]           = Field(default_factory=list)
    main_obligations: List[str]          = Field(default_factory=list)
    additional_data: Dict[str, Any]      = Field(default_factory=dict)
    termination_clause: Optional[str]    = None

    @classmethod
    def from_contract(cls, orm: Contract) -> "ContractData":
        return cls(
            parties=json.loads(orm.parties or "[]"),
            monetary_values=json.loads(orm.monetary_values or "[]"),
            main_obligations=json.loads(orm.main_obligations or "[]"),
            additional_data=json.loads(orm.additional_data or "{}"),
            termination_clause=orm.termination_clause,
        )

class ContractResponse(ContractBase):
    id: int
    uploaded_at: datetime
    contract_data: ContractData

    class Config:
        from_attributes = True
        json_dumps = lambda x: json.dumps(x, indent=2)
        json_loads = json.loads

    @classmethod
    def from_contract(cls, orm: Contract) -> "ContractResponse":
        return cls(
            id=orm.id,
            file_name=orm.file_name,
            uploaded_at=orm.uploaded_at,
            contract_data=ContractData.from_contract(orm),
        )