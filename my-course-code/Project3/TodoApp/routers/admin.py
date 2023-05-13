'''This module handles CRUDing Todo Items.'''
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from models import Todos
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user

# Create a new instance of a FastAPI Application
router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)

def get_db():
    ''' this function is responsible for returning and instance of our database'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized.")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}")
async def delete_user(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None or user.get('role') != 'admin':
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return HTTPException(status_code=status.HTTP_200_OK, detail=f"Todo {todo_id} was deleted.")