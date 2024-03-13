# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel

Base = declarative_base()

class Form(Base):
    __tablename__ = 'forms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)

# Pydantic models for data validation
class FormData(BaseModel):
    name: str
    email: str
