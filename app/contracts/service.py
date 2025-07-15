# app/contracts/service.py
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from ..models import Contract
from .utils import extract_text_from_pdf, extract_text_from_docx, process_contract_with_ai
import json # Para serializar/deserializar JSON

class ContractService:
    def __init__(self, db: Session):
        self.db = db

    async def upload_and_process_contract(self, file: UploadFile):
        if not file.filename:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="No file name provided.")

        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ["pdf", "docx"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only .pdf and .docx are supported."
            )

        # Verifica se o arquivo já existe pelo nome
        existing_contract = self.db.query(Contract).filter(Contract.file_name == file.filename).first()
        if existing_contract:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Contract '{file.filename}' already exists."
            )

        # 1. Extrair texto do documento
        contract_text = ""
        if file_extension == "pdf":
            contract_text = extract_text_from_pdf(file)
        elif file_extension == "docx":
            contract_text = extract_text_from_docx(file)

        if not contract_text:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Could not extract text from the document.")

        # 2. Processar texto com a API de IA
        ai_extracted_data = await process_contract_with_ai(contract_text)

        # 3. Persistir no banco de dados
        db_contract = Contract(
            file_name=file.filename,
            original_text=contract_text, # Opcional, para referência
            parties=json.dumps(ai_extracted_data.get("parties")),
            monetary_values=json.dumps(ai_extracted_data.get("monetary_values")),
            main_obligations=json.dumps(ai_extracted_data.get("main_obligations")),
            additional_data=json.dumps(ai_extracted_data.get("additional_data")),
            termination_clause=ai_extracted_data.get("termination_clause"),
        )
        self.db.add(db_contract)
        self.db.commit()
        self.db.refresh(db_contract)

        return db_contract

    def get_contract_by_name(self, contract_name: str):
        contract = self.db.query(Contract).filter(Contract.file_name == contract_name).first()
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Contract '{contract_name}' not found."
            )

        # Desserializa os campos JSON antes de retornar
        contract_data = {
            "parties": json.loads(contract.parties) if contract.parties else [],
            "monetary_values": json.loads(contract.monetary_values) if contract.monetary_values else [],
            "main_obligations": json.loads(contract.main_obligations) if contract.main_obligations else [],
            "additional_data": json.loads(contract.additional_data) if contract.additional_data else {},
            "termination_clause": contract.termination_clause,
        }

        # Cria um objeto para se adequar ao ContractResponse schema
        response_contract = {
            "id": contract.id,
            "file_name": contract.file_name,
            "uploaded_at": contract.uploaded_at,
            "contract_data": contract_data
        }

        return response_contract