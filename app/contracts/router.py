# app/contracts/router.py
from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from ..database import get_db
from .schemas import ContractResponse
from .service import ContractService

router = APIRouter(tags=["Contracts"])

@router.post("/contracts/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    contract_service = ContractService(db)
    uploaded_contract = await contract_service.upload_and_process_contract(file)

    return uploaded_contract


@router.get("/contracts/{contract_name}", response_model=ContractResponse)
async def get_contract(
    contract_name: str,
    db: Session = Depends(get_db),
):
    contract_service = ContractService(db)
    contract = contract_service.get_contract_by_name(contract_name)
    return contract