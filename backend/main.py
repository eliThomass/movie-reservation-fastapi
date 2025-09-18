from fastapi import FastAPI, Depends
from typing import Annotated
from database import get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from auth import get_password_hash, verify_password
import models

app = FastAPI()
db_dependency = Annotated[Session, Depends(get_db)]

class SignUpBase(BaseModel):
    username: str
    password: str

class SignUpOut(BaseModel):
    id: int
    username: str
    password: str
    created_at: str

@app.post("/sign_up", response_model=SignUpOut)
async def sign_up(account: SignUpBase, db: db_dependency):
    account = models.Account(name=account.username, password=get_password_hash(account.password))
    db.add(account)
    db.commit()
    db.refresh(account)
    return {
        "id": account.id,
        "username": account.name,
        "password": account.password,
        "created_at": account.created_at.isoformat()
    }

@app.get("/sign_in")
async def sign_in(name: str, password: str, db: db_dependency):
    return {}
    