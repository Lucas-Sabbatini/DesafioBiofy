from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from .database import Base
import json

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, unique=True, index=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    parties = Column(Text) # JSON string ou Text para armazenar listas/dicionários
    monetary_values = Column(Text)
    main_obligations = Column(Text)
    additional_data = Column(Text)
    termination_clause = Column(Text)

    @classmethod
    def create_from_ai(cls, file_name: str, ai_data: dict) -> "Contract":
        return cls(
            file_name=file_name,
            parties=json.dumps(ai_data.get("parties", [])),
            monetary_values=json.dumps(ai_data.get("monetary_values", [])),
            main_obligations=json.dumps(ai_data.get("main_obligations", [])),
            additional_data=json.dumps(ai_data.get("additional_data", {})),
            termination_clause=ai_data.get("termination_clause"),
        )