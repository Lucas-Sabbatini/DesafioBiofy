from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..auth.service import get_current_user
from .schemas import ContractResponse
from .service import ContractService

router = APIRouter(tags=["Contracts"])

@router.post("/contracts/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    contract_service = ContractService(db)
    uploaded_contract = await contract_service.upload_and_process_contract(file)

    return uploaded_contract

@router.get("/contracts/{contract_name}", response_model=ContractResponse)
async def get_contract(
    contract_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    contract_service = ContractService(db)
    contract = contract_service.get_contract_by_name(contract_name)
    return contract