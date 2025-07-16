# app/contracts/service.py
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from ..models import Contract
from .utils import extract_text_from_pdf, extract_text_from_docx, process_contract_with_ai
from .schemas import ContractResponse

class ContractService:
    def __init__(self, db: Session):
        self.db = db

    async def upload_and_process_contract(self, file: UploadFile) -> ContractResponse:
        self.__validate_file(file)

        file_extension = file.filename.rsplit('.', 1)[-1].lower()
        # 1. Extrair texto do documento
        if file_extension == "pdf":
            contract_text = extract_text_from_pdf(file)
        else:
            contract_text = extract_text_from_docx(file)

        if not contract_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from the document."
            )

        # 2. Processar texto com a API de IA
        ai_extracted_data = await process_contract_with_ai(contract_text)

        # 3. Persistir no banco de dados
        db_contract = Contract.create_from_ai(
            file_name=file.filename,
            ai_data=ai_extracted_data
        )
        self.db.add(db_contract)
        self.db.commit()
        self.db.refresh(db_contract)

        return ContractResponse.from_contract(db_contract)

    def get_contract_by_name(self, contract_name: str):
        contract = self.db.query(Contract).filter(Contract.file_name == contract_name).first()
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract '{contract_name}' not found."
            )

        return ContractResponse.from_contract(contract)

    def __validate_file(self, file: UploadFile) -> None:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file name provided."
            )

        extension = file.filename.rsplit('.', 1)[-1].lower()
        if extension not in {"pdf", "docx"}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only .pdf and .docx are supported."
            )

        exists = (self.db.query(Contract).filter(Contract.file_name == file.filename).first())
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Contract '{file.filename}' already exists."
            )
