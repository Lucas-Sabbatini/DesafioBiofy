# app/contracts/router.py
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ContractResponse
from .service import ContractService

router = APIRouter(tags=["Contracts"])

@router.post("/contracts/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    contract_service = ContractService(db)
    uploaded_contract = await contract_service.upload_and_process_contract(file)

    # Converte para o schema de resposta
    contract_data = {
        "parties": json.loads(uploaded_contract.parties) if uploaded_contract.parties else [],
        "monetary_values": json.loads(uploaded_contract.monetary_values) if uploaded_contract.monetary_values else [],
        "main_obligations": json.loads(uploaded_contract.main_obligations) if uploaded_contract.main_obligations else [],
        "additional_data": json.loads(uploaded_contract.additional_data) if uploaded_contract.additional_data else {},
        "termination_clause": uploaded_contract.termination_clause,
    }
    return ContractResponse(
        id=uploaded_contract.id,
        file_name=uploaded_contract.file_name,
        uploaded_at=uploaded_contract.uploaded_at,
        contract_data=contract_data
    )


@router.get("/contracts/{contract_name}", response_model=ContractResponse)
async def get_contract(
    contract_name: str,
    db: Session = Depends(get_db),
):
    contract_service = ContractService(db)
    contract = contract_service.get_contract_by_name(contract_name)
    return contract