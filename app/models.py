# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from .database import Base

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
    original_text = Column(Text) # Armazenar o texto completo para referência