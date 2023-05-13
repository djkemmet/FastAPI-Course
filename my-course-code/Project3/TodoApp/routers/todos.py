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

    tags=['Todos']
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


class TodoRequest(BaseModel):
    '''Defines the data validator for a Todo Item'''
    title: str = Field(min_length=3 ,title="What do you need to do?")
    description: str = Field(min_length=3, max_length=100 ,title="Why do you need to do that?")
    priority: int = Field(gt= 0, lt=6, title= "How important is it for you to do this?")
    complete: bool

@router.get("/", status_code=status.HTTP_200_OK)
# Depends is dependency injection which basically means get an instance of
# our DB before we try to do something, which in this case is the read_all function.
async def read_all(user: user_dependency, db: db_dependency):
    '''This function returns all todo items in the API'''
    if user is None: 
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must sign in.")
    return db.query(Todos).filter(Todos.owner_id== user.get('id')).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt= 0)):
    '''This function returns a single todo item by it's ID'''
    if user is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You need to sign in first.")
    todo_model = db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo item not found.")

@router.post("/todo/new", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    '''This method creates a Todo item.'''
    
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    new_todo_item = Todos(**todo_request.dict(), owner_id=user.get('id'))
    db.add(new_todo_item)
    db.commit()

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,todo_request: TodoRequest, todo_id: int):
    '''This method updates an existing Todo item.'''
    if user is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must login.")
    
    todo_model = db.query(Todos).filter(Todos.id==todo_id).todo(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    todo_model.title = todo_request.title
    todo_model.complete = todo_request.complete
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int):
    '''This method deletes the todo item at the ID specified.'''
    if user is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must login.")

    todo_object = db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if not todo_object:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested todo not found.")
    db.query(Todos).filter(Todos).filter(Todos.id==todo_id).delete()
    db.commit()