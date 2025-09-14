from fastapi import FastAPI, Depends
from typing import Annotated
from database import get_db
from sqlalchemy.orm import Session

app = FastAPI()
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def testing():
    return []