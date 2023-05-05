from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException, status, Path, Body
import models
from models import Todos
from database import engine, SessionLocal

from pydantic import BaseModel, Field

# Create a new instance of a FastAPI Application
app = FastAPI()

# call on the Base (database) to create all models defined
# in the models.py file.
models.Base.metadata.create_all(bind=engine)

def get_db():
    ''' this function is responsible for returning and instance of our database'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    
    title: str = Field(min_length=3 ,title="What do you need to do?")
    description: str = Field(min_length=3, max_length=100 ,title="Why do you need to do that?")
    priority: int = Field(gt= 0, lt=6, title= "How important is it for you to do this?")
    complete: bool



@app.get("/", status_code=status.HTTP_200_OK)
# Depends is dependency injection which basically means get an instance of 
# our DB before we try to do something, which in this case is the read_all function.
async def read_all(db: db_dependency):
    '''This function returns all todo items in the API'''
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt= 0)):
    '''This function returns a single todo item by it's ID'''
    todo_model = db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo item not found.")


@app.post("/todo/new", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    new_todo_item = Todos(**todo_request.dict())
    
    db.add(new_todo_item)
    db.commit()
