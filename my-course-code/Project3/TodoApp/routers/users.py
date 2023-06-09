from typing import Annotated
#Framework Dependencies
from fastapi import HTTPException, APIRouter, status, Depends
# Application-specific Dependencies
from database import SessionLocal
from models import Users
from .auth import get_current_user, SECRET_KEY, ALGORITHM, bcrypt_context
#SQLAlchemy Dependencies
from sqlalchemy.orm import Session
# Pydantic Dependencies
from pydantic import BaseModel, Field

class PasswordChangeRequestModel(BaseModel):
    new_password: str = Field(min_length=8)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


database_dependency = Annotated[Session, Depends(get_db)]


user_dependency = Annotated[dict, Depends(get_current_user)]
# Dependencies


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/get", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependency, db: database_dependency):
    '''This function fetches the user's profile from the DB '''
    if user is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Logged In.")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def reset_password(user: user_dependency, db: database_dependency, password: PasswordChangeRequestModel):
    if user is None: 
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login.")
    new_password = bcrypt_context.hash(password.new_password)
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()
    current_user.hashed_password = new_password
    db.add(current_user)
    db.commit()
    return {"Message": "Password Updated",}
