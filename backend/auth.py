from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_id(user_id: int, db: db_dependency):
    return db.query(models.Accounts).filter(user_id=user_id).first()