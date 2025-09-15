from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Account(Base):
    __tablename__ = "account"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)