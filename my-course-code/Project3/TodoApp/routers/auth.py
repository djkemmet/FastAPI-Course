'''This module handles user authentication, logging in.'''
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from jose import jwt, JWTError # used to generate JSON Web Tokens.
from datetime import timedelta, datetime # used to calculate token expiry



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

database_dependecy = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

# SECURITY Settings
## Password Hashing
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
## JSON Web Tokens
SECRET_KEY = '791c6be741aae4836fbed9e759be59ab81c80c4727e2828cc25835ff715c6be7d6b3f32fa09559870ea8ca747b2e49345d5de9fcbef0eb307b1a05992e50a812'
ALGORITHM = "HS256"
OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/auth/token")



def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(OAuth2PasswordBearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role = str = payload.get('role')
        if username is None or user_id is None: 
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, "id": user_id, "role": user_role}
    except JWTError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")


class CreateUserRequest(BaseModel):
    '''This class provides a Data Validator for User Object Requests.'''
    email: str = Field()
    username: str = Field()
    first_name: str = Field()
    last_name:str = Field()
    password:str = Field()
    is_active: bool = Field()
    role: str = Field()


class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: database_dependecy,create_user_request: CreateUserRequest):
    '''This function adds a user to the product'''
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password= bcrypt_context.hash(create_user_request.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: database_dependecy):
    ## TODO: Investigate handling invalid dict error. 
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(username=user.username, user_id=user.id, role=user.role, expires_delta=timedelta(minutes=20))
    return {'access_token': token, 'token_type': "bearer"}
